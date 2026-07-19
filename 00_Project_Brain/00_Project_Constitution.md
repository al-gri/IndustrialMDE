# IndustrialMDE Project Constitution

**Version:** 2.1

**Status:** Approved

**Effective Date:** 2026-07-19

**Supersedes:** Version 2.0

**Approval Record:** [Constitution 2.1 Amendment Record](05_Constitution_Amendment_2.1.md)

## 1. Authority and Normative Language

This Constitution is the highest normative authority for the IndustrialMDE project. Every RFC, ADR, compiler specification, implementation, plugin, target, workflow, and generated artifact MUST conform to it.

A lower-level document MUST NOT silently override a higher-level document. A conflict requires rejection or revision of the lower-level proposal, or an explicit versioned amendment to the higher-level document.

Repository records establish normative status. Conversation history, implementation behavior, examples, tests, and generated output MUST NOT independently establish or change normative semantics.

The following normative keywords apply throughout the Constitution, RFCs, ADRs, and public specifications:

- **MUST** and **MUST NOT** define mandatory requirements.
- **SHOULD** and **SHOULD NOT** define strong recommendations that require documented justification when not followed.
- **MAY** defines an optional capability.

Normative keywords apply only when written in uppercase.

## 2. Project Identity, Mission, and Scope

IndustrialMDE is a Model-Driven Engineering platform for declaratively describing industrial automation systems and deterministically generating production-grade target artifacts, including control logic, hardware mappings, HMI and SCADA artifacts, diagnostics, documentation, verification artifacts, and vendor project formats where supported.

The target audience includes system integrators, industrial control and SCADA engineers, platform architects, machine and equipment builders, and hardware vendors.

The mission is to provide a compiler-platform foundation in which safety-relevant meaning is explicit, analyzable, traceable, and preserved through deterministic lowering. Architecture, correctness evidence, and long-term maintainability take precedence over short-term feature velocity.

IndustrialMDE is designed for industrial systems with service lives measured in decades. Long lifecycle intent does not replace the managed compatibility policy in Section 9.

IndustrialMDE is not:

- a general-purpose programming language;
- an interpreted target runtime;
- a simple text-templating engine;
- a vendor-locked source language;
- a claim that compilation alone makes a system safe or certified; or
- an architecture whose semantics are defined by a visual editor, parser framework, emitter template, or vendor tool.

The governing engineering principles are:

- vendor-neutral core semantics;
- deterministic and reproducible compilation;
- immutable published phase artifacts;
- explicit rather than hidden behavior;
- composition over deep inheritance;
- bounded execution and statically bounded resources;
- production-grade generation without manual patches;
- managed compatibility;
- documented public extension contracts;
- evidence-based quality claims; and
- no undocumented architectural hacks.

## 3. Product Claims and Vendor Neutrality

IndustrialMDE MUST maintain a vendor-neutral core semantic model and MUST preserve sufficient semantic information for static analysis, traceability, and formal verification where the modeled property and selected target permit it.

The platform reduces classes of manual engineering error but does not claim to eliminate process, integration, configuration, equipment, network, operator, or organizational error.

Vendor-specific constraints MUST enter through target profiles, target lowering, Target IR, or explicitly namespaced target extensions. They MUST NOT silently redefine core language semantics.

Core language entities MUST NOT encode vendor object models, addresses, memory syntax, task models, or project-file conventions unless an Accepted RFC explicitly defines a vendor-neutral abstraction for the underlying concept.

## 4. Reproducibility Contract

A reproducible build is defined by the complete build input set:

- source contents and normalized logical source paths;
- project manifest and effective language version;
- compiler and standard-library versions;
- dependency lock and resolved package contents;
- plugin identities, versions, and declared capabilities;
- target profile and target-toolchain identity;
- compiler configuration; and
- normalized environment inputs explicitly declared by the build contract.

Given an identical complete build input set, the compiler MUST produce:

- structurally and semantically identical compiler representations;
- deterministic symbol, node, allocation, and artifact ordering;
- deterministic generated identifiers;
- deterministic diagnostic codes, locations, related information, and ordering; and
- byte-identical artifacts for formats fully controlled by IndustrialMDE.

Concurrency, hash-map iteration, file discovery order, host operating system, and locale MUST NOT change observable compiler results after normalization.

Vendor tools that post-process IndustrialMDE output MAY produce non-byte-identical files. Such processing is outside the byte-identity boundary and MUST be declared in the artifact manifest with the relevant tool version and known non-deterministic fields.

## 5. Compiler Pipeline Contract

The compiler follows this strict unidirectional pipeline:

