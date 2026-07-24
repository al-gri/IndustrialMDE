# Spike A: Step 1 Structural Resolution

**Artifact Contract:** `experimental-resolved-structural-model/0`

**Resolution Algorithm:** `experimental-structural-resolution/0`

**Input Contract:** `experimental-structural-input/0`

**Status:** Experimental Design

**Lifecycle:** Non-normative, Non-conforming, Non-interoperable, Replaceable,
Disposable

**Implementation Status:** Not Authorized

**Task Envelope:** `TE-STRUCTURAL-SPIKE-STEP-1`

**Design Base:** `1c48928d28aa35c4f2b231c31327d828fed8129b`

## 1. Purpose and Lifecycle

This document defines the exact experimental boundary for Structural Reference
Spike A pipeline step 1:

```text
immutable Resolved Project Context fixture
+
immutable Collected Structural Input fixture
    -> ordinary-symbol collection and collision analysis
    -> candidate Declaration Identity construction
    -> import and reference resolution
    -> RFC-0002 intrinsic Type recognition
    -> explicit invalid recovery records
    -> immutable Resolved Structural Model
```

The architectural hypothesis is:

> Complete structured identity and deterministic resolution can be established
> before semantic-kind validation, Application Assembly selection, closure
> construction, cycle analysis, expansion, and snapshot publication.

This contract is not:

- a public compiler API;
- a public or stable serialization;
- Canonical IR;
- Target IR;
- a production symbol-table contract;
- a language-version conformance claim;
- a promise that the spike implementation will be retained; or
- authority to infer language semantics not already owned by an RFC.

An incompatible change replaces schema `0` and algorithm `0` with new
experimental identifiers. There is no compatibility or migration promise.

## 2. Authority and Scope

This contract is subordinate to:

1. Approved Project Constitution version 2.1;
2. Proposed RFC-0001A Semantic Object Model;
3. Proposed RFC-0001B Identifiers, Scopes, and Namespaces;
4. Proposed RFC-0001C Compilation Units, Modules, Packages, and Dependencies;
5. Proposed RFC-0002 Type System;
6. the Draft structural layers of RFC-0005, RFC-0006, and RFC-0007;
7. [`Spike_A_Experimental_Snapshot.md`](Spike_A_Experimental_Snapshot.md);
8. [`Spike_A_Experimental_Input.md`](Spike_A_Experimental_Input.md); and
9. the accepted fixture-loader boundary and evidence.

This document closes only experimental representation, ordering, recovery, and
phase-handoff choices required to test step 1. It does not alter an RFC
diagnostic, identity, visibility, import, or type rule.

If implementation requires a new public diagnostic, semantic kind, input
field, public limit, phase owner, or language rule, implementation must stop.
The discrepancy must be resolved in the owning specification rather than
hidden in code.

## 3. Exact Phase Boundary

### 3.1 Step 1 owns

Step 1 owns:

- construction of the Project Resolution Universe from the two accepted input
  artifacts;
- logical Namespace merge groups;
- structured candidate Declaration Identities;
- ordinary-symbol collision detection;
- direct Dependency Alias and Package Import Root views needed by source
  imports;
- file-local Import Environments;
- RFC-0001B and RFC-0001C import resolution and accessibility;
- ordinary structural reference resolution;
- RFC-0002 intrinsic Type recognition before ordinary Type lookup;
- explicit invalid resolution records;
- reference-dependency records needed for bounded diagnostic recovery;
- deterministic Step-1 diagnostics and warnings; and
- publication of one immutable Resolved Structural Model when bounded
  resolution completes.

### 3.2 Step 1 does not own

Step 1 must not:

- parse JSON or `.plant`;
- rerun input-schema or loader-integrity validation;
- fetch a Package or resolve a manifest/lock;
- validate the semantic required kind of a resolved reference;
- validate, parse, or resolve the Application Assembly selector;
- construct Structural Validation Closure, Expansion Closure, or a blocking
  versus non-blocking classification;
- detect Definition containment cycles;
- expand an Instance;
- construct an occurrence identity or occurrence graph;
- validate Endpoint locality;
- validate contextual direction;
- apply Type Equality or Connection compatibility;
- validate duplicate drivers;
- count published semantic entities;
- construct snapshot provenance;
- serialize or publish a snapshot;
- emit any `SPIKEA` diagnostic; or
- emit any `IMDE2xxx` semantic-kind, containment, expansion, or Connection
  diagnostic.

### 3.3 Phase-owner matrix

| Concern | Owner | Step-1 treatment |
| --- | --- | --- |
| JSON, schema, framing, loader limits, input integrity | Fixture Loader | Consume only successful immutable artifacts |
| Project/package graph resolution | Resolved Project Context producer | Reuse exact resolved facts |
| Declaration collision and identity candidates | Step 1 | Diagnose and preserve no-winner candidate groups |
| Import and ordinary reference resolution | Step 1 | Resolve or publish explicit invalid record |
| Intrinsic Type recognition | Step 1 | Recognize exact type-context spelling |
| Semantic required-kind validation | Step 2a | Carry expected/actual facts without verdict |
| Application Assembly selector | Step 2b | Carry unchanged |
| Validation scopes | Step 2b | Carry anchors only |
| Definition containment cycles | Step 3 | No Step-1 verdict |
| Expansion and semantic entity accounting | Step 4 | No Step-1 occurrence |
| Locality, direction, types, drivers | Steps 5–8 | No Step-1 verdict |
| Snapshot validation/publication | Step 9 | No Step-1 artifact is a snapshot |

