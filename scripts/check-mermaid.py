#!/usr/bin/env python3
"""Mermaid parser-breaking-character check (Phase 6 Issue 15).

Scans every ```mermaid fenced block under <specs-root> for three patterns
that break the Mermaid parser in author-emitted sequence diagrams:
semicolons in message text, angle-bracket placeholders in message text,
and unquoted participant aliases containing /, :, or ,.

Invocation: ./scripts/check-mermaid.py <specs-root>
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Make `lib.spec_parser` importable when the script is invoked directly.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.spec_parser import find_md_files, iter_mermaid_blocks  # noqa: E402

# Sequence-diagram message line: "<actor> <arrow> <actor>: <text>".
# Arrows: -> ->> --> -->> -x --x -) --)
_ARROW_ALT = r"(?:-->>|-->|->>|->|--x|-x|--\)|-\))"
_MSG_LINE_RE = re.compile(
    r"^\s*([A-Za-z0-9_]+)\s*" + _ARROW_ALT + r"\s*([A-Za-z0-9_]+)\s*:(.*)$"
)

# participant / actor alias declaration. Captures the alias text after `as`.
_ALIAS_LINE_RE = re.compile(
    r"^\s*(?:participant|actor)\s+\S+\s+as\s+(.+?)\s*$"
)

_ANGLE_PLACEHOLDER_RE = re.compile(r"<[\w/]+>")

_NON_SEQUENCE_HEADERS = {
    "flowchart",
    "graph",
    "statediagram",
    "statediagram-v2",
    "classdiagram",
    "erdiagram",
    "journey",
    "gantt",
    "pie",
    "mindmap",
    "timeline",
    "quadrantchart",
    "requirementdiagram",
    "gitgraph",
    "c4context",
}


def _is_sequence_diagram(block_text: str) -> bool:
    """Best-effort detection: skip blocks whose first non-empty line names a
    non-sequence diagram type. Otherwise treat as sequence (Mermaid's default
    for ambiguous blocks)."""
    for raw in block_text.splitlines():
        line = raw.strip()
        if not line:
            continue
        first_token = re.split(r"[\s\-]", line, maxsplit=1)[0].lower()
        if first_token in _NON_SEQUENCE_HEADERS:
            return False
        # Also strip a trailing direction marker like "flowchart TB".
        head = line.split(None, 1)[0].lower()
        if head in _NON_SEQUENCE_HEADERS:
            return False
        return True
    return False


def _check_block(
    file_path: Path, block_text: str, start_line: int
) -> list[tuple[Path, int, str, str]]:
    """Return findings for one mermaid block. start_line is the line of the
    opening ```mermaid fence; the first inner line is start_line + 1."""
    findings: list[tuple[Path, int, str, str]] = []
    if not _is_sequence_diagram(block_text):
        return findings

    for offset, raw_line in enumerate(block_text.splitlines()):
        line_no = start_line + 1 + offset
        line = raw_line.rstrip("\r")

        msg_match = _MSG_LINE_RE.match(line)
        if msg_match:
            message_text = msg_match.group(3)
            if ";" in message_text:
                findings.append(
                    (
                        file_path,
                        line_no,
                        "mermaid.semicolon-in-message",
                        "semicolon in sequence-diagram message text breaks "
                        "Mermaid parser; replace with em-dash or comma",
                    )
                )
            if _ANGLE_PLACEHOLDER_RE.search(message_text):
                findings.append(
                    (
                        file_path,
                        line_no,
                        "mermaid.angle-bracket-in-message",
                        "angle-bracket placeholder in message text may be "
                        "HTML-escaped or break parsing; use literal "
                        "placeholder name (PATH) or square brackets",
                    )
                )
            continue

        alias_match = _ALIAS_LINE_RE.match(line)
        if alias_match:
            alias = alias_match.group(1)
            quoted = alias.startswith('"') and alias.endswith('"')
            if not quoted and re.search(r"[/:,]", alias):
                findings.append(
                    (
                        file_path,
                        line_no,
                        "mermaid.unquoted-alias-special-char",
                        "participant alias contains special character "
                        "(/ : ,); quote with double quotes or replace",
                    )
                )

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
        print(f"check-mermaid: input not found: {exc}", file=sys.stderr)
        return 2

    findings: list[tuple[Path, int, str, str]] = []
    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(f"check-mermaid: cannot read {md}: {exc}", file=sys.stderr)
            return 2
        for block_text, start_line, _end_line in iter_mermaid_blocks(text):
            findings.extend(_check_block(md, block_text, start_line))

    findings.sort(key=lambda f: (str(f[0]), f[1], f[2]))
    for path, line, rule, msg in findings:
        print(f"{path}:{line}:{rule}:{msg}")

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
