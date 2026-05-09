#!/usr/bin/env python3
"""Implicit-verifies citation check (Phase 6 Issue 21).

Within every testspec case, scan `preconditions:` and `expected:` text for
upstream IDs (REQ-, IC-, ADR-, ARCH.*) and flag any ID that is mentioned in
prose but is not listed in the case's `verifies:`. Implicit citations break
mechanical traceability — anything load-bearing enough to name in the case
narrative is load-bearing enough to verify formally.

Invocation: ./scripts/check-implicit-verifies.py <specs-root>
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


_PATTERNS = {
    "REQ": re.compile(r"\bREQ-\d+\b"),
    "IC": re.compile(r"\bIC-\d+\b"),
    "ADR": re.compile(r"\bADR-\d+\b"),
    "ARCH": re.compile(r"\bARCH\.[A-Za-z][A-Za-z0-9_.-]*\b"),
}


def _is_testspec(fm: dict | None, path: Path) -> bool:
    if fm:
        if str(fm.get("artifact_type", "")).lower() in {
            "testspec",
            "test-spec",
            "test_spec",
        }:
            return True
        if str(fm.get("type", "")).lower() in {"testspec", "test-spec"}:
            return True
    if path.name == "testspec.md":
        return True
    return False


def _flatten_strings(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out.extend(_flatten_strings(item))
        return out
    if isinstance(value, dict):
        out = []
        for v in value.values():
            out.extend(_flatten_strings(v))
        return out
    return [str(value)]


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


def _verifies_contains(verifies: list[str], upstream_id: str) -> bool:
    """An ID counts as listed if a verifies entry equals it OR starts with
    `<id>.` (e.g., ARCH.interfaces.IValidate covers ARCH.interfaces.IValidate.errors.X)
    OR if the upstream is an ARCH.* path that is a prefix of a verifies entry."""
    for v in verifies:
        if v == upstream_id:
            return True
        if v.startswith(upstream_id + "."):
            return True
        if upstream_id.startswith(v + "."):
            return True
    return False


def _scan_case(
    case: dict,
) -> list[tuple[str, str, str]]:
    """Return list of (case_id, upstream_id, field) for implicit citations
    in this case. Caller adds path/line."""
    findings: list[tuple[str, str, str]] = []
    case_id = str(case.get("id", "<no-id>"))
    verifies = _flatten_verifies(case.get("verifies"))

    for field in ("preconditions", "expected"):
        if field not in case:
            continue
        seen_in_field: set[tuple[str, str]] = set()
        for text in _flatten_strings(case[field]):
            for _kind, pattern in _PATTERNS.items():
                for match in pattern.findall(text):
                    if (match, field) in seen_in_field:
                        continue
                    if _verifies_contains(verifies, match):
                        continue
                    seen_in_field.add((match, field))
                    findings.append((case_id, match, field))

    return findings


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
            f"check-implicit-verifies: input not found: {exc}",
            file=sys.stderr,
        )
        return 2

    findings: list[tuple[Path, int, str, str]] = []
    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(
                f"check-implicit-verifies: cannot read {md}: {exc}",
                file=sys.stderr,
            )
            return 2
        fm, _body, _end = parse_yaml_frontmatter(text)
        if not _is_testspec(fm, md):
            continue

        for block_text, start_line, _end_line in iter_yaml_blocks(text):
            loaded = safe_yaml_load(block_text)
            if loaded is None:
                continue
            cases: list[dict]
            if isinstance(loaded, list):
                cases = [c for c in loaded if isinstance(c, dict)]
            elif isinstance(loaded, dict):
                cases = [loaded]
            else:
                continue
            for case in cases:
                if "id" not in case or "verifies" not in case:
                    continue
                for case_id, upstream_id, field in _scan_case(case):
                    findings.append(
                        (
                            md,
                            start_line,
                            "testspec.implicit-verifies-uncited",
                            f"case {case_id} mentions {upstream_id} in "
                            f"{field} but does not list it in verifies:",
                        )
                    )

    findings.sort(key=lambda f: (str(f[0]), f[1], f[3]))
    for path, line, rule, msg in findings:
        print(f"{path}:{line}:{rule}:{msg}")

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
