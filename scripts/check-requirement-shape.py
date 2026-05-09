#!/usr/bin/env python3
"""Requirement-shape gates (Phase 6 Issue 11).

Checks materialised requirement statements for atomicity (single shall/must),
EARS opening shape (Ubiquitous / Event-driven / State-driven / Optional /
Unwanted-behaviour), and a small implementation-prescription vocabulary
heuristic. Inputs: requirements files (REQ-*), ADR materialised statements,
and architecture-derived sub-requirements.

Invocation: ./scripts/check-requirement-shape.py <specs-root>
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


# Implementation-prescription vocabulary. Intentionally tiny — heuristic
# complement to human review, not a replacement. Add tokens by literal
# string; matching is whole-token (with explicit word-boundary handling for
# tokens containing `/`).
IMPL_VOCAB: tuple[str, ...] = (
    "html/template",
    "encoding/json",
    "goccy/go-yaml",
)


_SHALL_MUST_RE = re.compile(r"\b(?:shall|must)\b", re.IGNORECASE)


# EARS separator: comma, em-dash (—), or en-dash (–). Canonical EARS uses comma,
# but em-dashes are equivalent punctuation when bracketing a parenthetical clause
# (e.g., "When X — clarification — the system shall ..."). Accept all three.
_SEP = r"[,–—]"

_EARS_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    # Ubiquitous: "The|A|An <subject> shall|must <action>"
    ("ubiquitous", re.compile(r"^(?:The|A|An)\s+\S+.*\b(?:shall|must)\b", re.DOTALL)),
    # Event-driven: "When <event>, the <subject> shall|must <action>"
    (
        "event-driven",
        re.compile(
            rf"^When\s+.+?{_SEP}\s*the\s+\S+.*\b(?:shall|must)\b", re.DOTALL
        ),
    ),
    # State-driven: "While <state>, the <subject> shall|must <action>"
    (
        "state-driven",
        re.compile(
            rf"^While\s+.+?{_SEP}\s*the\s+\S+.*\b(?:shall|must)\b", re.DOTALL
        ),
    ),
    # Optional-feature: "Where <feature is included>, the <subject> shall|must"
    (
        "optional",
        re.compile(
            rf"^Where\s+.+?{_SEP}\s*the\s+\S+.*\b(?:shall|must)\b", re.DOTALL
        ),
    ),
    # Unwanted-behaviour: "If <unwanted condition>, then the <subject> shall|must"
    (
        "unwanted",
        re.compile(
            rf"^If\s+.+?{_SEP}\s*then\s+the\s+\S+.*\b(?:shall|must)\b", re.DOTALL
        ),
    ),
)


_INLINE_MATERIALISED_RE = re.compile(
    r"Materialised\s+as:\s*(REQ-\d+)\s*[—\-:]\s*[\"']([^\"']+)[\"']",
    re.IGNORECASE,
)


def _is_requirements(fm: dict | None, path: Path) -> bool:
    if fm and str(fm.get("artifact_type", "")).lower() == "requirements":
        return True
    if fm and str(fm.get("type", "")).lower() == "requirements":
        return True
    if path.name == "requirements.md":
        return True
    return False


def _is_adr(fm: dict | None, path: Path) -> bool:
    if fm and str(fm.get("artifact_type", "")).lower() == "adr":
        return True
    if fm and str(fm.get("type", "")).lower() == "adr":
        return True
    if "adrs" in path.parts:
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


_REQ_ID_RE = re.compile(r"^REQ-\d+$")


def _statements_from_requirements(
    md_text: str,
) -> list[tuple[str, str, int]]:
    """Yield (req_id, statement_text, block_start_line) tuples."""
    out: list[tuple[str, str, int]] = []
    for block_text, start_line, _end in iter_yaml_blocks(md_text):
        loaded = safe_yaml_load(block_text)
        if loaded is None:
            continue
        items = (
            loaded
            if isinstance(loaded, list)
            else [loaded]
            if isinstance(loaded, dict)
            else []
        )
        for item in items:
            if not isinstance(item, dict):
                continue
            req_id = item.get("id")
            statement = item.get("statement")
            if not isinstance(req_id, str) or not _REQ_ID_RE.match(req_id):
                continue
            if not isinstance(statement, str):
                continue
            out.append((req_id, statement, start_line))
    return out


def _statements_from_adr(
    md_text: str,
) -> list[tuple[str, str, int]]:
    """ADR materialised statements via either YAML form or inline prose."""
    out: list[tuple[str, str, int]] = []
    yaml_ids_seen: set[str] = set()

    for block_text, start_line, _end in iter_yaml_blocks(md_text):
        loaded = safe_yaml_load(block_text)
        if loaded is None:
            continue
        if isinstance(loaded, dict):
            items = [loaded]
        elif isinstance(loaded, list):
            items = [i for i in loaded if isinstance(i, dict)]
        else:
            continue
        for item in items:
            for key in ("materialised_as", "materialised_requirement"):
                if key not in item:
                    continue
                materialised = item[key]
                if isinstance(materialised, dict):
                    mid = materialised.get("id")
                    stmt = materialised.get("statement")
                    if isinstance(mid, str) and isinstance(stmt, str):
                        out.append((mid, stmt, start_line))
                        yaml_ids_seen.add(mid)

    if not out:
        # Fall back to inline-prose extraction only if YAML form absent.
        for line_no, raw in enumerate(md_text.splitlines(), start=1):
            for m in _INLINE_MATERIALISED_RE.finditer(raw):
                rid, stmt = m.group(1), m.group(2)
                if rid in yaml_ids_seen:
                    continue
                out.append((rid, stmt, line_no))

    return out


def _statements_from_architecture(
    md_text: str,
) -> list[tuple[str, str, int]]:
    out: list[tuple[str, str, int]] = []
    for block_text, start_line, _end in iter_yaml_blocks(md_text):
        loaded = safe_yaml_load(block_text)
        if loaded is None:
            continue
        if isinstance(loaded, dict):
            items = [loaded]
        elif isinstance(loaded, list):
            items = [i for i in loaded if isinstance(i, dict)]
        else:
            continue
        for item in items:
            if "derived_requirement" not in item:
                continue
            derived = item["derived_requirement"]
            if isinstance(derived, dict):
                mid = derived.get("id") or "<derived>"
                stmt = derived.get("statement")
                if isinstance(stmt, str):
                    out.append((str(mid), stmt, start_line))
            elif isinstance(derived, str):
                out.append(("<derived>", derived, start_line))
    return out


def _check_compound(stmt: str) -> int:
    """Return number of shall/must keywords."""
    return len(_SHALL_MUST_RE.findall(stmt))


def _check_ears(stmt: str) -> bool:
    """Return True if the statement opens with a valid EARS pattern."""
    head = stmt.lstrip()
    for _name, pattern in _EARS_PATTERNS:
        if pattern.match(head):
            return True
    return False


def _check_implementation_prescription(stmt: str) -> list[str]:
    """Return list of impl-vocab tokens detected. Conservative: each token
    matched as whole-token (word boundaries when alphanumeric chars; literal
    substring when the token contains a path separator or other non-word
    char that defeats `\\b`)."""
    hits: list[str] = []
    for token in IMPL_VOCAB:
        # Tokens containing `/` (e.g., html/template) defeat \b at the slash;
        # use a custom boundary that requires non-identifier on both sides.
        escaped = re.escape(token)
        starts_word = bool(re.match(r"\w", token))
        ends_word = bool(re.search(r"\w$", token))
        prefix = r"(?<![A-Za-z0-9_])" if not starts_word else r"\b"
        suffix = r"(?![A-Za-z0-9_])" if not ends_word else r"\b"
        if re.search(prefix + escaped + suffix, stmt):
            hits.append(token)
    return hits


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
            f"check-requirement-shape: input not found: {exc}",
            file=sys.stderr,
        )
        return 2

    findings: list[tuple[Path, int, str, str]] = []
    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(
                f"check-requirement-shape: cannot read {md}: {exc}",
                file=sys.stderr,
            )
            return 2
        fm, _body, _end = parse_yaml_frontmatter(text)

        statements: list[tuple[str, str, int]] = []
        if _is_requirements(fm, md):
            statements.extend(_statements_from_requirements(text))
        if _is_adr(fm, md):
            statements.extend(_statements_from_adr(text))
        if _is_architecture(fm, md):
            statements.extend(_statements_from_architecture(text))

        for req_id, stmt, line in statements:
            stmt_clean = stmt.strip()

            n_keywords = _check_compound(stmt_clean)
            if n_keywords >= 2:
                findings.append(
                    (
                        md,
                        line,
                        "req.compound",
                        f"statement contains {n_keywords} shall/must "
                        f"keywords; split into atomic statements ({req_id})",
                    )
                )

            if not _check_ears(stmt_clean):
                findings.append(
                    (
                        md,
                        line,
                        "req.ears-invalid",
                        f"statement does not open with a valid EARS keyword "
                        f"(Ubiquitous/Event-driven/State-driven/Optional/"
                        f"Unwanted) ({req_id})",
                    )
                )

            for token in _check_implementation_prescription(stmt_clean):
                findings.append(
                    (
                        md,
                        line,
                        "req.implementation-prescription",
                        f'statement names implementation token "{token}"; '
                        f"use what-not-how — name the observable behaviour, "
                        f"not the mechanism ({req_id})",
                    )
                )

    findings.sort(key=lambda f: (str(f[0]), f[1], f[2], f[3]))
    for path, line, rule, msg in findings:
        print(f"{path}:{line}:{rule}:{msg}")

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
