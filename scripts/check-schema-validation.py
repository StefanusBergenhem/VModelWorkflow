#!/usr/bin/env python3
"""JSON-Schema validation check (Phase 6 — closes Issue 28).

For every artifact under a specs root (or for a single .md path):

  1. Read ``artifact_type`` from the front-matter.
  2. Locate the corresponding per-artifact schema under
     ``schemas/artifacts/<artifact_type>.schema.json``.
  3. Validate the front-matter against the per-artifact schema (which
     composes the universal envelope via ``allOf``).
  4. Walk embedded ``yaml`` fenced blocks and, when a block declares a known
     section-shape key (``public_interface``, ``data_structures``,
     ``decomposition``, ``interfaces``, ``requirements`` family, …) or is a
     top-level list of cases (TestSpec ``Cases``), validate each entry
     against the matching ``$defs`` member.

The script is interim scaffolding for the period before ``vmodel-core``
ships its ``validate`` subcommand. Once ``vmodel-core validate`` is the
canonical validator, this script can be retired and author skills' Step-11
self-check entries replaced with the CLI invocation.

Stable contract:
  stdout: one finding per line, ``<file>:<line>:<rule-id>:<message>``.
  stderr: pre-flight failures only (input-not-found, schema-not-found,
          dependency-not-installed); rule-id ``script-error``.
  exit 0: clean; exit 1: findings; exit 2: script error.

Invocation:
  ./scripts/check-schema-validation.py <specs-root>
  ./scripts/check-schema-validation.py path/to/single/artifact.md
  ./scripts/check-schema-validation.py <specs-root> --schemas-root path/to/schemas
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.spec_parser import (  # noqa: E402
    find_md_files,
    iter_yaml_blocks,
    parse_yaml_frontmatter,
    safe_yaml_load,
)


try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
except ImportError as exc:  # pragma: no cover
    print(
        f"check-schema-validation:script-error:dependency-not-installed: "
        f"{exc.name} (install via: pip install jsonschema referencing)",
        file=sys.stderr,
    )
    sys.exit(2)


# Artifact types that have a per-artifact JSON Schema published under
# schemas/artifacts/. Keep in step with the framework's canonical set.
_ARTIFACT_TYPES = {
    "product-brief",
    "requirements",
    "architecture",
    "architecture-interface-detail",
    "adr",
    "detailed-design",
    "test-spec",
}


# Section-shape keys → ($defs member name) per artifact type. When a YAML
# block contains the listed key whose value is a list, every list item is
# validated against the named $def. Section context (header text) is NOT
# used — block-key inspection is robust to header wording variations.
_SECTION_DEFS: dict[str, dict[str, str]] = {
    "detailed-design": {
        "public_interface": "public_interface_entry",
        "data_structures": "data_structure_entry",
        "error_matrix": "error_matrix_row",
    },
    "architecture": {
        "decomposition": "decomposition_child",
        "interfaces": "interface",
    },
    "architecture-interface-detail": {},
    # Requirements artifacts hold typed requirement lists under several
    # section keys; every list element validates against $defs/requirement.
    # NB: 'inherited_constraints' uses IC-NNN identifiers, which the current
    # $defs/requirement regex (^REQ-...$) does not accept. Skipped pending a
    # schema-side decision (separate $def for ICs, or relaxed id pattern).
    "requirements": {
        "functional": "requirement",
        "quality_attributes": "requirement",
        "interfaces": "requirement",
        "data": "requirement",
        "constraints": "requirement",
        "requirements": "requirement",
    },
    "adr": {},
    "product-brief": {},
}


# TestSpec cases are authored as a top-level YAML list (one or more blocks),
# each item being a test_case. Handled separately from the dict-key lookup.
_TESTSPEC_DEF = "test_case"


def _load_all_schemas(schemas_root: Path) -> tuple[Registry, dict[str, dict]]:
    """Load every *.schema.json under schemas_root into a referencing.Registry.

    Returns (registry, by_artifact_type) where by_artifact_type maps each
    per-artifact schema's ``artifact_type`` const (or its filename stem
    when no const is present) to the raw schema dict.
    """
    registry = Registry()
    by_artifact_type: dict[str, dict] = {}
    for schema_path in sorted(schemas_root.rglob("*.schema.json")):
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(
                f"check-schema-validation:script-error:schema-load: "
                f"{schema_path}: {exc}",
                file=sys.stderr,
            )
            continue
        schema_id = schema.get("$id")
        if isinstance(schema_id, str):
            resource = Resource(contents=schema, specification=DRAFT202012)
            registry = registry.with_resource(uri=schema_id, resource=resource)
        artifact_type = _artifact_type_const(schema)
        if artifact_type:
            by_artifact_type[artifact_type] = schema
        else:
            # Fall back to filename stem (envelope, common-defs) — these are
            # referenced via $ref but never authored as artifact_type.
            stem = schema_path.stem.replace(".schema", "")
            by_artifact_type.setdefault(f"_stem:{stem}", schema)
    return registry, by_artifact_type


def _artifact_type_const(schema: dict) -> str | None:
    """Return the artifact_type const value declared in a per-artifact schema, if any."""
    for clause in schema.get("allOf", []):
        if not isinstance(clause, dict):
            continue
        props = clause.get("properties", {})
        at = props.get("artifact_type") if isinstance(props, dict) else None
        if isinstance(at, dict):
            const = at.get("const")
            if isinstance(const, str):
                return const
    # Top-level properties.artifact_type.const (alt layout).
    props = schema.get("properties", {})
    at = props.get("artifact_type") if isinstance(props, dict) else None
    if isinstance(at, dict):
        const = at.get("const")
        if isinstance(const, str):
            return const
    return None


def _validate_node(
    validator: Draft202012Validator,
    instance,
    file_path: Path,
    line: int,
    rule_prefix: str,
) -> list[tuple[Path, int, str, str]]:
    """Run a validator over an instance; return [(path, line, rule, msg), …]."""
    findings: list[tuple[Path, int, str, str]] = []
    for err in sorted(validator.iter_errors(instance), key=lambda e: e.path):
        loc = ".".join(str(p) for p in err.absolute_path) or "<root>"
        msg = f"{loc}: {err.message}"
        findings.append((file_path, line, rule_prefix, msg))
    return findings


def _validate_frontmatter(
    fm: dict,
    schema: dict,
    registry: Registry,
    file_path: Path,
    fm_end_line: int,
) -> list[tuple[Path, int, str, str]]:
    validator = Draft202012Validator(schema, registry=registry)
    return _validate_node(
        validator,
        fm,
        file_path,
        fm_end_line,
        "schema.frontmatter-invalid",
    )


def _ref_def(schema_id: str, def_name: str) -> dict:
    """Return a $ref schema pointing to a $defs entry of the given schema id."""
    return {"$ref": f"{schema_id}#/$defs/{def_name}"}


def _validate_yaml_blocks(
    body_text: str,
    artifact_type: str,
    artifact_schema: dict,
    registry: Registry,
    file_path: Path,
) -> list[tuple[Path, int, str, str]]:
    findings: list[tuple[Path, int, str, str]] = []
    schema_id = artifact_schema.get("$id")
    if not isinstance(schema_id, str):
        return findings

    section_defs = _SECTION_DEFS.get(artifact_type, {})
    has_test_case_def = (
        artifact_type == "test-spec"
        and "test_case" in artifact_schema.get("$defs", {})
    )

    for block_text, start_line, _end_line in iter_yaml_blocks(body_text):
        loaded = safe_yaml_load(block_text)
        if loaded is None:
            continue

        # TestSpec cases — top-level list of dicts.
        if has_test_case_def and isinstance(loaded, list):
            sub_schema = _ref_def(schema_id, _TESTSPEC_DEF)
            validator = Draft202012Validator(sub_schema, registry=registry)
            for idx, item in enumerate(loaded):
                if not isinstance(item, dict):
                    continue
                findings.extend(
                    _validate_node(
                        validator,
                        item,
                        file_path,
                        start_line,
                        f"schema.test-case-invalid[{idx}]",
                    )
                )
            continue

        # Section-keyed dict blocks.
        if isinstance(loaded, dict) and section_defs:
            for key, def_name in section_defs.items():
                entries = loaded.get(key)
                if not isinstance(entries, list):
                    continue
                sub_schema = _ref_def(schema_id, def_name)
                validator = Draft202012Validator(sub_schema, registry=registry)
                for idx, item in enumerate(entries):
                    if not isinstance(item, dict):
                        continue
                    findings.extend(
                        _validate_node(
                            validator,
                            item,
                            file_path,
                            start_line,
                            f"schema.{def_name}-invalid[{key}/{idx}]",
                        )
                    )
    return findings


def _validate_artifact(
    md: Path,
    registry: Registry,
    by_artifact_type: dict[str, dict],
) -> list[tuple[Path, int, str, str]]:
    try:
        text = md.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(
            f"check-schema-validation:{md}: cannot read: {exc}",
            file=sys.stderr,
        )
        return [(md, 0, "schema.read-error", str(exc))]

    fm, body, fm_end = parse_yaml_frontmatter(text)
    if fm is None:
        # No front-matter — not necessarily an artifact (e.g., README). Skip silently.
        return []
    if not isinstance(fm, dict):
        return []

    # Discriminator: artifact_type wins; kind is the Rule-8 architecture-bundle
    # back-channel for interface detail files (whose schema also publishes both).
    discriminator = (
        str(fm.get("artifact_type", "")).strip()
        or str(fm.get("kind", "")).strip()
    )

    if not discriminator:
        # Narrative docs (glossary, README) carry front-matter without a
        # discriminator — skip silently. An artifact missing both is a real
        # defect but distinguishing requires inspecting the path/template,
        # which is out of this script's scope.
        if md.name in {"glossary.md", "README.md"}:
            return []
        return [
            (
                md,
                fm_end or 1,
                "schema.frontmatter-invalid",
                "front-matter missing 'artifact_type' (or 'kind' for "
                "Rule-8 architecture-bundle detail files)",
            )
        ]

    # Root-product variants without a published schema (needs, pd) are skipped
    # silently — the framework's canonical schema set covers only the 7
    # artifact types listed in _ARTIFACT_TYPES.
    if discriminator not in _ARTIFACT_TYPES:
        return []

    schema = by_artifact_type.get(discriminator)
    if not schema:
        return [
            (
                md,
                fm_end or 1,
                "schema.no-schema-found",
                f"no per-artifact schema published for artifact_type "
                f"'{discriminator}' under schemas/artifacts/",
            )
        ]

    artifact_type = discriminator

    findings = _validate_frontmatter(fm, schema, registry, md, fm_end or 1)
    findings.extend(
        _validate_yaml_blocks(body, artifact_type, schema, registry, md)
    )
    return findings


def _iter_inputs(target: Path) -> Iterable[Path]:
    if target.is_file():
        if target.suffix == ".md":
            yield target
        return
    yield from find_md_files(target)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "target",
        type=Path,
        help="Path to a specs directory or a single .md file.",
    )
    parser.add_argument(
        "--schemas-root",
        type=Path,
        default=None,
        help=(
            "Root of the schemas/ tree. Defaults to the framework's "
            "schemas/ directory two levels up from this script's location."
        ),
    )
    args = parser.parse_args()

    if not args.target.exists():
        print(
            f"check-schema-validation:script-error:input-not-found: {args.target}",
            file=sys.stderr,
        )
        return 2

    schemas_root = (
        args.schemas_root
        if args.schemas_root is not None
        else Path(__file__).resolve().parent.parent / "schemas"
    )
    if not schemas_root.is_dir():
        print(
            f"check-schema-validation:script-error:schemas-root-not-found: "
            f"{schemas_root}",
            file=sys.stderr,
        )
        return 2

    try:
        registry, by_artifact_type = _load_all_schemas(schemas_root)
    except Exception as exc:  # noqa: BLE001 — pre-flight, surface anything.
        print(
            f"check-schema-validation:script-error:registry-build: {exc}",
            file=sys.stderr,
        )
        return 2

    all_findings: list[tuple[Path, int, str, str]] = []
    for md in _iter_inputs(args.target):
        all_findings.extend(_validate_artifact(md, registry, by_artifact_type))

    # Dedupe — when allOf composes envelope+per-artifact required arrays,
    # jsonschema can emit the same finding twice. (path, line, rule, msg)
    # uniqueness collapses these without losing distinct findings.
    seen: set[tuple[str, int, str, str]] = set()
    unique: list[tuple[Path, int, str, str]] = []
    for f in all_findings:
        key = (str(f[0]), f[1], f[2], f[3])
        if key in seen:
            continue
        seen.add(key)
        unique.append(f)

    unique.sort(key=lambda f: (str(f[0]), f[1], f[2], f[3]))
    for path, line, rule, msg in unique:
        print(f"{path}:{line}:{rule}:{msg}")

    return 1 if unique else 0


if __name__ == "__main__":
    sys.exit(main())
