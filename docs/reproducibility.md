# Reproducibility

## What is reproducible here

This repository is reproducible in a narrow, intentional sense:

- The **data contracts** (`schemas/*.schema.json`) are machine-checkable and
  self-contained.
- The **toy runtime** (`cp_gfm_public/toy_runtime.py`) runs deterministically
  on synthetic data and can be executed by anyone with a Python 3.9+ environment.

## What is not reproducible here

- No production model, ranking, or oracle behavior is reproduced.
- No scientific result, measurement, or sequence of value is reproduced.
- No paper figure or claim depends on the toy runtime.

## How to reproduce the toy run

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e .
python -m cp_gfm_public.toy_runtime --config examples/toy_example.yaml
pytest
```

The run is deterministic: the same config produces the same evidence output.
The config (`examples/toy_example.yaml`) is self-describing and synthetic.

## Environment

- Python `>=3.9`.
- Dependencies are listed in `pyproject.toml`: `jsonschema` and `PyYAML`
  (runtime), `pytest` (dev).

## Intentional limits

Reproducibility here means **"the demonstration runs and can be inspected"**,
not **"the science is reproducible from this repository"**. The scientific
method is described, but the production engine is not included.
