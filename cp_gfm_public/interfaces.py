"""Contract-level interfaces for the CP-GFM public scientific interface.

These are **contract stubs only**. They define the conceptual data flow and
method signatures of the framework. They deliberately contain no ranking
logic, no learned coefficients, no thresholds, and no production behavior.

Conceptual flow::

    TargetContext + TopologyContract
        -> GeneratorInterface
        -> GateInterface
        -> RankerInterface
        -> ParetoInterface
        -> OracleAuditInterface
        -> EvidenceObject

Every class here is either a passive data contract or an abstract interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple


# ---------------------------------------------------------------------------
# Data contracts
# ---------------------------------------------------------------------------

@dataclass
class TargetContext:
    """Abstract description of the design problem.

    Carries only synthetic, non-identifying target context. It must not carry
    private receptor coordinates or wet-lab decision inputs.
    """

    target_id: str
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TopologyContract:
    """Reduced public topology contract.

    For v0.1 this supports a single demonstrative head-to-tail cyclic topology.
    """

    topology_class: str = "head_to_tail"
    residue_count: int = 10
    closure_type: str = "backbone_cyclization"
    residue_alphabet: str = "canonical_example"

    def as_dict(self) -> Dict[str, Any]:
        return {
            "topology": {
                "class": self.topology_class,
                "residue_count": self.residue_count,
            },
            "closure": {"type": self.closure_type},
            "chemistry": {"residue_alphabet": self.residue_alphabet},
            "validation": {"topology_valid": True},
        }


@dataclass
class CandidateSet:
    """A collection of proposals with synthetic objective values.

    ``objective_names`` declares the objectives that the ranker attaches to
    each candidate. Values are synthetic; no scoring function is specified.
    """

    candidates: List[Dict[str, Any]] = field(default_factory=list)
    objective_names: Tuple[str, ...] = (
        "interaction_proxy",
        "topology_validity",
        "developability_proxy",
    )

    def __len__(self) -> int:
        return len(self.candidates)


@dataclass
class EvidenceObject:
    """Structured outcome of a synthetic pipeline run."""

    run_id: str
    generated: int
    gated: int
    ranked: int
    selected: int
    audited: int
    confirmed: int
    candidates: List[Dict[str, Any]] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "pipeline": {
                "generated": self.generated,
                "gated": self.gated,
                "ranked": self.ranked,
                "selected": self.selected,
            },
            "candidates": self.candidates,
            "audit": {
                "audited": self.audited,
                "confirmed": self.confirmed,
            },
        }


# ---------------------------------------------------------------------------
# Abstract interfaces
# ---------------------------------------------------------------------------

class GeneratorInterface(ABC):
    """Propose candidates given a target and a topology contract.

    The framework is **generator-agnostic**: this interface is the only thing
    the rest of the framework depends on. The public interface defines the
    proposal contract and nothing about any specific generator's internals.
    """

    @abstractmethod
    def propose(
        self,
        target_context: TargetContext,
        topology_contract: TopologyContract,
        generation_budget: int,
    ) -> CandidateSet:
        """Return a ``CandidateSet`` of up to ``generation_budget`` proposals."""
        raise NotImplementedError


class GateInterface(ABC):
    """Apply coarse, contract-level admission checks to a proposal.

    Gating is about validity, not preference. This interface carries no
    threshold and no scoring logic.
    """

    @abstractmethod
    def admit(
        self,
        candidate: Mapping[str, Any],
        topology_contract: TopologyContract,
    ) -> bool:
        """Return True if ``candidate`` is well-formed for the contract."""
        raise NotImplementedError

    @abstractmethod
    def filter(
        self,
        candidates: CandidateSet,
        topology_contract: TopologyContract,
    ) -> CandidateSet:
        """Return the subset of ``candidates`` that passes the gate."""
        raise NotImplementedError


class RankerInterface(ABC):
    """Attach declared objectives to candidates.

    Only the *shape* of multi-objective scoring is described; no scoring
    function, weight, or coefficient is specified.
    """

    @abstractmethod
    def rank(self, candidates: CandidateSet) -> CandidateSet:
        """Attach synthetic objective values to each candidate."""
        raise NotImplementedError


class ParetoInterface(ABC):
    """Select the non-dominated subset with respect to declared objectives.

    No production nomination policy is specified here.
    """

    @abstractmethod
    def select(self, candidates: CandidateSet) -> CandidateSet:
        """Return the non-dominated subset of ``candidates``."""
        raise NotImplementedError


class OracleAuditInterface(ABC):
    """Model sparse high-fidelity oracle auditing.

    A small number of candidates are re-evaluated by an expensive, higher-
    fidelity oracle and the result is recorded as evidence. The audit contract
    only is defined here; no oracle implementation is exposed.
    """

    @abstractmethod
    def audit(
        self,
        candidates: CandidateSet,
        audit_budget: int,
    ) -> Tuple[Sequence[Dict[str, Any]], int]:
        """Return audit evidence and the number of confirmed candidates."""
        raise NotImplementedError
