# Structural Input Contract Review Decision

**Status:** Approved

**Decision Date:** 2026-07-24

**Decision Owner:** IndustrialMDE Project Owner

**Review ID:** `AUDIT-PR13-INPUT-CONTRACT`

**Scope:** `experimental-structural-input/0`, its closed Draft 2020-12 schema, loader boundaries, and the 44-scenario fixture matrix

**Verified Base:** `ba53d012883b5325f1c9978becf03de31904edba`

**Verified Head:** `7fdbfbc1b1cba0cb4a144244beccc4e855ec3234`

## 1. Decision Effect

The independent audit returns `GO` for the Experimental Structural Input Contract at Pull Request #13 head `7fdbfbc`.

The review approves the contract and all 44 named fixture scenarios as sufficient inputs for planning a bounded, separately authorized fixture loader. It closes the input-contract review and fixture-matrix gates recorded in `03_Next_Tasks.md`.

The reviewed artifact remains:

- Experimental;
- Non-normative;
- Non-conforming;
- Non-interoperable;
- disposable; and
- outside every public compatibility promise.

This decision does not make the contract an Accepted language RFC, a public compiler API, a production serialization, Canonical IR, or Target IR. It does not approve or merge Pull Request #13 and does not authorize Structural Reference Spike A compiler phases.

## 2. Exact Review Scope

The audit inspected the unified diff for exactly:

1. [`02_Decisions.md`](02_Decisions.md);
2. [`03_Next_Tasks.md`](03_Next_Tasks.md); and
3. [`Spike_A_Experimental_Input.md`](../02_Architecture/Spike_A_Experimental_Input.md).

The verified change set contains:

```text
3 changed files
1,707 insertions
2 deletions
```

No repository mutation occurred during the independent audit.

## 3. Confirmed Contract Properties

The review confirms:

- the exact identifier is `experimental-structural-input/0`;
- the schema uses JSON Schema Draft 2020-12;
- all 38 `$defs` are declared and referenced consistently;
- every object schema is closed with `additionalProperties: false`;
- unknown fields, kinds, and marker categories remain schema failures;
- zero, incomplete, one, and multiple selector candidates remain representable so selector validation stays in pipeline step 2b;
- declarations, references, selectors, and marker owner contexts remain unresolved at the loader boundary;
- typed unsupported markers carry only classification, ownership, origin, and an opaque payload range;
- expression payload is neither transported nor evaluated;
- Definition and Application Assembly `members` arrays preserve semantic declaration order;
- `declaration_ordinal` is derived from the complete zero-based member index;
- set-like collections have complete deterministic normalization keys;
- the loader diagnostic domain is limited to `INPUT_SYNTAX_001`, `INPUT_SCHEMA_001`, `INPUT_LIMIT_001`, and `INPUT_INTEGRITY_001`;
- every loader failure is all-or-nothing and publishes neither input artifact;
- loader byte, JSON-depth, record, origin, marker-span, and diagnostic limits are independent from semantic expansion limits;
- the exact semantic entity limit remains `262,144`;
- the exact semantic entity formula remains `instances.length + endpoints.length + connections.length`; and
- the fixture never authorizes path, URL, shell, template, expression, or opaque-payload execution.

## 4. Fixture Matrix Approval

The review approves exactly the 44 scenario identifiers `input_01_valid_flat` through `input_44_project_graph_integrity`.

For the loader boundary:

- nine scenarios are loader failures owned by `INPUT_*`;
- the other 35 scenarios must publish both immutable input artifacts, even when a later Spike A phase is expected to reject them.

The nine loader-failure scenarios are:

```text
input_04_schema_unknown_kind
input_05_duplicate_key
input_38_loader_byte_limit
input_39_loader_depth_limit
input_40_loader_record_limit
input_41_marker_span_limit
input_42_loader_diagnostic_limit
input_43_origin_integrity
input_44_project_graph_integrity
```

Approval of a later-phase expected result records a fixture requirement. It does not authorize the loader to emit `SPIKEA` or `IMDE` diagnostics, resolve a selector, construct a closure, expand an Instance, or publish a snapshot.

## 5. Implementation Boundary

The next implementation candidate is a duplicate-key-aware, token-preserving, bounded JSON fixture loader that:

1. consumes one untrusted byte stream;
2. enforces loader limits before over-limit materialization;
3. performs closed-schema validation;
4. performs only pre-step-1 input-integrity validation;
5. deterministically normalizes set-like collections; and
6. publishes immutable Resolved Project Context and Collected Structural Input fixture artifacts.

[`ADR0005_StructuralSpikeFixtureLoader.md`](../02_Architecture/ADR/ADR0005_StructuralSpikeFixtureLoader.md) is the spike-only owner for that replaceable choice. Independent audit `AUDIT-PR14-PHASE-A` returned `GO` against exact Phase A head `9bffef773a8af159db482ca19e5e8f9a789b4c3d`, and the Project Owner subsequently accepted the ADR.

That acceptance does not complete or accept the production choices listed in `ADR0001_TechStack.md`. Implementation remains on hold until Phase B is separately authorized against the exact commit that records acceptance.

## 6. Explicit Non-Authorization

This decision does not authorize:

- a commit to the audited Pull Request #13 head;
- marking Pull Request #12 or #13 Ready for Review;
- approving, retargeting, or merging either pull request;
- production `.plant` grammar or textX parsing;
- expression parsing or evaluation;
- declaration, import, type, or reference resolution;
- selector validation or resolution;
- Structural Validation Closure or Expansion Closure construction;
- semantic cycle, locality, direction, type, or driver diagnostics;
- Instance expansion;
- Structural Snapshot publication;
- Canonical IR or Target IR;
- public `IMDE` diagnostics;
- a production compiler API or CLI;
- runtime, target, emitter, plugin, UI, or LSP work; or
- promotion of RFC-0005, RFC-0006, or RFC-0007 beyond Draft.

## 7. Next Gates

The Project Owner authorized `TE-STRUCTURAL-LOADER-01 PHASE A` on 2026-07-24.

Phase A is limited to recording this review and proposing the spike-only loader ADR. It does not authorize loader source, dependencies, fixtures, or tests.

`AUDIT-PR14-PHASE-A` completed the independent ADR review with verdict `GO` against exact Phase A head `9bffef773a8af159db482ca19e5e8f9a789b4c3d`.

The Project Owner explicitly accepted ADR0005 on 2026-07-24. The commit containing this acceptance record is the accepted Gate A commit.

The remaining gate is a separate authorization naming that exact commit:

```text
AUTHORIZE TE-STRUCTURAL-LOADER-01 PHASE B AT <accepted-gate-commit>
```

Until that exact authorization is issued, fixture-loader implementation and every Structural Reference Spike A compiler phase remain on hold.
