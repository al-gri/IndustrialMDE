# RFC-0001C Review Decision

**Status:** Approved

**Decision Date:** 2026-07-20

**Decision Owner:** IndustrialMDE Project Owner

**Scope:** RFC-0001C Proposed transition, RFC-0001D Draft ownership, and the language-version `0.1` prelude clarification in RFC-0001B

## 1. Decision Effect

The independent architectural review authorizes RFC-0001C to advance from Draft to Proposed after the amendments recorded here are incorporated.

The same review authorizes creation of Draft RFC-0001D as the sole public-contract owner for Project Manifest, Package Manifest, and Dependency Lock serialization. RFC-0001D defines a complete strict JSON schema `0.1` for review; it remains Draft and non-normative.

Proposed remains a non-normative review status. This decision does not make RFC-0001C or RFC-0001D Accepted, Implemented, or Stabilized. It does not authorize production compiler, package-manager, PLC-runtime, or target-emitter implementation.

## 2. Confirmed Architectural Direction

The review confirms that RFC-0001C remains consistent with Approved Project Constitution version 2.1 and the Proposed RFC-0000 through RFC-0001B direction. It approves the following Proposed architecture:

- Project is an explicit build boundary and is not an Application Assembly;
- one root Package participates in a foundational Project;
- Package Identity is distinct from Package Version, Package Content Identity, and Package Revision;
- one Package Revision per Package Identity participates in one Project;
- one `.plant` file is one Compilation Unit in language version `0.1`;
- Modules own source, visibility, export, direct Module dependencies, and incremental boundaries without becoming Namespaces;
- Package and Module dependency graphs are acyclic;
- imports do not create dependencies and transitive packages are not source-visible;
- cross-package imports begin with a direct Dependency Alias;
- top-level declarations are private by default;
- Package export requires both a Public declaration and an exported Module;
- normal compilation treats the Dependency Lock as immutable input;
- a Dependency Lock is mandatory for reproducible or production compilation, while an explicitly unlocked development mode may omit it without triggering implicit discovery;
- exact dependency artifact and manifest digests are verified;
- clean and incremental compilation must remain observationally equivalent; and
- public graph, diagnostic, identity, and fingerprint processing is deterministic.

## 3. Required Amendments Incorporated for Proposed Status

The Proposed transition includes these material clarifications:

### 3.1 Public Serialization Ownership

- RFC-0001C owns the semantic document and cross-document build model.
- RFC-0001D owns public filenames, encoding, exact schemas, duplicate handling, spans, canonical serialization, and migration.
- An ADR may select a parser library or internal codec architecture but cannot define or override the public format.
- ADR0005 is not created because no replaceable reference-spike codec implementation has been selected.

### 3.2 Graph Direction and Scheduling

Public dependency edges remain `consumer → dependency`. Dependency-first processing uses deterministic reverse topological scheduling based on remaining outgoing dependency edges. Canonical serialization order and invalidation traversal remain distinct operations.

### 3.3 Root Workspace Content Identity

Package Content Identity is tagged as `immutable-artifact` or `workspace-snapshot`.

The root Workspace Content Fingerprint includes root-package-owned manifest, path, and source bytes after an immutable compilation snapshot. It excludes the Project Manifest, Dependency Lock, dependency artifacts, compiler version, and project configuration. Those inputs are combined separately in the Project Resolution Fingerprint, preventing a self-referential lock hash.

### 3.4 Language Version and Prelude

One foundational Project uses exactly one effective language version. Mixed-version linking is unsupported in version `0.1`.

Language version `0.1` has no implicit Package, Namespace, ordinary-symbol, or standard-library prelude. RFC-0002 may define intrinsic type entities, but they are not hidden Package declarations, imports, or ordinary-symbol bindings.

This decision supersedes only the language-prelude delegation recorded in section 3 of the [RFC-0001B Review Decision](07_RFC-0001B_Review_Decision.md). The other RFC-0001B review findings and gates remain in force.

