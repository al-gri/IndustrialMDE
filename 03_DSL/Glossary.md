# IndustrialMDE Glossary

**Status:** Draft

**Version:** 0.1

**Created:** 2026-07-19

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
| Compilation Unit | Reserved | Incremental and diagnostic source boundary to be defined by RFC-0001C |
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
| Project | Reserved | Build and deployment root whose exact contents are defined by RFC-0001C and the semantic-model RFC |
| Module | Reserved | Compilation and visibility construct to be defined by RFC-0001C |
| Namespace | Reserved | Qualified naming domain to be defined by RFC-0001B |
| Package | Reserved | Versioned dependency and distribution unit to be defined by RFC-0001C |
| Library | Reserved | Published collection of reusable definitions; relationship to Package remains unresolved |
| Import | Reserved | Explicit dependency or symbol-visibility declaration to be defined by RFC-0001B and RFC-0001C |

## 6. Semantic-Kernel Terms

| Term | Status | Working definition |
| --- | --- | --- |
| Definition | Proposed | Reusable compile-time declaration that can be referenced by statically known instances |
| Instance | Proposed | Statically declared occurrence associated with a Definition and a stable qualified identity |
| Interface | Reserved | Contract implemented by definitions or exposed instances; conformance rules remain undefined |
| Port | Reserved | Typed interaction endpoint whose relationship to Signal remains unresolved |
| Signal | Reserved | Typed data or control endpoint with direction and runtime semantics to be defined by RFC-0005 |
| Connection | Proposed | First-class relationship between compatible endpoints, including direction and traceability |
| Parameter | Reserved | Configurable value category whose mutability and lifecycle remain undefined |
| Constant | Reserved | Compile-time immutable value to be defined by the type and expression RFCs |
| State Variable | Reserved | Runtime storage category governed by the Execution Model RFC |
| Mapping | Reserved | Deployment relationship between logical entities and target resources, not reusable domain containment |
| Profile | Proposed | Named domain or target specialization layered over the core semantic kernel without silently changing core rules |
| Domain Model | Proposed | Reusable target-neutral definitions and instances describing industrial intent |
| Deployment Model | Proposed | Project-specific bindings, target profiles, hardware mappings, and deployment configuration |

## 7. Industrial Hierarchy Terms

The following terms are candidate profile roles rather than confirmed universal core entities:

| Term | Status | Working definition |
| --- | --- | --- |
| Plant | Reserved | Industrial site role; placement in the core or an industrial profile is unresolved |
| Area | Reserved | Industrial subdivision role |
| ProcessCell | Reserved | Process-oriented cell role |
| Unit | Reserved | Independently meaningful process or machine unit role |
| Equipment | Reserved | Functional industrial assembly role |
| ControlModule | Reserved | Logical grouping of cooperating control elements |
| Component | Reserved | Candidate generic role for a nested static instance; exact semantics unresolved |
| Device | Reserved | Candidate physical-asset role; MUST NOT be used as a synonym for Component until defined |
| Primitive | Reserved | Candidate minimal standard-library definition; exact semantics unresolved |
| Atom | Avoid | Ambiguous synonym previously used for Component, Device, or Primitive |

## 8. External and Target Identity Terms

| Term | Status | Working definition |
| --- | --- | --- |
| Internal Identifier | Proposed | ASCII language identifier used for deterministic semantic resolution |
| External Tag | Proposed | Engineering identifier stored as validated data rather than parsed as an internal identifier |
| Generated Target Name | Proposed | Deterministically lowered name satisfying target-profile constraints and traceable to its semantic identity |
| Target Profile | Proposed | Versioned declaration of target capabilities, constraints, naming rules, and supported lowering behavior |

## 9. Terms to Avoid in Normative Text

- “IR is the single source of truth” without distinguishing user input from generation input.
- “Fully isolated plugin” without naming the process and trust boundary.
- “Mathematically verified system” without identifying the verified property, method, assumptions, and target.
- “Backward compatible forever” without a language-version support policy.
- “Component / Atom / Device” as interchangeable semantic entities.
