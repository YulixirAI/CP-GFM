"""Synthetic toy runtime for the CP-GFM public scientific interface.

This module demonstrates the **contract data flow** of the framework with
fully synthetic, obviously non-production behavior. It is the reference toy
implementation behind ``README.md``.

It demonstrates:

    TargetContext + TopologyContract
        -> GeneratorInterface
        -> GateInterface
        -> RankerInterface
        -> ParetoInterface
        -> OracleAuditInterface
        -> EvidenceObject

Nothing here reproduces, approximates, imitates, or reverse-engineers
production decision logic. Objective values are synthetic and deterministic;
they are not weighted by any learned coefficient.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Mapping, Sequence, Tuple

from .interfaces import (
    CandidateSet,
    EvidenceObject,
    GateInterface,
    GeneratorInterface,
    OracleAuditInterface,
    ParetoInterface,
    RankerInterface,
    TargetContext,
    TopologyContract,
)

try:
    import yaml
except ImportError:  # pragma: no cover - yaml is a declared dependency
    yaml = None


# ---------------------------------------------------------------------------
# Synthetic, deterministic objective values. These are obviously not real
# scores: each candidate is assigned a fixed, hand-written synthetic triple.
# ---------------------------------------------------------------------------

_SYNTHETIC_OBJECTIVES: Sequence[Dict[str, float]] = (
    {"interaction_proxy": 0.1, "topology_validity": 1.0, "developability_proxy": 0.7},
    {"interaction_proxy": 0.9, "topology_validity": 1.0, "developability_proxy": 0.2},
    {"interaction_proxy": 0.4, "topology_validity": 1.0, "developability_proxy": 0.5},
    {"interaction_proxy": 0.7, "topology_validity": 1.0, "developability_proxy": 0.4},
    {"interaction_proxy": 0.6, "topology_validity": 1.0, "developability_proxy": 0.6},
)


class ToyGenerator(GeneratorInterface):
    """Generate synthetic, obviously placeholder candidates.

    Candidate IDs are plain synthetic labels. No sequence, structure, or
    molecular representation is generated.
    """

    def propose(
        self,
        target_context: TargetContext,
        topology_contract: TopologyContract,
        generation_budget: int,
    ) -> CandidateSet:
        n = max(0, min(generation_budget, len(_SYNTHETIC_OBJECTIVES)))
        candidates = [
            {
                "candidate_id": f"toy-{i + 1}",
                "synthetic": True,
                "objectives": dict(_SYNTHETIC_OBJECTIVES[i]),
            }
            for i in range(n)
        ]
        return CandidateSet(candidates=candidates)


class ToyGate(GateInterface):
    """Admit only candidates that are structurally well-formed (synthetic)."""

    def admit(
        self,
        candidate: Mapping[str, Any],
        topology_contract: TopologyContract,
    ) -> bool:
        # Well-formedness is a purely synthetic check: a candidate carries the
        # synthetic marker and the declared objectives. No threshold involved.
        objectives = candidate.get("objectives")
        return (
            candidate.get("synthetic") is True
            and isinstance(objectives, Mapping)
            and "topology_validity" in objectives
        )

    def filter(
        self,
        candidates: CandidateSet,
        topology_contract: TopologyContract,
    ) -> CandidateSet:
        kept = [c for c in candidates.candidates if self.admit(c, topology_contract)]
        return CandidateSet(candidates=kept, objective_names=candidates.objective_names)


class ToyRanker(RankerInterface):
    """Leave the already-attached synthetic objectives in place.

    Ranking here is declarative: objectives already exist on the candidates and
    this implementation makes no change beyond re-normalizing the set. No
    coefficient or scoring function is applied.
    """

    def rank(self, candidates: CandidateSet) -> CandidateSet:
        return CandidateSet(candidates=list(candidates.candidates),
                            objective_names=candidates.objective_names)


class ToyPareto(ParetoInterface):
    """Select the non-dominated subset (all objectives maximized).

    This is a generic Pareto-front operation on synthetic values. It encodes no
    production nomination policy.
    """

    def select(self, candidates: CandidateSet) -> CandidateSet:
        kept: List[Dict[str, Any]] = []
        for cand in candidates.candidates:
            obj = cand["objectives"]
            dominated = False
            for other in candidates.candidates:
                if other is cand:
                    continue
                oobj = other["objectives"]
                if _dominates(oobj, obj):
                    dominated = True
                    break
            if not dominated:
                kept.append(cand)
        return CandidateSet(candidates=kept, objective_names=candidates.objective_names)


class ToyOracle(OracleAuditInterface):
    """Sparse synthetic audit.

    Confirms a candidate if its ``topology_validity`` is at least 1.0. This is
    a synthetic demonstration of a high-fidelity re-check, not a real oracle.
    """

    def audit(
        self,
        candidates: CandidateSet,
        audit_budget: int,
    ) -> Tuple[Sequence[Dict[str, Any]], int]:
        subset = candidates.candidates[: max(0, audit_budget)]
        evidence: List[Dict[str, Any]] = []
        confirmed = 0
        for cand in subset:
            confirmed_flag = float(cand["objectives"].get("topology_validity", 0.0)) >= 1.0
            if confirmed_flag:
                confirmed += 1
            evidence.append(
                {
                    "candidate_id": cand["candidate_id"],
                    "audit_confirmed": confirmed_flag,
                }
            )
        return evidence, confirmed


def _dominates(a: Mapping[str, float], b: Mapping[str, float]) -> bool:
    """Return True if ``a`` weakly dominates ``b`` and strictly better in one."""
    keys = list(b.keys())
    all_at_least = all(a.get(k, 0.0) >= b[k] for k in keys)
    any_better = any(a.get(k, 0.0) > b[k] for k in keys)
    return all_at_least and any_better


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline(
    target_context: TargetContext,
    topology_contract: TopologyContract,
    generation_budget: int,
    audit_budget: int,
) -> EvidenceObject:
    """Run the synthetic pipeline end-to-end and return an ``EvidenceObject``."""
    generator: GeneratorInterface = ToyGenerator()
    gate: GateInterface = ToyGate()
    ranker: RankerInterface = ToyRanker()
    pareto: ParetoInterface = ToyPareto()
    oracle: OracleAuditInterface = ToyOracle()

    proposed = generator.propose(target_context, topology_contract, generation_budget)
    gated = gate.filter(proposed, topology_contract)
    ranked = ranker.rank(gated)
    selected = pareto.select(ranked)

    audit_evidence, confirmed = oracle.audit(selected, audit_budget)

    return EvidenceObject(
        run_id=f"toy-{target_context.target_id}",
        generated=len(proposed),
        gated=len(gated),
        ranked=len(ranked),
        selected=len(selected),
        audited=len(audit_evidence),
        confirmed=confirmed,
        candidates=selected.candidates,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _load_config(path: str) -> Dict[str, Any]:
    if yaml is None:  # pragma: no cover
        raise RuntimeError("PyYAML is required to load the toy config.")
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the synthetic CP-GFM toy pipeline."
    )
    parser.add_argument(
        "--config",
        default="examples/toy_example.yaml",
        help="Path to the toy config (YAML).",
    )
    args = parser.parse_args(argv)

    config = _load_config(args.config)

    target_context = TargetContext(
        target_id=config.get("target_id", "toy-target"),
        description=config.get("description", ""),
    )
    topology_contract = TopologyContract(**config.get("topology_contract", {}))

    evidence = run_pipeline(
        target_context=target_context,
        topology_contract=topology_contract,
        generation_budget=int(config.get("generation_budget", 5)),
        audit_budget=int(config.get("audit_budget", 2)),
    )

    print(json.dumps(evidence.as_dict(), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
