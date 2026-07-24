# ADR0006: Structural Spike A Step-1 Resolver Technology

**Status:** Proposed

**Date:** 2026-07-24

**Decision Scope:** Disposable
`experimental-resolved-structural-model/0` Step-1 resolver only

**Decision Owner:** IndustrialMDE Project Owner

**Task Envelope:** `TE-STRUCTURAL-SPIKE-STEP-1`

**Proposal Base:** `1c48928d28aa35c4f2b231c31327d828fed8129b`

**Implementation Authorization:** Not Granted

## 1. Context

The accepted fixture loader publishes two immutable artifacts conforming to
`experimental-structural-input/0`:

- a Resolved Project Context fixture; and
- Collected Structural Input.

[`Spike_A_Step_1_Resolution.md`](../Spike_A_Step_1_Resolution.md) defines the
next experimental boundary. Step 1 must construct candidate Declaration
Identities, collision groups, import environments, resolved or explicitly
invalid structural references, and one immutable Resolved Structural Model.

Step 1 must preserve strict phase isolation:

- required-kind validation remains step 2a;
- Application Assembly selection and closure construction remain step 2b;
- containment cycles remain step 3;
- expansion remains step 4;
- locality, direction, type, and driver validation remain steps 5 through 8;
  and
- snapshot publication remains step 9.

Approved Project Constitution version 2.1 requires replaceable implementation
choices to be recorded in an ADR. The Accepted ADR0005 selects CPython,
`uv`, `jsonschema`, a custom bounded JSON parser, and immutable fixture records
for the loader only. ADR0005 explicitly does not authorize compiler resolution
or establish a production compiler precedent.

ADR0001 and ADR0003 remain incomplete. This ADR must not complete or accept
their production choices by implication.

## 2. Decision Drivers

The disposable resolver needs:

- direct consumption of the accepted loader's immutable in-memory artifacts;
- no lossy conversion through another serialized representation;
- structured identities rather than delimiter-concatenated strings;
- deterministic exact and ASCII-folded collision indexes;
- complete collection before forward-reference resolution;
- immutable shared candidate sets for ambiguity recovery;
- iterative left-to-right path traversal without backtracking;
- explicit reference-dependency edges;
- deterministic bounded diagnostics;
- no source, manifest, filesystem, network, expression, or template execution;
- no Step-2-or-later semantic behavior;
- regression reuse of the existing 44-scenario loader corpus;
- a small, reviewable implementation suitable for deletion; and
- isolation from the production compiler architecture.

Throughput is not a conformance claim. Correct identity, resolution, recovery,
ordering, bounds, and phase ownership take priority.

## 3. Proposed Decision

Subject to independent audit, explicit Project Owner acceptance, and a separate
Phase B authorization, implement Step 1 in the existing disposable Structural
Spike A project using:

```text
CPython 3.12.13
uv 0.11.29
the existing committed uv.lock
Python standard library only for new Step-1 code
unittest for evidence
in-process immutable artifact handoff
no internal serialization
```

The implementation package is:

```text
04_Compiler/StructuralSpikeA/structural_spike_step1/
```

The loader package remains:

```text
04_Compiler/StructuralSpikeA/structural_spike_loader/
```

Dependency direction is one way:

```text
structural_spike_loader
          |
          v
structural_spike_step1
```

The loader must not import Step 1.

## 4. Runtime and Lock

### 4.1 Runtime

Use the exact runtime already accepted for the disposable loader evidence:

```text
CPython 3.12.13
```

The project constraint remains:

```text
requires-python = "==3.12.*"
```

Evidence must record the full implementation and patch version.

A different Python minor version requires an ADR amendment. A later `3.12.x`
security patch may replace `3.12.13` only through a reviewed lock/tool refresh
and complete loader plus Step-1 regression run.

This choice minimizes boundary conversion and permits direct reuse of the
accepted frozen loader records. It is not evidence for a production compiler
runtime.

### 4.2 Project and lock tool

Reuse:

```text
uv 0.11.29
04_Compiler/StructuralSpikeA/pyproject.toml
04_Compiler/StructuralSpikeA/uv.lock
```

Phase B must use:

