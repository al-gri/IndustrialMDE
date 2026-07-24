# Testing Strategy

## Structural Spike A Fixture Loader

The `experimental-structural-input/0` loader uses an executable evidence suite
under `09_Testing/StructuralSpikeA`. This suite is scoped to the disposable
boundary before Structural Reference Spike A pipeline step 1; it does not
claim production parser, compiler, or language conformance.

The evidence layers are:

1. raw-byte lexical and parser-state tests;
2. exact before-admission resource-boundary tests;
3. a structural drift comparison between the executable Draft 2020-12 schema
   and the reviewed Markdown-embedded schema;
4. cross-record input-integrity and deterministic-normalization tests;
5. recursive immutability, security, I/O-isolation, and phase-boundary tests;
6. one manifest-driven run of all 44 reviewed scenarios.

Large cases are deterministic recipes rather than committed blobs. The manifest
records each scenario identity, generator source, exact parameters, expected
loader owner, and the fixed randomized-order seed. Boundary readers verify that
the byte source is not consumed beyond `10,485,761` bytes. Record and depth
tests assert that the next value or container is rejected before admission.

The locked validation command is:

```bash
cd 04_Compiler/StructuralSpikeA
uv sync --locked
uv run --locked python -m unittest discover \
  -s ../../09_Testing/StructuralSpikeA \
  -p 'test_*.py'
```

Phase B evidence on CPython `3.12.13`, `uv 0.11.29`, and the committed lock is
`78` tests passed, `0` failed, `0` errors, and `0` skipped. The manifest run
confirms exactly `44` scenarios partitioned into `35` loader successes and `9`
loader failures.

This evidence authorizes no downstream invocation. Loader failure publishes no
artifact, and loader success publishes only Resolved Project Context Fixture
and Collected Structural Input Fixture.
