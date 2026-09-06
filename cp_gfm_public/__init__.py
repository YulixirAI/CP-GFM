"""CP-GFM public scientific interface.

This package exposes contract-level interfaces and a synthetic toy runtime.
It contains no production implementation, no ranking/decision logic, and no
private molecular data.
"""

from .interfaces import (  # noqa: F401
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

__all__ = [
    "CandidateSet",
    "EvidenceObject",
    "GateInterface",
    "GeneratorInterface",
    "OracleAuditInterface",
    "ParetoInterface",
    "RankerInterface",
    "TargetContext",
    "TopologyContract",
]

__version__ = "0.1.0"
