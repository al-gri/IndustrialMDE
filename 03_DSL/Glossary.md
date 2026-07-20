# IndustrialMDE Glossary

**Status:** Draft

**Version:** 0.1

**Created:** 2026-07-19

**Last Updated:** 2026-07-21

## 1. Purpose

This glossary provides a shared vocabulary for Project Brain, RFCs, ADRs, compiler specifications, and implementation discussions.

The glossary does not independently establish language semantics. An Accepted RFC or the Project Constitution remains authoritative when a term has normative consequences.

## 2. Status Labels

- **Established** — already required by the Approved Project Constitution.
- **Proposed** — recommended by architectural review but not yet accepted as language semantics.
- **Reserved** — the term is recognized, but its exact meaning must be defined by a named RFC.
- **Avoid** — ambiguous or misleading usage that should not appear in new normative text.

## 3. Governance Terms

| Term | Status | Working definition |
| --- | --- | --- |
| Project Constitution | Established | Highest project-level normative document; lower-level records cannot silently override it |
| RFC | Proposed | Record defining language semantics, syntax, user-visible validation, compatibility, or another public contract |
| ADR | Established | Record explaining a replaceable implementation or architecture decision and its consequences |
| Normative | Proposed | Text that defines conformance requirements within its declared authority and version scope |
| Non-normative | Proposed | Explanatory text, examples, or implementation guidance that does not independently define conformance |
| Conformance | Proposed | Demonstrated satisfaction of the observable requirements of an Accepted specification |

## 4. Source and Compiler Terms

| Term | Status | Working definition |
| --- | --- | --- |
| Source Model | Proposed | Authoritative user-authored model together with its declared build inputs |
| Compilation Unit | Proposed | RFC-0001C build and incremental boundary represented by one owned `.plant` source file in language version 0.1 |
| Syntax Tree | Proposed | Parse representation preserving concrete source structure needed for syntax diagnostics and tooling |
| AST | Proposed | Normalized syntax representation used when it adds value beyond the syntax tree |
| Semantic Model | Proposed | Immutable representation containing resolved identities, types, relationships, and language meaning |
| Canonical IR | Established principle; clarification Proposed | Sole authoritative input to target lowering and artifact generation; target-neutral and traceable |
| Target Lowering | Proposed | Deterministic transformation from Canonical IR plus a target profile into target-specific structures |
| Target IR | Proposed | Target-specific lowered representation consumed by emitters or builders |
| Emitter | Established | Component that serializes or builds target artifacts from Target IR without defining language semantics |
| Phase Artifact | Proposed | Immutable published output of a completed compiler phase |
| Diagnostic | Proposed | Structured compiler finding with stable code, severity, message, origin, and deterministic ordering |
| Traceability | Proposed | Mapping from source spans through semantic and IR identities to generated artifact locations |
| Reference Spike | Proposed | Deliberately limited, non-conforming implementation used to test explicit architecture hypotheses |

## 5. Module and Dependency Terms