```text
uv sync --locked
uv lock --check
uv run --locked python -m unittest discover \
  -s ../../09_Testing/StructuralSpikeA \
  -p 'test_*.py'
```

No lock or dependency change is expected.

If implementing Step 1 changes `uv.lock`, adds a direct dependency, changes a
transitive dependency, changes an index, or relaxes the Python constraint,
implementation must stop for ADR amendment and explicit review.

## 5. Dependency Policy

### 5.1 New Step-1 dependencies

The new resolver uses the Python standard library only.

It must not add:

- a parser framework;
- a graph library;
- a persistent collection library;
- a database;
- a serializer;
- a property-testing framework;
- a network client;
- a template engine;
- a native extension; or
- a dynamic plugin system.

### 5.2 Existing locked graph

The accepted loader retains its existing exact runtime dependency graph:

```text
jsonschema 4.26.0
attrs 26.1.0
jsonschema-specifications 2025.9.1
referencing 0.37.0
rpds-py 2026.6.3
typing-extensions 4.16.0
```

Step 1 must not import or call `jsonschema` or any transitive validator
dependency. Their presence is inherited from the loader project and does not
make them Step-1 dependencies.

No new license review is required when the lock remains byte-identical. Any
dependency change reopens license, provenance, and supply-chain review.

## 6. Process Topology and Entry Point

### 6.1 In-process boundary

Run Step 1 in the same process after a successful fixture load.

The conceptual public-in-the-spike entry point is:

```python
resolve_structural_step1(loaded: LoadSuccess) -> Step1Outcome
```

The entry point accepts no:

- path;
- URL;
- source text;
- JSON bytes;
- manifest;
- parser node;
- mutable dictionary;
- callback;
- executor;
- network session; or
- dependency resolver.

### 6.2 Why no subprocess

A subprocess would require:

- an internal wire format;
- another serialization and validation boundary;
- identity and origin encoding;
- process failure mapping;
- extra resource controls; and
- duplicate conformance evidence.

Those costs do not test the Step-1 hypothesis. The in-process choice remains
replaceable because it is confined to the disposable spike.

### 6.3 Internal invariant failure

A forged or corrupted `LoadSuccess` produces an internal
`Step1InvariantError`. It does not produce a user-facing `INPUT_*`, `SPIKEA`,
or `IMDE` diagnostic.

Unexpected exceptions remain implementation failures. They must not be
converted into fabricated language semantics.

## 7. Package Layout

The exact Phase B file split may be adjusted within the authorized package, but
responsibilities must remain separated:

```text
structural_spike_step1/
  __init__.py          public-in-the-spike entry point and result exports
  model.py             immutable phase records and result algebra
  identities.py        structured identity/order keys
  universe.py          Package, Module, unit, Namespace views
  collisions.py        exact/folded collision groups
  imports.py           Import Root and file-local Import Environments
  references.py        ordinary and member-path resolution
  diagnostics.py       facts, ordering, cap, omitted count
  resolver.py          phase orchestration and freeze boundary
```

No module may parse `.plant`, JSON, a selector spelling, or an opaque payload.

The package has no:

- wheel;
- package-index release;
- console script;
- public CLI;
- server;
- daemon;
- plugin discovery;
- stable import API; or
- compatibility guarantee.

## 8. Immutable Record Strategy

### 8.1 Published records

Use frozen, slotted dataclasses and tuples for published records.

Every nested published value must be:

- an immutable scalar;
- a frozen record;
- a tuple of immutable values; or
- an ADR-approved immutable lookup view over immutable tuples.

Published artifacts must not contain:

- `list`;
- `dict`;
- mutable `set`;
- iterator;
- generator;
- lazy callback;
- parser node;
- schema-validator object;
- file handle;
- socket;
- lock;
- mutable cache; or
- builder.

### 8.2 Internal builders

Private mutable dictionaries, sets, and lists may be used while constructing:

- Namespace indexes;
- collision domains;
- declaration indexes;
- import environments;
- use counts;
- reference dependencies;
- diagnostic candidates; and
- freeze-order lists.

They must not escape. They become unreachable before
`ResolutionComplete` is returned.

### 8.3 No internal serialization

