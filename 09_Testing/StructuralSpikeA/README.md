# Structural Spike A Loader Evidence

This directory is the executable evidence corpus for the disposable
`experimental-structural-input/0` fixture loader.

`fixture_manifest.json` is the normative scenario index. It contains exactly
the 44 reviewed identifiers and the fixed loader partition:

- 35 loader successes that publish both immutable input-boundary artifacts;
- 9 loader failures owned by one of the four `INPUT_*` codes.

`scenario_factory.py` materializes small cases and deterministic semantic
recipes. Large byte, JSON-depth, record-count, diagnostic-count, and
randomized-order cases are generated from the exact parameters and seed
recorded in the manifest; no multi-megabyte fixture blob is committed.
`raw_cases.py` keeps lexical and malformed inputs as reviewable byte literals.

The suite covers:

- RFC 8259 state and differential cases, decoded duplicate keys, Unicode
  escapes, canonical integer lexemes, and exact pre-admission limits;
- all 38 schema definitions, closed objects, selector delegation, and
  executable-schema drift;
- project graph, Module graph, Compilation Unit, origin, and marker integrity;
- deterministic normalization, member-order preservation, ordinal gaps, and
  deep immutability;
- no fixture-controlled path open, no network access, escaped diagnostics, and
  an inert opaque-payload boundary; and
- absence of step-1 or later identities, selection, closure, expansion,
  occurrence, snapshot, or diagnostic behavior.

Run from `04_Compiler/StructuralSpikeA`:

```bash
uv run --locked python -m unittest discover \
  -s ../../09_Testing/StructuralSpikeA \
  -p 'test_*.py'
```
