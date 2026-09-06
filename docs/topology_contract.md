# Topology Contract

The topology contract is the public, reduced description of the molecular
topology that a generator is asked to produce.

> **Important:** this contract is written from scratch for the public release.
> It is *not* a subset of any internal schema. It describes a simple,
> demonstrative head-to-tail cyclic topology only.

## v0.1 demonstrative contract

For v0.1, the public contract supports a single, simple topology:

```yaml
topology:
  class: head_to_tail
  residue_count: 10

closure:
  type: backbone_cyclization

chemistry:
  residue_alphabet: canonical_example

validation:
  topology_valid: true
```

### Field meanings (public, demonstrative)

| Field | Meaning |
|---|---|
| `topology.class` | The topology family. v0.1 uses `head_to_tail` only. |
| `topology.residue_count` | The number of residues in the (synthetic) example. |
| `closure.type` | How the chain is closed. v0.1 uses `backbone_cyclization` only. |
| `chemistry.residue_alphabet` | The demonstrative residue alphabet label. v0.1 uses `canonical_example` only. |
| `validation.topology_valid` | A demonstrative validity flag for the example. |

## Machine-checkable form

The same contract is defined as a JSON Schema at
`schemas/topology_public.schema.json`. The schema is intentionally narrow: it
accepts only the demonstrative values above and rejects anything outside them.

## What is deliberately out of scope for v0.1

The public topology contract does **not** expose:

- extended chemistry or residue alphabets beyond the demonstrative example, or
  their enablement states;
- molecular-mechanics configuration states;
- internal identifier registries;
- campaign feature flags;
- production validation thresholds or roundtrip thresholds.

These are production concerns and are retained outside the public boundary.

## Why a narrow contract

A narrow, explicitly-demonstrative contract makes the public repository
self-evidently a *contract demonstration* rather than a partial production
schema. It supports the scientific claim that the framework is
topology-aware, without exposing how production topology validation is
implemented.