## 4. Inputs and Entry Preconditions

Step 1 consumes the two artifacts contained in one accepted loader
`LoadSuccess`:

- `ResolvedProjectContextFixture`; and
- `CollectedStructuralInputFixture`.

The conceptual entry point is:

```text
resolve_structural_step1(LoadSuccess) -> Step1Outcome
```

This is an in-memory boundary. It has no path, URL, byte-stream, manifest
resolver, Package fetcher, parser callback, database, or network entry point.

Before semantic work, the resolver asserts these internal bundle invariants:

1. both artifacts use exact identifier
   `experimental-structural-input/0`;
2. their normalized Compilation Unit ownership keys agree;
3. every Compilation Unit belongs to one participating Package Revision and
   Module from the resolved context;
4. the exact language version is `0.1`;
5. the Project Resolution Fingerprint is present;
6. active expansion, entity, and diagnostic limits are present; and
7. the artifacts contain only accepted immutable loader value types.

The accepted loader already owns:

- UTF-8 and JSON validity;
- duplicate object-key rejection;
- closed Draft 2020-12 schema validation;
- loader byte, depth, record, origin, payload, and diagnostic limits;
- Project graph and Compilation Unit integrity;
- origin ranges and owner identity consistency;
- typed unsupported-marker integrity; and
- deterministic normalization of set-like collections.

Step 1 must not duplicate those passes or remap their failures.

A forged or programmatically corrupted bundle that violates an internal
precondition produces an internal `Step1InvariantError`. It produces no
`INPUT_*`, `SPIKEA`, or `IMDE` diagnostic and no phase artifact.

## 5. Result Algebra

Step 1 returns exactly one of:

```text
ResolutionComplete
  model: ResolvedStructuralModel
  ordered_diagnostics: tuple[Step1Diagnostic, ...]
  omitted_diagnostic_count: integer >= 0

ResolutionAbort
  abort_reason: resolver-resource-limit
  ordered_diagnostics: tuple[Step1Diagnostic, ...]
  omitted_diagnostic_count: integer >= 0
  model: absent
```

### 5.1 `ResolutionComplete`

`ResolutionComplete` means the complete bounded Project Resolution Universe has
been indexed and every admitted Step-1 reference has one explicit outcome.

It does not mean the selected compilation is valid.

The result may contain:

- declaration or Namespace collision groups;
- invalid declaration candidates;
- invalid imports;
- unresolved, ambiguous, inaccessible, or traversal-invalid references;
- references blocked by another invalid prerequisite;
- errors and warnings;
- diagnostics from declarations later proven unreachable; and
- selector and marker records that have not yet been classified.

This is required because closure membership is unknown until step 2b. Step 1
must not globally reject an error that may be wholly outside the selected
Structural Validation Closure.

### 5.2 `ResolutionAbort`

`ResolutionAbort` is used only when the fixed Step-1 name-index or
candidate-retention bound cannot be honored. It carries `IMDE3015` and no
partial model.

An unexpected exception, failed assertion, out-of-memory condition, or
implementation bug is an internal implementation failure. It is not rewritten
as a language or input diagnostic.

## 6. Resolved Structural Model

The immutable phase artifact has this conceptual record:

```text
ResolvedStructuralModel
  artifact_contract_identifier
  input_contract_identifier
  resolution_algorithm_identifier
  language_version
  project_resolution_fingerprint
  project_resolution_universe
  selector_request
```

Required identifier values are:

```text
artifact_contract_identifier = experimental-resolved-structural-model/0
input_contract_identifier    = experimental-structural-input/0
resolution_algorithm_identifier
                             = experimental-structural-resolution/0
```

The artifact is build-local and in-memory only. No JSON schema, byte encoding,
cache schema, pickle, database schema, wire format, public API, or stable
serialization is defined.

All published records and nested collections are immutable. A published model
must not contain:

- a mutable list, dictionary, or set;
- an iterator or generator;
- a parser or schema-validator object;
- an open file or socket;
- a callback;
- a work queue;
- a cache with observable insertion order; or
- a source string used as a substitute for a resolved identity.

## 7. Structured Identity Model

### 7.1 Input-kind mapping

Step 1 uses this exact mapping:

| Input `kind` | Declaration Identity `entity_kind` |
| --- | --- |
| `definition` | `definition` |
| `application-assembly` | `application-assembly` |
| `instance` | `instance-declaration` |
| `endpoint` | `endpoint-declaration` |
| `connection` | `connection-declaration` |
| `unsupported-marker` | No Declaration Identity |

An unsupported marker is a classified input record. Step 1 must not fabricate a
Declaration Identity for it.

### 7.2 Canonical Declaration Identity

Every candidate Declaration Identity is structured data:

```text
DeclarationIdentity
  package_identity
  namespace_path
  owner_path
  identifier
  entity_kind
```

For a top-level Definition or Application Assembly:

```text
owner_path = ()
```

For a schema-`0` member:

```text
owner_path = (top_level_owner_identifier,)
```

The identity excludes:

- Package Version;
- Package Content Identity;
- Package Revision;
- Module Identity;
- Compilation Unit Identity;
- Portable Package Path;
- source identity and span;
- declaration order;
- import alias;
- selector spelling;
- target-generated name;
- timestamp;
- process or object identity; and
- random UUID.

