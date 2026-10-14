# Preprint reader's guide

This repository is a public interface layer for the associated CP-GFM-SGX
preprint, not a full reproduction of the paper's scientific results.

## How to read the paper alongside this repository

- Architecture: map the preprint's scientific workflow to the architecture
  described in `docs/architecture.md`. The repository makes the component roles
  and information flow explicit, including the separation between public
  interfaces and production-side logic.

- Topology contract: read the work in the context of
  `docs/topology_contract.md` and the public schema definitions under
  `schemas/`. These artifacts define the structural constraints and the public
  contract that the synthetic toy runtime is designed to exercise.

- Evaluation protocol: use `docs/evaluation_protocol.md` to understand the
  evaluation framing described in the paper and how public interfaces encode
  expected evidence, gating, and audit structure.

- Schemas: the JSON Schema files under `schemas/` are the machine-checkable
  contract layer. They document the public objects and relationships that the
  scientific workflow depends on, without exposing the production implementation.

- Toy runtime: the code in `cp_gfm_public/toy_runtime.py` and the example config
  under `examples/` are intentionally synthetic. They demonstrate the public data
  flow and contract usage, but they do not reproduce the scientific results
  reported in the preprint. The toy runtime is for inspection and interface
  validation, not for re-deriving the paper's experimental conclusions.
