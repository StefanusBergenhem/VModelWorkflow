#!/usr/bin/env python3
"""ADR-bound binding landing-field check (Phase 6 Issue 16).

Cross-references ADR Propagation `bindings:` declarations against
architecture decomposition entries. Bindings (library / protocol / vendor
names) must land in `rationale` only — not in `purpose`, `responsibilities`,
or interface operation signatures.

Invocation: ./scripts/check-adr-landing.py <specs-root>
"""

from __future__ import annotations

import argparse
import re
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


def _is_adr(fm: dict | None, path: Path) -> bool:
    if fm and str(fm.get("artifact_type", "")).lower() == "adr":
        return True
    if fm and str(fm.get("type", "")).lower() == "adr":
        return True
    parts = path.parts
    if "adrs" in parts:
        return True
    return False


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
    return False


def _adr_id(fm: dict | None, path: Path) -> str:
    if fm and fm.get("id"):
        return str(fm["id"])
    return path.stem


def _extract_bindings(
    md_text: str, adr_id: str
) -> list[dict]:
    """Return list of binding dicts {name, scope, kind, adr_id} found in any
    yaml block declaring `propagation: bindings:`."""
    out: list[dict] = []
    for block_text, _start, _end in iter_yaml_blocks(md_text):
        loaded = safe_yaml_load(block_text)
        if not isinstance(loaded, dict):
            continue
        prop = loaded.get("propagation")
        if not isinstance(prop, dict):
            continue
        bindings = prop.get("bindings")
        if not isinstance(bindings, list):
            continue
        for entry in bindings:
            if not isinstance(entry, dict):
                continue
            name = entry.get("name")
            scope = entry.get("scope")
            if not name or not scope:
                continue
            out.append(
                {
                    "name": str(name),
                    "scope": str(scope),
                    "kind": str(entry.get("kind", "")),
                    "adr_id": adr_id,
                }
            )
    return out


def _extract_decomposition_entries(
    md_text: str,
) -> list[tuple[dict, int]]:
    """Return list of (entry_dict, approx_line) for every decomposition child.

    Recognises two shapes:
      1. Top-level YAML block with key `decomposition:` whose value is a list.
      2. Top-level YAML block whose top-level keys include both `purpose:` and
         `responsibilities:` (a single decomposition entry block).
    """
    entries: list[tuple[dict, int]] = []
    for block_text, start_line, _end in iter_yaml_blocks(md_text):
        loaded = safe_yaml_load(block_text)
        if loaded is None:
            continue
        if isinstance(loaded, dict) and isinstance(
            loaded.get("decomposition"), list
        ):
            for child in loaded["decomposition"]:
                if isinstance(child, dict):
                    entries.append((child, start_line))
        elif isinstance(loaded, dict) and (
            "purpose" in loaded and "responsibilities" in loaded
        ):
            entries.append((loaded, start_line))
        elif isinstance(loaded, list):
            for child in loaded:
                if isinstance(child, dict) and "purpose" in child and (
                    "responsibilities" in child
                ):
                    entries.append((child, start_line))
    return entries


def _extract_interfaces(md_text: str) -> list[dict]:
    """Return list of interface entries (each a dict from any block declaring
    `interfaces:` as a list)."""
    out: list[dict] = []
    for block_text, _start, _end in iter_yaml_blocks(md_text):
        loaded = safe_yaml_load(block_text)
        if not isinstance(loaded, dict):
            continue
        ifs = loaded.get("interfaces")
        if not isinstance(ifs, list):
            continue
        for entry in ifs:
            if isinstance(entry, dict):
                out.append(entry)
    return out


def _flatten_strings(value) -> Iterable[str]:
    """Yield string leaves from arbitrarily-nested dict/list/scalar."""
    if value is None:
        return
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from _flatten_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from _flatten_strings(item)
    else:
        yield str(value)


def _word_boundary_pattern(name: str) -> re.Pattern[str]:
    """Build a word-boundary regex when the name has word characters; fall
    back to plain substring escape when leading/trailing chars defeat \\b."""
    escaped = re.escape(name)
    starts_word = bool(re.match(r"\w", name))
    ends_word = bool(re.search(r"\w$", name))
    prefix = r"\b" if starts_word else r"(?<![A-Za-z0-9_])"
    suffix = r"\b" if ends_word else r"(?![A-Za-z0-9_])"
    return re.compile(prefix + escaped + suffix)