Moving a declaration between source files or Modules preserves Declaration
Identity when Package Identity, Namespace Path, owner path, declaration
spelling, and semantic entity kind remain unchanged. The move may still change
accessibility, origins, the Project Resolution Fingerprint, and build-local
handles.

### 7.3 Experimental semantic-kind order

Schema `0` closes the RFC-0001B entity-kind ordering requirement with:

```text
0  definition
1  application-assembly
2  instance-declaration
3  endpoint-declaration
4  connection-declaration
```

This order is experimental. It is not a public registry and does not constrain
a future Semantic Model contract.

### 7.4 Candidate key

Every top-level declaration, member, and marker receives a build-local recovery
key:

```text
CandidateKey
  normalized_compilation_unit_identity
  normalized_top_level_candidate_index
  optional_member_index
```

The top-level index is taken after the accepted loader's deterministic
normalization. The member index is the original semantic array position and is
not normalized.

A Candidate Key:

- distinguishes collected records during recovery;
- orders candidates with equal proposed identities;
- anchors diagnostics before a valid semantic identity exists;
- is not a Declaration Identity;
- does not enter a snapshot; and
- may change after source relocation or input-contract replacement.

### 7.5 Candidate, admitted declaration, and handle

Every declaration candidate retains:

```text
DeclarationCandidate
  candidate_key
  proposed_declaration_identity
  owning_compilation_unit
  owning_module
  visibility
  origin
  optional_declaration_ordinal
  admission_state
```

`admission_state` is one of:

```text
admitted
invalid-reserved-spelling
invalid-exact-collision
invalid-case-collision
invalid-namespace-binding
invalid-owner
```

Only one unambiguous admissible candidate receives a resolved build-local
handle:

```text
DeclarationHandle
  declaration_identity
  exact_owning_package_revision
  project_resolution_fingerprint
```

Module, Compilation Unit, visibility, and origin facts remain associated
records. They do not alter semantic equality.

When two candidates propose the same identity, Step 1 retains both candidates
and one collision group. It creates no winner, fallback identity, order-based
suffix, or handle for either candidate.

### 7.6 Namespace Identity

A logical Namespace Identity is:

```text
(Package Identity, Namespace Path)
```

Module Identity and physical directory are not Namespace components. Exact
Namespace contributions from one Package merge regardless of file discovery
order.

Namespace nodes and ordinary declarations share the collision rules defined by
RFC-0001B. A Namespace node is not a Declaration Identity.

### 7.7 Intrinsic Type Identity

An intrinsic Type is recognized only in a Type Reference context and has:

```text
domain:           industrialmde.language.intrinsic-type
language_version: 0.1
kind:             BOOL | INT | REAL | TIME
```

Its build-local handle is:

```text
(Intrinsic Type Identity, Project Resolution Fingerprint)
```

Intrinsic Types have no Package Revision, Package, Namespace, import, ordinary
binding, or hidden prelude.

### 7.8 Declaration ordinal

For every Definition or Application Assembly member:

```text
declaration_ordinal = zero-based index in the complete input members array
```

Unsupported markers consume positions. Invalid and pending-wrong-kind members
remain in the complete member order. Collision processing never compacts or
renumbers the array.

Schema `0` has no partial owner declarations or cross-unit member merge.
Therefore the complete input member index is also the post-collection,
pre-filtering semantic ordinal required by the snapshot contract.

## 8. Project Resolution Universe Records

The immutable Project Resolution Universe retains:

1. exact root and dependency Package Revisions;
2. direct Package dependency edges and aliases;
3. Module identities, exposure, source roots, and direct Module edges;
4. Compilation Unit identities and Canonical Source Identities;
5. logical Namespace identities and contributing units;
6. Package Import Root Domains;
7. every top-level and member declaration candidate;
8. every admitted Declaration Handle;
9. every collision group and invalid binding state;
10. every owner Member View;
11. every per-unit Import Environment and import result;
12. every structural reference and its resolution outcome;
13. every reference-dependency edge;
14. every unsupported marker, owner candidate, and optional member ordinal;
15. the exact selector request, unchanged; and
16. source and non-source origins needed by later diagnostics and traceability.

Mutable implementation indexes are not phase records. Lookup views exposed to
step 2 must be immutable sorted records or deterministic methods over immutable
records.

Invalid candidates remain queryable by proposed identity and Candidate Key so:

- selector resolution can detect an invalid or colliding candidate;
- closure construction can discover that a reachable fact is invalid;
- diagnostic scope can be classified after selection; and
- unreachable invalid declarations need not block snapshot publication.

## 9. Binding and Collision Domains

### 9.1 Identity-bearing scopes

Schema `0` uses:

- Package root;
- logical Namespace;
- Definition;
- Application Assembly; and
- file-local Import Environment.

Every Definition and Application Assembly member belongs to exactly one owner
scope. Independent owners may reuse one spelling.

### 9.2 Unified ordinary-symbol namespace

Within one identity-bearing owner scope, all ordinary declaration kinds share
one collision domain. Kind is not used to select a winner.

Therefore:

- an Endpoint and Instance in one Definition cannot share a spelling;
- a Definition and Application Assembly in one Namespace cannot share a
  spelling;
- private declarations still participate in collisions; and
- a wrong expected kind never triggers a second hidden-namespace lookup.

### 9.3 Exact and ASCII-folded collisions

For every collision domain, Step 1 retains:

- exact spelling;
- ASCII Case-Folded Key;
- all participating candidate keys;
- proposed structured identities;
- declaration or Namespace origins; and
- the single owning diagnostic.

