"""Tests for scripts/walk-impact.py — candidate-set propagation walker.

Fixture spec tree under tests/fixtures/walk-impact/specs/ exercises every
canonical link type (derived_from, parent_architecture, allocates, verifies,
governing_adrs) plus per-element references (REQ-NNN, TC-NNN, decomposition
child IDs).

Run:
    .venv/bin/python -m unittest tests.test_walk_impact -v
"""

from __future__ import annotations

import io
import json
import os
import sys
import unittest
from contextlib import redirect_stdout, redirect_stderr
from importlib import import_module
from pathlib import Path

# Walker module lives under scripts/ with a hyphen in its filename, so we import
# via importlib (mirrors tests/test_generate_arch_diagram.py).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
walk_impact = import_module("walk-impact")


FIXTURES = Path(__file__).resolve().parent / "fixtures" / "walk-impact" / "specs"


# --------------------------------------------------------------------------
# Discovery — IDs and forward links
# --------------------------------------------------------------------------


class TestDiscovery(unittest.TestCase):
    """The discovery pass finds every artifact id and every per-element id."""

    def test_discovers_all_artifact_ids(self):
        graph = walk_impact.build_graph(FIXTURES)
        expected_artifact_ids = {
            "PB",
            "REQS",
            "ARCH",
            "TS",
            "ADR-001-use-redis",
            "REQS-app",
            "ARCH-app",
            "TS-app",
            "DD-app-checkout-discount",
            "TS-app-checkout",
        }
        self.assertTrue(
            expected_artifact_ids.issubset(set(graph.nodes)),
            f"missing artifact ids: {expected_artifact_ids - set(graph.nodes)}",
        )

    def test_discovers_per_requirement_ids(self):
        graph = walk_impact.build_graph(FIXTURES)
        # Per-requirement entries from requirements.md and app/requirements.md
        for req_id in ("REQ-001", "REQ-002", "REQ-app-001"):
            self.assertIn(req_id, graph.nodes, f"{req_id} not discovered")

    def test_artifact_path_is_recorded(self):
        graph = walk_impact.build_graph(FIXTURES)
        self.assertTrue(
            str(graph.nodes["DD-app-checkout-discount"].path).endswith(
                os.path.join("app", "checkout", "detailed_design.md")
            )
        )


# --------------------------------------------------------------------------
# Forward-link extraction
# --------------------------------------------------------------------------


class TestForwardLinks(unittest.TestCase):
    """Forward-link extraction reads the canonical link types."""

    def setUp(self):
        self.graph = walk_impact.build_graph(FIXTURES)

    def _outgoing(self, source_id):
        return [(lt, t) for (lt, t) in self.graph.outgoing.get(source_id, [])]

    def test_derived_from_envelope_link(self):
        # REQS-app derives from REQS
        self.assertIn(("derived_from", "REQS"), self._outgoing("REQS-app"))

    def test_parent_architecture_link(self):
        # DD-app-checkout-discount has parent_architecture: ARCH-app
        self.assertIn(
            ("parent_architecture", "ARCH-app"),
            self._outgoing("DD-app-checkout-discount"),
        )

    def test_governing_adrs_link(self):
        # REQS-app has governing_adrs: [ADR-001-use-redis]
        self.assertIn(
            ("governing_adrs", "ADR-001-use-redis"),
            self._outgoing("REQS-app"),
        )

    def test_envelope_verifies_link(self):
        # TS-app envelope verifies: [REQ-app-001, ARCH-app]
        outgoing = self._outgoing("TS-app")
        self.assertIn(("verifies", "REQ-app-001"), outgoing)
        self.assertIn(("verifies", "ARCH-app"), outgoing)

    def test_per_case_verifies_link(self):
        # TC-checkout-001 in TS-app-checkout verifies DD-app-checkout-discount
        # The walker treats per-case verifies as a link from the containing
        # artifact (TS-app-checkout) — so the source is TS-app-checkout.
        self.assertIn(
            ("verifies", "DD-app-checkout-discount"),
            self._outgoing("TS-app-checkout"),
        )

    def test_per_child_allocates_link(self):
        # ARCH has a decomposition child (walker-engine) with allocates: [REQ-001, REQ-002]
        # Walker treats per-child allocates as forward links from the containing artifact.
        outgoing = self._outgoing("ARCH")
        self.assertIn(("allocates", "REQ-001"), outgoing)
        self.assertIn(("allocates", "REQ-002"), outgoing)


# --------------------------------------------------------------------------
# Reverse-direction BFS — the candidate-set walk
# --------------------------------------------------------------------------


