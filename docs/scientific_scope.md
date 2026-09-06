# Scientific Scope

## What CP-GFM addresses

CP-GFM targets the discovery of **target-specific cyclic peptides**. The design
problem couples several scientific concerns:

- **Topology-aware generation** — the molecular topology (for example,
  head-to-tail cyclic) is a first-class design constraint, not an afterthought.
- **Multi-objective decision** — candidates are evaluated against more than one
  objective (for example, interaction quality, topology validity, and
  developability proxies), and a non-dominated subset is selected.
- **Sparse high-fidelity oracle auditing** — because exhaustive high-fidelity
  evaluation is expensive, a small subset is re-evaluated by a higher-fidelity
  oracle to produce evidence.
- **Evidence feedback** — oracle results are recorded as structured evidence
  that can inform the next design iteration.

## What this repository demonstrates

For v0.1, this repository demonstrates:

1. The **architecture** (see [`architecture.md`](architecture.md)).
2. The **public data contracts** for topology, candidate, and evidence
   (see `schemas/`).
3. A **synthetic toy execution** that exercises the contract data flow with
   synthetic data only.

## What this repository does not demonstrate

- It does **not** provide a usable generative model.
- It does **not** provide ranking, admission, or nomination logic.
- It does **not** provide any high-fidelity oracle.
- It does **not** provide any target package, receptor structure, or candidate
  sequence of scientific value.
- It does **not** claim to be a released foundation model.

## Positioning statement

The public interface is a **scientific and architectural artifact**. Its value
is that the framework is (a) well-defined enough to be inspected, and (b)
cleanly separated from the production decision engine, which is retained and
not released.

## Non-claims

- No priority claims ("first", "best") are made.
- No performance claims are made.
- No biological or pharmacological efficacy claim is made about any molecule.
- No specific target or indication is named in this repository.