Do not serialize the Resolved Structural Model.

Tests compare immutable normalized records directly. A test-only diagnostic
projection may produce ordinary values for assertions, but it is not an
artifact format and must not be consumed by a later phase.

Do not use:

- JSON;
- pickle;
- marshal;
- SQLite;
- YAML;
- Protocol Buffers;
- MessagePack;
- a cache file; or
- a hash digest as a substitute for complete identity.

## 9. Identity and Key Representation

### 9.1 Structured records

Represent Package, Namespace, Declaration, Intrinsic Type, candidate, reference,
and scope-anchor identities as distinct frozen record types.

Do not represent semantic equality through:

- delimiter-joined strings;
- rendered qualified names;
- Python object identity;
- source paths;
- integer allocation IDs; or
- hashes without complete collision checks.

### 9.2 Ordering keys

Each record type supplies one explicit canonical tuple key.

Strings compare by encoded ASCII or UTF-8 bytes as required by the owning
contract. No locale-aware comparison is permitted.

The Step-1 entity-kind order is a closed mapping:

```text
definition             -> 0
application-assembly   -> 1
instance-declaration   -> 2
endpoint-declaration   -> 3
connection-declaration -> 4
```

An unknown kind is an internal invariant failure because the loader's closed
schema has already rejected it.

### 9.3 Handle context

Resolved declaration handles store:

```text
(Declaration Identity, Package Revision, Project Resolution Fingerprint)
```

Intrinsic Type handles store:

```text
(Intrinsic Type Identity, Project Resolution Fingerprint)
```

No handle is persisted across builds or used as a public identity.

## 10. Index and Collision Strategy

### 10.1 Complete collection

Build all scope binding sets before resolving references in those scopes.

Use private indexes keyed by:

- exact Identifier spelling; and
- ASCII Case-Folded Key.

The folded key is collision evidence only. It never replaces exact spelling or
makes the language case-insensitive.

### 10.2 No-winner collision groups

When a collision occurs:

1. retain every candidate;
2. construct one immutable collision group;
3. order candidates canonically;
4. attach the owning diagnostic facts;
5. create no admitted binding for the group; and
6. never select the first, last, nearest, public, matching-kind, or
   source-earliest candidate.

### 10.3 Candidate-set sharing

Ambiguous references must share one immutable canonical candidate tuple for an
equal lookup result. Do not copy a large candidate set for every reference.

An internal interning map may deduplicate candidate tuples during construction.
The map is not published, and correctness must not depend on Python hash order.

### 10.4 Complexity target

Within the fixed input contract:

- scope collection is linear in admitted candidates and Namespace segments;
- exact/folded index insertion is expected constant time with equality checks;
- lookup does not scan all Packages;
- one qualified reference processes at most 64 segments; and
- Definition containment is not traversed recursively.

These are implementation-review expectations, not public performance
guarantees.

## 11. Import Resolution Strategy

Build one Package Import Root Domain from:

- current-Package root Namespace segments; and
- direct Dependency Aliases.

Resolve each import target iteratively left to right. Never use another import
as an import-target root.

Build each file-local Import Environment only after:

- target resolution;
- direct-dependency validation;
- Module and Package accessibility;
- Namespace-alias form validation;
- redundant-import grouping; and
- collision analysis.

Track binding use by stable import-binding record, not by text search.

An invalid import creates no fallback binding.

## 12. Reference Resolution Strategy

### 12.1 Ordinary references

Represent each applicable environment as an immutable or private indexed view.
Combine eligible exact candidates without shadow priority.

Expected semantic kind is data attached to the resolved reference. It is never
a lookup filter.

### 12.2 Intrinsic Types

Recognize intrinsic Types through an exact four-entry branch or frozen mapping
before ordinary Type lookup.

The mapping is fixed:

```text
BOOL
INT
REAL
TIME
```

No registry or plugin may add an intrinsic Type.

### 12.3 Qualified paths

Use an iterative loop over at most 64 segments.

At each segment, carry:

- current explicit view;
- resolved prefix;
- candidate set or handle;
- originating reference key; and
- prerequisite reference keys.

Do not use recursion or backtracking.

