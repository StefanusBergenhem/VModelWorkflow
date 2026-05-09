"""Shared parsing helpers for VModelWorkflow check scripts.

Used by the Phase 6 Cluster 3 mechanical check scripts under scripts/.
Every helper is deterministic and side-effect free; line numbers returned
are 1-based to match the script-output contract documented in
docs/authoring-self-check.md.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterator, Optional, Tuple, Union

import yaml


def parse_yaml_frontmatter(
    md_text: str,
) -> Tuple[Optional[dict], str, int]:
    """Split a Markdown document into (frontmatter_dict, body_text, frontmatter_end_line).

    Recognises the canonical opener ``---\\n...\\n---\\n`` only when it is the
    very first content of the file. Returns ``(None, md_text, 0)`` when no
    front-matter is present. ``frontmatter_end_line`` is the 1-based line of
    the closing ``---`` (so the body starts on the next line).

    YAML parse errors return ``({}, body_text, end_line)`` — callers that
    care about parse failure should use ``safe_yaml_load`` on the captured
    text directly.
    """
    if not md_text.startswith("---\n") and not md_text.startswith("---\r\n"):
        return None, md_text, 0

    # Find the closing ---. It must sit on its own line.
    lines = md_text.splitlines(keepends=True)
    if len(lines) < 2:
        return None, md_text, 0

    closing_idx = None
    for i in range(1, len(lines)):
        stripped = lines[i].rstrip("\r\n")
        if stripped == "---":
            closing_idx = i
            break

    if closing_idx is None:
        return None, md_text, 0

    fm_text = "".join(lines[1:closing_idx])
    body_text = "".join(lines[closing_idx + 1 :])
    end_line = closing_idx + 1  # 1-based

    try:
        fm = yaml.safe_load(fm_text) or {}
        if not isinstance(fm, dict):
            fm = {}
    except yaml.YAMLError:
        fm = {}

    return fm, body_text, end_line


_FENCE_OPEN_RE = re.compile(r"^([ \t]*)```(\w+)\s*$")
_FENCE_CLOSE_RE = re.compile(r"^([ \t]*)```\s*$")


def _iter_fenced_blocks(
    md_text: str, lang: str
) -> Iterator[Tuple[str, int, int]]:
    """Yield (block_text, start_line, end_line) for each fenced code block of ``lang``.

    ``start_line`` is the 1-based line of the opening fence; ``end_line`` is
    the 1-based line of the closing fence. ``block_text`` is the inner content
    (without the fence markers themselves), preserving the original line
    endings.
    """
    lines = md_text.splitlines(keepends=True)
    i = 0
    while i < len(lines):
        line = lines[i].rstrip("\r\n")
        m_open = _FENCE_OPEN_RE.match(line)
        if m_open and m_open.group(2).lower() == lang.lower():
            start_line = i + 1
            inner: list[str] = []
            j = i + 1
            while j < len(lines):
                inner_line = lines[j].rstrip("\r\n")
                if _FENCE_CLOSE_RE.match(inner_line):
                    end_line = j + 1
                    yield "".join(inner), start_line, end_line
                    i = j + 1
                    break
                inner.append(lines[j])
                j += 1
            else:
                # No closing fence — treat remainder as the block.
                end_line = len(lines)
                yield "".join(inner), start_line, end_line
                i = len(lines)
        else:
            i += 1


def iter_yaml_blocks(md_text: str) -> Iterator[Tuple[str, int, int]]:
    """Yield each ```yaml fenced block as (block_text, start_line, end_line)."""
    yield from _iter_fenced_blocks(md_text, "yaml")


def iter_mermaid_blocks(md_text: str) -> Iterator[Tuple[str, int, int]]:
    """Yield each ```mermaid fenced block as (block_text, start_line, end_line)."""
    yield from _iter_fenced_blocks(md_text, "mermaid")


def safe_yaml_load(text: str) -> Union[dict, list, None]:
    """Wrap ``yaml.safe_load``. Returns None on parse error, empty input, or ``null``.

    Callers decide whether None is a finding; the parser does not flag.
    """
    try:
        loaded = yaml.safe_load(text)
    except yaml.YAMLError:
        return None
    return loaded


def find_md_files(specs_root: Path) -> Iterator[Path]:
    """Yield every ``*.md`` file under ``specs_root`` recursively.

    If ``specs_root`` is itself a ``.md`` file, yield only that file. The
    caller is responsible for validating the path exists; we raise
    ``FileNotFoundError`` for non-existent inputs to keep error handling
    explicit at the script boundary.
    """
    if not specs_root.exists():
        raise FileNotFoundError(str(specs_root))
    if specs_root.is_file():
        if specs_root.suffix == ".md":
            yield specs_root
        return
    yield from sorted(p for p in specs_root.rglob("*.md") if p.is_file())
