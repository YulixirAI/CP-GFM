
## Technical report

[Read the CP-GFM-SGX Technical Report](docs/CP-GFM-SGX_Technical_Report.md)
## Associated preprint

CP-GFM-SGX: Topology-Aware Cyclic Peptide Generation and Design with
Receptor-Conditioned Structural Evaluation and Experimental KRAS Affinity Optimization

Versioned DOI: https://doi.org/10.26434/chemrxiv.15010253/v1

This repository is the public scientific interface and synthetic toy demonstration
for the associated CP-GFM-SGX work. The preprint carries the underlying scientific
method, results, and experimental KRAS affinity conclusions. This repository is
not the full scientific implementation or the production evaluation pipeline; it
serves to expose the public architecture, data contracts, and an illustrative
runtime for inspection and reproducibility-oriented review.

# CP-GFM Public Interface

> **Scientific architecture + data contracts + reproducibility discipline.**

This repository is the **public scientific interface** of CP-GFM — a
topology-aware generative and runtime decision framework for target-specific
cyclic peptide discovery.

**What this repository is:** a clean-room description of the architecture, the
public data contracts, and a synthetic toy execution that demonstrates the
contract data flow. It is designed to be read and inspected by scientists and
engineers, not to perform drug design.

**What this repository is not:** the production implementation. CP-GFM's
generative models, ranking and admission logic, oracle auditing service, private
target packages, and molecular assets are **not** in this repository and are
**not** released here.

---

## What you can verify here (≈5 minutes)

1. **This is not a slide deck.** The public interfaces and the toy runtime are
   runnable Python, and the data contracts are machine-checkable JSON Schema.
2. **The architecture is explicit and inspectable.** See
   [`docs/architecture.md`](docs/architecture.md) for the full component and
   data-flow model.
3. **The production layer is deliberately retained.** The interfaces define
   *contracts*, not decision logic. The framework is described as
   **generator-agnostic** and **oracle-audited**, and the production decision
   layer is intentionally outside the disclosure boundary.

## Quick start

No installation is required to read the contracts. To exercise the synthetic
toy runtime:

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e .
python -m cp_gfm_public.toy_runtime --config examples/toy_example.yaml
pytest
```

The toy runtime uses **synthetic data only**. It demonstrates the shape of the
pipeline — `TargetContext + TopologyContract → GeneratorInterface → GateInterface
→ RankerInterface → ParetoInterface → OracleAuditInterface → EvidenceObject` —
and does not approximate any production algorithm.

## Repository layout

```
CP-GFM/
├── README.md
├── CITATION.cff
├── LICENSE-or-NOTICE.md
├── PATENT_NOTICE.md
├── SECURITY.md
├── pyproject.toml
├── docs/
│   ├── architecture.md
│   ├── scientific_scope.md
│   ├── topology_contract.md
│   ├── evaluation_protocol.md
│   ├── reproducibility.md
│   └── limitations.md
├── schemas/
│   ├── topology_public.schema.json
│   ├── candidate_public.schema.json
│   └── evidence_public.schema.json
├── cp_gfm_public/
│   ├── __init__.py
│   ├── interfaces.py
│   └── toy_runtime.py
├── examples/
│   └── toy_example.yaml
└── tests/
    └── test_toy_runtime.py
```

## Status and legal notices

- This is a **v0.1 public interface release**. It is not a released foundation
  model and does not claim to be one.
- License and patent terms are **placeholder drafts** pending final legal
  review. See [`LICENSE-or-NOTICE.md`](LICENSE-or-NOTICE.md) and
  [`PATENT_NOTICE.md`](PATENT_NOTICE.md).
- Report security issues per [`SECURITY.md`](SECURITY.md).

## Citation

If you reference this work, please use [`CITATION.cff`](CITATION.cff).
