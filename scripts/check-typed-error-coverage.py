#!/usr/bin/env python3
"""Typed-error enum coverage check (Phase 6 Issue 20).

For every error code declared on an architecture interface
(`ARCH.interfaces.<name>.errors.<code>`), verify that at least one testspec
case lists the matching ID in its `verifies:` list. Uncovered error codes
indicate missing negative-path coverage at the architecture/testspec seam.

Invocation: ./scripts/check-typed-error-coverage.py <specs-root>
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.spec_parser import (  # noqa: E402
    find_md_files,
    iter_yaml_blocks,
    parse_yaml_frontmatter,
    safe_yaml_load,
)


def _is_architecture(fm: dict | None, path: Path) -> bool:
    if fm and str(fm.get("artifact_type", "")).lower() in {
        "architecture",
        "software-architecture",
    }:
        return True
    if fm and str(fm.get("type", "")).lower() == "architecture":
        return True
    if path.name == "architecture.md":
        return True
    # Detail files belonging to architecture: kind == architecture-interface-detail
    if fm and str(fm.get("kind", "")).lower() == "architecture-interface-detail":
        return True
    return False


def _is_testspec(fm: dict | None, path: Path) -> bool:
    if fm:
        artifact_type = str(fm.get("artifact_type", "")).lower()
        if artifact_type in {"testspec", "test-spec", "test_spec"}:
            return True
        if str(fm.get("type", "")).lower() in {"testspec", "test-spec"}:
            return True
    if path.name == "testspec.md":
        return True
    return False


def _is_detailed_design(fm: dict | None, path: Path) -> bool:
    if fm and str(fm.get("artifact_type", "")).lower() in {
        "detailed-design",
        "detailed_design",
    }:
        return True
    if path.name == "detailed_design.md":
        return True
    return False


_DD_TO_ARCH_INTERFACE_RE = re.compile(r"^ARCH-IF-([A-Za-z0-9_-]+)$")


def _collect_dd_arch_interface_links(md_files: list[Path]) -> dict[str, list[str]]:
    """Return {DD-id: [ARCH interface name, ...]} from DD front-matter `derived_from`.

    A leaf DD whose `derived_from` list names ARCH-IF-<NAME> entries declares
    that the DD's typed errors close the corresponding ARCH interface's error
    rows. Used by `_synthesize_arch_level_verifies` below to broaden a leaf
    TestSpec's `verifies` from DD-level error paths to the implied ARCH-level
    error rows.
    """
    out: dict[str, list[str]] = {}
    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        fm, _body, _end = parse_yaml_frontmatter(text)
        if not _is_detailed_design(fm, md):
            continue
        if not fm:
            continue
        dd_id = fm.get("id")
        if not isinstance(dd_id, str):
            continue
        derived = fm.get("derived_from") or []
        if not isinstance(derived, list):
            continue
        iface_names: list[str] = []
        for entry in derived:
            if not isinstance(entry, str):
                continue
            m = _DD_TO_ARCH_INTERFACE_RE.match(entry.strip())
            if m:
                iface_names.append(m.group(1))
        if iface_names:
            out[dd_id] = iface_names
    return out


# Captures DD-level error verifies. Two shapes:
#   DD-<scope>.public_interface.<fn>.errors.<code>
#   DD-<scope>.error_handling.<code>
_DD_ERROR_VERIFIES_RE = re.compile(
    r"^(DD-[A-Za-z0-9_-]+)"
    r"\.(?:public_interface\.[A-Za-z0-9_-]+\.errors\.([A-Za-z0-9_-]+)"
    r"|error_handling\.([A-Za-z0-9_-]+))$"
)


def _synthesize_arch_level_verifies(
    verified: set[str], dd_to_arch: dict[str, list[str]]
) -> set[str]:
    """Broaden DD-level error verifies to the implied ARCH-level paths.

    For every verifies-id matching a DD-level error path, look up the DD's
    ARCH interface names (from `derived_from`) and synthesize the
    corresponding `ARCH.interfaces.<NAME>.errors.<CODE>` ids. Returns the
    augmented verified set (original ∪ synthesized).
    """
    augmented = set(verified)
    for v in list(verified):
        m = _DD_ERROR_VERIFIES_RE.match(v)
        if not m:
            continue
        dd_id = m.group(1)
        code = m.group(2) or m.group(3)
        if not code:
            continue
        iface_names = dd_to_arch.get(dd_id, [])
        for iface in iface_names:
            augmented.add(f"ARCH.interfaces.{iface}.errors.{code}")
    return augmented


def _collect_error_codes_from_block(
    block: dict, interface_name: str | None = None
) -> list[tuple[str, int]]:
    """Return (code, source_line_offset_unknown→0) pairs from one YAML block.

    Walks the block looking for either:
      - top-level `interfaces:` list whose entries carry `name:` + `errors:`
      - a top-level `errors:` list when interface_name is supplied (interface
        detail files keep `errors:` at top level and the interface name in
        front-matter).
    """
    out: list[tuple[str, int]] = []

    if isinstance(block, dict):
        ifs = block.get("interfaces")
        if isinstance(ifs, list):
            for iface in ifs:
                if not isinstance(iface, dict):
                    continue
                name = iface.get("name")
                if not name:
                    continue
                errs = iface.get("errors")
                if not isinstance(errs, list):
                    continue
                for err in errs:
                    if isinstance(err, dict) and err.get("code"):
                        out.append((f"ARCH.interfaces.{name}.errors.{err['code']}", 0))
                    elif isinstance(err, str):
                        out.append((f"ARCH.interfaces.{name}.errors.{err}", 0))

        if interface_name and isinstance(block.get("errors"), list):
            for err in block["errors"]:
                if isinstance(err, dict) and err.get("code"):
                    out.append(
                        (
                            f"ARCH.interfaces.{interface_name}.errors.{err['code']}",
                            0,
                        )
                    )
                elif isinstance(err, str):
                    out.append(
                        (f"ARCH.interfaces.{interface_name}.errors.{err}", 0)
                    )

    return out


def _collect_expected_codes(
    md_files: list[Path],
) -> dict[str, tuple[Path, int]]:
    """Return {expected_id: (source_path, line)} for every architecture-
    declared error code. Line is the line of the YAML block declaring it."""
    expected: dict[str, tuple[Path, int]] = {}

    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(
                f"check-typed-error-coverage: cannot read {md}: {exc}",
                file=sys.stderr,
            )
            raise

        fm, _body, _end = parse_yaml_frontmatter(text)
        if not _is_architecture(fm, md):
            continue

        # Detail files: front-matter `subject:` names the interface.
        detail_iface_name: str | None = None
        if fm and str(fm.get("kind", "")).lower() == "architecture-interface-detail":
            detail_iface_name = (
                str(fm.get("subject")) if fm.get("subject") else None
            )

        for block_text, start_line, _end_line in iter_yaml_blocks(text):
            loaded = safe_yaml_load(block_text)
            if loaded is None:
                continue
            if not isinstance(loaded, dict):
                continue
            for expected_id, _ in _collect_error_codes_from_block(
                loaded, interface_name=detail_iface_name
            ):
                if expected_id not in expected:
                    expected[expected_id] = (md, start_line)

    return expected


_VERIFIES_TARGET_RE = re.compile(
    r"^ARCH\.interfaces\.[A-Za-z0-9_.-]+\.errors\.[A-Za-z0-9_.-]+$"
)


def _flatten_verifies(value) -> list[str]:
    out: list[str] = []
    if isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict):
                target = item.get("id") or item.get("target")
                if isinstance(target, str):
                    out.append(target)
    elif isinstance(value, str):
        out.append(value)
    return out


def _collect_verified_codes(md_files: list[Path]) -> set[str]:
    verified: set[str] = set()
    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(
                f"check-typed-error-coverage: cannot read {md}: {exc}",
                file=sys.stderr,
            )
            raise
        fm, _body, _end = parse_yaml_frontmatter(text)
        if not _is_testspec(fm, md):
            continue

        # Front-matter level verifies (root testspec).
        if fm:
            for v in _flatten_verifies(fm.get("verifies")):
                verified.add(v)

        for block_text, _start, _end_line in iter_yaml_blocks(text):
            loaded = safe_yaml_load(block_text)
            if loaded is None:
                continue
            cases = (
                loaded
                if isinstance(loaded, list)
                else [loaded]
                if isinstance(loaded, dict)
                else []
            )
            for case in cases:
                if not isinstance(case, dict):
                    continue
                if "verifies" in case:
                    for v in _flatten_verifies(case["verifies"]):
                        verified.add(v)
    return verified


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "specs_root",
        type=Path,
        help="Path to a specs directory or a single .md file.",
    )
    args = parser.parse_args()

    try:
        md_files = list(find_md_files(args.specs_root))
    except FileNotFoundError as exc:
        print(
            f"check-typed-error-coverage: input not found: {exc}",
            file=sys.stderr,
        )
        return 2

    try:
        expected = _collect_expected_codes(md_files)
        verified = _collect_verified_codes(md_files)
        dd_to_arch = _collect_dd_arch_interface_links(md_files)
    except (OSError, UnicodeDecodeError):
        return 2

    if not expected:
        return 0

    # Broaden leaf-correct DD-level verifies to the implied ARCH-level paths,
    # so a layer-correct authoring pass (leaf cites DD only) closes the ARCH
    # interface's error row automatically. The dual-citation discipline still
    # applies — authors SHOULD list both for explicit traceability — but the
    # check no longer flags an honest single-cite as uncovered.
    verified = _synthesize_arch_level_verifies(verified, dd_to_arch)

    findings: list[tuple[Path, int, str, str]] = []
    for expected_id, (path, line) in sorted(expected.items()):
        if expected_id in verified:
            continue
        findings.append(
            (
                path,
                line,
                "testspec.typed-error-uncovered",
                f"typed error {expected_id} declared in architecture but no "
                f"testspec case verifies it",
            )
        )

    findings.sort(key=lambda f: (str(f[0]), f[1], f[3]))
    for path, line, rule, msg in findings:
        print(f"{path}:{line}:{rule}:{msg}")

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
