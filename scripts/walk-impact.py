#!/usr/bin/env python3
"""Candidate-set propagation walker (TARGET_ARCHITECTURE §8.3).

Given a spec artifact (or per-element id) that is being changed, walk the
spec tree's traceability graph in the reverse direction and emit the set of
artifacts that may need to be revisited as a consequence. The change is
incomplete until every candidate is either updated or explicitly closed as
"no change needed" with a brief reason.

Forward links extracted:
    - envelope  ``derived_from``        (list)
    - envelope  ``parent_architecture`` (scalar)
    - envelope  ``governing_adrs``      (list)
    - envelope  ``verifies``            (list)
    - envelope  ``supersedes`` / ``superseded_by`` (scalar; ADR lineage)
    - per-child YAML block ``allocates`` (list; Architecture decomposition)
    - per-case  YAML block ``verifies``  (list; TestSpec cases)

Per-element ids (REQ-NNN, TC-NNN, decomposition child ids) are discovered as
graph nodes so that ``allocates: [REQ-001]`` and ``verifies: [REQ-001]``
resolve. They are not themselves emitted as candidates — the candidate set
lists *artifacts* (the file you would open to make a change), not internal
ids.

Out of scope for v1:
    - ADR ``scope_tags`` / ``affected_scopes`` (target scopes, not artifact ids)
    - per-interface YAML blocks in Architecture (rarely carry outgoing links)

Invocation:
    ./scripts/walk-impact.py <ARTIFACT-ID-OR-ELEMENT-ID> [--specs-root PATH] [--format text|json]

Exit codes: 0 (success) | 1 (entry id not found) | 2 (specs root not found).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.spec_parser import (  # noqa: E402
    find_md_files,
    iter_yaml_blocks,
    parse_yaml_frontmatter,
    safe_yaml_load,
)


ENVELOPE_LIST_LINKS = ("derived_from", "governing_adrs", "verifies")
ENVELOPE_SCALAR_LINKS = ("parent_architecture", "supersedes", "superseded_by")
PER_ELEMENT_LIST_LINKS = ("verifies", "allocates", "governing_adrs")


# --------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------


@dataclass
class Node:
    """One discovered id in the spec tree.

    ``kind`` distinguishes top-level artifacts (the change unit) from
    per-element ids (REQ-NNN, TC-NNN, decomposition child ids) so the walker
    can include only artifacts in the emitted candidate set.
    """

    id: str
    path: Path
    kind: str  # 'artifact' | 'element'


@dataclass
class Candidate:
    id: str
    path: str
    link_type: str
    hops: int


@dataclass
class Graph:
    nodes: dict = field(default_factory=dict)
    outgoing: dict = field(default_factory=lambda: defaultdict(list))
    reverse: dict = field(default_factory=lambda: defaultdict(list))

    def rebuild_reverse(self) -> None:
        """Recompute ``reverse`` from ``outgoing``. Used after mutations in tests."""
        self.reverse = defaultdict(list)
        for src, edges in self.outgoing.items():
            for link_type, tgt in edges:
                self.reverse[tgt].append((link_type, src))


# --------------------------------------------------------------------------
# Discovery + forward-link extraction
# --------------------------------------------------------------------------


def _add_envelope_links(graph: Graph, artifact_id: str, fm: dict) -> None:
    for link_type in ENVELOPE_SCALAR_LINKS:
        target = fm.get(link_type)
        if isinstance(target, str) and target:
            graph.outgoing[artifact_id].append((link_type, target))
    for link_type in ENVELOPE_LIST_LINKS:
        targets = fm.get(link_type) or []
        if isinstance(targets, list):
            for target in targets:
                if isinstance(target, str) and target:
                    graph.outgoing[artifact_id].append((link_type, target))


def _add_per_element_links(graph: Graph, artifact_id: str, body: str, md_path: Path) -> None:
    for block_text, _, _ in iter_yaml_blocks(body):
        block = safe_yaml_load(block_text)
        if not isinstance(block, dict):
            continue

        elem_id = block.get("id")
        if isinstance(elem_id, str) and elem_id and elem_id not in graph.nodes:
            # Register the element id so per-element references can resolve to it.
            # The containing artifact is what callers care about as a change unit;
            # elements are landing points only.
            graph.nodes[elem_id] = Node(id=elem_id, path=md_path, kind="element")

        for link_type in PER_ELEMENT_LIST_LINKS:
            targets = block.get(link_type) or []
            if isinstance(targets, list):
                for target in targets:
                    if isinstance(target, str) and target:
                        # Forward link is attributed to the containing artifact —
                        # if the artifact changes, the per-element link's target
                        # is what may need revisiting.
                        graph.outgoing[artifact_id].append((link_type, target))


def build_graph(specs_root: Path) -> Graph:
    """Walk ``specs_root``, parse every artifact's front-matter + body YAML, return a Graph."""
    graph = Graph()

    for md_path in find_md_files(specs_root):
        try:
            text = md_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        fm, body, _ = parse_yaml_frontmatter(text)
        if not fm or not isinstance(fm.get("id"), str):
            continue

        artifact_id = fm["id"]
        graph.nodes[artifact_id] = Node(id=artifact_id, path=md_path, kind="artifact")
        _add_envelope_links(graph, artifact_id, fm)
        _add_per_element_links(graph, artifact_id, body, md_path)

    graph.rebuild_reverse()
    return graph