### 12.4 Connection paths and prerequisite recovery

For a Connection path that traverses an Instance Declaration, consult the
Instance's already resolved definition reference.

If that prerequisite is invalid or pending wrong kind, publish
`BlockedByPrerequisite` and its dependency edge. Do not issue a cascading
lookup error.

Step 1 may compare actual and expected kind only to determine that traversal
depends on a pending semantic prerequisite. It must not emit a kind verdict or
retry through another kind namespace.

## 13. Diagnostics

### 13.1 Representation

Use frozen diagnostic records containing:

```text
code
severity
validation_step
primary_origin
related_origins
scope_anchor
structured identity or Candidate Key
reason-specific fact record
```

Do not expose Python exception strings, object representations, absolute host
paths, or library error order.

### 13.2 Collection and order

Private builders may collect independently provable diagnostics.

Before publication:

1. choose the primary origin under the owning rule;
2. sort related origins;
3. compute the complete Step-1 diagnostic key;
4. sort deterministically;
5. retain the active-limit prefix; and
6. record the exact omitted count.

### 13.3 Abort diagnostic

The before-admission resource guard must retain `IMDE3015` in
`ResolutionAbort`, even when other diagnostic candidates already exist.

No partial model is returned.

### 13.4 Domain restriction

The package may emit only the exact Step-1 codes authorized by
`Spike_A_Step_1_Resolution.md`.

It must contain no implementation path that emits:

- `INPUT_*`;
- `SPIKEA*`;
- `IMDE2xxx`;
- `IMDE5002` through `IMDE5005`; or
- an unregistered code.

## 14. Resource Enforcement

Use the fixed bounds from the Step-1 contract:

```text
maximum index entries:                    1,000,000
maximum retained ambiguity candidates:    1,000,000
maximum qualified/reference segments:     64
maximum imports in one Compilation Unit:  65,536
maximum retained diagnostics:             active maximum_diagnostics
```

Check the index and candidate bound before admitting the next entry.

The public accepted loader result structurally proves the index cannot exceed
the fixed maximum when each Namespace node, declaration candidate, and import
binding contributes at most one counted entry. Phase B tests must also exercise
a private reduced-bound admission harness to prove exact-before-next behavior
without constructing a million-record fixture for every unit test.

The private harness must not create a user-configurable production limit or
change public behavior.

Step-1 work items never consume the expansion depth or published semantic
entity limit.

## 15. Determinism Strategy

Private dictionaries and sets are permitted for lookup only. Every observable
collection is reconstructed from a canonical sorted sequence before freezing.

Tests must vary:

- Compilation Unit insertion;
- Namespace contribution insertion;
- declaration insertion for set-like collections;
- import insertion;
- dictionary construction order;
- collision candidate discovery;
- diagnostic discovery;
- candidate-tuple interning order; and
- private work-queue order.

Equal accepted inputs must produce structurally equal:

- candidate identities;
- admitted handles;
- collision groups;
- import environments;
- reference outcomes;
- dependency edges;
- diagnostics;
- omitted counts; and
- complete Resolved Structural Models.

No production concurrency is selected for Step 1. Tests may randomize private
work scheduling but the proposed implementation remains single-process and
single-threaded.

## 16. Security

The Step-1 resolver treats every string as inert data.

It must not:

- call `open` for a fixture-controlled value;
- create a socket;
- invoke a subprocess;
- inspect or modify environment variables based on fixture data;
- dynamically import a fixture-supplied name;
- evaluate source or expression text;
- interpolate a shell, template, SQL, regex, or HTML program from fixture data;
- fetch a Package or schema;
- follow a symlink or Portable Package Path;
- expose a host cache or checkout path; or
- deserialize another format.

Use ordinary exact string equality and byte ordering. Do not compile
fixture-controlled regular expressions.

The accepted loader artifacts remain unchanged. Deep immutability tests must
attempt mutation at every published nesting level.

In-process execution is not a security sandbox. The safety claim is limited to
the absence of fixture-directed capabilities and bounded resolver work.

## 17. Test Strategy

Use standard-library `unittest`. Add no new test dependency.

Phase B evidence must include:

- all accepted loader tests;
- all 44 accepted loader scenarios;
- the 36-scenario Step-1 matrix;
- focused identity and ordering tests;
- collision no-winner tests;
- direct, transitive, and inaccessible import tests;
- intrinsic exactness tests;
- wrong-kind deferral tests;
- prerequisite-recovery tests;
- exact diagnostic order and cap tests;
- private before-admission bound tests;
- randomized internal-order tests;
- deep immutability tests;
- no-I/O/no-network/no-process tests; and
- phase-boundary tests proving no Step-2-or-later fact appears.

Generated fixtures use fixed generator identifiers and seeds. Randomized tests
must print or retain the seed on failure.

No snapshot golden file is created by Step 1.

## 18. Alternatives Considered

### 18.1 Extend `structural_spike_loader`

Rejected.

The accepted loader has a deliberately closed pre-Step-1 responsibility and
diagnostic domain. Adding resolution there would invalidate its phase-boundary
evidence, permit `IMDE` emission from the loader, and couple input parsing to
semantic resolution.

A separate package preserves one-way dependency and accepted loader evidence.

### 18.2 Separate Rust resolver subprocess

Rejected for this disposable step.

Rust could provide strong static typing and explicit ownership, but a separate
process would require:

- a new toolchain and lock;
- an internal wire format;
- duplicate immutable model definitions;
- process resource and failure policy;
- origin and identity encoding;
- cross-language fixture tooling; and
- new supply-chain review.

Those costs test process/serialization architecture rather than the Step-1
identity and resolution hypothesis.

This rejection does not decide the production compiler language.

### 18.3 SQLite or relational resolution engine

Rejected.

A relational engine could express symbol tables and joins, but it would add:

- persistence and schema choices;
- collation risk;
- transaction and temporary-file behavior;
- host SQLite version dependence;
- another resource model; and
- cleanup/security concerns.

The bounded in-memory graph does not justify those choices.

### 18.4 Persistent immutable collection dependency

Rejected.

The phase boundary needs immutable published records, not a public persistent
data-structure API. Frozen records plus canonical tuples are sufficient. A
library would add lock, license, version, and semantic-ordering surface without
testing a required hypothesis.

### 18.5 Production compiler symbol table

Rejected.

ADR0001 and ADR0003 are incomplete, and Canonical IR is undefined. Reusing or
inventing a production symbol table here would let disposable spike behavior
constrain public compiler architecture.

### 18.6 Serialize between loader and resolver

Rejected.

Serialization would duplicate the reviewed input schema or create an
unreviewed internal schema. Direct immutable handoff preserves exact accepted
values and avoids another parser, schema, and resource boundary.

### 18.7 Kind-filtered lookup

Rejected as semantically incorrect.

RFC-0001B defines one unified ordinary-symbol namespace. Expected kind cannot
choose among duplicate bindings or trigger a second lookup. Step 1 retains the
actual target; step 2a owns the kind verdict.

### 18.8 Source-order winner

Rejected as semantically incorrect and nondeterministic.

Collisions retain all candidates and no winner.

## 19. Consequences

### 19.1 Positive

- The accepted loader artifacts pass directly into Step 1.
- No new dependency or lock change is expected.
- Identity, handle, and recovery-key types remain explicit.
- Collision recovery cannot silently select a declaration.
- Wrong-kind resolution remains separate from kind validation.
- Large ambiguity sets can be shared.
- Diagnostics can be normalized independently of discovery order.
- The implementation remains small enough for independent audit and deletion.
- The loader's no-resolution boundary remains intact.

### 19.2 Negative

- Python does not enforce deep immutability automatically.
- Internal dictionaries require disciplined canonical freeze passes.
- Static typing is weaker than a compiled algebraic-data-type implementation.
- A custom resolver can accidentally leak kind checks or source-order behavior.
- One process shares memory with the loader and is not a security sandbox.
- The fixed one-million-entry envelope can still require substantial memory.
- The implementation is intentionally throwaway and may not be reusable.