```text
Source Files + Project Manifest + Configuration
                    ↓
         Lexical and Syntax Analysis
                    ↓
             Syntax Tree / AST
                    ↓
        Symbol Collection and Indexing
                    ↓
             Name Resolution
                    ↓
              Type Checking
                    ↓
            Semantic Model
                    ↓
           Dependency Graph
                    ↓
            Validation Passes
                    ↓
             Canonical IR
                    ↓
 Semantics-Preserving Optimization Passes
                    ↓
             Target Lowering
                    ↓
       Target Memory Model and Planning
                    ↓
               Target IR
                    ↓
        Emitters / Exporters / Builders
                    ↓
 Generated Artifacts + Manifest + Traceability
```

Diagnostics are a cross-cutting subsystem and MAY be emitted by every compiler phase. Diagnostics MUST NOT be modeled as only the final pipeline stage.

Each representation MUST have a documented phase contract and MUST add information or normalization required by later phases. A representation MUST NOT be introduced solely to duplicate the previous representation.

Optimization passes MUST be deterministic and semantics-preserving under the Accepted execution model. Target-specific memory planning occurs only after target lowering has established the applicable target memory model.

## 6. Authority of Source and Canonical IR

The source model and its declared build inputs are the authoritative user input. Canonical IR is the sole authoritative input to target lowering and artifact generation.

Emitters, exporters, templates, memory planners, and target plugins MUST NOT read source text, parser objects, or AST nodes as an alternative semantic channel.

Source spans and source-level structure MAY remain available through immutable traceability records for diagnostics, tooling, and generated-artifact mapping.

Templates and generated files MUST NOT define or silently change language semantics. Manual changes to generated artifacts MUST NOT become authoritative project input.

## 7. Phase Immutability and Identity

Published output from a completed compiler phase MUST be immutable to downstream phases and plugins.

Mutable builders MAY be used inside a phase, provided that they:

- do not escape the phase;
- are not retained as published artifacts; and
- cannot mutate previously published compiler state.

Stable identities MUST be derived deterministically from declared build inputs. Random UUIDs MUST NOT be used for persistent semantic or IR identity unless their value is explicitly supplied as an input.

A phase MUST NOT use shared mutable state, undocumented caches, or plugin side effects to create semantic behavior that is absent from its declared inputs and contract.

## 8. RFC and ADR Governance

The authority hierarchy is:

1. Project Constitution;
2. Accepted language and public-contract RFCs;
3. Accepted implementation ADRs;
4. compiler and tooling specifications;
5. implementation and tests.

RFCs MUST define language syntax, language semantics, user-visible validation rules, compatibility contracts, and public language-extension contracts.

ADRs MUST record implementation choices, including implementation language, parser framework, internal serialization, process topology, and concrete library selection.

An RFC or ADR MUST NOT silently conflict with a higher-level normative document. A conflict requires rejection of the proposal or an explicit amendment to the higher-level document.

The repository MUST contain a canonical RFC index that records status, dependencies, supersession, and implementation state. Conversation history alone MUST NOT establish normative status.

Only explicit project-owner approval recorded in the repository MAY move a Constitution amendment or RFC into an Approved or Accepted normative state. Implementation and tests demonstrate conformance; they do not grant normative status.

## 9. Managed Compatibility Contract

IndustrialMDE uses managed compatibility:

- every compilation MUST have an unambiguous effective language version;
- each compiler release MUST publish its supported language-version range;
- Accepted behavior MUST NOT change silently within the same language version;
- deprecation MUST precede ordinary removal by at least one minor release cycle;
- ordinary breaking changes MUST occur only at a major language-version boundary;
- removals MUST include migration documentation and SHOULD include migration tooling when mechanical migration is practical;
- dependency, standard-library, plugin, and target-profile versions MUST participate in compatibility checks; and
- unsupported legacy language versions MAY be removed only according to a published support policy.

An urgent safety or security correction MAY use an expedited compatibility process, but it MUST include a documented rationale, impact assessment, diagnostic, and migration path.

Pre-1.0 Draft and Proposed specifications MAY change incompatibly under the RFC governance process. Accepted and Stabilized behavior follows its published compatibility contract.

## 10. Diagnostic Contract

Every diagnostic MUST provide:

- a stable diagnostic code;
- severity;
- a human-readable message;
- a primary source span or an explicit non-source origin; and
- deterministic ordering relative to other diagnostics.

A diagnostic SHOULD provide, when applicable:

- related source spans;
- an explanation or contextual notes; and
- a stable documentation reference.

A diagnostic MAY provide:

- a fix suggestion;
- an automated fix-it; or
- an IDE code action.

The compiler MUST NOT silently modify erroneous source. Automated fixes require an explicit user action or an explicitly selected migration command.

Diagnostics from every phase MUST preserve sufficient context to identify the governing source, configuration, dependency, plugin, target, or non-source origin.

## 11. Bounded-Semantics Contract