# --------------------------------------------------------------------------
# BFS reverse traversal
# --------------------------------------------------------------------------


def walk(entry_id: str, graph: Graph) -> list:
    """BFS reverse from ``entry_id``. Returns artifacts in (hops, id) order."""
    visited = {entry_id}
    queue = deque([(entry_id, 0)])
    first_hop = {}  # id -> (link_type, hops)

    while queue:
        current, hops = queue.popleft()
        for link_type, source in graph.reverse.get(current, []):
            if source in visited:
                continue
            visited.add(source)
            first_hop[source] = (link_type, hops + 1)
            queue.append((source, hops + 1))

    candidates = []
    for cand_id, (link_type, hops) in first_hop.items():
        node = graph.nodes.get(cand_id)
        if node is None or node.kind != "artifact":
            continue
        candidates.append(Candidate(id=cand_id, path=str(node.path), link_type=link_type, hops=hops))

    candidates.sort(key=lambda c: (c.hops, c.id))
    return candidates


# --------------------------------------------------------------------------
# Output formatters
# --------------------------------------------------------------------------


def format_text(entry_id: str, candidates: list) -> str:
    if not candidates:
        return f"Candidate set for {entry_id}: (empty)\n"
    by_hops = defaultdict(list)
    for c in candidates:
        by_hops[c.hops].append(c)
    lines = [f"Candidate set for {entry_id}:"]
    for hops in sorted(by_hops):
        label = "Direct (1 hop)" if hops == 1 else f"Transitive ({hops} hops)"
        lines.append(f"  {label}:")
        for c in sorted(by_hops[hops], key=lambda x: x.id):
            lines.append(f"    {c.id} — {c.path} ({c.link_type})")
    return "\n".join(lines) + "\n"


def format_json(entry_id: str, candidates: list) -> str:
    payload = {
        "entry": entry_id,
        "candidates": [
            {"id": c.id, "path": c.path, "link_type": c.link_type, "hops": c.hops}
            for c in candidates
        ],
    }
    return json.dumps(payload, indent=2) + "\n"


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="walk-impact",
        description="Candidate-set propagation walker (TARGET_ARCHITECTURE §8.3).",
    )
    parser.add_argument("entry_id", help="Artifact id (or per-element id) to walk reverse from.")
    parser.add_argument(
        "--specs-root",
        default="specs",
        help="Root of the spec tree (default: %(default)s).",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: %(default)s).",
    )
    args = parser.parse_args(argv)

    specs_root = Path(args.specs_root)
    if not specs_root.exists():
        print(f"error: specs root not found: {specs_root}", file=sys.stderr)
        return 2

    graph = build_graph(specs_root)
    if args.entry_id not in graph.nodes:
        print(
            f"error: artifact id '{args.entry_id}' not found under {specs_root}",
            file=sys.stderr,
        )
        return 1

    candidates = walk(args.entry_id, graph)
    if args.format == "json":
        sys.stdout.write(format_json(args.entry_id, candidates))
    else:
        sys.stdout.write(format_text(args.entry_id, candidates))
    return 0


if __name__ == "__main__":
    sys.exit(main())