### 19.3 Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Mutable builder escapes | Frozen slotted records, tuple-only nested values, deep mutation tests |
| Hash order affects output | Canonical sort before freeze; randomized insertion tests |
| Collision selects winner | Collision-group API has no winner field; negative tests |
| Expected kind filters lookup | Resolver API receives kind only as retained fact; wrong-kind fixtures |
| Import chaining occurs | Separate Package Import Root resolver with no Import Environment input |
| Visibility removes collision | Collect collisions before accessibility filtering |
| Dependency access falls back globally | Direct alias index only; transitive/undeclared fixtures |
| Intrinsic becomes hidden binding | Dedicated four-value Type-context branch; environment absence tests |
| Connection path cascades errors | Explicit prerequisite edge and `BlockedByPrerequisite` outcome |
| Candidate lists multiply memory | Intern canonical immutable candidate tuples |
| Diagnostic cap erases invalid fact | Complete invalid records plus exact omitted count |
| Step-1 count consumes semantic limit | Independent counters and phase-boundary tests |
| Fixture string gains capability | No path/URL/callback API; monkey-patched side-effect tests |
| Spike becomes production precedent | Explicit lifecycle, separate package, no public serialization, mandatory replacement review |

## 20. Compliance Rules

Any separately authorized Phase B implementation must:

- use the exact accepted Gate A commit named in its authorization;
- remain inside the authorized path roots;
- use the exact runtime and existing lock;
- add no dependency without an accepted amendment;
- import the loader in only one direction;
- accept only `LoadSuccess`;
- publish only the Step-1 result algebra;
- implement the exact contract identifiers;
- preserve structured identity fields;
- implement no-winner collisions;
- keep expected kind out of candidate selection;
- retain explicit invalid outcomes and dependency edges;
- keep selector and markers unresolved;
- emit only authorized Step-1 diagnostics;
- enforce independent Step-1 work bounds;
- publish no mutable value;
- perform no fixture-controlled I/O or execution;
- implement no Step-2-or-later fact; and
- make no production compatibility or performance claim.

Every divergence requires an ADR amendment before implementation.

## 21. Review and Implementation Gate

This ADR is `Proposed`.

It does not authorize:

- source code;
- tests;
- fixtures;
- dependency or lock changes;
- modification of the accepted loader;
- a branch merge;
- PR approval or Ready-for-Review transition; or
- any compiler phase.

Independent review must inspect this ADR together with
`Spike_A_Step_1_Resolution.md`.

Only explicit Project Owner acceptance recorded at the exact reviewed Phase A
head may change this ADR to `Accepted`.

After acceptance, Phase B still requires:

```text
AUTHORIZE TE-STRUCTURAL-SPIKE-STEP-1 PHASE B AT <accepted-gate-a-commit>
```

Acceptance of this ADR is not Phase B authorization.

## 22. Replacement and Supersession

This ADR does not supersede:

- ADR0001 Tech Stack;
- ADR0002 IR Design;
- ADR0003 Compiler Architecture; or
- ADR0005 Structural Spike A Fixture Loader Technology.

It supplements ADR0005 only for one downstream disposable phase.

It applies only while:

```text
experimental-structural-input/0
experimental-resolved-structural-model/0
experimental-structural-resolution/0
```

remain active.

Replacing any identifier, changing the phase boundary, or adopting a production
compiler architecture triggers review. The Step-1 package may be deleted rather
than migrated after its architectural evidence is recorded.

Production implementation must use separately accepted ADRs and must not cite
this proposal as implicit approval of Python, in-process resolution, frozen
dataclasses, the package layout, or the internal index design.

## 23. Decision Evidence

The proposal was prepared against:

- Approved Project Constitution version 2.1;
- Proposed RFC-0001A, RFC-0001B, RFC-0001C, and RFC-0002;
- Draft RFC-0005, RFC-0006, and RFC-0007 structural layers;
- `experimental-structural-input/0`;
- `experimental-structural-snapshot/0`;
- `experimental-resolved-structural-model/0`;
- Accepted ADR0005;
- accepted fixture-loader implementation evidence at
  `d60fb889b5313143c2afacbdd376ea1d55f19178`; and
- exact Phase A base
  `1c48928d28aa35c4f2b231c31327d828fed8129b`.

Repository contracts control the decision. External runtime documentation does
not create language semantics or override the reviewed phase contract.
