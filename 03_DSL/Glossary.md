# IndustrialMDE Glossary

**Status:** Draft

**Version:** 0.1

**Created:** 2026-07-19

**Last Updated:** 2026-07-20

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
| Compilation Unit | Reserved | Draft RFC-0001C build and incremental boundary represented by one owned `.plant` source file in language version 0.1 |
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
| Project | Reserved | Draft RFC-0001C build and orchestration boundary selecting one root Package Revision and Dependency Lock |
| Project Manifest | Reserved | Draft versioned build input selecting the root Package Manifest, Dependency Lock, language constraints, and project configuration |
| Module | Reserved | Draft package-owned source, visibility, dependency, export, and incremental-compilation boundary that is not a Namespace |
| Namespace | Proposed | Package-scoped logical naming domain whose path, merge, and ownership rules are proposed in RFC-0001B |
| Package | Reserved | Draft distribution and direct-dependency unit represented by a stable Package Identity and one exact resolved Package Revision |
| Package Identity | Reserved | Draft structured logical identity consisting of Package Authority and Package Name, excluding version, digest, alias, origin, and checkout path |
| Package Version | Reserved | Draft exact three-component revision number associated with a Package Identity |
| Package Content Identity | Reserved | Draft algorithm-qualified cryptographic digest of one immutable package artifact |
| Package Revision | Reserved | Draft tuple of Package Identity, Package Version, and Package Content Identity |
| Package Manifest | Reserved | Draft declarative package description of modules, source roots, permitted language versions, and direct dependencies |
| Library | Reserved | Draft publication role for a reusable Package rather than a global semantic container |
| Source Root | Reserved | Draft explicit portable package-relative directory contributing `.plant` files to exactly one Module |
| Portable Package Path | Reserved | Draft normalized ASCII package-relative path with `/` separators and portable collision rules |
| Dependency Alias | Reserved | Draft manifest identifier used as the first segment of a cross-package import target |
| Dependency Lock | Reserved | Draft immutable build input resolving the complete package graph to exact revisions, digests, origins, aliases, and edges |
| Export Surface | Reserved | Draft set of Public declarations owned by exported Modules of one Package |
| Public Semantic API Fingerprint | Reserved | Draft deterministic digest of one resolved Export Surface under a versioned signature schema |
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

## 7. Industrial Hierarchy Terms

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

## 8. External and Target Identity Terms

| Term | Status | Working definition |
| --- | --- | --- |
| Internal Identifier | Proposed | ASCII language identifier used for deterministic semantic resolution |
| Canonical Identity Key | Proposed | Structured tuple of package, namespace, owner, spelling, and entity-kind components used for semantic identity |
| External Tag | Proposed | Engineering identifier stored as validated data rather than parsed as an internal identifier |
| Generated Target Name | Proposed | Deterministically lowered name satisfying target-profile constraints and traceable to its semantic identity |
| Target Profile | Proposed | Versioned declaration of target capabilities, constraints, naming rules, and supported lowering behavior |

## 9. Terms to Avoid in Normative Text

- “IR is the single source of truth” without distinguishing user input from generation input.
- “Fully isolated plugin” without naming the process and trust boundary.
- “Mathematically verified system” without identifying the verified property, method, assumptions, and target.
- “Backward compatible forever” without a language-version support policy.
- “Component / Atom / Device” as interchangeable semantic entities.