RFC-0001B's delegated-gate table is synchronized to describe the now-existing Proposed RFC-0001C rules; RFC-0001C remains their owning contract, so this synchronization does not make those rules Accepted through RFC-0001B.

### 3.5 Portable Paths and Module Privacy

Portable Package Paths reject Windows reserved device stems even with extensions. Selected build documents must be regular non-link files, and participating symbolic links, junctions, reparse points, and archive links are rejected below declared roots.

Module privacy restricts accessibility but does not create a Module-owned semantic collision domain. Private declarations in different Modules still collide when they contribute the same spelling to one merged logical Namespace.

### 3.6 Resolved Handles and Cache Safety

Compiler APIs and caches must distinguish Canonical Semantic Identity from a build-local resolved handle that includes Package Revision and Project Resolution Fingerprint. Semantic identity alone cannot authorize cross-build cache reuse or reuse of a previously resolved type relation; type identity and equality remain owned by RFC-0002.

## 4. RFC-0001D Review Boundary

Draft RFC-0001D selects a strict RFC 8259 JSON profile for schema `0.1` and defines:

- exact canonical filenames;
- UTF-8 without a byte-order mark;
- closed object schemas and exact value kinds;
- duplicate-member rejection before map construction;
- exact Package Identity, version, language-version, path, and digest forms;
- independent manifest-schema and Language Version coordinates, with unsupported well-formed language versions delegated to RFC-0001C diagnostics;
- Project, Package, Module, dependency, lock-package, and lock-edge objects;
- raw byte spans and JSON Pointer field paths;
- deterministic diagnostics `IMDE4101` through `IMDE4107`;
- explicit precedence of serialization diagnostics over semantic document-graph diagnostics for the same fact;
- stable artifact-based diagnostic origins that exclude host cache and extraction paths;
- RFC 8785 canonical serialization after semantic array ordering and canonical-key uniqueness validation; and
- explicit schema migration with no compilation-time rewrite.

Selection of JSON is Proposed only through this Draft review artifact. It does not become a stable public format until RFC-0001D is separately accepted.

## 5. Remaining Acceptance and Downstream Conformance Gates

RFC-0001C cannot become Accepted until its listed normative dependencies and every unresolved behavior inside its own final scope are Accepted or resolved.

RFC-0001D depends on RFC-0001C and therefore is not an upstream RFC-0001C acceptance prerequisite. Instead, end-to-end tooling that reads or writes the public files requires compatible Accepted versions of both RFCs. The same rule applies to downstream Type System, composition, deployment, distribution, and compiler-conformance contracts: they gate claims in their own scope without creating a circular RFC lifecycle dependency.

The remaining downstream or complete-toolchain gates include:

- RFC-0001D must complete independent serialization review before public manifest or lock tooling claims conformance;
- RFC-0002 and RFC-0006 must define public type and member signature closure;
- RFC-0007 must define Application Assembly and Deployment entry-point selection where applicable;
- a Package Distribution RFC must define authority ownership, archive, retrieval, and publication behavior;
- security and distribution contracts must define signatures and provenance before trusted package distribution is claimed;
- a public compiler or fingerprint specification must define exact fingerprint encoding;
- a Compiler Conformance Specification must define production resource minima; and
- conformance evidence for each claimed scope must cover positive, negative, boundary, compatibility, randomized-order, integrity, and incremental-equivalence cases.

No implementation may fill these gates with undocumented behavior.

## 6. Next Authorized Work

After this transition package is published for review:

1. review Draft RFC-0001D independently as a public compatibility contract;
2. begin a minimal RFC-0002 Type System design, including intrinsic type resolution;
3. define the minimum RFC-0005, RFC-0006, and RFC-0007 structural slices needed by a full Application Assembly spike;
4. define explicitly experimental grammar and structural IR snapshot contracts before implementing their parsers or serializers; and
5. implement only a non-conforming Structural Reference Spike until the applicable semantic contracts are Accepted.

Behavioral expressions, interlocks, scan-cycle behavior, initialization, and PLC-like lowering remain blocked on RFC-0003 and RFC-0004.