| Term | Status | Working definition |
| --- | --- | --- |
| Project | Proposed | RFC-0001C build and orchestration boundary selecting one root Package Revision and, for a locked build, one explicit Dependency Lock |
| Project Manifest | Proposed | Versioned build input selecting the root Package Manifest, optional explicit Dependency Lock, exact language version, and project configuration identity; the lock is mandatory for reproducible or production compilation |
| Manifest Schema | Proposed | RFC-0001D closed public serialization schema selected by an exact schema-version string |
| Canonical Serialization | Proposed | RFC-0001D RFC 8785 JSON bytes produced after validating a document, establishing unique semantic collection keys, and canonically ordering semantically unordered arrays |
| Module | Proposed | Package-owned source, visibility, dependency, export, and incremental-compilation boundary that is not a Namespace |
| Namespace | Proposed | Package-scoped logical naming domain whose path, merge, and ownership rules are proposed in RFC-0001B |
| Package | Proposed | Distribution and direct-dependency unit represented by a stable Package Identity and one exact resolved Package Revision |
| Package Identity | Proposed | Structured logical identity consisting of Package Authority and Package Name, excluding version, digest, alias, origin, and checkout path |
| Package Version | Proposed | Exact three-component revision number associated with a Package Identity |
| Package Content Identity | Proposed | Tagged, algorithm-qualified digest of either exact immutable artifact bytes or one immutable root workspace snapshot |
| Workspace Content Fingerprint | Proposed | `workspace-snapshot` Package Content Identity over root-package-owned manifest, portable path, and source bytes, excluding Project and lock inputs |
| Package Revision | Proposed | Tuple of Package Identity, Package Version, and Package Content Identity |
| Package Manifest | Proposed | Declarative package description of Modules, Source Roots, one exact language version, and direct dependencies |
| Library | Proposed | Publication role for a reusable Package rather than a global semantic container |
| Source Root | Proposed | Explicit portable package-relative directory contributing `.plant` files to exactly one Module |
| Portable Package Path | Proposed | Normalized ASCII package-relative path with `/` separators, case-collision rules, and portable device-name restrictions |
| Dependency Alias | Proposed | Manifest identifier used as the first segment of a cross-package import target |
| Dependency Lock | Proposed | Immutable build input resolving immutable dependency packages to exact revisions, digests, origins, aliases, and edges while recording the root identity and version separately |
| Export Surface | Proposed | Set of Public declarations owned by exported Modules of one Package |
| Project Resolution Fingerprint | Proposed | Versioned digest combining Project, root workspace, lock, dependency, compiler-semantic, configuration, and resource-limit inputs without self-reference |
| Resolved Entity Handle | Proposed | Build-local reference combining Canonical Semantic Identity with Package Revision and Project Resolution context |
| Public Semantic API Fingerprint | Proposed | Deterministic digest of one resolved Export Surface under a versioned signature schema |
| Import | Proposed | File-local explicit binding to one accessible declaration or namespace; package availability remains owned by RFC-0001C |
| Scope | Proposed | Identity-bearing owner of one ordinary-symbol collision domain, as proposed in RFC-0001B |
| Binding | Proposed | Association from a source-visible identifier to one resolved semantic identity |
| Qualified Name | Proposed | Dot-separated identifier path resolved left to right without backtracking |
| Collision Domain | Proposed | Set of bindings required to have distinct exact and ASCII case-folded spellings |
| Import Environment | Proposed | File-local set of bindings introduced by explicit import directives |

## 6. Semantic-Kernel Terms

| Term | Status | Working definition |
| --- | --- | --- |
| Definition | Proposed | Named reusable declaration that owns a statically fixed set of semantic Member Declarations |
| Member Declaration | Proposed | Declaration owned by one Definition and interpreted or instantiated in that Definition's context |
| Instance Declaration | Proposed | Static composition site that references one Definition and expands in each applicable parent context |
| Instance | Proposed | Immutable expanded occurrence associated with one Definition, one creating Instance Declaration, and a stable path identity |
| Application Assembly | Proposed | Target-neutral root selecting root instances, logical configuration, and application-level relationships |
| Interface | Reserved | Contract implemented by definitions or exposed instances; conformance rules remain undefined |
| Endpoint | Proposed | Neutral kernel category for an interaction endpoint; Port and Signal semantics remain reserved for RFC-0005 |
| Port | Reserved | Candidate public endpoint concept whose relationship to Signal remains unresolved |
| Signal | Reserved | Typed data or control endpoint with direction and runtime semantics to be defined by RFC-0005 |
| Connection | Proposed | First-class declaration relating explicit Endpoint references in one composition context |
| Parameter | Proposed | Per-instance configuration input that generated behavior cannot assign by default |
| Constant | Proposed | Compile-time immutable named value; type and evaluation rules remain reserved |
| State Variable | Proposed | Per-instance runtime storage owned by bounded behavior |
| Mapping | Proposed | Deployment-only relationship between a resolved logical identity and a target resource |
| Profile Role | Proposed | Qualified classification or contextual role applied to an eligible kernel entity without changing its entity kind |
| Semantic Profile | Proposed | Versioned role vocabulary and validation contract layered over the Core Semantic Kernel |
| Industrial Profile | Proposed | Target-neutral Semantic Profile providing industrial roles and domain constraints |
| Domain Definition Plane | Proposed | Reusable target-neutral Definitions and their declared members |
| Application Assembly Plane | Proposed | Target-neutral root instances, logical configuration, and application-level connections |
| Deployment Model | Proposed | Project-specific target selection, hardware bindings, mappings, and deployment values |