Exact duplicate declarations use `IMDE3002`. Distinct spellings with one ASCII
Case-Folded Key use `IMDE3003`.

No locale, Unicode normalization, filesystem case rule, Module boundary,
visibility rule, or source order alters the result.

### 9.4 Namespace and declaration collision

A child Namespace segment and an ordinary declaration in the same parent
Namespace cannot share exact spelling or ASCII Case-Folded Key.

The collision invalidates the parent binding. It does not erase candidate
records below the Namespace or invent a replacement Namespace identity.

### 9.5 Intrinsic spelling reservation

The exact spellings:

```text
BOOL
INT
REAL
TIME
```

must not be introduced as:

- an ordinary declaration identifier;
- a Namespace segment;
- a Dependency Alias;
- an import alias; or
- another source-visible alias that can begin traversal.

Each introduction produces `IMDE5001`.

Independent violations remain independently reportable. Two declarations named
`INT`, for example, can establish two reserved-spelling violations and one
separate exact collision.

## 10. Package Import Roots and Accessibility

### 10.1 Import Root Domain

Each consuming Package has one Import Root Domain containing:

- every current-Package root Namespace segment; and
- every direct Dependency Alias.

A Dependency Alias and current-Package root Namespace segment must not collide
exactly or by ASCII Case-Folded Key. A joint-domain conflict produces
`IMDE4011` and no winner.

Dependency Alias is valid only as the first segment of an Import target. It is
not inserted into the ordinary unqualified environment and is not part of the
target Declaration Identity.

### 10.2 Import target traversal

An import target resolves left to right:

1. if the first segment is a direct Dependency Alias, enter that dependency's
   Export Surface;
2. otherwise enter a root Namespace of the current Package; and
3. resolve every remaining segment without backtracking.

Import directives never resolve through another import. Import order has no
resolution semantics.

A missing later segment does not reinterpret the first segment through another
Package, Namespace, alias, declaration, filesystem directory, or loaded
Package.

### 10.3 Accessibility

Accessibility is:

| Target | Required access |
| --- | --- |
| Private declaration in current Module | Accessible |
| Private declaration in another Module | Inaccessible |
| Public declaration in current Module | Accessible |
| Public declaration in another Module of same Package | Direct Module dependency |
| Public declaration in direct dependency Package | Owning Module exported, direct Package dependency, explicit source import |
| Any declaration in transitive-only dependency | Inaccessible |

An inaccessible declaration never becomes a successful resolution candidate.
An exact inaccessible match produces `IMDE4013`, not a successful binding or
generic unresolved result.

An undeclared, transitive-only, or self-dependency access produces
`IMDE4012`.

### 10.4 Import bindings

An import resolves to exactly one accessible:

- top-level semantic declaration; or
- logical Namespace.

A declaration import:

- uses its explicit alias when present; or
- otherwise uses the target's final identifier segment.

A Namespace import must have an explicit alias. Missing alias or invalid import
target kind produces `IMDE3011`.

Import aliases are file-local and share one Import Environment collision
domain with:

- every other import binding in that file; and
- directly visible declarations in the current merged Namespace.

### 10.5 Redundant, conflicting, and unused imports

Two imports with the same target and binding spelling produce one binding and
`IMDE3009`.

Two imports that request the same exact binding spelling for different targets
produce `IMDE3006`. Distinct case-only spellings produce `IMDE3003`. No source
order selects a winner.

An import binding counts as used when it uniquely supplies the first segment of
an ordinary resolution attempt, even if a later qualified segment fails.

- a redundant import does not also receive `IMDE3010`;
- an invalid or conflicting binding does not receive `IMDE3010`; and
- a valid binding never selected by a reference receives `IMDE3010`.

## 11. Ordinary Resolution

### 11.1 Complete collection before lookup

Step 1 collects every binding in an applicable scope before resolving any
order-independent reference. Every schema-`0` structural forward reference is
therefore supported.

Declaration order, unit order, source discovery order, and import order cannot
change a lookup.

### 11.2 Unqualified environment

An unqualified structural reference considers only:

1. the current owner Member View when the reference form permits owner
   members;
2. the current merged logical Namespace; and
3. the current source file's explicit Import Environment.

These sets have no shadowing priority.

If more than one distinct eligible accessible identity remains, resolution is
ambiguous and produces `IMDE3005`. Expected semantic kind never filters the
candidate set.

The resolver does not search:

- a parent Namespace;
- a sibling Namespace;
- every loaded Package;
- a transitive dependency;
- a filesystem directory;
- a hidden prelude; or
- a target-generated name.

### 11.3 Qualified traversal

Qualified traversal proceeds left to right:

1. resolve the first segment in exactly one authorized environment;
2. enter the Namespace or Member View exposed by that target;
3. resolve the next segment in that explicit view; and
4. continue without backtracking.

When a directly resolved prefix has no valid view, resolution produces
`IMDE3007`. The resolver does not reinterpret an earlier segment because a
later segment failed.

Qualification through a Definition denotes declaration members. Qualification
through an Instance Declaration follows the Member View associated with its
definition reference and records that dependency.

## 12. Structural Reference Classes

### 12.1 Reference record

Every structural reference publishes:

```text
ResolvedReference
  reference_key
  owner_candidate_key
  role
  raw_segments
  origin
  expected_target_kind
  outcome
  dependency_keys
```

A `reference_key` is:

```text
(owner_candidate_key, reference_role)
```

Import targets use:

