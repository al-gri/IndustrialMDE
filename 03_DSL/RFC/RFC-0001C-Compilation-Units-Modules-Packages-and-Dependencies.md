# RFC-0001C: Compilation Units, Modules, Packages, and Dependencies

**Status:** Proposed

**Authors:** IndustrialMDE Project

**Created:** 2026-07-20

**Last Updated:** 2026-07-20

**Target Language Version:** Pre-1.0

**Dependencies:** RFC-0000, RFC-0001, RFC-0001A, RFC-0001B

**Supersedes:** None

**Superseded By:** None

**Implementation Status:** Not Started

**Review:** Initial Draft in [Pull Request #9](https://github.com/al-gri/IndustrialMDE/pull/9); Proposed transition review pending

## 1. Summary

This RFC defines the build and distribution boundaries that make IndustrialMDE source resolution deterministic. It specifies Project, Package Identity, Package Revision, Package Manifest, Module, Source Root, Compilation Unit, direct dependency, dependency lock, visibility, export, source discovery, graph validation, and incremental fingerprint contracts.

The foundational model deliberately separates:

- a Project as one build and orchestration boundary;
- a Package Identity as a stable logical distribution identity;
- a Package Revision as one exact version and content realization of that identity;
- a Module as an explicit source, visibility, and incremental-compilation boundary;
- a Compilation Unit as one normalized `.plant` source file; and
- a Namespace as the logical naming domain defined by RFC-0001B.

Packages, modules, namespaces, files, and semantic declarations are not synonyms. Physical directory layout does not create semantic namespaces, and dependency availability does not create an import binding.

This RFC also closes the package-facing decision gates delegated by RFC-0001B. Cross-package import targets begin with an explicit direct-dependency alias. Package and module dependency graphs are acyclic. Transitive dependencies are not source-visible. Public re-export is not supported in language version `0.1`.

This document is a non-normative Proposed specification. Public Project Manifest, Package Manifest, and Dependency Lock serialization is owned by Draft RFC-0001D. A compiler implementation MUST NOT treat either Proposed semantics or a Draft serialization as Accepted language behavior.

## 2. Motivation

Deterministic name resolution requires more than identifier and namespace rules. A compiler must know:

- which source files participate in a build;
- which package owns each file;
- which module owns each compilation unit;
- which package revision satisfies each dependency;
- which declarations are accessible across module and package boundaries;
- which external bytes were verified by a dependency lock;
- which graph edges affect compilation and invalidation; and
- which changes preserve semantic identity.

Without a public contract, common implementation conveniences can silently become language semantics. Examples include:

- searching parent directories for a manifest;
- interpreting folders as namespaces;
- accepting whichever package version a registry returns first;
- making transitive dependencies importable;
- merging equal namespace paths from unrelated packages;
- using filesystem enumeration as source order;
- treating a symlinked file as two compilation units;
- allowing module or package cycles because they appear type-only;
- changing package identity whenever its version changes; or
- using a random cache identifier as persistent semantic identity.

Those behaviors conflict with the Approved Project Constitution, RFC-0000, and RFC-0001B. This RFC establishes a bounded, explicit, and traceable build graph before the Type System and reference compiler spike depend on it.

## 3. Goals

This RFC is intended to provide:

- one explicit Project boundary for each compilation;
- stable Package Identity independent of version, content digest, and source location;
- one exact resolved Package Revision per Package Identity in a Project;
- explicit Package Manifests, Module declarations, and direct dependencies;
- deterministic and portable source discovery;
- one Compilation Unit identity for every compiled `.plant` file;
- explicit module and package dependency DAGs;
- direct-dependency aliases for deterministic cross-package imports;
- private-by-default top-level visibility and explicit public exports;
- no implicit re-export or transitive dependency visibility;
- a mandatory dependency lock for reproducible and production builds;
- content-integrity verification for resolved packages;
- deterministic graph ordering and cycle diagnostics;
- public-surface and implementation fingerprints for incremental compilation;
- bounded package, module, source, graph, and archive processing; and
- traceability from manifests and package artifacts to semantic declarations.

## 4. Non-Goals

This RFC does not define:

- a public package registry service or network protocol;
- registry account, organization, or authority-ownership procedures;
- a general dependency constraint solver;
- non-exact version ranges in language version `0.1`;
- side-by-side revisions of one Package Identity;
- multi-root Projects or monorepo workspace orchestration;
- dependency patching, replacement, or override mechanisms;
- conditional, target-specific, optional, or feature-selected dependencies;
- generated source participation in the foundational source set;
- precompiled semantic-interface or binary package formats;
- runtime module initialization or global mutable module state;
- type-only, expression, execution, state-machine, or target dependency cycles;
- member-level visibility inside a Definition;
- Application Assembly or Deployment selection by a Project;
- target profiles, hardware mapping, or artifact emission;
- package signing infrastructure or certification claims;
- standard-library contents; or
- internal parser, object-model, or cache serialization choices.

Public Project Manifest, Package Manifest, and Dependency Lock serialization belongs to RFC-0001D. This RFC owns the semantic document model and cross-document build rules; RFC-0001D owns filenames, encoding, exact fields, duplicate handling, source spans, canonical serialization, and format migration.

## 5. Terminology

This RFC uses terms from the [IndustrialMDE Glossary](../Glossary.md).

- **Project** — one explicit build and orchestration boundary selecting one root Package Revision and, for a locked build, one explicit Dependency Lock.
- **Project Manifest** — versioned build input that identifies the root Package Manifest, lock, language constraints, and project-level build configuration.
- **Package Identity** — stable structured logical identity consisting of Package Authority and Package Name.
- **Package Authority** — lowercase ASCII ownership coordinate used as part of Package Identity.
- **Package Name** — lowercase ASCII package label scoped by one Package Authority.
- **Package Version** — exact three-part release revision in the foundational contract.
- **Package Content Identity** — tagged, algorithm-qualified cryptographic digest of either one immutable package artifact or one immutable root-workspace content snapshot.
- **Workspace Content Fingerprint** — the `workspace-snapshot` Package Content Identity computed from root-package-owned manifest, path, and source bytes after those inputs are snapshotted for one compilation.
- **Package Revision** — exact tuple of Package Identity, Package Version, and Package Content Identity.
- **Package Manifest** — versioned declarative description of one package revision's modules, source roots, language constraints, and direct dependencies.
- **Library** — a package published for reuse; not a global semantic container or distinct kernel entity.
- **Module** — named package-owned grouping that defines source ownership, declared module dependencies, visibility, export eligibility, and an incremental-compilation boundary.
- **Source Root** — explicit portable package-relative directory recursively contributing `.plant` files to exactly one Module.
- **Portable Package Path** — normalized ASCII package-relative path using `/` separators and no filesystem-dependent segments.
- **Compilation Unit** — one `.plant` source file with one Package owner, one Module owner, one Portable Package Path, and one explicit language version.
- **Dependency Declaration** — package-manifest entry naming one direct dependency alias, Package Identity, and exact required Package Version.
- **Dependency Alias** — source-visible manifest identifier used as the first segment of a cross-package import target.
- **Dependency Lock** — immutable build input resolving the complete package graph to exact Package Revisions, origins, digests, and edges.
- **Export Surface** — public declarations owned by exported Modules of one Package.
- **Public Semantic API Fingerprint** — deterministic digest of the resolved Export Surface under a versioned semantic-fingerprint schema.
- **Implementation Fingerprint** — deterministic digest of all compilation inputs relevant to a Module or Package implementation.

A Package Identity is not a Package Revision. A Module is not a Namespace. A Compilation Unit is not a semantic declaration. A Dependency Alias is not part of the target Package Identity.

## 6. Normative Specification

### 6.1 Foundational Ownership Model

The foundational build model is:

```text
Project
├── Project Manifest
├── root Package Revision
│   ├── Package Manifest
│   └── one or more Modules
│       ├── one or more Source Roots
│       └── zero or more Compilation Units
├── zero or more resolved dependency Package Revisions
└── zero or one Dependency Lock
```

Each semantically compiled source file MUST have exactly one owner at every required level:

```text
Project
→ Package Revision
→ Module
→ Compilation Unit
→ Namespace contribution
→ semantic declarations
```

Ownership MUST be established before name resolution. An implementation MUST NOT infer a missing owner from an import, a semantic declaration, a target configuration, or a neighboring file.

Project, Package Revision, Module, Compilation Unit, Namespace, and semantic owner paths MUST remain distinct in compiler representations. An implementation MAY use compact internal indexes, but it MUST preserve enough information to reconstruct each boundary and its source of authority.

### 6.2 Project

A Project is a build and orchestration boundary. It is not:

- a Definition;
- an Application Assembly;
- an Industrial Profile role;
- a Namespace;
- a Package Identity; or
- a runtime object.

One language version `0.1` Project MUST select exactly one root Package Manifest. Multi-root Projects require a later RFC revision.

Compilation MUST begin from an explicitly supplied Project Manifest. A compiler MUST NOT search the current directory, parent directories, user home, environment-specific workspace metadata, or registry configuration to select a Project Manifest implicitly.

The explicitly supplied Project Manifest entry MUST be a regular non-link file. It MUST NOT itself be a symbolic link, junction, reparse point, or archive link entry.

For a local root package:

- the Project root is the directory containing the explicitly supplied Project Manifest;
- the root Package Manifest path is resolved relative to that Project root;
- the root package root is the directory containing the selected Package Manifest; and
- neither physical root enters Package Identity or semantic identity.

The resolved root Package Manifest, Dependency Lock when present, every immutable dependency Package Manifest, and every participating source path MUST remain below their declared physical roots without link or parent-traversal escape. A selected build document MUST be a regular non-link file, and no relative path component below its declared root may be a symbolic link, junction, reparse point, or archive link entry.

The Project Manifest MUST identify:

| Field | Requirement |
| --- | --- |
| manifest schema version | Required |
| root Package Manifest | Required portable path |
| Dependency Lock | Required for reproducible or production compilation |
| language version | Required exact version |
| project configuration identity | Required when configuration changes semantic or generated results |

A language version `0.1` Project Manifest selects exactly one effective language version for the complete Project. It MUST NOT replace, synthesize, or silently override the `dsl` directive required in each source file by RFC-0001. Every participating directive must agree with the selected version under section 6.16.

Project names, workspace display names, checkout directories, and CI job names MUST NOT enter Package Identity or semantic identity unless a later Accepted RFC explicitly makes one a structured identity input.

### 6.3 Declarative Manifest Contract

Project Manifests, Package Manifests, and Dependency Locks are declarative data. They MUST NOT contain or trigger:

- executable scripts;
- shell commands;
- arbitrary code evaluation;
- environment-variable interpolation;
- current-time or random-value expansion;
- network queries during semantic interpretation;
- conditional inclusion based on host operating system; or
- plugin callbacks that can change manifest meaning.

Each document MUST declare an explicit schema version. Duplicate fields are invalid. Unknown fields that could affect build meaning MUST NOT be silently ignored.

Field ordering MUST NOT change semantics. Where a field represents a set or map, its semantic interpretation is unordered and its canonical processing order is defined by section 7.

RFC-0001D owns the public schema `0.1` serialization and MUST:

- preserve exact string and integer values;
- detect duplicate keys before map construction;
- define encoding and newline handling;
- define schema-version representation;
- reject non-finite or otherwise unsupported numeric values;
- avoid executable interpolation;
- define unknown-field and extension behavior; and
- support deterministic diagnostics with document spans.

An implementation claiming public manifest or lock conformance MUST conform to a compatible Accepted serialization RFC. The semantic model in this RFC does not authorize an alternative public encoding.

An experimental implementation MAY use a temporary encoding only when it identifies that encoding as non-conforming and does not publish it as the stable manifest contract.

### 6.4 Package Identity, Version, Content Identity, and Revision

#### 6.4.1 Package Authority

A Package Authority is one or more lowercase ASCII labels separated by dots. Each label MUST match:

```regex
^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$
```

Examples:

```text
org.industrialmde
com.acme.automation
```

Empty labels, uppercase letters, underscores, leading or trailing hyphens, consecutive dots, and Unicode characters are prohibited.

The language contract does not prove ownership of an authority. Registry policy, provenance, and signature systems MAY verify ownership separately.

#### 6.4.2 Package Name

A Package Name is one lowercase ASCII label matching the Package Authority label grammar.

Examples:

```text
motor-library
water-treatment
```

Package Name is not an RFC-0001 source identifier and does not participate directly in a Namespace Path.

#### 6.4.3 Package Identity

Package Identity is the structured tuple:

```text
(Package Authority labels, Package Name)
```

It MUST be stored and compared as structured components rather than as an escaped concatenated string.

Package Identity excludes:

- Package Version;
- content digest;
- dependency alias;
- registry URL;
- download URL;
- checkout path;
- source-control revision;
- Project name; and
- Module names.

Changing Package Authority or Package Name changes Package Identity. Moving an unchanged package artifact between registries does not.

#### 6.4.4 Package Version

Language version `0.1` Package Version is exactly:

```text
Major "." Minor "." Patch
```

Each component is a decimal integer from `0` through `2147483647`. A component has no leading zero unless the value is exactly `0`.

Examples:

```text
0.1.0
1.0.0
12.34.56
```

Prerelease identifiers, build metadata, ranges, wildcards, and implicit latest-version selection are not supported by the foundational contract.

Package Version participates in package-revision and compatibility checks but not in Package Identity or RFC-0001B Canonical Declaration Identity.

#### 6.4.5 Package Content Identity

A Package Content Identity is the tagged tuple:

```text
(Content Kind, Digest Algorithm, Digest Bytes)
```

The foundational Content Kinds are:

| Content Kind | Meaning |
| --- | --- |
| `immutable-artifact` | Exact immutable dependency package artifact bytes |
| `workspace-snapshot` | Exact root-package-owned inputs snapshotted for one compilation |

The foundational digest algorithm is `sha256`.

For `immutable-artifact`, the digest is computed over the exact package artifact bytes supplied by the distribution system.

For `workspace-snapshot`, the Workspace Content Fingerprint MUST use a versioned, length-delimited encoding of:

- exact root Package Manifest bytes;
- every participating root-package Portable Package Path;
- the exact source bytes at each participating path; and
- any additional package-owned input explicitly assigned by a later public contract.

The Workspace Content Fingerprint MUST NOT include the Project Manifest, Dependency Lock, project configuration, dependency artifacts, compiler version, or active resource limits. Those are separate Project Resolution Fingerprint inputs. This exclusion prevents a lock from becoming a self-referential hash input.

All root workspace inputs MUST be snapshotted before the fingerprint is published. A participating path or byte sequence that changes during compilation produces `IMDE4015`; the compiler MUST NOT combine bytes from different workspace states.

A content digest does not prove publisher identity, review status, or safety. It proves only equality to the identified bytes under the selected algorithm and Content Kind.

#### 6.4.6 Package Revision

A Package Revision is:

```text
(Package Identity, Package Version, Package Content Identity)
```

Exactly one Package Revision for a given Package Identity MAY participate in one Project. If two dependency paths require different versions or content identities for the same Package Identity, resolution fails.

This single-revision rule prevents one logical namespace identity from splitting into incompatible package instances inside the same semantic graph.

### 6.5 Package Manifest

Every root or dependency package MUST have exactly one Package Manifest for the selected Package Revision.

The Package Manifest MUST declare:

| Field | Requirement |
| --- | --- |
| manifest schema version | Required |
| Package Authority | Required |
| Package Name | Required |
| Package Version | Required |
| language version | Required exact version |
| Modules | Required non-empty set |
| direct Dependency Declarations | Required, possibly empty |

The Package Manifest is part of the package content represented by Package Content Identity.

Package Manifest meaning MUST NOT depend on:

- its physical filename beyond the Project or package-tool selection contract;
- field order;
- source-directory enumeration order;
- host path separators;
- current working directory;
- user-specific package caches; or
- undeclared registry defaults.

An immutable dependency package's manifest MUST agree with the Package Identity, Package Version, and digest recorded in the Dependency Lock. A mismatch is an integrity error, not a warning.

The root package manifest MAY describe unpublished application source. It still has a Package Identity and Package Version so that its semantic identities and compatibility surface are explicit.

Source Roots in a local root package are resolved relative to the root package root. Source Roots in an immutable dependency package are resolved relative to that artifact's isolated extraction root. The physical root is a resolution boundary and not a semantic identity component.

### 6.6 Library

A Library is a Package intended to expose reusable declarations. It is not:

- a global child of Project;
- a semantic owner above Package;
- a second dependency mechanism;
- an implicitly available standard library; or
- a reason to bypass the Dependency Lock.

Library publication intent MAY later be recorded as package metadata. It does not change Package Identity, Module semantics, Namespace identity, or import resolution.

Project source accesses a Library through an explicit direct Dependency Declaration and explicit source imports.

### 6.7 Module

Every Package Manifest MUST declare one or more Modules.

A Module has:

| Property | Requirement |
| --- | --- |
| Module Name | Required RFC-0001 Identifier |
| exposure | Required: `exported` or `internal` |
| Source Roots | Required non-empty set |
| direct module dependencies | Required, possibly empty |

Module names SHOULD follow `PascalCase`. A convention violation produces a Warning and does not change Module identity.

Module Identity is:

```text
(Package Identity, Module Name)
```

A Module:

- owns Compilation Units for source discovery and diagnostics;
- defines one private visibility boundary;
- declares direct access to other Modules in the same Package;
- contributes an incremental-compilation boundary; and
- may be eligible to expose public declarations when marked `exported`.

A Module is not a Namespace and MUST NOT add a segment to Namespace Path or Canonical Declaration Identity.

Moving a declaration between Modules without changing Package Identity, Namespace Path, semantic owner path, spelling, or kind preserves its Canonical Declaration Identity. The move MAY still change visibility, dependency legality, cache invalidation, and compatibility.

Module declarations MUST be unique by exact spelling and ASCII Case-Folded Key within one Package.

The direct module dependency graph MUST be acyclic. A Module MUST NOT depend on itself. Direct module dependencies do not become transitively source-visible.

Modules have no runtime initialization, static constructor, or mutable global state under this RFC.

### 6.8 Portable Package Paths and Source Discovery

#### 6.8.1 Portable Package Path

A Portable Package Path is a non-empty sequence of ASCII path segments separated by `/`.

Each segment MUST match:

```regex
^[A-Za-z0-9_](?:[A-Za-z0-9._-]*[A-Za-z0-9_])?$
```

A Portable Package Path:

- is relative to the package root;
- MUST NOT begin or end with `/`;
- MUST NOT contain an empty segment;
- MUST NOT contain `.` or `..` segments;
- MUST NOT contain `\`, a drive prefix, a URI scheme, NUL, or Unicode;
- MUST NOT resolve outside the package root; and
- is compared by exact ASCII bytes.

For portability to Windows filesystem APIs, the ASCII-case-folded stem before the first `.` in every segment MUST NOT be one of:

```text
CON PRN AUX NUL
COM1 COM2 COM3 COM4 COM5 COM6 COM7 COM8 COM9
LPT1 LPT2 LPT3 LPT4 LPT5 LPT6 LPT7 LPT8 LPT9
```

The prohibition applies with or without an extension. For example, `CON`, `con.txt`, and `Lpt1.plant` are invalid Portable Package Path segments.

Two participating package paths MUST NOT differ only by ASCII case. This is rejected before source parsing so the source set is portable across case-sensitive and case-insensitive filesystems.

Host-native paths MUST be converted to Portable Package Paths before they become build inputs. Host path normalization MUST NOT change a package-relative spelling silently.

#### 6.8.2 Source Root

Each Module declares one or more Source Roots as Portable Package Paths.

A Source Root contributes every regular file below it whose final path segment ends with the exact lowercase suffix `.plant`.

Source discovery:

1. validates all declared Source Roots;
2. recursively enumerates candidate regular files;
3. rejects symbolic links, junctions, reparse points, and archive link entries in a participating source path;
4. converts candidates to Portable Package Paths;
5. rejects exact and ASCII case-folded path collisions;
6. assigns every candidate to exactly one Module; and
7. orders the resulting Compilation Units by exact Portable Package Path.

Filesystem enumeration order has no semantic meaning.

Every Source Root MUST exist as a directory at source-discovery time.

No two Source Roots in one Package MAY overlap or nest, even when they belong to the same Module. A `.plant` file MUST NOT be owned by more than one Module.

Files not ending in exact lowercase `.plant` are not Compilation Units. Their presence does not affect source discovery unless another declared build input explicitly owns them.

Generated source directories, editor backups, hidden filesystem state, source-control metadata, and undeclared include paths MUST NOT enter the source set.

### 6.9 Compilation Unit

In language version `0.1`, one Compilation Unit is exactly one participating `.plant` source file.

Compilation Unit Identity is:

```text
(Package Identity, Module Name, Portable Package Path)
```

Compilation Unit Identity is a build and incremental-compilation identity. It is not a semantic declaration identity.

Every Compilation Unit MUST:

- belong to exactly one Package Revision;
- belong to exactly one Module;
- have exactly one Portable Package Path;
- satisfy RFC-0001 source encoding and resource limits;
- contain its own explicit `dsl` directive;
- contain exactly one Namespace Directive when semantically compiled under RFC-0001B; and
- contribute declarations only to its declared Namespace in its owning Package.

Changing a Portable Package Path changes Compilation Unit Identity and its source cache key. It does not by itself change semantic declaration identity when Package Identity, Namespace Path, semantic owner path, spelling, and kind remain unchanged.

Combining several source files into one Compilation Unit, splitting one file into implicit fragments, textual inclusion, and preprocessor-generated units are not supported.

Compilation Unit discovery order and declaration order MUST NOT select a duplicate, resolve an ambiguity, or establish Package or Module dependencies.

### 6.10 Direct Package Dependencies

Every package dependency MUST be declared directly in the consuming Package Manifest.

A Dependency Declaration contains:

```text
(Dependency Alias, required Package Identity, exact required Package Version)
```

Dependency Alias MUST satisfy the RFC-0001 Identifier grammar and SHOULD use `PascalCase`.

Within one consuming Package, Dependency Aliases MUST be unique by exact spelling and ASCII Case-Folded Key. A Package Identity MUST NOT appear under more than one Dependency Alias.

A package MUST NOT declare itself as a dependency.

Language version `0.1` does not support:

- version ranges;
- optional dependencies;
- target-conditioned dependencies;
- feature-selected dependencies;
- dependency replacement;
- dependency patching;
- registry fallback;
- implicit standard-library dependencies; or
- dependencies synthesized from source imports.

An Import Directive does not add a Dependency Declaration. A missing direct dependency is an error even when an identically named package exists in a transitive graph, global cache, registry, or neighboring checkout.

### 6.11 Dependency Lock

A reproducible or production compilation MUST use a Dependency Lock.

The lock MUST record:

- lock schema version;
- root Package Identity and Package Version;
- every resolved immutable dependency Package Revision;
- exact Package Content Identity;
- origin or retrieval locator as provenance data;
- each consuming-package to direct-dependency edge;
- each Dependency Alias;
- the manifest digest for every immutable dependency package; and
- enough data to reconstruct one deterministic resolved dependency graph.

The lock MUST contain exactly one immutable dependency Package Revision per Package Identity and MUST NOT repeat the root Package Identity as a locked dependency package.

Every locked Package Revision MUST be reachable from the root Package through locked direct-dependency edges. Unreachable package entries and edges are stale lock data and are invalid. The root Workspace Content Fingerprint is computed from the immutable compilation snapshot and is not stored in the Dependency Lock.

Normal compilation treats the Dependency Lock as immutable input. It MUST NOT:

- select a newer version;
- rewrite an origin;
- refresh a digest;
- add a missing transitive package;
- repair an alias;
- or otherwise mutate the lock.

Creating or updating a lock is a separate explicit package-management operation. That operation is not itself a reproducible compilation and MUST report every changed Package Revision, digest, origin, and edge before the resulting lock is used.

Before semantic compilation, the package resolver MUST verify that:

- every manifest dependency has one matching locked edge;
- every locked edge corresponds to a manifest dependency;
- Package Identity and exact Package Version agree;
- package artifact bytes match the locked digest;
- package manifest bytes match their locked manifest digest; and
- no extra unresolved package revision participates in the graph.

A cache hit does not replace digest verification under a production profile.

### 6.12 Deterministic Package Resolution

Given a Project Manifest, root Package Manifest, Dependency Lock, and locally available immutable package artifacts, resolution proceeds as follows:

1. validate document schema versions and structural limits;
2. validate the root Package Identity and Package Version;
3. load each locked Package Revision by exact Package Identity;
4. verify artifact and manifest digests;
5. compare every Package Manifest Dependency Declaration with the locked edge;
6. reject multiple revisions of one Package Identity;
7. construct the complete package dependency graph;
8. reject cycles;
9. validate each package's Modules and module graph;
10. discover and assign Compilation Units;
11. construct direct-dependency alias environments; and
12. publish an immutable Resolved Project Graph.

No step uses registry ordering, cache enumeration, current time, network search, or an unlocked latest-version rule.

If an exact locked artifact is unavailable, normal compilation fails with a non-source diagnostic. Fetching the exact digest MAY be offered as a separate explicit operation.

Fresh dependency selection without a lock is a package-management operation. A compiler MAY support it in a development profile, but it MUST identify the build as unlocked and non-reproducible and MUST NOT report production compilation success.

### 6.13 Package and Module Dependency Graphs

The Package Dependency Graph has one node per Package Identity and one directed edge from a consuming Package to each direct dependency.

The Module Dependency Graph of one Package has one node per Module and one directed edge from a consuming Module to each directly required Module.

Both graphs MUST be directed acyclic graphs.

Cycles are prohibited even when:

- every source reference appears type-only;
- no runtime initialization exists;
- source files could be parsed in an arbitrary order; or
- an implementation could break the cycle through a multi-pass algorithm.

This rule establishes a bounded public dependency model. A future RFC may propose a narrower cycle capability only with deterministic interface construction, invalidation, diagnostics, and compatibility rules.

Source imports target semantic declarations or namespaces, not files. This RFC does not create a file-import graph.

Cycles inside later semantic graphs, including Definition expansion, types, constants, expressions, behavior, connections, and state machines, remain governed by their owning RFCs.

For deterministic cycle diagnostics, the compiler MUST:

- compute strongly connected components;
- order components by their smallest canonical node key;
- order nodes inside a component by canonical node key; and
- report the directed edges and manifest spans that prove the cycle.

### 6.14 Dependency Aliases and Import Roots

Each Package has one Import Root Domain used only while resolving Import Directive targets.

The Import Root Domain contains:

- every root Namespace segment owned by the current Package; and
- every direct Dependency Alias declared by the current Package.

These bindings MUST be unique by exact spelling and ASCII Case-Folded Key. A Dependency Alias that collides with a current-package root Namespace segment is invalid.

In language version `0.1`, the Package root contains only root Namespace segments for semantic name resolution. Package-level semantic declarations outside a non-empty Namespace are prohibited. Dependency Aliases remain separate manifest bindings in the Import Root Domain and are not Namespace contributions.

An import target is resolved left to right without backtracking:

1. if its first segment is a direct Dependency Alias, resolution enters that dependency's Export Surface;
2. otherwise, the first segment is resolved as a root Namespace segment of the current Package; and
3. failure after the first segment MUST NOT cause reinterpretation through another Package or binding.

Conceptual examples:

```plant
// Same-package import.
import Common.Local.Valve;

// Cross-package import through direct dependency alias Motors.
import Motors.Common.Motors.MotorVfd;
```

Dependency Alias is not inserted into the ordinary unqualified symbol environment. It is valid only as the first segment of an Import Directive target.

The alias is not part of the imported declaration's Canonical Identity Key. Renaming an alias changes consuming source and import fingerprints but not the target declaration identity.

Transitive dependency aliases are not present. A package that needs a transitive package MUST declare its own direct dependency and alias.

### 6.15 Visibility, Module Access, and Package Export

RFC-0001 reserved `public` and `private`. This RFC assigns them to top-level semantic declarations:

```text
VisibilityModifier ::= "public" | "private"
```

The exact placement relative to each declaration keyword is finalized by the declaration and grammar RFCs. The semantic rule is:

- an explicitly `public` top-level declaration has Public visibility;
- an explicitly `private` top-level declaration has Private visibility; and
- a top-level declaration with no modifier has Private visibility.

Private-by-default is a stable safety rule, not an implementation default.

Accessibility is:

| Target declaration | Required access |
| --- | --- |
| Private declaration in current Module | Accessible |
| Private declaration in another Module | Inaccessible |
| Public declaration in current Module | Accessible |
| Public declaration in another Module of the same Package | Direct Module dependency required |
| Public declaration in a direct dependency Package | Owning Module MUST be `exported`; direct Package dependency and explicit source import required |
| Any declaration in a transitive-only dependency | Inaccessible |

An `internal` Module cannot contribute declarations to the Package Export Surface, even when a declaration is marked `public`.

An `exported` Module contributes its Public top-level declarations to the Package Export Surface. Private declarations never enter the Export Surface.

Visibility does not alter collision domains. Exact and ASCII case-folded duplicate checks still apply across all source files and Modules contributing to one logical Namespace in one Package.

Public import, alias export, wildcard export, and dependency re-export are prohibited in language version `0.1`. A Package Export Surface contains only declarations owned by that Package.

Member visibility inside Definitions and public signature closure remain delegated to RFC-0002 and RFC-0006. A Package MUST NOT be considered fully export-conformant until every entity kind in its Public Semantic API has a defined public-signature contract.

An import cannot bypass Module or Package visibility. An inaccessible exact match produces a visibility diagnostic rather than an unresolved-name success.

### 6.16 Language-Version and Prelude Constraints

Every Compilation Unit retains the effective language version declared by its own `dsl` directive.

In foundational language version `0.1`:

- the Project Manifest MUST select exactly one language version;
- every Package Manifest MUST declare exactly that language version;
- every participating Compilation Unit `dsl` directive MUST declare exactly that language version;
- the compiler MUST explicitly declare support for that exact language version; and
- a Project containing more than one effective language version is invalid.

Manifests MUST NOT rewrite or infer a Compilation Unit's language version. Mixed-version linking requires a later RFC that defines grammar, type, identity, public-signature, and compatibility behavior across versions.

Language version `0.1` has no implicit package, namespace, or ordinary-symbol prelude. A compiler MUST NOT synthesize a hidden Package, dependency, Namespace contribution, Import Environment binding, or standard-library declaration.

RFC-0002 MAY define intrinsic type entities such as `BOOL`, `INT`, `REAL`, and `TIME`. Such entities are language-owned type constructs rather than Package declarations or implicit imports, and their exact syntax, collision behavior, and type-context resolution belong to RFC-0002. A future Standard Library remains an explicit dependency and import unless a later Accepted language-version contract states otherwise.

### 6.17 Resource Bounds

Compilers and package tools MUST bound at least:

- manifest and lock byte size;
- manifest nesting and collection sizes;
- Package Authority label count and length;
- Portable Package Path segment count and total length;
- Modules per Package;
- Source Roots per Module;
- Compilation Units per Module and Project;
- direct dependencies per Package;
- direct module dependencies per Module;
- total resolved Packages and dependency edges;
- package and module graph depth;
- package artifact byte size;
- archive entry count and extracted byte size;
- cycle diagnostic node and edge count; and
- fingerprint input size.

Active limits are deterministic build inputs. Exceeding a limit produces `IMDE4016` and MUST NOT publish a partial Resolved Project Graph or partial Semantic Model.

Required minimum production values remain owned by the compiler conformance specification. A reference spike MAY use smaller declared limits only when it identifies itself as non-conforming.

### 6.18 Diagnostic Expectations

The following diagnostic codes are reserved by this Proposed specification and may be refined before acceptance.

When a compatible serialization RFC applies, its encoding, JSON syntax, closed-schema, value-kind, and serialized field-grammar diagnostics take precedence. The compiler MUST NOT also emit an RFC-0001C diagnostic for the same serialization fact. The codes below govern missing build inputs, selection failures, filesystem validation, and semantic or cross-document validation after the required fields have been parsed.

| Code | Severity | Condition | Required facts |
| --- | --- | --- | --- |
| `IMDE4001` | Error | Missing or unavailable Project Manifest, implicit discovery attempt, or invalid Project selection after schema validation | Explicit requested origin and failure reason |
| `IMDE4002` | Error | Package Identity or Package Version violates a semantic or cross-document rule after field parsing | Invalid component, value, and governing rule |
| `IMDE4003` | Error | Package Manifest or Module declaration violates a semantic rule after schema validation | Package identity, field, and manifest span |
| `IMDE4004` | Error | Missing, stale, extra, or inconsistent Dependency Lock entry | Consumer, alias, expected requirement, and locked facts |
| `IMDE4005` | Error | Package artifact or manifest digest mismatch | Package Revision, algorithm, expected digest, and observed digest |
| `IMDE4006` | Error | More than one Package Revision for one Package Identity | Identity, revisions, and dependency paths |
| `IMDE4007` | Error | Package dependency cycle | Ordered component nodes, directed edges, and manifest spans |
| `IMDE4008` | Error | Module dependency cycle or invalid module edge | Package, ordered Modules, directed edges, and spans |
| `IMDE4009` | Error | Invalid, escaping, linked, colliding, overlapping, or multiply owned participating build-document or source path | Document role or Package and Module, path, and conflicting origin |
| `IMDE4010` | Error | Compilation Unit has no owner or inconsistent owner metadata | Path and candidate Package or Module owners |
| `IMDE4011` | Error | Unknown, duplicate, or colliding Dependency Alias | Consumer Package, exact aliases, folded keys, and spans |
| `IMDE4012` | Error | Undeclared, transitive-only, or self dependency access | Consumer, requested package or alias, and available direct dependencies |
| `IMDE4013` | Error | Declaration is inaccessible through Module or Package visibility | Target identity, visibility, owning Module, and required direct edge |
| `IMDE4014` | Error | Language version violates Project, Package, single-version, or compiler constraints | Unit path, declared version, and applicable constraints |
| `IMDE4015` | Error | Package content, manifest, or source set differs from its resolved build input | Package Revision and changed input identity |
| `IMDE4016` | Error | Manifest, package, source, graph, archive, or fingerprint resource limit exceeded | Active limit, observed count, and affected origin |
| `IMDE4017` | Error | Reproducible or production compilation attempted without an exact lock | Project origin and required explicit package operation |
| `IMDE4018` | Warning | Package, Module, or Dependency Alias naming convention violation | Spelling and expected convention |

Manifest and lock diagnostics use an explicit non-source origin when the final serialization cannot provide a source span. Once the serialization defines spans, the primary span MUST identify the relevant field or entry.

Diagnostics MUST follow the deterministic ordering contract in section 7. A fix-it is optional. A compiler MUST NOT silently edit a manifest, regenerate a lock, rename an alias, change visibility, or move a source file.

## 7. Determinism and Ordering

### 7.1 Complete Build Inputs

For the concerns owned by this RFC, deterministic resolution depends on:

- Project Manifest bytes and schema version;
- root Package Manifest bytes;
- Dependency Lock bytes and schema version;
- every resolved immutable package artifact;
- root workspace source paths and bytes;
- every Package Manifest;
- exact Project and Package language version;
- active resource limits;
- compiler version and supported manifest schemas; and
- package-tool configuration explicitly declared as a build input.

Changing any listed input changes the reproducibility envelope even when the final Semantic Model happens to remain equivalent.

### 7.2 Canonical Ordering Keys

Canonical ordering uses structured keys:

| Entity | Canonical ordering key |
| --- | --- |
| Package Identity | Package Authority labels, then Package Name, by exact ASCII bytes |
| Package Revision | Package Identity, Package Version components, Content Kind, digest algorithm, digest bytes |
| Module | Package Identity, then Module Name by exact ASCII bytes |
| Compilation Unit | Package Identity, Module Name, Portable Package Path by exact ASCII bytes |
| Dependency edge | consumer Package Identity, Dependency Alias, target Package Identity |
| Module edge | consumer Module Identity, target Module Identity |
| Manifest or lock diagnostic | validation layer, document role, expected or declared Package Identity when applicable, Package Content Identity fallback, stable portable path or non-file origin, primary raw span, diagnostic code, field path |

The public Package and Module graphs store edges as `consumer → dependency`.

Dependency-first processing MUST therefore use reverse topological scheduling:

1. count each node's remaining outgoing dependency edges;
2. place every node with zero remaining dependencies in a ready set;
3. select the ready node with the smallest applicable canonical ordering key;
4. after processing that node, remove each incoming edge from a consumer and update that consumer's remaining dependency count; and
5. continue until every node is processed or a previously diagnosed cycle prevents completion.

Consumer-first presentation order, when needed, is the reverse of this dependency-first order. An implementation MUST NOT interpret `consumer → dependency` as authorization to compile a consumer before its required dependency.

Filesystem enumeration order, manifest field order, lock entry order, cache order, registry result order, hash-map iteration, concurrency, locale, and host path rules MUST NOT change the Resolved Project Graph.

### 7.3 Canonical Graph Diagnostics

Strongly connected components are ordered by their smallest canonical node key. Nodes and reported edges inside a component are ordered by canonical key.

If resource limits prevent reporting every edge, the diagnostic MUST report a deterministic bounded prefix and the omitted count.

### 7.4 Content and Fingerprint Algorithms

Immutable dependency Package Content Identity uses the algorithm recorded in the lock. Root Workspace Content Identity uses the algorithm and `workspace-snapshot` domain defined by the applicable fingerprint schema. The foundational algorithm is `sha256`.

Compiler fingerprints MUST use:

- a registered algorithm identifier;
- a versioned, length-delimited canonical encoding;
- structured fields rather than delimiter-concatenated strings; and
- canonical ordering for sets and maps.

Random UUIDs, object memory addresses, absolute checkout paths, file timestamps, inode numbers, and cache insertion order MUST NOT enter a persistent identity or fingerprint.

The Project Resolution Fingerprint MUST combine, through a versioned length-delimited encoding:

- Project Manifest exact bytes and schema version;
- root Workspace Content Fingerprint;
- Dependency Lock exact bytes and schema version when present;
- every immutable dependency Package Revision;
- exact project configuration identity when applicable;
- compiler semantic version and selected exact language version;
- active resource limits; and
- every other declared build input that can change the Resolved Project Graph.

The Project Resolution Fingerprint is computed outside the Dependency Lock. Neither value contains itself directly or indirectly.

This RFC standardizes fingerprint inputs, domains, and required properties, but not the final public byte encoding. Until a compatible Accepted fingerprint specification registers that encoding, an implementation MUST NOT describe its concrete Workspace Content, Project Resolution, implementation, or public-API fingerprint bytes as interoperable IndustrialMDE fingerprints.

## 8. Compatibility and Migration

### 8.1 Package Identity and Revision

Changing Package Authority or Package Name changes every semantic identity owned by that Package.

Changing only Package Version or Package Content Identity changes Package Revision and resolution fingerprints but does not by itself change Canonical Declaration Identity. This permits compatible package upgrades to preserve source and traceability identities.

An upgrade is not automatically compatible. Its Export Surface, behavior, resource requirements, target capabilities, and migration contract still require compatibility analysis.

### 8.2 Source Relocation

Moving a source file changes Compilation Unit Identity and source cache keys.

The move preserves semantic declaration identity only when Package Identity, Namespace Path, semantic owner path, spelling, and semantic entity kind remain unchanged.

Moving a file to another Module preserves Canonical Declaration Identity under the same rule but MAY change visibility and legal dependency edges. Tooling MUST perform impact analysis.

### 8.3 Module Evolution

Renaming a Module changes Module Identity and every Compilation Unit Identity owned by it. It does not automatically change semantic declaration identities.

Changing a Module from `internal` to `exported` may add public API. Changing from `exported` to `internal` is a breaking package change when consumers use its declarations.

Adding or removing a direct module dependency changes accessibility and invalidation behavior and MUST be treated as a compatibility-sensitive manifest change.

### 8.4 Dependency Alias Evolution

Renaming a Dependency Alias requires source migration in the consuming Package but does not change the target Package Identity or target declaration identities.

Adding a direct dependency may create an Import Root Domain collision with an existing root Namespace segment or alias. Such a change is not source-compatible until the collision is resolved explicitly.

### 8.5 Lock Evolution

Lock changes are explicit build-input changes. Tooling MUST present Package Revision, digest, origin, and graph-edge changes.

Normal compilation MUST NOT hide a lock update inside a successful build.

### 8.6 Manifest Schema Evolution

Manifest and lock schema versions follow managed compatibility. A compiler MUST reject an unsupported schema rather than guess its meaning.

A migration tool MAY rewrite a document only through an explicit user-selected command and SHOULD preserve presentation data when the selected serialization supports it. Schema `0.1` RFC-0001D JSON does not support comments.

## 9. Safety and Security Considerations

Project Manifests, Package Manifests, Dependency Locks, package artifacts, archives, paths, and imported metadata are untrusted input.

Implementations MUST:

- enforce declared byte, count, depth, and graph limits;
- reject absolute paths and parent traversal;
- reject build-document and source symlinks, junctions, reparse points, and archive links in participating paths;
- prevent archive writes outside an isolated extraction root;
- verify locked artifact and manifest digests;
- reject duplicate Package Identities and multiple revisions;
- avoid executing manifest or package scripts;
- avoid implicit credential, environment, or registry lookup during semantic interpretation;
- bound diagnostic amplification from large dependency cycles;
- avoid exposing inaccessible dependency contents across a tooling trust boundary; and
- preserve provenance facts in the build and artifact manifests.

Exact hashes do not establish package trust. A malicious package can have a valid locked digest. Publisher verification, signature verification, allowlists, code review, and registry trust remain separate controls.

Package Authority syntax does not establish legal or organizational ownership. A distribution system SHOULD validate authority ownership and MAY require signatures or provenance attestations.

This RFC does not prove process safety, generated-code safety, package correctness, or certification suitability.

## 10. Tooling and Incremental Compilation

### 10.1 Required Project Graph Records

Tooling MUST retain:

- Project Manifest identity and schema version;
- Package Identity and Package Revision;
- manifest and lock origins;
- Module Identity and exposure;
- Portable Package Path and Compilation Unit Identity;
- direct package and module dependency edges;
- Dependency Aliases and target Package Identities;
- visibility and Export Surface membership;
- digest verification status;
- exact language version;
- active resource limits; and
- traceability spans for every declared edge and owner.

Compiler APIs and caches MUST distinguish:

```text
Canonical Semantic Identity
```

from a build-local resolved handle such as:

```text
(Canonical Semantic Identity, Package Revision, Project Resolution Fingerprint)
```

Canonical Semantic Identity alone MUST NOT authorize cross-build cache reuse, reuse of a previously resolved type-compatibility or type-equality result, or entity dereference after a Package Revision, language version, compiler semantic version, or relevant configuration change. The Type System remains responsible for defining type identity and equality.

### 10.2 Compilation Unit Fingerprint

A Compilation Unit Fingerprint MUST include:

- Package Identity;
- Module Name;
- Portable Package Path;
- raw source content digest;
- effective language version;
- relevant source-frontend configuration identity; and
- schema version of the fingerprint encoding.

Moving a file therefore invalidates its Compilation Unit cache even when its semantic declarations preserve identity.

### 10.3 Module Fingerprints

A Module Implementation Fingerprint MUST include:

- Module Identity and exposure;
- ordered Compilation Unit Fingerprints;
- direct module dependency identities;
- relevant package configuration; and
- Public Semantic API Fingerprints of directly used Modules.

A Module Public Semantic API Fingerprint includes only accessible public declarations and every semantic fact that an Accepted owning RFC defines as part of their public signature.

Until the Type System and composition contracts define complete public signatures, a reference spike MUST label its API fingerprint incomplete and non-conforming.

### 10.4 Package Fingerprints

A Package Resolution Fingerprint MUST include:

- Package Revision;
- Package Manifest digest;
- ordered Module identities and exposures;
- ordered Dependency Declarations;
- locked target Package Revisions; and
- relevant manifest schema versions.

A Project Resolution Fingerprint additionally includes the exact Project Manifest, Dependency Lock when present, root Workspace Content Fingerprint, compiler semantic version, exact language version, project configuration identity, and active resource limits under section 7.4.

A Package Public Semantic API Fingerprint is derived from the Export Surfaces of exported Modules and their versioned public-signature schemas.

### 10.5 Invalidation Rules

At minimum:

| Change | Required invalidation |
| --- | --- |
| source bytes change | owning Compilation Unit and Module implementation |
| Portable Package Path changes | old and new Compilation Unit identities |
| Namespace or declaration identity changes | affected namespace index and all semantic dependents |
| private implementation changes with stable public API fingerprint | owning Module implementation; downstream public consumers MAY remain cached |
| public API fingerprint changes | every direct semantic consumer and its transitive invalidation dependents |
| Module exposure or dependency changes | owning Package visibility graph and affected consumers |
| Package Revision or lock edge changes | resolved Package, import roots, and dependent resolution |
| Dependency Alias changes | every importing Compilation Unit in the consuming Package |
| Project or Package language constraints change | every affected Compilation Unit |

Caches are optimization artifacts. A cache miss, eviction, corruption, or implementation change MUST NOT change semantic results.

### 10.6 IDE Behavior

An IDE SHOULD:

- show the owning Project, Package, Module, and Compilation Unit for a declaration;
- distinguish semantic Namespace from physical directories;
- explain why a package or module is inaccessible;
- navigate from a Dependency Alias to its manifest declaration and locked revision;
- preview lock and Export Surface changes;
- perform source-move impact analysis;
- expose stale-lock and digest failures without silently repairing them; and
- preserve deterministic diagnostic ordering.

## 11. Examples

Manifest examples use the Draft RFC-0001D schema `0.1` public serialization. RFC-0001D remains non-normative until separately Accepted.

### 11.1 Positive: Root Project and Package

```json
{
  "schema_version": "0.1",
  "root_package_manifest": "industrialmde.package.json",
  "dependency_lock": "industrialmde.lock.json",
  "language_version": "0.1"
}
```

```json
{
  "schema_version": "0.1",
  "package": {
    "authority": "com.acme.automation",
    "name": "water-treatment"
  },
  "version": "0.1.0",
  "language_version": "0.1",
  "modules": [
    {
      "name": "Application",
      "exposure": "internal",
      "source_roots": ["src/application"],
      "dependencies": ["Domain"]
    },
    {
      "name": "Domain",
      "exposure": "exported",
      "source_roots": ["src/domain"],
      "dependencies": []
    }
  ],
  "dependencies": [
    {
      "alias": "Motors",
      "package": {
        "authority": "org.industrialmde",
        "name": "motor-library"
      },
      "version": "1.2.3"
    }
  ]
}
```

The Project has one root Package Identity:

```text
(["com", "acme", "automation"], "water-treatment")
```

`Application` may access Public declarations in `Domain` through its direct module dependency. Only Public declarations in exported Module `Domain` can enter the Package Export Surface.

### 11.2 Positive: Cross-Package Import

```plant
dsl "0.1";
namespace Process.WaterTreatment;

import Motors.Common.Motors.MotorVfd;
```

`Motors` is resolved only as the direct Dependency Alias declared by the current Package Manifest. `Common.Motors.MotorVfd` is traversed inside the locked `org.industrialmde` `motor-library` Package Export Surface.

### 11.3 Positive: Same-Package Import

```plant
dsl "0.1";
namespace Process.Application;

import Process.Domain.PumpStation;
```

`Process` is a root Namespace segment in the current Package. The import does not search any dependency.

### 11.4 Positive: Semantic Identity Survives File Move

Before:

```text
src/domain/Pump.plant
```

After:

```text
src/domain/equipment/Pump.plant
```

When Package Identity, Module, Namespace Path, semantic owner path, spelling, and kind are unchanged:

- Compilation Unit Identity changes;
- source cache keys change; and
- Canonical Declaration Identity remains unchanged.

### 11.5 Positive: Explicit Lock Entry

```json
{
  "package": {
    "authority": "org.industrialmde",
    "name": "motor-library"
  },
  "version": "1.2.3",
  "content_identity": {
    "kind": "immutable-artifact",
    "algorithm": "sha256",
    "value": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
  },
  "manifest_digest": {
    "algorithm": "sha256",
    "value": "abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789"
  },
  "origin": "https://packages.example.invalid/org.industrialmde/motor-library/1.2.3"
}
```

The origin is provenance, not Package Identity. Compilation verifies exact locked bytes and does not search for a newer version.

### 11.6 Negative: Transitive Dependency Access

Package `Application` directly depends on `Equipment`, and `Equipment` directly depends on `Sensors`. `Application` does not declare `Sensors`.

```plant
import Sensors.Common.Sensors.PressureSensor;
```

Expected result: `IMDE4012`. `Sensors` is not in `Application`'s direct Import Root Domain.

### 11.7 Negative: Dependency Alias and Namespace Collision

The current Package owns root Namespace `Motors` and also declares direct Dependency Alias `Motors`.

Expected result: `IMDE4011`. Import target order or later segments do not select a winner.

### 11.8 Negative: Multiple Package Revisions

One dependency path locks:

```text
org.industrialmde / motor-library / 1.2.3
```

Another locks:

```text
org.industrialmde / motor-library / 2.0.0
```

Expected result: `IMDE4006`. The compiler does not create two logical Package instances.

### 11.9 Negative: Package Cycle

```text
A depends on B
B depends on C
C depends on A
```

Expected result: `IMDE4007` with the ordered strongly connected component and the three manifest edges.

### 11.10 Negative: Module Cycle

```text
Domain depends on Application
Application depends on Domain
```

Expected result: `IMDE4008`. Absence of runtime initialization does not make the cycle valid.

### 11.11 Negative: Overlapping Source Roots

```text
Module Domain owns "src"
Module Application owns "src/application"
```

Expected result: `IMDE4009` because Source Roots overlap and files could receive multiple Module owners.

### 11.12 Negative: Symlink Escape

Source Root `src/domain` contains a symlink, junction, reparse point, or archive link to `../../external`.

Expected result: `IMDE4009`. The compiler does not follow the link or compile a partial source set.

### 11.13 Negative: Private Cross-Module Access

Module `Application` directly depends on Module `Domain`, but `Domain` declaration `InternalPumpModel` is Private.

Expected result: `IMDE4013`. A direct module edge does not expose Private declarations.

### 11.14 Negative: Private Declarations Still Collide in a Merged Namespace

Module `DomainA` and Module `DomainB` each contribute a Private declaration named `InternalConfig` to the same logical Namespace in the same Package.

Expected result: RFC-0001B `IMDE3002`. Module privacy restricts accessibility; it does not create a separate semantic identity or collision domain.

### 11.15 Negative: Windows Reserved Device Stem

```text
src/domain/CON.plant
src/domain/Lpt1.config
```

Expected result: `IMDE4009`. The reserved device stem is rejected ASCII-case-insensitively even when the segment has an extension.

### 11.16 Negative: Mixed Language Versions

The Project Manifest and most Compilation Units select language version `0.1`, but one dependency Package Manifest or source `dsl` directive selects another version.

Expected result: `IMDE4014`. Foundational language version `0.1` has no cross-version linking contract.

### 11.17 Negative: Stale Lock

The Package Manifest requires version `1.2.3`, while the lock records version `1.2.2`.

Expected result: `IMDE4004`. Normal compilation does not update the lock.

### 11.18 Boundary Fixtures

Conformance fixtures MUST include:

- minimum and maximum Package Authority labels;
- Package Version components `0` and `2147483647`;
- rejected leading-zero and out-of-range version components;
- Portable Package Paths at the active segment and total-length limits;
- Windows reserved device stems with case and extension variants;
- linked Project, Package, and lock documents and link components below each declared root;
- two paths differing only by ASCII case;
- zero, one, and the maximum direct dependencies;
- zero, one, and the maximum direct module dependencies;
- the maximum Package and Module graph depth and one above it;
- a source tree with randomized filesystem enumeration;
- a lock with randomized entry ordering;
- a cycle diagnostic exceeding its edge-reporting limit;
- exact digest success and one-bit digest mismatch;
- a package with one exported and one internal Module; and
- a Project containing two effective language versions; and
- an empty Source Root that contributes zero Compilation Units.

An empty Source Root is permitted when the Module and Package remain structurally valid. A Package with zero declared Modules is invalid.

### 11.19 Compatibility: Package Upgrade

Version `1.2.3` and `1.2.4` have the same Package Identity. If their Export Surface and public semantic signatures are compatible, imports resolve to the same Canonical Declaration Identities after an explicit lock update.

The Package Revision and Package Resolution Fingerprint still change.

## 12. Alternatives Considered

### 12.1 Directory Structure Defines Namespace

Rejected because checkout layout, case behavior, source roots, and build-tool conventions would become semantic naming inputs.

### 12.2 Package Version Is Part of Package Identity

Rejected because every compatible dependency upgrade would change all declaration and instance identities, damaging traceability and persistent migration.

### 12.3 Multiple Revisions of One Package Identity

Rejected for language version `0.1` because RFC-0001B Namespace Identity would split, cross-version type identity would become ambiguous, and public API closure would require a substantially more complex model.

### 12.4 Transitive Dependencies Are Automatically Visible

Rejected because a dependency's internal graph would become the consumer's source API and could change without a direct manifest edit.

### 12.5 Imports Create Package Dependencies

Rejected because source parsing would mutate the build graph and make missing packages dependent on resolver search behavior.

### 12.6 Package Alias Uses a Separate `::` Syntax

Deferred rather than selected. A separate delimiter is visually explicit, but the existing RFC-0001B Qualified Name grammar can remain deterministic when dependency aliases and current-package root Namespace segments share one collision-checked Import Root Domain.

### 12.7 Modules Are Semantic Namespaces

Rejected because refactoring source ownership or incremental boundaries would change public semantic identities and expose build topology in domain naming.

### 12.8 Implicit Single Module

Rejected because hidden source ownership would complicate visibility, diagnostics, and future package growth. Even a small package explicitly declares one Module.

### 12.9 File-to-File Import Graph

Rejected because imports bind semantic identities, not textual files. File-level dependencies are derived incremental edges, not user-visible inclusion semantics.

### 12.10 Permit Type-Only Package Cycles

Rejected because type semantics and public interface closure are not yet defined, and cycle-sensitive interface construction would undermine the bounded foundational dependency model.

### 12.11 Executable Build Manifests

Rejected because scripts, host conditionals, and environment interpolation create undeclared build inputs and arbitrary-code execution risk.

### 12.12 Resolve Latest Versions During Compilation

Rejected because registry state and network timing would become semantic build inputs and ordinary compilation could not be reproduced.

## 13. Resolved Version 0.1 Limits and Delegated Decisions

### 13.1 Resolved Version 0.1 Limits

The following items are deliberate foundational limits rather than unresolved behavior:

| Topic | Version `0.1` rule |
| --- | --- |
| Public manifest and lock format | Strict JSON schema `0.1` is defined by RFC-0001D |
| Package Version | Exact `Major.Minor.Patch`; no prerelease or build fields |
| Dependency requirements | Exact versions only; no ranges, wildcards, or implicit latest |
| Project roots | Exactly one root Package |
| Local workspace | No multi-package workspace orchestration |
| Language versions | Exactly one effective language version throughout one Project |
| Prelude | No implicit Package, Namespace, ordinary-symbol, or standard-library prelude |
| Built-in types | May be intrinsic language entities only under RFC-0002; not hidden Package declarations or imports |
| Graph processing | Public edges are `consumer → dependency`; compilation uses deterministic dependency-first reverse topological scheduling |
| Root content identity | `workspace-snapshot` Package Content Identity excludes Project and lock inputs; Project Resolution Fingerprint combines them separately |
| Portable paths | Windows device stems and participating symlink, junction, reparse, and archive links are prohibited |
| Module privacy | Visibility does not create a Module-owned semantic collision domain |
| External dependency availability | Direct dependencies are declared Package-wide; Module-specific external allowlists are not present |

Changing one of these rules requires a later public RFC and compatibility analysis. An implementation MUST NOT treat a current absence as an extension point.

### 13.2 Delegated Decisions

RFC-0001C may become Accepted when its own normative scope and listed dependencies are complete. A downstream RFC that serializes, consumes, or extends this model is not made an upstream dependency merely by that relationship.

An implementation claiming behavior in a delegated topic MUST conform to a compatible Accepted owning contract. End-to-end compiler or package-tool conformance therefore may require Accepted downstream RFCs even when the abstract RFC-0001C model is independently Accepted.

| Topic | Current Proposed direction | Owner |
| --- | --- | --- |
| Manifest and lock serialization | Complete Draft schema `0.1` exists; public file-format conformance requires its compatible Accepted contract | RFC-0001D |
| Package Authority ownership | Syntax defined; ownership and registry validation external | Package Distribution RFC |
| Package archive canonicalization | Lock hashes exact artifact bytes; canonical publication archive format unset | Package Distribution RFC |
| Signature and provenance policy | Distribution control; not a compilation-success guarantee | Security and Package Distribution RFCs |
| Public member signature closure | Top-level visibility defined; member and type signature closure unresolved | RFC-0002 and RFC-0006 |
| Application and Deployment entry-point selection | Project is a build boundary only | RFC-0007 and compiler specification |
| Minimum production resource limits | Required categories defined; numeric minima unset | Compiler Conformance Specification |
| Fingerprint canonical encoding | Required properties defined; exact binary schema unset | Public compiler or fingerprint specification; implementation codec MAY have an ADR |

A delegated item MUST NOT be filled by undocumented compiler, package-manager, registry, or filesystem behavior.

## 14. Conformance Requirements

An implementation conforms to an Accepted version of this RFC only if it:

- begins compilation from one explicit Project Manifest;
- selects exactly one root Package Revision;
- distinguishes Package Identity, Version, Content Identity, and Revision;
- permits exactly one Package Revision per Package Identity;
- validates Package and Module manifests without executable interpretation;
- discovers source files through explicit non-overlapping Source Roots;
- assigns every Compilation Unit to exactly one Package and Module;
- uses normalized Portable Package Paths and rejects case-only collisions;
- treats one `.plant` file as one Compilation Unit;
- constructs explicit direct Package and Module dependency DAGs;
- rejects package and module cycles deterministically;
- processes dependencies before consumers using the defined edge orientation and scheduling rule;
- requires exact direct dependencies and a lock for reproducible builds;
- verifies locked package and manifest digests;
- exposes only direct Dependency Aliases to import-target resolution;
- rejects transitive dependency access and implicit re-export;
- resolves import roots left to right without backtracking;
- applies private-by-default top-level visibility;
- requires direct Module access and exported Module status where applicable;
- preserves Namespace and Canonical Declaration Identity rules from RFC-0001B;
- enforces one exact Project language version without overriding source directives;
- introduces no implicit Package, Namespace, ordinary-symbol, or standard-library prelude;
- computes a root Workspace Content Fingerprint without a Project/lock self-reference;
- distinguishes Canonical Semantic Identity from build-local resolved handles and cache keys;
- publishes an immutable Resolved Project Graph;
- enforces deterministic resource limits;
- emits the required diagnostic facts and ordering;
- computes versioned structured fingerprints; and
- passes the positive, negative, boundary, compatibility, randomized-order, and digest-integrity fixtures.

Conformance to this RFC does not establish conformance to the Type System, Execution Model, package registry, target profile, or complete IndustrialMDE language.

An implementation that reads or writes public Project Manifests, Package Manifests, or Dependency Locks additionally requires conformance to a compatible Accepted serialization RFC. Draft RFC-0001D schema `0.1` is the current candidate and is not made normative by RFC-0001C conformance alone.

An implementation that publishes or exchanges concrete fingerprint bytes additionally requires a compatible Accepted fingerprint specification. RFC-0001C conformance alone establishes the input model and safety properties, not an interoperable byte encoding.

## 15. Non-Normative Implementation Notes

A reference compiler will commonly maintain:

- a Project Graph builder internal to the resolution phase;
- immutable Package Revision records;
- a content-addressed package cache;
- Package and Module adjacency indexes;
- a Portable Package Path index with exact and ASCII-folded keys;
- Compilation Unit ownership records;
- dependency-alias Import Root tables;
- Export Surface indexes;
- structured fingerprint encoders; and
- invalidation edges separated from public dependency declarations.

Mutable graph builders MAY exist inside resolution, but the published Resolved Project Graph MUST be immutable.

The package cache is not authoritative. Cache entries are selected by exact locked Package Content Identity and verified before use.

The concrete manifest parser, hash library, archive library, storage engine, and cache serialization are implementation choices. Public manifest and lock bytes are standardized by RFC-0001D and MUST NOT be redefined by an implementation ADR.

## 16. Change Log

### Proposed — 2026-07-20

- Advanced from Draft after architectural review confirmed the foundational Project, Package, Module, dependency, lock, visibility, and incremental-compilation direction.
- Delegated the complete public manifest and lock serialization contract to Draft RFC-0001D rather than an implementation ADR.
- Reconciled the Project model with explicit unlocked development builds while retaining mandatory locks for reproducible and production compilation.
- Fixed `consumer → dependency` graph scheduling by defining deterministic dependency-first reverse topological processing.
- Distinguished root `workspace-snapshot` content from immutable dependency artifacts and excluded Project and lock inputs from the Workspace Content Fingerprint to prevent self-reference.
- Restricted foundational Projects to one effective language version and closed the implicit-prelude question for language version `0.1`.
- Reserved intrinsic built-in type ownership for RFC-0002 without creating hidden Package or import bindings.
- Added Windows reserved device stems and participating symlink/junction/reparse/archive-link rules to build-document selection and source discovery.
- Confirmed that Module privacy does not create separate Namespace collision domains.
- Distinguished Canonical Semantic Identity from build-local resolved handles and Project Resolution cache keys.
- Restricted claims about interoperable fingerprint bytes to a compatible Accepted fingerprint specification.
- Moved fixed version `0.1` limitations out of unresolved questions and assigned every remaining gate to a compatible public owner.

### Draft — 2026-07-20

- Created the initial Project, Package Identity, Package Revision, Module, Compilation Unit, dependency, lock, visibility, source-discovery, and incremental-fingerprint proposal.
- Defined one root Package per Project and one `.plant` file per Compilation Unit for language version `0.1`.
- Proposed exact direct dependencies, a single Package Revision per Package Identity, and acyclic Package and Module graphs.
- Proposed direct Dependency Aliases, private-by-default top-level visibility, exported Modules, and no implicit re-export.
- Left concrete manifest and lock serialization as an explicit pre-Proposed decision gate.