## 7. Type-System Terms

| Term | Status | Working definition |
| --- | --- | --- |
| Type | Draft | Language-defined classification with a stable Type Identity and a semantic value domain |
| Intrinsic Type | Draft | Language-owned type defined directly by RFC-0002 rather than by a Package declaration |
| Intrinsic Type Designator | Draft | Exact Identifier spelling recognized as an Intrinsic Type only in a type-reference context without creating an ordinary binding or implicit prelude |
| Intrinsic Type Identity | Draft | Structured identity containing the intrinsic identity domain, exact Language Version, and Intrinsic Kind |
| Type Reference | Draft | Source or semantic reference occurring in a context that requires a Type |
| Type Equality | Draft | Exact equality relation over complete Type Identities |
| Type Compatibility | Draft | Relation used by an owning semantic rule to determine whether one typed position may satisfy another; equal to Type Equality in the RFC-0002 minimum subset |
| Semantic Value Domain | Draft | Complete target-neutral set of values denoted by a Type before target lowering |
| Representability | Draft | Membership of a mathematical or semantic value in a Type's Semantic Value Domain |
| Physical Representation | Draft | Implementation- or target-specific encoding of values that does not define source Type Identity |
| Invalid Type Placeholder | Draft | Build-local recovery value that is not a valid Type and cannot enter published semantic or generated artifacts |

## 8. Industrial Hierarchy Terms

The following terms are proposed `industrial.structure` profile roles rather than universal core entities:

| Term | Status | Working definition |
| --- | --- | --- |
| Plant | Proposed | Definition classification role for an industrial site or facility assembly |
| Area | Proposed | Definition classification role for a logical or physical facility subdivision |
| ProcessCell | Proposed | Definition classification role for a process-oriented production subdivision |
| Unit | Proposed | Definition classification role for an independently meaningful process or machine unit |
| Equipment | Proposed | Definition classification role for a functional industrial assembly or skid |
| ControlModule | Proposed | Definition classification role for a coordinated control assembly |
| Component | Proposed | Contextual role for an Instance Declaration nested in a parent composition |
| Device | Proposed | Definition classification role for a physical asset or device-abstraction boundary; not a synonym for Component |
| Primitive | Proposed | Definition classification role requiring zero child Instance Declarations; not a separate kernel entity kind |
| Atom | Avoid | Ambiguous synonym previously used for Component, Device, or Primitive |

## 9. External and Target Identity Terms

| Term | Status | Working definition |
| --- | --- | --- |
| Internal Identifier | Proposed | ASCII language identifier used for deterministic semantic resolution |
| Canonical Identity Key | Proposed | Structured tuple of package, namespace, owner, spelling, and entity-kind components used for semantic identity |
| External Tag | Proposed | Engineering identifier stored as validated data rather than parsed as an internal identifier |
| Generated Target Name | Proposed | Deterministically lowered name satisfying target-profile constraints and traceable to its semantic identity |
| Target Profile | Proposed | Versioned declaration of target capabilities, constraints, naming rules, and supported lowering behavior |

## 10. Terms to Avoid in Normative Text

- “IR is the single source of truth” without distinguishing user input from generation input.
- “Fully isolated plugin” without naming the process and trust boundary.
- “Mathematically verified system” without identifying the verified property, method, assumptions, and target.
- “Backward compatible forever” without a language-version support policy.
- “Component / Atom / Device” as interchangeable semantic entities.