```text
(normalized_compilation_unit_identity, normalized_import_index, import-target)
```

Reference keys are build-local recovery keys, not semantic identities.

### 12.2 Resolution outcomes

Every reference has exactly one outcome:

```text
ResolvedDeclaration
ResolvedIntrinsicType
Unresolved
Ambiguous
Inaccessible
InvalidTraversal
BlockedByPrerequisite
InvalidBinding
```

No invalid outcome has a valid target handle.

`Ambiguous` retains its complete deterministic candidate set within the fixed
candidate bound.

`BlockedByPrerequisite` names the exact invalid or pending reference on which
resolution depends. It does not invent an independent unresolved error.

### 12.3 Definition reference

Every Instance `definition_reference` resolves under ordinary RFC-0001B and
RFC-0001C rules.

The resulting record retains:

- expected kind `definition`;
- resolved target handle and actual kind when unique; or
- one typed invalid outcome.

A unique Application Assembly or another wrong-kind declaration remains a
successfully resolved name. Step 1 does not emit `IMDE2002` or `IMDE2009` and
does not retry lookup in a hidden Definition namespace.

### 12.4 Endpoint Type reference

In a Type Reference context:

1. when the complete reference is exactly one segment equal to `BOOL`, `INT`,
   `REAL`, or `TIME`, construct the corresponding Intrinsic Type handle;
2. perform no ordinary lookup for that reference; and
3. otherwise continue with ordinary resolution.

Comparison is exact ASCII and case-sensitive.

These are not intrinsic:

```text
Int
int
iNt
INT.Member
```

An unresolved ordinary Type Reference produces `IMDE3004`. A uniquely resolved
ordinary declaration retains expected Type kind and actual target kind for
step 2a.

Schema `0` has no user-defined Type declaration kind. `IMDE5002` is therefore
unreachable in Step 1.

### 12.5 Connection Endpoint reference

A Connection source or destination reference resolves to declaration/member
facts, not occurrence facts.

For a Definition-owned Connection:

- leading `self` is a contextual marker;
- it enters the current Definition Member View;
- it is not an ordinary binding or identity; and
- a child named `self` remains addressable as `self.self.<member>`.

An Application Assembly has no implicit `self`. A leading `self` there is
resolved as an ordinary first segment and is unresolved unless an ordinary
binding exists.

An Instance Declaration segment traverses the Member View supplied by its
resolved definition reference. Traversal is iterative, left to right, and
bounded by 64 segments.

Grandchild reach-through may resolve successfully in Step 1. Step 5 owns the
locality verdict.

The final target retains its actual semantic kind. Step 2a owns the Endpoint
required-kind verdict and any `IMDE2007`.

### 12.6 Prerequisite blocking

Member traversal may depend on an Instance definition reference.

When that prerequisite is:

- unresolved;
- ambiguous;
- inaccessible;
- an invalid binding; or
- uniquely resolved to a pending wrong semantic kind,

the dependent path records:

```text
BlockedByPrerequisite
  prerequisite_reference_key
```

It does not emit a cascading unresolved, traversal, locality, direction, type,
or driver diagnostic.

If a prefix directly selected by the current reference has no Namespace or
Member View and is not blocked by another semantic prerequisite, the reference
uses `InvalidTraversal` and `IMDE3007`.

Explicit dependency edges allow step 2a to suppress a derived wrong-kind
diagnostic that relies on an invalid prerequisite without suppressing
independent errors.

## 13. Selector and Unsupported Markers

### 13.1 Selector passthrough

Step 1 carries `selector_request` unchanged by immutable value.

It must not:

- require zero, one, or multiple candidates;
- check target completeness;
- parse `raw_spelling`;
- resolve a target;
- attach Application Assembly kind;
- validate root Package Revision ownership;
- choose a source-order or only-Assembly fallback; or
- emit `SPIKEA003`.

Step 2b alone owns those operations.

### 13.2 Unsupported-marker passthrough

Step 1 retains every typed unsupported marker with:

- exact marker record;
- Candidate Key;
- owner candidate;
- source origin;
- opaque payload range; and
- member ordinal when applicable.

Step 1 emits no marker diagnostic. Closure construction and the single-owner
matrix later determine `SPIKEA001`, `IMDE2004`, or a non-blocking diagnostic.

## 14. Diagnostic Contract

### 14.1 Authorized Step-1 codes

| Code | Condition |
| --- | --- |
| `IMDE3002` | Exact duplicate declaration/binding candidate in one ordinary collision domain |
| `IMDE3003` | ASCII case-only collision |
| `IMDE3004` | Unresolved ordinary name, import target, post-intrinsic Type Reference, or member segment |
| `IMDE3005` | Ambiguous name or import target |
| `IMDE3006` | Import binding or declaration would create exact implicit shadowing |
| `IMDE3007` | Qualified traversal reaches a prefix with no valid view |
| `IMDE3009` | Redundant identical import |
| `IMDE3010` | Valid unused import |
| `IMDE3011` | Namespace import lacks alias or resolved import target kind is invalid |
| `IMDE3013` | Identifier naming-convention warning |
| `IMDE3015` | Fixed name-index or candidate-retention limit exceeded |
| `IMDE4011` | Dependency Alias collides in the joint Package Import Root Domain |
| `IMDE4012` | Undeclared, transitive-only, or self dependency access |
| `IMDE4013` | Existing target is inaccessible under Module/Package visibility |
| `IMDE5001` | Exact intrinsic spelling introduced as a source-visible ordinary name or alias |

