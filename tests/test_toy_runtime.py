"""Tests for the synthetic CP-GFM toy runtime."""

import sys

from cp_gfm_public.interfaces import (
    CandidateSet,
    GateInterface,
    GeneratorInterface,
    OracleAuditInterface,
    ParetoInterface,
    RankerInterface,
    TargetContext,
    TopologyContract,
)
from cp_gfm_public.toy_runtime import ToyGate, ToyGenerator, ToyOracle, ToyPareto, run_pipeline


def test_topology_contract_shape():
    tc = TopologyContract()
    d = tc.as_dict()
    assert d["topology"]["class"] == "head_to_tail"
    assert d["topology"]["residue_count"] == 10
    assert d["closure"]["type"] == "backbone_cyclization"
    assert d["chemistry"]["residue_alphabet"] == "canonical_example"
    assert d["validation"]["topology_valid"] is True


def test_interfaces_are_abstract():
    for cls in (GeneratorInterface, GateInterface, RankerInterface, ParetoInterface, OracleAuditInterface):
        assert getattr(cls, "__abstractmethods__", None)


def test_toy_generator_respects_budget():
    gen = ToyGenerator()
    out = gen.propose(TargetContext("toy"), TopologyContract(), generation_budget=3)
    assert isinstance(out, CandidateSet)
    assert len(out) == 3
    assert all(c["synthetic"] is True for c in out.candidates)


def test_toy_pipeline_end_to_end():
    evidence = run_pipeline(
        target_context=TargetContext("toy-target"),
        topology_contract=TopologyContract(),
        generation_budget=5,
        audit_budget=2,
    )
    assert evidence.generated == 5
    assert evidence.gated == 5
    assert evidence.ranked == 5
    assert evidence.selected >= 1
    assert evidence.audited == 2


def test_pareto_is_non_dominated():
    gen = ToyGenerator()
    proposed = gen.propose(TargetContext("toy"), TopologyContract(), generation_budget=5)
    gate = ToyGate()
    pareto = ToyPareto()
    gated = gate.filter(proposed, TopologyContract())
    selected = pareto.select(gated)
    # No selected candidate may be dominated by another selected candidate.
    for cand in selected.candidates:
        for other in selected.candidates:
            if other is cand:
                continue
            assert not _dominates(other["objectives"], cand["objectives"])


def test_cli_runs(monkeypatch, tmp_path):
    from cp_gfm_public import toy_runtime

    config_path = tmp_path / "toy.yaml"
    config_path.write_text(
        "target_id: toy-target\n"
        "topology_contract:\n"
        "  topology_class: head_to_tail\n"
        "  residue_count: 10\n"
        "  closure_type: backbone_cyclization\n"
        "  residue_alphabet: canonical_example\n"
        "generation_budget: 3\n"
        "audit_budget: 1\n"
    )
    monkeypatch.setattr(sys, "argv", ["toy_runtime.py", "--config", str(config_path)])
    assert toy_runtime.main(["--config", str(config_path)]) == 0


def _dominates(a, b):
    keys = list(b.keys())
    all_at_least = all(a.get(k, 0.0) >= b[k] for k in keys)
    any_better = any(a.get(k, 0.0) > b[k] for k in keys)
    return all_at_least and any_better