class TestReverseWalk(unittest.TestCase):
    """Walking reverse from an entry id produces the candidate set."""

    def setUp(self):
        self.graph = walk_impact.build_graph(FIXTURES)

    def _candidate_ids(self, entry):
        return {c.id for c in walk_impact.walk(entry, self.graph)}

    def test_leaf_testspec_has_no_downstream(self):
        # TS-app-checkout sits at the bottom — no artifact references it.
        self.assertEqual(self._candidate_ids("TS-app-checkout"), set())

    def test_dd_change_finds_leaf_testspec(self):
        # DD-app-checkout-discount is verified by TS-app-checkout (envelope + per-case).
        candidates = self._candidate_ids("DD-app-checkout-discount")
        self.assertIn("TS-app-checkout", candidates)

    def test_arch_change_finds_dd_via_parent_architecture(self):
        # ARCH-app is the parent_architecture of DD-app-checkout-discount.
        # And TS-app verifies ARCH-app at the envelope level.
        # Transitively: from DD → TS-app-checkout via verifies.
        candidates = self._candidate_ids("ARCH-app")
        self.assertIn("DD-app-checkout-discount", candidates)
        self.assertIn("TS-app", candidates)
        self.assertIn("TS-app-checkout", candidates)  # transitive via DD

    def test_req_change_finds_arch_via_allocates(self):
        # REQ-001 is allocated by ARCH's walker-engine child entry.
        # TS verifies REQ-001 at the envelope level.
        # TC-001 in TS verifies REQ-001 (per-case).
        candidates = self._candidate_ids("REQ-001")
        self.assertIn("ARCH", candidates)
        self.assertIn("TS", candidates)

    def test_adr_change_propagates_to_all_governed_artifacts(self):
        # ADR-001-use-redis is referenced by:
        #   - ARCH (governing_adrs, envelope)
        #   - REQS-app (governing_adrs, envelope)
        #   - DD-app-checkout-discount (governing_adrs, envelope)
        # Transitive walk should also pull in everything downstream of those.
        candidates = self._candidate_ids("ADR-001-use-redis")
        self.assertIn("ARCH", candidates)
        self.assertIn("REQS-app", candidates)
        self.assertIn("DD-app-checkout-discount", candidates)
        # Transitive from DD → TS-app-checkout
        self.assertIn("TS-app-checkout", candidates)

    def test_pb_change_propagates_far(self):
        # PB is at the top — both REQS and ARCH derive from it.
        # Transitively reaches everything below.
        candidates = self._candidate_ids("PB")
        self.assertIn("REQS", candidates)
        self.assertIn("ARCH", candidates)

    def test_walk_results_carry_hop_distance(self):
        results = walk_impact.walk("DD-app-checkout-discount", self.graph)
        # TS-app-checkout is exactly one hop reverse from DD.
        ts = next(c for c in results if c.id == "TS-app-checkout")
        self.assertEqual(ts.hops, 1)

    def test_walk_results_carry_link_type(self):
        results = walk_impact.walk("DD-app-checkout-discount", self.graph)
        ts = next(c for c in results if c.id == "TS-app-checkout")
        self.assertEqual(ts.link_type, "verifies")

    def test_walk_does_not_loop_on_cycles(self):
        # Inject a synthetic cycle into the graph and ensure BFS terminates
        # with each node visited at most once.
        self.graph.outgoing.setdefault("TS-app-checkout", []).append(
            ("derived_from", "DD-app-checkout-discount")
        )
        # Recompute reverse links from outgoing
        self.graph.rebuild_reverse()
        results = walk_impact.walk("DD-app-checkout-discount", self.graph)
        ids = [c.id for c in results]
        self.assertEqual(len(ids), len(set(ids)), "node visited more than once")


# --------------------------------------------------------------------------
# CLI — invocation and output formats
# --------------------------------------------------------------------------


class TestCLI(unittest.TestCase):
    """The argparse entry point produces the documented output formats."""

    def _run(self, *args):
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = walk_impact.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_unknown_artifact_returns_exit_1(self):
        code, _, err = self._run(
            "REQ-does-not-exist", "--specs-root", str(FIXTURES)
        )
        self.assertEqual(code, 1)
        self.assertIn("not found", err.lower())

    def test_text_format_contains_candidate_ids(self):
        code, out, _ = self._run(
            "DD-app-checkout-discount",
            "--specs-root", str(FIXTURES),
            "--format", "text",
        )
        self.assertEqual(code, 0)
        self.assertIn("TS-app-checkout", out)

    def test_json_format_is_valid_json(self):
        code, out, _ = self._run(
            "DD-app-checkout-discount",
            "--specs-root", str(FIXTURES),
            "--format", "json",
        )
        self.assertEqual(code, 0)
        parsed = json.loads(out)
        self.assertEqual(parsed["entry"], "DD-app-checkout-discount")
        ids = {c["id"] for c in parsed["candidates"]}
        self.assertIn("TS-app-checkout", ids)

    def test_json_candidate_carries_link_type_and_hops(self):
        code, out, _ = self._run(
            "DD-app-checkout-discount",
            "--specs-root", str(FIXTURES),
            "--format", "json",
        )
        self.assertEqual(code, 0)
        parsed = json.loads(out)
        ts = next(c for c in parsed["candidates"] if c["id"] == "TS-app-checkout")
        self.assertEqual(ts["link_type"], "verifies")
        self.assertEqual(ts["hops"], 1)
        self.assertIn("path", ts)


if __name__ == "__main__":
    unittest.main()
