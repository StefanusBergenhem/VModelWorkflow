#!/usr/bin/env python3
"""Empty-scope ID encoding gate (Phase 6 Issue 17).

Detects malformed empty-scope identifier forms across the spec tree. The
canonical empty-scope rule (TARGET_ARCHITECTURE.md §5.4) states that at root
scope the scope segment is omitted from all derived identifiers — bare type
prefix, no trailing hyphen.

Three malformed-form classes flagged:

1. Trailing-hyphen artifact ids — ``TS-``, ``ARCH-``, ``REQS-``, ``PB-``,
   ``DD-`` followed by end-of-string, whitespace, or punctuation. (At
   non-empty scope these would carry a scope segment after the hyphen; the
   bare-prefix-with-trailing-hyphen form is wrong at any scope.)
2. Double-hyphen per-element ids — ``TC--NNN`` or ``REQ--NNN`` from a
   placeholder that resolved with empty scope but kept the surrounding
   hyphens.
3. Stranded-hyphen dotted-path refs — ``ARCH-.interfaces.X``,
   ``REQS-.functional.X``, ``DD-.public_interface.X``, ``TS-.cases.X`` from
   a path placeholder that resolved with empty scope.

Stable finding contract: ``<file>:<line>:<rule-id>:<message>``.
Exit codes: 0 (clean) | 1 (findings) | 2 (error).

Invocation: ./scripts/check-id-encoding.py <specs-root>
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.spec_parser import find_md_files  # noqa: E402


# Scrub these placeholder forms before regex scanning so legitimate template
# scaffolding (e.g., `id: TS-<<scope-suffix?>>`) doesn't trip a false positive.
# Real specs never contain ``<<...>>`` or unbalanced ``<...>`` placeholders.
_PLACEHOLDER_RE = re.compile(r"<<[^<>]*>>|<[A-Za-z][A-Za-z0-9_\-]*>")


# 1. Trailing-hyphen artifact ids: prefix followed by `-` then end-of-token.
#    Matches `TS-`, `ARCH-`, etc., but NOT `TS-app-checkout` (real scope).
#    Boundary: trailing-hyphen followed by whitespace, EOL, punctuation, or
#    closing brace — but NOT by `[A-Za-z0-9_]`, which would be a scope segment.
_TRAILING_HYPHEN_RE = re.compile(
    r"(?<![A-Za-z0-9_])(TS|ARCH|REQS|PB|DD)-(?![A-Za-z0-9_])"
)


# 2. Double-hyphen per-element ids: `TC--<digits>` or `REQ--<digits>`.
_DOUBLE_HYPHEN_RE = re.compile(r"(?<![A-Za-z0-9_])(TC|REQ)--(\d+)")


# 3. Stranded-hyphen dotted-path refs: `<PREFIX>-.<word>`.
_STRANDED_DOT_RE = re.compile(
    r"(?<![A-Za-z0-9_])(TS|ARCH|REQS|PB|DD)-(?=\.[A-Za-z_])"
)


def _scrub_placeholders(text: str) -> str:
    return _PLACEHOLDER_RE.sub("__PLACEHOLDER__", text)


def _line_of(text: str, char_index: int) -> int:
    """1-based line number for a character offset."""
    return text[:char_index].count("\n") + 1


def _scan(text: str, path: Path) -> list[tuple[Path, int, str, str]]:
    findings: list[tuple[Path, int, str, str]] = []
    scrubbed = _scrub_placeholders(text)

    for m in _TRAILING_HYPHEN_RE.finditer(scrubbed):
        prefix = m.group(1)
        line_no = _line_of(scrubbed, m.start())
        findings.append(
            (
                path,
                line_no,
                "id-encoding.trailing-hyphen",
                f'malformed empty-scope id "{prefix}-"; at root scope the '
                f'bare prefix "{prefix}" is canonical (TARGET §5.4)',
            )
        )

    for m in _DOUBLE_HYPHEN_RE.finditer(scrubbed):
        prefix, seq = m.group(1), m.group(2)
        line_no = _line_of(scrubbed, m.start())
        findings.append(
            (
                path,
                line_no,
                "id-encoding.double-hyphen",
                f'malformed empty-scope id "{prefix}--{seq}"; at root scope '
                f'the scope segment is dropped — use "{prefix}-{seq}" '
                f"(TARGET §5.4)",
            )
        )

    for m in _STRANDED_DOT_RE.finditer(scrubbed):
        prefix = m.group(1)
        line_no = _line_of(scrubbed, m.start())
        findings.append(
            (
                path,
                line_no,
                "id-encoding.stranded-hyphen-before-dot",
                f'malformed empty-scope dotted-path ref "{prefix}-."; at '
                f'root scope the bare prefix is canonical — use "{prefix}." '
                f"(TARGET §5.4)",
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
        print(f"check-id-encoding: input not found: {exc}", file=sys.stderr)
        return 2

    findings: list[tuple[Path, int, str, str]] = []
    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(f"check-id-encoding: cannot read {md}: {exc}", file=sys.stderr)
            return 2
        findings.extend(_scan(text, md))

    findings.sort(key=lambda f: (str(f[0]), f[1], f[2], f[3]))
    for path, line, rule, msg in findings:
        print(f"{path}:{line}:{rule}:{msg}")

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
