# Foundational RFC Review Decisions

**Status:** Approved

**Decision Date:** 2026-07-19

**Decision Owner:** IndustrialMDE Project Owner

**Scope:** RFC-0000, RFC-0001, and RFC-0001A

## 1. Decision Effect

The project-owner architectural audit authorizes RFC-0000, RFC-0001, and RFC-0001A to advance from Draft to Proposed after the decisions in this record are incorporated.

Proposed RFCs remain non-normative review artifacts. This decision does not make any RFC Accepted and does not approve compiler implementation. It did not itself amend the Constitution; Project Constitution version 2.1 was subsequently Approved and incorporated through its separate amendment record.

The audit explicitly approves the 255-character identifier limit, current BOM handling, full delegation of namespace syntax to RFC-0001B, permanent prohibition of anonymous Definitions, Endpoint as the neutral kernel term, and the Project versus Application Assembly distinction. Other completion resolutions recorded below are incorporated as Proposed semantics for review and are not represented as separately owner-accepted behavior.

The former constitutional conflict gate is resolved by Approved Project Constitution version 2.1. RFC-0000 still requires its own acceptance review and conformance evidence before it can become Accepted.

An RFC may become Proposed when its dependencies exist at a compatible review status. It may become Accepted only after every normative dependency required by its final scope is Accepted.

## 2. RFC-0000 Decisions

| Topic | Decision |
| --- | --- |
| Semantic model direction | Core Semantic Kernel plus versioned Industrial Profiles is the Proposed foundation defined by RFC-0001A |
| Language-version source | Every source file declares its effective version; a project manifest may constrain the permitted set but cannot silently override a file |
| Expressions and iteration | Detailed constructs remain owned by RFC-0003 and RFC-0004; RFC-0000 retains the boundedness invariant |
| Attribute model | Deferred to a dedicated public contract; no attribute spelling or semantics are authorized implicitly |
| Version 1.0 stabilization set | Deferred until the reference spike and conformance evidence exist |
| Deprecated-version support window | Deferred to the managed compatibility and release-support policy required before stabilization |

Deferring the stabilization set and support-window duration does not change the pre-1.0 design principles. Those decisions are gates for stabilization, not for Proposed review status.

## 3. RFC-0001 Decisions

| Topic | Decision |
| --- | --- |
| Core identifier length | 255 ASCII characters is approved for the Proposed lexical contract; stricter target limits belong to target validation or deterministic mangling |
| UTF-8 byte-order mark | One UTF-8 BOM is permitted only at byte offset zero and ignored for tokenization while retained in raw offsets |
| Canonical source span | Half-open raw UTF-8 byte spans are canonical; human positions and protocol-specific coordinates are derived views |
| Bidirectional controls | The core retains a tooling `SHOULD` to expose security-sensitive invisible characters; no mandatory compiler warning is added by RFC-0001 |
| Documentation before version | Documentation comments may precede the `dsl` directive as trivia; attachment semantics remain undefined |
| Standard metadata keys | RFC-0001 standardizes none; a later provenance or documentation contract may register keys |
| Binary and hexadecimal integers | Retained in the foundational lexical contract |
| Reserved punctuation | The proposed punctuation set is retained as reserved syntax space; reservation alone grants no semantics |
| Namespace and import syntax | Fully owned by RFC-0001B; RFC-0001 only reserves the keywords and does not specify directive grammar |
| Project language-version policy | RFC-0001C may constrain a project's supported versions but cannot replace or silently override the per-file directive |

## 4. RFC-0001A Decisions

| Topic | Decision |
| --- | --- |
| Project and Application Assembly | Project is a build boundary; Application Assembly is a target-neutral semantic graph root. A Project may contain zero or more Application Assemblies |
| Deployment selection | One Deployment Model references exactly one Application Assembly in the foundational model |
| Core endpoint term | Endpoint is the sole neutral Core Semantic Kernel term; Port and Signal semantics belong to RFC-0005 |
| Parameter lifecycle | A Parameter is immutable after initialization. A future runtime configuration facility must use an explicit category and transaction contract rather than silently weakening Parameter |
| State and Behavior | Retained as foundational member categories; runtime meaning remains owned by RFC-0004 |
| Role multiplicity | At most one role per profile namespace and role category applies to an entity; cross-profile composition requires declared compatibility |
| `industrial.structure` | Standardized by RFC-0001A as the foundational target-neutral industrial role vocabulary |
| Strict industrial hierarchies | Process, machine, building, power, and logistics containment matrices require separate profile contracts; no universal hierarchy enters the kernel |
| Primitive | Remains an `industrial.structure` Definition role and not a kernel kind; a standard library may apply the role |
| Static arrays and replication | Deferred to RFC-0006; RFC-0001A retains cardinality-one Instance Declarations |
| Anonymous definitions | Permanently prohibited as a core identity invariant; a future change requires a superseding RFC and compatible major-version process |
| Connection transformations | Deferred to RFC-0005 and must be explicit and source-traceable; target lowering cannot invent a hidden transformation |
| Baseline expansion capacity | A conforming production compiler supports at least depth 64 and 262,144 total expanded semantic entities per Application Assembly |
| Identity across relocation | Identity is preserved only when package identity, namespace, owning declaration path, and member path remain unchanged |
| Application-level connections | Explicit connections between root Instances are permitted in an Application Assembly without requiring a wrapper Definition |

Reference spikes may intentionally implement lower resource limits but must declare that they are non-conforming.

## 5. Next Authorized Work

After the status and decision updates are published for review, work may begin on Draft RFC-0001B: Identifiers, Scopes, and Namespaces.

RFC-0001B must preserve:

- ASCII identifier spelling and the 255-character core limit from RFC-0001;
- the Definition, Instance Declaration, Instance, and Endpoint distinctions from RFC-0001A;
- explicit imports and deterministic resolution from RFC-0000;
- separation between semantic identity, external tags, and generated target names;
- the Project versus Application Assembly distinction.