### 14.2 Unreachable or later codes

`IMDE3001`, `IMDE3008`, and `IMDE3012` represent syntax/placement facts that
cannot occur after the successful closed input contract.

`IMDE3014` and project-resolution codes other than the joint-domain
`IMDE4011`, import-access `IMDE4012`, and declaration-access `IMDE4013` are
owned before Step 1.

`IMDE5002` through `IMDE5005`, all `IMDE2xxx`, and all `SPIKEA` codes are not
Step-1 diagnostics.

### 14.3 Single-owner precedence

| Resolution fact | Single owner |
| --- | --- |
| Exact intrinsic Type designator in Type context | Intrinsic handle; no ordinary lookup |
| Exact intrinsic spelling introduced as binding | `IMDE5001` |
| Transitive, undeclared, or self dependency access | `IMDE4012`, not `IMDE3004` |
| Existing but inaccessible target | `IMDE4013`, not `IMDE3004` or `IMDE3011` |
| Ambiguous candidate set | `IMDE3005`, not `IMDE3004` |
| Later qualified segment has no view | `IMDE3007`, not `IMDE3004` |
| Namespace import lacks alias | `IMDE3011` |
| Same target and same import binding | `IMDE3009`; one binding |
| Exact import binding conflict | `IMDE3006` |
| Case-only collision | `IMDE3003` |
| Unique target has wrong semantic kind | Resolved record; step 2a diagnostic later |
| Connection path blocked by invalid prerequisite | `BlockedByPrerequisite`; no cascade |

Independent invalid facts remain independently reportable within the active
diagnostic limit.

### 14.4 Required diagnostic facts

Every retained diagnostic contains:

```text
code
severity
validation_step = 1
primary_origin
related_origins
scope_anchor
applicable structured identity or candidate key
reason-specific facts
```

Required reason-specific facts remain those defined by the owning RFC. In
particular:

- collision diagnostics retain all spellings, candidate identities, and
  origins;
- unresolved diagnostics retain the spelling and explicitly searched
  environments;
- ambiguity diagnostics retain the complete ordered candidate set;
- traversal diagnostics retain the failing segment and resolved prefix;
- access diagnostics retain target, visibility, Module, and required edge
  facts; and
- resource diagnostics retain active bound, observed next count, and affected
  scope.

No renderer-owned escaped string replaces structured facts.

### 14.5 Ordering

All Step-1 diagnostics have validation-step rank `1`, then order by:

1. primary origin-kind rank:
   `source`, `project-manifest`, `fixture-metadata`, `build-metadata`,
   `invocation`, `no-origin`;
2. Canonical Source Identity components or non-source origin identity;
3. raw start and raw end for source origins, or zero for non-source origins;
4. diagnostic code;
5. canonical structured semantic identity or empty tuple; and
6. stable reason-specific secondary key.

For a duplicate or collision, the lexicographically greater declaration origin
is primary and lower origins are related.

Candidate lists order by:

1. canonical structured identity;
2. canonical candidate origin; and
3. Candidate Key when identities and origins remain equal.

Related origins use canonical origin order.

Filesystem order, hash-map order, concurrency, locale, target selection, and
current time cannot affect output.

### 14.6 Diagnostic cap

The number of retained Step-1 diagnostics is at most:

```text
project_context.active_limits.maximum_diagnostics
```

The retained sequence is the deterministic prefix. The exact number of
otherwise reportable Step-1 diagnostics is recorded in
`omitted_diagnostic_count`.

Invalid records and diagnostic anchors remain complete when a rendered
diagnostic is omitted. A diagnostic cap cannot erase a blocking fact and cause
a later snapshot to publish.

An aborting `IMDE3015` is always retained in `ResolutionAbort`. Remaining
capacity may contain the deterministic prefix of independently discovered
Step-1 diagnostics.

The input contract carries no diagnostic-promotion configuration. Step 1 uses
the default RFC severities and must not infer promotion from environment,
filename, or invocation text.

## 15. Closure-Neutral Recovery

Step 1 does not classify a diagnostic as blocking or non-blocking.

Every invalid record and diagnostic carries one immutable scope anchor:

```text
ProjectAnchor
PackageAnchor
NamespaceAnchor
CompilationUnitAnchor
DeclarationCandidateAnchor
ReferenceAnchor
ImportAnchor
```

Step 2b uses those anchors and the selected reference graph to establish:

- Structural Validation Closure;
- Expansion Closure;
- Diagnostic Universe;
- closure-blocking diagnostics;
- shared-universe blocking diagnostics; and
- diagnostics wholly outside the selected closure.

A Step-1 error outside the selected closure may later remain non-blocking. A
collision, invalid binding, or reference failure that changes a selector,
shared identity, or reachable declaration becomes blocking.

No invalid record may cross a later boundary that requires its missing fact.
No invalid record may enter expansion, an occurrence identity, snapshot
provenance, or a published graph.

## 16. Resource Contract

### 16.1 Separation from semantic limits

Step 1 consumes none of:

```text
maximum expansion depth:             64
maximum published semantic entities: 262,144
```

The semantic entity count remains:

```text
instances.length + endpoints.length + connections.length
```

Namespace nodes, declaration candidates, handles, imports, references,
collision groups, diagnostics, and work items are not semantic entities.

### 16.2 Fixed Step-1 work envelope

The accepted input contract bounds Step-1 work:

