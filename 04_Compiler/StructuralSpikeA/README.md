# Structural Spike A Fixture Loader

This directory contains the disposable loader for
`experimental-structural-input/0`. It implements only the boundary before
Structural Reference Spike A pipeline step 1.

The loader:

- accepts bytes, a byte-oriented memory view, or an already-open binary source;
- enforces byte, JSON-depth, record, integer-token, and duplicate-key limits
  before admitting an over-limit value;
- validates the reviewed closed Draft 2020-12 schema with `jsonschema`;
- validates only the pre-step-1 project, origin, and marker integrity rules;
- normalizes only contract-declared set-like collections; and
- returns either two recursively immutable fixture artifacts or one bounded
  all-or-nothing failure.

It does not parse `.plant`, resolve names or types, select an Assembly, build a
closure, expand Instances, publish a snapshot, or emit `SPIKEA`/`IMDE`
diagnostics. It is not a package, CLI, production parser, or stable API.

## Locked environment

The Accepted ADR0005 stack is:

```text
CPython 3.12.13
uv 0.11.29
jsonschema 4.26.0
```

Create the environment and verify the lock from this directory:

```bash
uv sync --locked
uv lock --check
uv tree --locked --depth 10
```

Run the complete evidence suite:

```bash
uv run --locked python -m unittest discover \
  -s ../../09_Testing/StructuralSpikeA \
  -p 'test_*.py'
```

The executable schema is
`schema/experimental-structural-input-0.schema.json`. A test compares its
parsed JSON structure directly with the reviewed schema embedded in
`02_Architecture/Spike_A_Experimental_Input.md`.
