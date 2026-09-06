# Architecture

This document describes the **conceptual architecture** of CP-GFM as exposed to
the public. It is a contract-level description. It does not describe the
production implementation, its internals, or its decision policy.

## Working definition

> CP-GFM is a topology-aware generative and runtime decision framework for
> target-specific cyclic peptide discovery. It couples topology-aware proposal
> generation with multi-objective runtime decision, selective high-fidelity
> oracle auditing, and evidence feedback.

## Design principle: separate the interface from the engine

The framework is organized so that the **scientific interface** — what a
component is asked to do — is stable and inspectable, while the **engine** —
how each component is implemented — is a pluggable, generator-agnostic, and
deliberately retained production concern.

For v0.1, the public repository exposes only the interfaces and the contracts
between them.

## Components

### 1. TargetContext

An abstract description of the design problem: the target of interest and the
design constraints. It does not carry private receptor coordinates or wet-lab
decision inputs.

### 2. TopologyContract

A reduced, machine-checkable description of the molecular topology to be
generated (for v0.1: a simple head-to-tail cyclic topology). See
[`topology_contract.md`](topology_contract.md) and
`schemas/topology_public.schema.json`.

### 3. GeneratorInterface

Proposes candidate molecules given a `TargetContext` and a `TopologyContract`.

The framework is **generator-agnostic**: this interface is the only thing the
rest of the framework depends on, so any conforming generator can be used. The
public interface defines the proposal contract and nothing about any specific
generator's internals.

### 4. GateInterface

Applies coarse, contract-level admission checks to a proposal — for example,
whether the proposal is well-formed against the requested topology. It is
conceptually separate from ranking: gating is about validity, not preference.

### 5. RankerInterface

Assigns synthetic or declarative objectives to candidates that pass the gate.
In this public interface, ranking is described only as a multi-objective
scoring contract; no scoring function or coefficient is specified.

### 6. ParetoInterface

Selects the non-dominated subset of candidates with respect to the declared
objectives. The public interface describes the Pareto-front contract; it does
not specify any production nomination policy.

### 7. OracleAuditInterface

Models the concept of **sparse high-fidelity oracle auditing**: a small number
of candidates are re-evaluated by an expensive, higher-fidelity oracle, and the
result is recorded as evidence. The public interface defines the audit
contract only.

### 8. EvidenceObject

The structured output of the pipeline: which proposals were made, gated,
ranked, selected, audited, and what evidence was produced. See
`schemas/evidence_public.schema.json`.

## Data flow

```
TargetContext + TopologyContract
        │
        ▼
GeneratorInterface ──► CandidateSet
        │
        ▼
GateInterface ──► (filtered CandidateSet)
        │
        ▼
RankerInterface ──► (objectives per candidate)
        │
        ▼
ParetoInterface ──► (non-dominated subset)
        │
        ▼
OracleAuditInterface ──► (sparse high-fidelity audit)
        │
        ▼
EvidenceObject
```

Every arrow is a **contract boundary**. A component may be replaced without
changing the shape of the data that crosses the boundary.

## What is deliberately not shown

- The identity or internals of any concrete generator.
- Ranking coefficients, thresholds, or objective weighting.
- The admission or nomination policy.
- The oracle service implementation.
- Any production infrastructure, paths, or services.

## Generator-agnostic claim

Because the framework depends only on `GeneratorInterface`, CP-GFM is
positioned as **generator-agnostic**. This is a scientific claim about the
interface, not a claim about any particular generator.