| Work item | Maximum |
| --- | ---: |
| Input records admitted by loader | 1,000,000 |
| Step-1 index entries | 1,000,000 |
| Candidates retained for one ambiguous lookup | 1,000,000 |
| Namespace path segments | 64 |
| Qualified/reference path segments | 64 |
| Imports in one Compilation Unit | 65,536 |
| Retained diagnostics | Active `maximum_diagnostics`, 1–1,000,000 |

One Namespace node, declaration candidate, or import binding creates at most one
counted Step-1 index entry.

The implementation must:

- share immutable candidate sets rather than copy one complete ambiguity list
  for every reference;
- perform indexed lookup rather than all-Package scanning per reference;
- process each qualified path iteratively;
- avoid recursive Definition containment traversal;
- create no occurrence work queue; and
- check a fixed bound before admitting the next over-limit index entry or
  retained candidate.

If a bound cannot be honored, Step 1 produces `ResolutionAbort`,
`IMDE3015`, and no partial model. It must not report `IMDE2011` or
`INPUT_LIMIT_001`.

## 17. Determinism

### 17.1 Canonical identity order

Declaration Identities order by:

1. Package Authority labels and Package Name under RFC-0001C;
2. Namespace Path segments by exact ASCII bytes;
3. owner path segments by exact ASCII bytes;
4. identifier by exact ASCII bytes; and
5. the experimental semantic-kind ordinal in section 7.3.

Intrinsic kinds order by exact UTF-8 bytes:

```text
BOOL
INT
REAL
TIME
```

### 17.2 Non-input influences

These must not change identities, resolution, diagnostics, or the normalized
phase artifact:

- JSON object-member order;
- reordered set-like input arrays after loader normalization;
- filesystem discovery order;
- hash randomization;
- dictionary insertion or iteration order;
- concurrency schedule;
- locale;
- absolute checkout, cache, or extraction path;
- current time;
- process state; or
- random values.

### 17.3 Change effects

| Change | Declaration Identity | Build-local handle or other fact |
| --- | --- | --- |
| Source file relocation only | Preserved | Compilation Unit, origins, fingerprint, and handle context may change |
| Move between Modules with semantic components unchanged | Preserved | Accessibility and handle context may change |
| Package Version or content change only | Preserved | Package Revision and handle change |
| Dependency Alias rename | Target identity preserved | Import binding, source references, and fingerprint change |
| Member position change | Preserved | `declaration_ordinal` changes |
| Namespace, owner, spelling, Package Identity, or kind change | Changes | Dependent references invalidate |

## 18. Security and Isolation

All fixture strings remain untrusted data.

Step 1 must:

- perform no network access;
- open no fixture-controlled path;
- execute no string, expression, callback, template, shell fragment, or module
  name;
- perform no dynamic import based on fixture content;
- avoid exposing environment variables, host paths, credentials, or memory
  contents;
- retain `raw_spelling` as data only;
- use iterative bounded name traversal;
- avoid Definition-graph recursion;
- avoid unbounded diagnostic or candidate copying; and
- leave both loader artifacts unchanged.

In-process composition with the loader is not a security sandbox.

## 19. Required Fixture Matrix

A later separately authorized implementation must provide at least:

| Fixture | Required fact | Expected Step-1 result |
| --- | --- | --- |
| `step1_01_flat_intrinsics` | Flat valid model and all four intrinsic Types | Complete model; exact identities and handles |
| `step1_02_forward_reference` | Reference precedes target declaration | Same result as target-before-reference |
| `step1_03_merged_namespace` | Same Namespace across units/Modules | One logical Namespace |
| `step1_04_member_ordinals` | Marker and invalid member between valid members | Original gapped ordinals |
| `step1_05_selector_passthrough` | Zero, one, partial, and multiple candidates | Exact value; no `SPIKEA003` |
| `step1_06_marker_passthrough` | Every marker category | No Step-1 marker diagnostic |
| `step1_07_identity_kind_mapping` | Every schema-`0` declaration kind | Exact section 7.1 mapping |
| `step1_08_source_relocation` | Source path changes only | Identity stable; build context changes |
| `step1_09_package_revision_handle` | Package Revision changes only | Identity stable; handle changes |
| `step1_10_structured_components` | Components collide if delimiter-joined | Identities remain distinct |
| `step1_11_exact_duplicate` | Duplicate top-level and member declaration | `IMDE3002`; no winner |
| `step1_12_case_collision` | Case-only Namespace/declaration/member/import | `IMDE3003`; no winner |
| `step1_13_cross_kind_collision` | Member kinds share spelling | One collision domain |
| `step1_14_namespace_declaration_collision` | Namespace/declaration binding conflict | No source-order choice |
| `step1_15_intrinsic_reservation` | Intrinsic spelling used in every binding category | Exact `IMDE5001` facts |
| `step1_16_same_package_import` | Explicit same-Package import | Unique target and binding |
| `step1_17_direct_dependency_import` | Public declaration in exported direct dependency Module | Unique target |
| `step1_18_transitive_dependency` | Transitive-only Package access | `IMDE4012` |
| `step1_19_visibility` | Private cross-Module and non-exported target | `IMDE4013` |
| `step1_20_namespace_import_alias` | Namespace import with/without alias | Binding or `IMDE3011` |
| `step1_21_redundant_import` | Same target and alias repeated | One binding and `IMDE3009` |
| `step1_22_import_conflicts` | Exact and case-only conflicts | `IMDE3006` or `IMDE3003` |
| `step1_23_unused_import` | Used, unused, redundant, invalid imports | Exact `IMDE3010` ownership |
| `step1_24_unresolved_references` | Definition, Type, Endpoint-path misses | `IMDE3004` invalid records |
| `step1_25_ambiguity` | Multiple eligible explicit identities | `IMDE3005`; ordered candidates |
| `step1_26_invalid_traversal` | Prefix has no applicable view | `IMDE3007`; no backtracking |
| `step1_27_wrong_kind_deferred` | Unique wrong-kind targets | Resolved facts; no `IMDE2xxx` |
| `step1_28_self_and_member_paths` | `self`, child, sibling, grandchild | Targets resolved; locality deferred |
| `step1_29_prerequisite_block` | Path depends on invalid definition reference | Dependency block; no cascade |
| `step1_30_intrinsic_exactness` | Exact, case-variant, multi-segment types | Intrinsic only for exact one segment |
| `step1_31_diagnostic_order_cap` | Mixed diagnostics exceed cap | Deterministic prefix and omitted count |
| `step1_32_randomized_order` | Units, imports, maps, work queues shuffled | Equal model and diagnostics |
| `step1_33_index_bound` | Derived public bound and private admission harness | Bound proof; next entry aborts without model |
| `step1_34_security_boundary` | Path, URL, shell, template, environment strings | Inert data |
| `step1_35_phase_boundary` | Cycles, semantic limits, kind/direction/type/driver errors | No downstream diagnostic |
| `step1_36_loader_partition` | All accepted 44 loader scenarios | Nine never enter Step 1; 35 complete resolution |

