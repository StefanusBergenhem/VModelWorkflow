#!/usr/bin/env python3
"""Template/schema property-name divergence (Phase 6 Issue 6).

Catches deprecated-name regressions in author-skill templates. Walks every
``templates/*.tmpl`` file under each of the 5 author skills, parses YAML
front-matter and embedded YAML blocks (tolerating ``<<placeholder>>`` syntax
by string-substitution before parse), recursively walks every dict key, and
flags any key whose name appears in the deprecated-names table.

Why a narrow deprecated-names table rather than a strict schema diff: the
artifact schemas declare ``additionalProperties: true`` at the envelope and
inside several ``$defs``, so a strict-properties diff produces noise from
schema-side gaps (e.g., NFR ``planguage`` block, interface-requirement
five-dimension shape) that templates legitimately use. Those gaps are
schema-side improvements tracked separately; this script's job is to catch
template-side regressions when a property is renamed in the schema but the
templates drift.

Add a renamed property to ``DEPRECATED_NAMES`` and the script will catch
future regressions.

Stable finding contract: ``<file>:<line>:<rule-id>:<message>``.
Exit codes: 0 (clean) | 1 (findings) | 2 (error).

Invocation: ./scripts/check-template-schema-fields.py <skills-root>

The skills-root is typically one of:
  /home/stefanus/repos/VModelWorkflow/.claude/skills
  /home/stefanus/repos/vmodel-core/.claude/skills
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.spec_parser import (  # noqa: E402
    iter_yaml_blocks,
    parse_yaml_frontmatter,
    safe_yaml_load,
)


# Deprecated → canonical property names. Keys are deprecated; values are the
# replacement to suggest. Add entries when a schema property is renamed.
DEPRECATED_NAMES: dict[str, str] = {
    "governing_decisions": "governing_adrs",
}


# Five author skills the script audits.
AUTHOR_SKILLS: tuple[str, ...] = (
    "vmodel-skill-author-requirements",
    "vmodel-skill-author-architecture",
    "vmodel-skill-author-detailed-design",
    "vmodel-skill-author-testspec",
    "vmodel-skill-author-adr",
)


# Match `<<placeholder>>` and `<<placeholder?>>` for substitution before YAML parse.
_PLACEHOLDER_RE = re.compile(r"<<[^<>]*>>")


def _scrub_placeholders(text: str) -> str:
    """Replace ``<<...>>`` placeholders with a sentinel string so YAML parses."""
    return _PLACEHOLDER_RE.sub("__PLACEHOLDER__", text)


def _walk_keys(node: object, found: list[str]) -> None:
    """Collect every dict key recursively."""
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(k, str):
                found.append(k)
            _walk_keys(v, found)
    elif isinstance(node, list):
        for item in node:
            _walk_keys(item, found)


def _find_key_lines(template_text: str, key: str) -> list[int]:
    """Find 1-based line numbers where `key:` appears at the start of a YAML key.

    Tolerant of indentation; does not validate it's truly a key (vs a value
    that happens to look like one). Used only for reporting.
    """
    lines: list[int] = []
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*:", re.MULTILINE)
    for m in pattern.finditer(template_text):
        line_no = template_text[: m.start()].count("\n") + 1
        lines.append(line_no)
    return lines


def _audit_template(path: Path) -> list[tuple[Path, int, str, str]]:
    """Return a list of findings for one template file."""
    findings: list[tuple[Path, int, str, str]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return findings

    scrubbed = _scrub_placeholders(text)

    # Pull keys from front-matter (if any).
    keys_seen: list[str] = []
    fm, body, _ = parse_yaml_frontmatter(scrubbed)
    if isinstance(fm, dict):
        _walk_keys(fm, keys_seen)

    # Pull keys from every embedded YAML block.
    for block_text, _start, _end in iter_yaml_blocks(scrubbed):
        loaded = safe_yaml_load(block_text)
        if loaded is not None:
            _walk_keys(loaded, keys_seen)

    # Some .tmpl files are pure YAML (no Markdown wrapper); try a plain parse.
    if not fm and not list(iter_yaml_blocks(scrubbed)):
        loaded = safe_yaml_load(scrubbed)
        if loaded is not None:
            _walk_keys(loaded, keys_seen)

    # Flag deprecated names. Use the original (un-scrubbed) text for line numbers.
    seen_set = set(keys_seen)
    for deprecated, canonical in DEPRECATED_NAMES.items():
        if deprecated not in seen_set:
            continue
        for line_no in _find_key_lines(text, deprecated):
            findings.append(
                (
                    path,
                    line_no,
                    "template.deprecated-property",
                    f'property "{deprecated}" is deprecated; rename to '
                    f'"{canonical}"',
                )
            )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "skills_root",
        type=Path,
        help=(
            "Path to a `.claude/skills` directory containing the 5 author "
            "skills. The script audits each skill's templates/ subtree."
        ),
    )
    args = parser.parse_args()

    if not args.skills_root.exists() or not args.skills_root.is_dir():
        print(
            f"check-template-schema-fields: skills root not found or not a "
            f"directory: {args.skills_root}",
            file=sys.stderr,
        )
        return 2

    findings: list[tuple[Path, int, str, str]] = []
    for skill in AUTHOR_SKILLS:
        templates_dir = args.skills_root / skill / "templates"
        if not templates_dir.is_dir():
            continue
        for tmpl in sorted(templates_dir.rglob("*.tmpl")):
            findings.extend(_audit_template(tmpl))

    findings.sort(key=lambda f: (str(f[0]), f[1], f[2], f[3]))
    for path, line, rule, msg in findings:
        print(f"{path}:{line}:{rule}:{msg}")

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