IndustrialMDE source is not interpreted on the target. It declaratively defines bounded runtime behavior that is compiled into target control logic.

The core language MUST NOT permit:

- unbounded recursion or mutually recursive execution;
- runtime object creation or dynamic memory allocation;
- unbounded runtime collections;
- loops without a statically provable upper bound;
- uncontrolled thread or task creation;
- self-modifying configuration or runtime code generation; or
- dispatch whose possible targets cannot be statically bounded.

State machines and execution graphs MUST be finite. Storage allocation MUST be resolvable before deployment. Resource-cost analysis SHOULD be available for properties supported by the selected target profile.

Detailed scan-cycle, event, state-transition, initialization, side-effect, and scheduling semantics remain the responsibility of an Accepted Execution Model RFC.

## 12. Verification and Safety Scope

The compiler MUST distinguish between:

- syntax validation;
- name and type correctness;
- connectivity and mapping validation;
- bounded-resource checks;
- state-machine and data-flow analyses;
- target capability validation;
- formally verified properties; and
- properties that remain external engineering responsibilities.

IndustrialMDE MUST NOT describe generated systems as safe, correct, or certified solely because compilation succeeded.

A verification claim MUST identify the verified property, method, assumptions, applicable model subset, target boundary, and evidence. Unsupported properties MUST remain explicit external engineering responsibilities.

## 13. Plugin and Extension Contract

Plugins MUST interact with the compiler only through published extension interfaces and declared capabilities. They MUST NOT depend on undocumented compiler internals.

Artifacts passed to plugins MUST be immutable. Plugin discovery and execution ordering MUST be deterministic.

In-process API boundaries provide architectural isolation but MUST NOT be described as security isolation. Security isolation requires an explicit trust model and, where required, an out-of-process or sandboxed execution boundary.

Plugin filesystem, network, process, and credential access MUST be governed by declared capabilities and host policy.

A plugin MUST NOT mutate the Core Semantic Model, bypass Canonical IR, introduce hidden language semantics, or make target generation depend on undocumented discovery order.

## 14. Security and Traceability Contract

Source files, manifests, packages, plugins, and imported metadata MUST be treated as untrusted input.

The compiler and package tooling MUST define and enforce limits for applicable resources, including:

- source-file size and nesting depth;
- syntax, semantic, and dependency graph size;
- expression and type-instantiation complexity;
- emitted diagnostic count and related-span count;
- package and archive extraction size; and
- compiler memory and execution budgets.

Parsing, validation, package discovery, and documentation processing MUST NOT execute arbitrary code from project inputs.

Package and plugin resolution MUST support version pinning and content identity. Production build profiles SHOULD support dependency locks, cryptographic hashes, provenance records, and signature verification where the distribution system provides signing.

Archive extraction MUST prevent absolute-path writes, parent-directory traversal, link-based escape, and uncontrolled expansion.

Traceability MUST preserve a deterministic mapping through:

```text
Source Span
    ↓
Semantic Identity
    ↓
Canonical IR Identity
    ↓
Target IR Identity
    ↓
Generated Artifact Location
```

The artifact manifest MUST identify the complete build input set and SHOULD provide sufficient mappings for audit, generated-code explanation, impact analysis, and target-diagnostic correlation.

## 15. Performance Policy

Performance requirements MUST identify:

- benchmark corpus or workload shape;
- hardware and operating environment;
- cold or warm cache state;
- concurrency configuration;
- measured compiler phase; and
- percentile or maximum being evaluated.

Unqualified performance numbers MUST NOT be treated as conformance requirements. Measured budgets belong in `Performance_Budget.md`, where they can be versioned and supported by repeatable benchmarks.

Performance optimization MUST NOT weaken deterministic behavior, diagnostics, traceability, safety validation, or published phase contracts.

## 16. Production Generation and Documentation

Generated artifacts MUST be suitable for their declared production profile without manual modification. The source model remains authoritative, and regeneration MUST NOT destroy user-owned extension code stored through a documented extension mechanism.

Target-specific validation MUST complete before a target artifact is reported as successfully generated. Generated artifacts MUST identify their compiler, language, dependency, plugin, target-profile, and source-model provenance through the artifact manifest where the format permits it.

Project documentation, RFCs, ADRs, source code, source comments, tests, diagnostics references, and public API documentation MUST be written in English. User-authored DSL strings, descriptions, external tags, and localized product documentation MAY use other languages where their governing contracts permit it.

Every public DSL construct, compiler phase, plugin contract, emitter contract, target profile, diagnostic code, and public API MUST have version-appropriate documentation.

Documentation MUST NOT claim behavior, compatibility, validation, test execution, or certification that has not been implemented and evidenced.

## 17. AI Governance and Change Discipline