End-to-end cases must use the accepted loader entry point. Focused unit evidence
may exercise private builders only to prove before-admission and internal
ordering properties.

## 20. Implementation Evidence Requirements

A separately authorized implementation must prove:

1. all existing accepted loader tests remain unchanged and pass;
2. all 44 accepted loader scenarios preserve their loader verdict;
3. every fixture in section 19 passes;
4. every published nesting level is immutable;
5. randomized insertion, map, and work-queue orders produce equal results;
6. no collision selects a winner;
7. every structural reference has exactly one outcome;
8. wrong-kind targets are not re-resolved through a hidden kind namespace;
9. selector and marker records remain unchanged and unresolved;
10. no unauthorized diagnostic domain appears;
11. no Step-2-or-later record appears;
12. diagnostics and candidate lists remain bounded and deterministic;
13. no fixture-controlled file, network, process, template, or execution side
    effect occurs; and
14. the exact Accepted ADR runtime and locked environment are used.

These are future implementation requirements. This Phase A document contains
no implementation authorization.

## 21. Review and Implementation Gates

### 21.1 Phase A design review

This contract and Proposed
[`ADR0006_StructuralSpikeStep1Resolver.md`](ADR/ADR0006_StructuralSpikeStep1Resolver.md)
require independent review against exact repository head.

A positive audit must verify:

- identity versus recovery-key versus handle separation;
- no-winner collisions;
- phase ownership;
- reference dependencies and suppression;
- diagnostic ownership and precedence;
- closure-neutral recovery;
- fixed work bounds;
- security/isolation; and
- the complete fixture matrix.

### 21.2 ADR acceptance

ADR0006 remains `Proposed` until explicit Project Owner acceptance is recorded
in the repository at an exact reviewed commit.

### 21.3 Phase B authorization

Implementation requires a separate exact command:

```text
AUTHORIZE TE-STRUCTURAL-SPIKE-STEP-1 PHASE B AT <accepted-gate-a-commit>
```

Phase A authorization, a positive audit, or ADR acceptance alone does not
authorize source, fixture, test, dependency, or lock changes.

### 21.4 Later phases remain on HOLD

Acceptance or implementation of Step 1 does not authorize:

- step 2a semantic-kind validation;
- step 2b Assembly selection or scope construction;
- step 3 cycle validation;
- steps 4–8 expansion or structural validation; or
- step 9 snapshot publication.

## 22. Change and Disposal Policy

This contract applies only while:

```text
experimental-structural-input/0
experimental-resolved-structural-model/0
experimental-structural-resolution/0
```

remain the active Spike A identifiers.

Any change to:

- an identity field;
- entity-kind mapping or order;
- result algebra;
- reference outcome;
- collision rule;
- resolution environment;
- diagnostic owner or precedence;
- scope anchor;
- fixed work bound;
- ordering rule; or
- phase boundary

requires another experimental revision or an explicit declaration that all
schema-`0` Step-1 fixtures are replaced.

Production implementation must not silently adopt this in-memory model,
runtime, index structure, or recovery representation. It must use separately
accepted RFCs, ADRs, and compiler contracts.

The spike implementation may be deleted rather than migrated after the
architectural hypothesis has been evaluated and evidence recorded.

## 23. Design Decisions Closed by This Revision

This revision fixes:

- complete bounded resolution may publish a model containing invalid recovery
  records;
- only resource-bound failure publishes no model;
- collision groups have no winner;
- Candidate Key is distinct from Declaration Identity;
- build-local handle includes Package Revision and Project Resolution
  Fingerprint;
- Module and source path do not enter Declaration Identity;
- the schema-`0` entity-kind mapping and order;
- exact one-segment intrinsic recognition;
- selector and marker passthrough;
- prerequisite-blocked Connection path recovery;
- closure-neutral diagnostic anchors;
- exact Step-1 diagnostic ownership and precedence;
- independent Step-1 versus semantic expansion budgets; and
- the minimum 36-scenario implementation matrix.