def _interface_operation_strings(entry: dict) -> Iterable[str]:
    """Yield operation-signature strings from an interface decomposition
    entry's `interfaces:` field. Architectures sometimes nest interface
    declarations directly under a child entry."""
    ifs = entry.get("interfaces")
    if isinstance(ifs, list):
        for iface in ifs:
            if not isinstance(iface, dict):
                continue
            contract = iface.get("contract")
            if isinstance(contract, dict):
                op = contract.get("operation")
                if isinstance(op, str):
                    yield op
                elif isinstance(op, list):
                    for s in op:
                        if isinstance(s, str):
                            yield s


def _check_field_for_binding(
    field_value, name: str, pattern: re.Pattern[str]
) -> bool:
    for text in _flatten_strings(field_value):
        if pattern.search(text):
            return True
    return False


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
        print(f"check-adr-landing: input not found: {exc}", file=sys.stderr)
        return 2

    bindings: list[dict] = []
    architecture_files: list[tuple[Path, str]] = []
    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(
                f"check-adr-landing: cannot read {md}: {exc}",
                file=sys.stderr,
            )
            return 2
        fm, _body, _end = parse_yaml_frontmatter(text)
        if _is_adr(fm, md):
            bindings.extend(_extract_bindings(text, _adr_id(fm, md)))
        if _is_architecture(fm, md):
            architecture_files.append((md, text))

    if not bindings and not architecture_files:
        return 0
    if not bindings:
        return 0

    findings: list[tuple[Path, int, str, str]] = []
    for arch_path, arch_text in architecture_files:
        entries = _extract_decomposition_entries(arch_text)
        # Also include the operations from any top-level `interfaces:` block
        # at architecture scope (not nested inside a decomposition entry).
        top_level_interfaces = _extract_interfaces(arch_text)
        for binding in bindings:
            name = binding["name"]
            scope = binding["scope"]
            adr_id = binding["adr_id"]
            pattern = _word_boundary_pattern(name)

            for entry, entry_line in entries:
                if str(entry.get("id", "")) != scope and str(
                    entry.get("name", "")
                ) != scope:
                    continue
                if _check_field_for_binding(
                    entry.get("purpose"), name, pattern
                ):
                    findings.append(
                        (
                            arch_path,
                            entry_line,
                            "arch.adr-bound-mechanism-leaked",
                            f'binding "{name}" from {adr_id} appears in '
                            f"{scope}.purpose; ADR-bound mechanisms land in "
                            f"rationale only",
                        )
                    )
                if _check_field_for_binding(
                    entry.get("responsibilities"), name, pattern
                ):
                    findings.append(
                        (
                            arch_path,
                            entry_line,
                            "arch.adr-bound-mechanism-leaked",
                            f'binding "{name}" from {adr_id} appears in '
                            f"{scope}.responsibilities; ADR-bound mechanisms "
                            f"land in rationale only",
                        )
                    )
                for op_str in _interface_operation_strings(entry):
                    if pattern.search(op_str):
                        findings.append(
                            (
                                arch_path,
                                entry_line,
                                "arch.adr-bound-mechanism-leaked",
                                f'binding "{name}" from {adr_id} appears in '
                                f"{scope}.interfaces.operation; ADR-bound "
                                f"mechanisms land in rationale only",
                            )
                        )

            # Top-level interfaces whose `from` or `to` is the binding scope.
            for iface in top_level_interfaces:
                if (
                    str(iface.get("from", "")) != scope
                    and str(iface.get("to", "")) != scope
                ):
                    continue
                contract = iface.get("contract")
                if not isinstance(contract, dict):
                    continue
                op = contract.get("operation")
                op_strs: list[str] = []
                if isinstance(op, str):
                    op_strs = [op]
                elif isinstance(op, list):
                    op_strs = [s for s in op if isinstance(s, str)]
                for op_str in op_strs:
                    if pattern.search(op_str):
                        findings.append(
                            (
                                arch_path,
                                1,
                                "arch.adr-bound-mechanism-leaked",
                                f'binding "{name}" from {adr_id} appears in '
                                f"{scope}.interfaces.operation; ADR-bound "
                                f"mechanisms land in rationale only",
                            )
                        )

    # Deduplicate (same path/line/rule/message).
    seen: set[tuple[str, int, str, str]] = set()
    unique: list[tuple[Path, int, str, str]] = []
    for f in findings:
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
