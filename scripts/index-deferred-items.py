#!/usr/bin/env python3
"""Cross-artifact deferred-items index (Phase 6 Issue 12).

Walks a specs tree, extracts every ``[DEFER-DD: ...]`` and
``[DEFER-ADR: ...]`` inline marker plus every ``## Open follow-ups`` section
across all artifacts, and emits a structured YAML index keyed by artifact +
scope. Informational (always exit 0); not a gate.

Distinct from the planned ``vmodel-core`` ``list-pending`` reporting
capability (a v1.x candidate). This script is the framework-side stopgap
that gives adopters a tree-level view of pending work without waiting on
``vmodel-core``.

Stable contract:
  exit 0 always (informational).
  stdout: structured YAML by default; ``--format json`` switches.
  stderr: pre-flight errors only (input-not-found etc.); exit 2.

Invocation: ./scripts/index-deferred-items.py <specs-root> [--format yaml|json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.spec_parser import find_md_files, parse_yaml_frontmatter  # noqa: E402


# Owning inline defer markers. Permissive on the description (any
# non-bracket chars). Square brackets are reserved for the OWNING form per
# authoring-discipline.md Rule 6 — the artifact that carries the marker is
# where the deferred decision will be answered.
_DEFER_RE = re.compile(r"\[DEFER-(DD|ADR):\s*([^\]]+)\]")

# Cite-form defer references — guillemet delimiters distinguish a reference
# to another artifact's owning marker from an owning marker itself. Body
# convention is "<owner-artifact-id> — <topic>" but the regex only requires
# the DEFER-(DD|ADR): prefix; the body is captured permissively.
_DEFER_CITE_RE = re.compile(r"«DEFER-(DD|ADR):\s*([^»]+)»")


# Header for the per-artifact open-follow-ups section. Match `## Open follow-ups`,
# `## Open Follow-ups`, `## Open gaps and follow-ups` (legacy variant), and
# similar near-cognates.
_OPEN_FOLLOWUPS_HEADER_RE = re.compile(
    r"^\s*##+\s+Open\s+(?:gaps?\s+and\s+)?follow[- ]ups?\s*$",
    re.IGNORECASE | re.MULTILINE,
)


# Markdown bullet starting a list item (- / * / numbered).
_BULLET_RE = re.compile(r"^\s*(?:[-*]|\d+\.)\s+(.*)$")


def _scope_from_fm_or_path(fm: dict | None, path: Path, specs_root: Path) -> str:
    """Resolve scope: prefer front-matter ``scope:``, fall back to relative path."""
    if isinstance(fm, dict):
        s = fm.get("scope")
        if isinstance(s, str):
            return s
    try:
        rel = path.relative_to(specs_root)
    except ValueError:
        rel = path
    parent = rel.parent
    return "" if parent == Path(".") else str(parent).replace("\\", "/")


def _artifact_id_from_fm(fm: dict | None) -> str | None:
    if isinstance(fm, dict):
        v = fm.get("id")
        if isinstance(v, str):
            return v
    return None


def _extract_defer_markers(text: str) -> list[dict]:
    """Owning markers — square-bracket form [DEFER-(DD|ADR): ...]."""
    out: list[dict] = []
    for m in _DEFER_RE.finditer(text):
        kind = m.group(1)  # DD | ADR
        body = m.group(2).strip()
        line_no = text[: m.start()].count("\n") + 1
        out.append(
            {
                "type": f"DEFER-{kind}",
                "line": line_no,
                "description": body,
            }
        )
    return out


def _extract_defer_citations(text: str) -> list[dict]:
    """Cite-form references — guillemet form «DEFER-(DD|ADR): owner-id — topic».

    Per authoring-discipline.md Rule 6, cite-form names another artifact's
    owning deferral without creating a second owner. Reported separately so
    the index can distinguish owners from cross-references.
    """
    out: list[dict] = []
    for m in _DEFER_CITE_RE.finditer(text):
        kind = m.group(1)
        body = m.group(2).strip()
        line_no = text[: m.start()].count("\n") + 1
        out.append(
            {
                "type": f"DEFER-{kind}-cite",
                "line": line_no,
                "description": body,
            }
        )
    return out


def _extract_open_follow_ups(text: str) -> list[dict]:
    """Extract bullet lines from any ``## Open follow-ups`` section.

    A section runs from its header until the next ``## ``-or-deeper header
    or end-of-file. We collect every bullet line (Markdown ``-`` / ``*`` /
    numbered). Empty section (``(none)`` literal or zero bullets) yields an
    empty list.
    """
    out: list[dict] = []
    headers = list(_OPEN_FOLLOWUPS_HEADER_RE.finditer(text))
    if not headers:
        return out

    next_header_re = re.compile(r"^\s*##+\s+", re.MULTILINE)
    lines = text.splitlines()

    for hdr in headers:
        hdr_line = text[: hdr.start()].count("\n") + 1  # 1-based line of the header

        # Section ends at the next ## header following this one.
        section_end_line = len(lines)  # exclusive 1-based-end (i.e., past EOF)
        for nh in next_header_re.finditer(text, pos=hdr.end()):
            nh_line = text[: nh.start()].count("\n") + 1
            section_end_line = nh_line - 1
            break

        for i in range(hdr_line, section_end_line):
            if i >= len(lines):
                break
            raw = lines[i]
            bm = _BULLET_RE.match(raw)
            if not bm:
                continue
            content = bm.group(1).strip()
            if content.lower() in {"(none)", "none"}:
                continue
            out.append({"line": i + 1, "text": content})
    return out


def _walk(specs_root: Path) -> list[dict]:
    items: list[dict] = []
    md_files = list(find_md_files(specs_root))
    for md in md_files:
        text = md.read_text(encoding="utf-8")
        fm, body, _ = parse_yaml_frontmatter(text)

        markers = _extract_defer_markers(text)
        citations = _extract_defer_citations(text)
        follow_ups = _extract_open_follow_ups(text)
        if not markers and not citations and not follow_ups:
            continue

        scope = _scope_from_fm_or_path(fm, md, specs_root)
        artifact_id = _artifact_id_from_fm(fm)
        try:
            rel_path = str(md.relative_to(specs_root))
        except ValueError:
            rel_path = str(md)

        items.append(
            {
                "scope": scope,
                "artifact_id": artifact_id,
                "path": rel_path,
                "defer_markers": markers,
                "defer_citations": citations,
                "open_follow_ups": follow_ups,
            }
        )
    return items


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("specs_root", type=Path, help="Path to a specs/ directory.")
    parser.add_argument(
        "--format",
        choices=("yaml", "json"),
        default="yaml",
        help="Output format (default: yaml).",
    )
    args = parser.parse_args()

    if not args.specs_root.exists() or not args.specs_root.is_dir():
        print(
            f"index-deferred-items: specs root not found or not a directory: "
            f"{args.specs_root}",
            file=sys.stderr,
        )
        return 2

    items = _walk(args.specs_root)

    total_markers = sum(len(it["defer_markers"]) for it in items)
    total_citations = sum(len(it.get("defer_citations", [])) for it in items)
    total_follow_ups = sum(len(it["open_follow_ups"]) for it in items)

    payload = {
        "specs_root": str(args.specs_root),
        "summary": {
            "artifacts_with_pending_items": len(items),
            "total_defer_markers": total_markers,
            "total_defer_citations": total_citations,
            "total_open_follow_ups": total_follow_ups,
        },
        "items": items,
    }

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True))

    return 0


if __name__ == "__main__":
    sys.exit(main())