AI assists engineers but MUST NOT replace deterministic compiler logic or accountable architectural review.

An AI agent MUST NOT:

- change architecture or normative language semantics without explicit approval;
- represent a proposal as an Accepted decision;
- claim that tests, analysis, review, or validation ran when they did not;
- introduce undocumented vendor conditions, name matching, parser ordering dependencies, or semantic emitter logic; or
- suppress diagnostics without a documented rule.

Temporary workarounds require a documented reason, issue or decision record, owner, scope, removal condition, and regression test when applicable.

The default engineering workflow is:

```text
Analysis
    ↓
Architecture Review
    ↓
Risk Assessment
    ↓
Patch Plan
    ↓
Approval
    ↓
Implementation
    ↓
Testing
    ↓
Regression
    ↓
Documentation
    ↓
Release
```

The workflow MAY be scaled to the risk of a change, but normative or safety-relevant changes MUST retain explicit review and evidence.

## 18. Definition of Done

Definition of Done items MUST be unchecked requirements, not pre-completed claims.

A change is complete only when all applicable requirements have recorded evidence. A requirement MAY be marked not applicable only with a short justification.

A task MUST NOT claim tests, static analysis, review, or documentation completion unless those activities actually occurred.

Applicable completion evidence includes:

- acceptance criteria satisfied;
- unit, integration, conformance, and regression tests passed where applicable;
- static analysis and deterministic-output checks passed where applicable;
- security and resource-bound checks passed where applicable;
- architecture or semantic review recorded where required;
- documentation, RFCs, and ADRs updated where required;
- compatibility and migration impact assessed; and
- no unresolved critical defect within the declared scope.

## 19. Roadmap and Reference-Spike Principle

Language semantics and compilation-unit contracts MUST precede production grammar and compiler implementation.

A deliberately limited reference spike MAY be developed before the full language is specified when its purpose is to test an explicit architectural hypothesis. Such a spike MUST:

- declare its supported subset;
- avoid claiming language conformance;
- remain replaceable;
- produce conformance fixtures and architecture feedback; and
- trigger review of any RFC assumptions it disproves.

Production implementation MUST NOT silently convert experimental spike behavior into language semantics.

## 20. Code and Artifact Preservation

User-authored source, configuration, migration material, and extension code MUST be preserved unless a change explicitly authorizes its replacement or removal.

Destructive repository changes, global refactoring, and removal of working behavior require explicit scope, impact analysis, and appropriate approval. Aesthetic preference alone is insufficient justification.

Generated code MUST NOT be manually patched as the normal development model. A target requiring user-owned code MUST provide a documented extension boundary that survives deterministic regeneration.

A parser, compiler pass, plugin, target, or template MUST NOT rely on an undocumented special case. A temporary special case follows the change-discipline requirements in Section 17.

## 21. Versioning and Constitutional Amendment

Language, compiler, package, plugin, target-profile, and public API versions MUST follow their published versioning contracts. Semantic Versioning SHOULD be used where its compatibility model fits the artifact.

This Constitution uses explicit document versions. A constitutional amendment requires:

1. a recorded proposal and rationale;
2. architectural and impact review;
3. resolution or explicit deferral of material objections;
4. explicit project-owner approval recorded in the repository;
5. incorporation into a new Constitution version; and
6. an amendment-history entry identifying the superseded version.

An amendment is not normative until incorporation is complete. Editorial corrections that do not change meaning MAY be recorded without incrementing the minor version, but their non-semantic nature MUST be reviewable in repository history.

## 22. Decisions Delegated to RFCs and ADRs

This Constitution does not independently decide:

- the Core Semantic Kernel and Industrial Profile model;
- the exact Definition and Instance metamodel;
- the type system;
- execution scheduling semantics;
- the attribute system;
- package resolution;
- plugin process topology;
- parser or template framework selection; or
- concrete target or standard-library behavior.

Language and public-contract decisions require their respective RFCs. Replaceable implementation decisions require their respective ADRs.

## 23. Future Direction

IndustrialMDE is intended to become a durable industrial compiler platform with a vendor-neutral semantic foundation, deterministic target generation, explicit traceability, analyzable behavior, and a maintainable extension ecosystem.

Functional growth MUST preserve the contracts in this Constitution. New features do not justify hidden semantics, weakened determinism, unbounded behavior, undocumented target coupling, or unsupported safety claims.

## 24. Amendment History

| Version | Status | Date | Effect |
| --- | --- | --- | --- |
| 2.0 | Superseded | 2026-07-19 | Replaced by version 2.1 |
| 2.1 | Approved | 2026-07-19 | Establishes reproducibility, phase immutability, bounded semantics, managed compatibility, cross-cutting diagnostics, governance, security, and traceability contracts |
