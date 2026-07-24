# Structural Spike A Step 1 Design Review Decision

**Status:** Accepted Design Gate

**Decision Date:** 2026-07-24

**Decision Owner:** IndustrialMDE Project Owner

**Review ID:** `AUDIT-STEP1-PHASE-A`

**Verdict:** `GO`

**Scope:** Disposable Structural Reference Spike A Step 1 resolution contract
and resolver ADR

**Verified Base:** `1c48928d28aa35c4f2b231c31327d828fed8129b`

**Verified Head:** `db1ec1b119691b4f621a0caf8ce4231cb7be58b4`

**Pull Request:** Draft Pull Request #16

## 1. Decision Effect

The independent Phase A audit returns `GO` for the Structural Reference Spike A
Step 1 design at exact Pull Request #16 head
`db1ec1b119691b4f621a0caf8ce4231cb7be58b4`.

The Project Owner accepts that audit at the exact verified head. This closes
the Phase A design gate for `TE-STRUCTURAL-SPIKE-STEP-1`, accepts ADR0006, and
confirms the reviewed `experimental-resolved-structural-model/0` and
`experimental-structural-resolution/0` boundaries as the accepted experimental
boundaries for a separately authorized disposable Step 1 implementation.

The accepted design remains:

- Experimental;
- Non-normative;
- Non-conforming;
- Non-interoperable;
- replaceable;
- disposable; and
- isolated from the production compiler architecture.

This decision does not approve, merge, retarget, close, or mark Pull Request
#16 Ready for Review. It does not authorize source, fixtures, tests,
dependencies, lock changes, or any compiler implementation.

## 2. Exact Review Scope

The audit inspected the unified diff from accepted fixture-loader gate commit
`1c48928d28aa35c4f2b231c31327d828fed8129b` to exact Phase A head
`db1ec1b119691b4f621a0caf8ce4231cb7be58b4`:

```text
5 changed files
2,308 insertions
4 deletions
```

The exact reviewed paths were:

```text
00_Project_Brain/02_Decisions.md
00_Project_Brain/03_Next_Tasks.md
00_Project_Brain/04_Project_State.md
02_Architecture/ADR/ADR0006_StructuralSpikeStep1Resolver.md
02_Architecture/Spike_A_Step_1_Resolution.md
```

No source, fixture, test, dependency, lock, accepted loader, normative RFC,
public grammar, Canonical IR, Target IR, runtime, emitter, plugin, UI, or LSP
path was changed.

## 3. Confirmed Design Properties

The review confirms:

- Step 1 consumes only an accepted loader `LoadSuccess`;
- the output algebra is either one immutable Resolved Structural Model or an
  explicit `ResolutionAbort`, never a partial published model;
- `CandidateKey` is a recovery identity and `DeclarationHandle` is a
  successful-resolution identity;
- Declaration Identities are structured values and never
  delimiter-concatenated strings;
- ordinary-symbol collision groups use no-winner behavior for exact,
  ASCII-case-only, and cross-kind collisions;
- source order and expected semantic kind never select an ambiguity winner;
- all ordinary declarations are collected before forward-reference
  resolution;
- imports do not chain and do not create implicit re-export;
- qualified traversal is iterative, left to right, limited to 64 segments,
  performs no backtracking, and preserves explicit invalid outcomes;
- intrinsic Type recognition is restricted to exact `BOOL`, `INT`, `REAL`,
  and `TIME` spellings in Type Reference context;
- wrong-kind validation remains Step 2a;
- Application Assembly selector validation and Structural Validation Closure
  construction remain Step 2b;
- selector candidates and typed unsupported-feature markers pass through
  unresolved and unevaluated;
- Step 1 owns only its reviewed `IMDE` diagnostic subset and emits no
  `INPUT_*`, `SPIKEA*`, `IMDE2xxx`, or later structural-validation
  diagnostic;
- diagnostic precedence, scope anchors, prerequisite blocking, ordering, and
  truncation are deterministic;
- name-index and retained-candidate pools are independently limited to
  1,000,000 admitted entries;
- a limit failure retains `IMDE3015`, publishes `ResolutionAbort`, and
  publishes no partial model;
- Step 1 performs no fixture-controlled filesystem, network, subprocess,
  environment, template, expression, or plugin action;
- all published values are deeply immutable; and
- the required matrix contains exactly 36 scenarios, from
  `step1_01_flat_intrinsics` through `step1_36_loader_partition`.

## 4. Accepted ADR0006 Choice

ADR0006 is accepted only for the disposable Step 1 resolver. Subject to a
separate exact Phase B authorization, the accepted implementation choice is:

```text
CPython 3.12.13
uv 0.11.29
the existing committed uv.lock
Python standard library only for new Step-1 code
unittest for evidence
in-process immutable artifact handoff
no internal serialization
```

The accepted package boundary is:

```text
04_Compiler/StructuralSpikeA/structural_spike_step1/
```

Dependency direction is one way from the Step 1 package to the accepted loader
package. The loader must not import Step 1, and Step 1 must not modify or
reimplement the loader.

Acceptance of ADR0006 does not complete or accept ADR0001, ADR0002, or ADR0003.
It does not establish CPython, `uv`, frozen dataclasses, in-process topology,
the package layout, or any internal index representation as a production
compiler precedent.

## 5. Explicit Non-Authorization

This decision does not authorize:

- source, fixture, test, dependency, or lock-file changes;
- modification of the accepted fixture loader or its 78-test evidence;
- approving, merging, retargeting, closing, or marking Pull Request #16 Ready
  for Review;
- production `.plant` grammar or textX parsing;
- a public compiler API, CLI, serialization, or compatibility promise;
- semantic-kind validation owned by Step 2a;
- Assembly-selector validation or resolution;
- Structural Validation Closure or Expansion Closure construction;
- semantic cycle, locality, direction, type, or driver diagnostics;
- Instance expansion or semantic resource accounting;
- Structural Snapshot publication;
- Canonical IR or Target IR;
- runtime, target, emitter, plugin, UI, or LSP work; or
- promotion of RFC-0005, RFC-0006, or RFC-0007 beyond Draft.

## 6. Next Gate

Structural Reference Spike A Step 1 implementation and every later compiler
phase remain on HOLD.

The commit containing this acceptance record is the accepted Gate A commit.
Phase B may begin only after the Project Owner issues a separate exact
authorization naming that commit:

```text
AUTHORIZE TE-STRUCTURAL-SPIKE-STEP-1 PHASE B AT <accepted-gate-a-commit>
```

Acceptance of this record is not Phase B authorization.
