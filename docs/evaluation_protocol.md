# Evaluation Protocol

This document describes, at a **contract level**, how candidates in a CP-GFM
iteration are evaluated. It defines *what* is measured and in what *order*; it
does not define *how* any measurement is computed.

## Objectives

A candidate is evaluated against declarative objectives. For the public
interface these are named, not computed:

- **interaction_proxy** — a stand-in for the quality of the interaction with the
  target.
- **topology_validity** — whether the candidate satisfies the requested topology.
- **developability_proxy** — a stand-in for downstream developability concerns.

These are **synthetic, demonstrative objective names**. They do not correspond
to any production scoring function and no coefficient, weight, or threshold is
specified.

## Pipeline order

1. **Generate** — produce proposals against the topology contract.
2. **Gate** — drop proposals that are not well-formed against the contract.
3. **Rank** — attach the declared objectives to each surviving candidate.
4. **Pareto** — retain the non-dominated subset.
5. **Audit** — re-evaluate a sparse subset with a higher-fidelity oracle.
6. **Evidence** — record the outcome as structured evidence.

## Metric definitions

Public metrics are defined as **concepts**, not as numbers:

| Metric | Definition (conceptual) |
|---|---|
| Non-dominated rate | Fraction of gated candidates that lie on the Pareto front. |
| Audit yield | Fraction of audited candidates whose audit result confirms the ranking proxy. |
| Contract conformance | Fraction of proposals that satisfy the topology contract at the gate. |

None of these metrics carries a learned value, a target, or a threshold. They
exist so an external reader can understand *what an evaluation measures*,
without learning *how production evaluates*.

## Reproducibility note

The synthetic toy runtime produces **reproducible, synthetic** outputs only. It
does not reproduce any production evaluation. See
[`reproducibility.md`](reproducibility.md).
