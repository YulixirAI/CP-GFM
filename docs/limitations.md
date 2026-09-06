# Limitations

This repository is a **public scientific interface**, not a product and not a
released model. The following limitations are explicit and intentional.

## Scientific limitations

- The toy runtime uses **synthetic data only**. Nothing it outputs has
  scientific, chemical, or biological meaning.
- No generative model, ranking function, oracle, or target package is included.
- No efficacy, potency, selectivity, safety, or developability claim is made
  about any molecule.
- The demonstrative topology contract covers a single head-to-tail case and
  does not represent the breadth of the internal framework.

## Engineering limitations

- The interfaces are **contract stubs**. They define method signatures and
  conceptual flow; they do not implement real behavior.
- The data contracts are **demonstrative schemas**, intentionally narrower than
  any production schema.
- The package is not intended for installation as a dependency of other work.

## Legal limitations

- License and patent terms are **placeholder drafts** pending final legal
  review. No license is granted by this repository as published.
- See [`LICENSE-or-NOTICE.md`](../LICENSE-or-NOTICE.md) and
  [`PATENT_NOTICE.md`](../PATENT_NOTICE.md).

## What this means for a reader

An external engineer can understand the **shape** of the framework and verify
that it is runnable and inspectable. They cannot reconstruct the production
decision engine or any private molecular asset from this repository. That
separation is the point.
