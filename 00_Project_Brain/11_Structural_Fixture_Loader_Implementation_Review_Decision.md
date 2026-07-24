# Structural Fixture Loader Implementation Review Decision

**Status:** Accepted Implementation Gate

**Decision Date:** 2026-07-24

**Decision Owner:** IndustrialMDE Project Owner

**Review ID:** `AUDIT-PR15-PHASE-B`

**Verdict:** `IMPLEMENTATION GO / COMPILER HOLD`

**Scope:** Disposable `experimental-structural-input/0` fixture-loader implementation and its executable evidence

**Verified Base:** `4591552fa478f53c65ee3b1f4342a0e3d7a9b938`

**Verified Head:** `d60fb889b5313143c2afacbdd376ea1d55f19178`

**Pull Request:** Draft Pull Request #15

## 1. Decision Effect

The independent Phase B audit returns `IMPLEMENTATION GO / COMPILER HOLD`
for the Structural Spike A fixture-loader implementation at exact Pull Request
#15 head `d60fb889b5313143c2afacbdd376ea1d55f19178`.

The Project Owner accepts that audit at the exact verified head. This closes
the implementation-evidence gate for `TE-STRUCTURAL-LOADER-01` and confirms
that the disposable loader satisfies the reviewed input contract and Accepted
ADR0005 within its authorized scope.

The accepted implementation remains:

- Experimental;
- Non-normative;
- Non-conforming;
- Non-interoperable;
- disposable; and
- isolated from the production compiler architecture.

This decision does not merge or approve Pull Request #15, mark it Ready for
Review, make its API stable, or authorize Structural Reference Spike A step 1
or any later compiler phase.

## 2. Exact Review Scope

The audit inspected the unified diff from accepted Gate A commit `4591552` to
Phase B implementation head `d60fb889`:

```text
27 changed files
5,658 insertions
4 deletions
```

The exact reviewed paths were:

```text
00_Project_Brain/03_Next_Tasks.md
00_Project_Brain/04_Project_State.md
01_Documentation/Testing_Strategy.md
04_Compiler/StructuralSpikeA/.gitignore
04_Compiler/StructuralSpikeA/README.md
04_Compiler/StructuralSpikeA/pyproject.toml
04_Compiler/StructuralSpikeA/schema/experimental-structural-input-0.schema.json
04_Compiler/StructuralSpikeA/structural_spike_loader/__init__.py
04_Compiler/StructuralSpikeA/structural_spike_loader/bounded_json.py
04_Compiler/StructuralSpikeA/structural_spike_loader/diagnostics.py
04_Compiler/StructuralSpikeA/structural_spike_loader/integrity.py
04_Compiler/StructuralSpikeA/structural_spike_loader/loader.py
04_Compiler/StructuralSpikeA/structural_spike_loader/model.py
04_Compiler/StructuralSpikeA/structural_spike_loader/normalization.py
04_Compiler/StructuralSpikeA/structural_spike_loader/schema_validation.py
04_Compiler/StructuralSpikeA/uv.lock
09_Testing/StructuralSpikeA/.gitignore
09_Testing/StructuralSpikeA/README.md
09_Testing/StructuralSpikeA/fixture_manifest.json
09_Testing/StructuralSpikeA/raw_cases.py
09_Testing/StructuralSpikeA/scenario_factory.py
09_Testing/StructuralSpikeA/support.py
09_Testing/StructuralSpikeA/test_integrity_normalization.py
09_Testing/StructuralSpikeA/test_parser.py
09_Testing/StructuralSpikeA/test_scenarios.py
09_Testing/StructuralSpikeA/test_schema_contract.py
09_Testing/StructuralSpikeA/test_security_phase_boundary.py
```

No normative RFC, public grammar, production parser, Canonical IR, Target IR,
runtime, emitter, plugin, UI, or LSP path was changed.

## 3. Confirmed Implementation Properties

The review confirms:

- the loader package entry point accepts bytes or an already-open binary source
  and exposes no path or URL entry point;
- the custom JSON parser is iterative and preserves number-token spelling;
- byte, JSON-depth, and input-record limits are checked before admitting the
  next over-limit byte, container, or value;
- duplicate object keys are detected after JSON string decoding, including
  escape-equivalent keys;
- canonical integers are converted directly to integers without binary64;
- the executable schema contains the reviewed 38 `$defs`, uses an explicit
  `Draft202012Validator`, and has internal-only references;
- validation implements only the authorized pre-step-1 integrity boundary;
- only contract-declared set-like collections are normalized;
- Definition and Application Assembly `members` retain their exact order;
- both published success artifacts are recursively immutable;
- every expected input failure returns an all-or-nothing `LoadFailure`;
- the diagnostic domain contains only `INPUT_SYNTAX_001`,
  `INPUT_SCHEMA_001`, `INPUT_LIMIT_001`, and `INPUT_INTEGRITY_001`;
- no `SPIKEA` or public `IMDE` diagnostic is emitted;
- fixture-controlled path, URL, shell, environment, template, and opaque
  payload text remains inert;
- the loader performs no fixture-controlled file open or network access; and
- no resolved Declaration Identity, resolved Type Identity, selected Assembly,
  closure, occurrence, expanded graph, snapshot, or provenance is published.

## 4. Executable Evidence

The accepted evidence uses:

```text
CPython 3.12.13
uv 0.11.29
jsonschema 4.26.0
```

The committed lock resolves the exact dependency graph accepted by ADR0005:

```text
attrs 26.1.0
jsonschema 4.26.0
jsonschema-specifications 2025.9.1
referencing 0.37.0
rpds-py 2026.6.3
typing-extensions 4.16.0
```

The audited validation result is:

```text
78 tests passed
0 failures
0 errors
0 skipped
```

The manifest contains exactly 44 reviewed scenarios:

- 35 loader successes publishing both immutable boundary artifacts; and
- nine loader failures with the reviewed `INPUT_*` owner.

Semantic depth and entity scenarios `input_34` through `input_37` are carried
without the loader consuming or enforcing the downstream semantic limits.

## 5. Schema-Drift Evidence Clarification

`test_executable_projection_has_no_drift_from_reviewed_markdown` parses the
executable schema and the Markdown-embedded reviewed schema as JSON and proves
structural equality of the resulting JSON values.

The test does not claim byte-for-byte equality of whitespace or formatting.
This clarification preserves the intended no-drift guarantee and does not
change the audit verdict.

## 6. Explicit Non-Authorization

This decision does not authorize:

- approving, merging, retargeting, closing, or marking Pull Request #15 Ready
  for Review;
- mutation of Pull Request #13 or Pull Request #14;
- production `.plant` grammar or textX parsing;
- declaration, import, type, or reference resolution;
- semantic-kind validation;
- Assembly-selector validation or resolution;
- Structural Validation Closure or Expansion Closure construction;
- semantic cycle, locality, direction, type, or driver diagnostics;
- Instance expansion or semantic resource accounting;
- Structural Snapshot publication;
- Canonical IR or Target IR;
- public compiler API or CLI work;
- runtime, target, emitter, plugin, UI, or LSP work; or
- promotion of RFC-0005, RFC-0006, or RFC-0007 beyond Draft.

## 7. Next Gate

Structural Reference Spike A step 1 and every later compiler phase remain on
HOLD.

The next work item is a separately reviewed, bounded Task Envelope defining
the exact step-1 input, Declaration Identity construction, resolution universe,
invalid-record recovery, diagnostics, resource limits, fixture expectations,
and phase output. Design or implementation of that work requires a new
explicit Project Owner authorization naming the applicable accepted gate
commit.

Acceptance of this record is not that authorization.
