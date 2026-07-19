# RFC-0000: Language Design Principles

**Status:** Proposed

**Authors:** IndustrialMDE Project

**Created:** 2026-07-19

**Last Updated:** 2026-07-19

**Target Language Version:** Pre-1.0

**Dependencies:** Project Constitution version 2.1

**Supersedes:** None

**Superseded By:** None

**Implementation Status:** Not Started

**Review:** [Foundational RFC Review Decisions](../../00_Project_Brain/06_Foundational_RFC_Review_Decisions.md)

**Approval Context:** [Project Constitution 2.1 Amendment Record](../../00_Project_Brain/05_Constitution_Amendment_2.1.md)

## 1. Summary

This RFC defines the design constraints for the IndustrialMDE language. Later language RFCs, examples, grammar specifications, compiler behavior, and public extension contracts must conform to these principles before they can become Accepted.

IndustrialMDE is a declarative modeling and generative language for industrial automation. It may describe bounded runtime behavior, but IndustrialMDE source is compiled rather than interpreted on the target.

This Proposed RFC is written under Approved Project Constitution version 2.1. Constitutional alignment no longer blocks review, but this RFC remains non-normative until its own dependencies, decision gates, and conformance requirements satisfy the RFC acceptance process.

## 2. Motivation

Industrial automation models live for years or decades, cross vendor boundaries, and produce safety-relevant software and configuration. A parser-first language design would allow implementation details, template behavior, or vendor constraints to become accidental language semantics.

This RFC establishes a durable language boundary before grammar and compiler implementation begin.

## 3. Goals

The language is designed to be:

- deterministic and reproducible within a declared build-input envelope;
- vendor-neutral at its semantic core;
- explicit about dependencies, connections, mappings, and conversions;
- declarative and bounded by construction;
- human-readable by industrial engineers;
- machine-analyzable and amenable to formal verification where applicable;
- composition-oriented;
- compatible with precise diagnostics and source-to-artifact traceability;
- independent of a particular parser or compiler framework;
- suitable for incremental compilation once compilation boundaries are defined;
- extensible through versioned, declared contracts;
- governed by managed compatibility rather than silent semantic change.

## 4. Non-Goals

IndustrialMDE is not intended to be:

- a general-purpose programming language;
- an interactive scripting or interpreted runtime language;
- a replacement syntax for Structured Text, SCL, or another PLC language;
- an arbitrary code-execution environment;
- a dynamic object or reflection system;
- a universal process simulator;
- a guarantee that every generated industrial system is safe or formally verified;
- a direct representation of one vendor’s project, memory, task, or address model;
- a visual-editor file format;
- a template language whose templates define compiler semantics.

## 5. Terminology

This RFC uses terms from the [IndustrialMDE Glossary](../Glossary.md).

Key terms for this RFC:

- **Source Model** — the user-authored model together with its declared build inputs.
- **Semantic Model** — resolved, typed, immutable language meaning.
- **Canonical IR** — target-neutral generation representation consumed by target lowering.
- **Target Profile** — versioned target capabilities and constraints.
- **Reference Spike** — deliberately limited implementation used to test architecture hypotheses without claiming conformance.

## 6. Normative Language Principles

### 6.1 Declarative Modeling Boundary

IndustrialMDE source MUST describe industrial structure, configuration, relationships, constraints, and bounded behavior declaratively.

The source language MUST NOT require an IndustrialMDE interpreter on the deployed target.

The language MAY describe runtime behavior such as interlocks, state transitions, signal flow, and alarm conditions when their semantics and resource bounds are statically defined by an Accepted RFC.

The language MUST NOT expose arbitrary target-language escape blocks in the vendor-neutral core.

### 6.2 Explicit Semantics

The language MUST require explicit declarations for material semantic relationships, including:

- imports and dependencies;
- definition references and instances;
- signal or port connections;
- parameter overrides;
- interface conformance;
- deployment mappings;
- target-profile selection;
- conversions that can lose information, change units, or affect safety behavior.

The language MUST NOT introduce hidden mutable global state, implicit imports, implicit hardware bindings, or undeclared runtime dependencies.

Language-defined built-in types and literals are not considered hidden imports when their behavior is fully specified by an Accepted RFC.

### 6.3 Vendor-Neutral Core

Core syntax and semantics MUST NOT require concepts unique to a specific automation vendor.

Vendor-specific memory areas, task models, addresses, project structures, function blocks, and export formats MUST be represented through target profiles, target lowering, target IR, or explicitly namespaced target extensions.

A vendor extension MUST NOT silently redefine core language semantics.

A reusable domain model SHOULD remain deployable to more than one compatible target profile without source changes to its core definitions.

### 6.4 Composition Before Inheritance

Reusable industrial structures MUST be expressible through definitions, static instances, interfaces, and explicit connections.

Core language design SHOULD prefer composition over inheritance.

Inheritance MUST NOT be introduced unless a later RFC defines its identity, substitution, conflict-resolution, initialization, and compatibility semantics. Until such an RFC is Accepted, inheritance is prohibited.

Interface conformance MAY provide substitutability without implementation inheritance.

### 6.5 Definitions and Instances

The language MUST distinguish reusable declarations from their statically declared occurrences.

The exact Definition and Instance metamodel is owned by RFC-0001A. Grammar, examples, and compiler classes MUST NOT collapse a definition, an instance, and a reference into an undocumented single concept.

Runtime creation of new model instances is prohibited.

### 6.6 Deterministic Semantics

Given the same complete build-input set, observable language and compiler behavior MUST be deterministic.

The language MUST define deterministic rules for:

- declaration and resolution ordering;
- overload or candidate selection if overloading is introduced;
- connection and driver ordering;
- evaluation and state-transition ordering;
- generated identity derivation;
- diagnostics and related-information ordering;
- metadata and IR serialization ordering.

Source-file discovery order, host hash iteration, process scheduling, and parallel compilation MUST NOT select different valid meanings.

An ambiguity MUST produce a deterministic diagnostic rather than an implementation-dependent choice.

### 6.7 Bounded Semantics

The language MUST be bounded by construction.

The core language MUST NOT permit:

- unbounded recursion or mutually recursive execution;
- runtime object creation or dynamic allocation;
- unbounded runtime collections;
- loops without a statically provable upper bound;
- uncontrolled task or thread creation;
- runtime code generation;
- self-modifying model structure;
- dispatch whose possible targets cannot be statically bounded.

All state machines MUST have a finite declared structure. Storage requirements MUST be resolvable before deployment.

Detailed execution, scheduling, and resource-analysis semantics are deferred to RFC-0004.

### 6.8 Static Analysis and Verification

The language MUST preserve enough semantic information for static analysis of properties defined by Accepted RFCs.

The compiler MUST distinguish a successfully compiled model from a model whose safety or process behavior has been formally verified.

A verification claim MUST identify:

- the property being verified;
- the analysis or proof method;
- assumptions and environmental constraints;
- the language and target versions;
- unsupported or externally validated properties.

Compilation success alone MUST NOT be presented as safety certification.

### 6.9 Frontend and Grammar Independence

The language contract MUST be independent of textX, Arpeggio, or any other parser framework.

The grammar MUST be deterministic, unambiguous, and suitable for predictable tooling and error recovery.

Basic syntax-tree construction MUST NOT depend on name resolution or type information.

The grammar SHOULD remain friendly to top-down parsing. If a later construct requires another parsing strategy, its RFC MUST justify the tooling and ambiguity consequences rather than encoding framework-specific workarounds into the language.

There MUST be no automatic semicolon insertion or other whitespace-sensitive token synthesis unless a later RFC explicitly defines it.

### 6.10 Canonical Generation Path

Target generation MUST follow this semantic path:

```text
Source Model
    ↓
Semantic Model
    ↓
Canonical IR
    ↓
Target Lowering
    ↓
Target IR
    ↓
Emitter or Builder
```

Emitters, templates, exporters, memory planners, and target plugins MUST NOT use source text, parser objects, or AST nodes as an alternative source of semantic truth.

Templates MUST NOT perform name resolution, type checking, validation, memory planning, or semantics-changing optimization.

### 6.11 Immutability and Traceability

Published compiler-phase outputs MUST be immutable to downstream phases.

Every semantic entity and generated artifact SHOULD be traceable through stable identities from source spans to Semantic Model, Canonical IR, Target IR, and artifact locations.

Persistent identities MUST be deterministic functions of declared inputs. Random identity generation MUST NOT affect reproducible output.

### 6.12 Diagnostics

Invalid source MUST produce explicit diagnostics. The compiler MUST NOT silently repair it.

Every diagnostic MUST include:

- a stable diagnostic code;
- severity;
- a human-readable message;
- a primary source span or explicit non-source origin;
- deterministic ordering.

Related spans and documentation references SHOULD be provided when useful. Fix suggestions and automated code actions MAY be provided when a safe and unambiguous correction exists.

Error recovery MAY continue analysis after an error, but recovered nodes MUST be marked so they cannot silently reach artifact generation.

### 6.13 Compatibility and Language Versions

Every compilation MUST have an unambiguous effective language version.

The same language version MUST NOT change accepted semantics silently.

Deprecation, removal, support windows, and migration follow the managed compatibility contract in Approved Project Constitution version 2.1. The exact deprecated-version support window remains delegated to a published release-support policy.

A compiler MAY support multiple language versions, but it MUST resolve each compilation unit under one declared version and MUST reject unsupported combinations deterministically.

### 6.14 Extensibility

Extensions MUST use declared, versioned extension points.

Unknown extensions MUST NOT be silently ignored when they can affect semantics or generated artifacts.

Vendor extensions SHOULD use a namespace that cannot collide with core language features.

An extension MUST declare its required language version, capabilities, and compatibility range.

The exact attribute, profile, plugin, and target-extension mechanisms are deferred to later RFCs.

### 6.15 Incremental Compilation

The language SHOULD support incremental compilation through explicit compilation units, stable public identities, and deterministic dependency edges.

Incremental compilation is a design goal rather than an implemented guarantee until RFC-0001C defines compilation boundaries, fingerprints, invalidation, and dependency resolution.

An incremental compilation result MUST be observationally equivalent to a clean compilation with the same complete build-input set.

### 6.16 Security and Resource Control

Source files, manifests, dependencies, packages, and extensions MUST be treated as untrusted input.

Language features MUST NOT require arbitrary code execution during parsing, resolution, validation, or generation.

Implementations MUST enforce declared resource limits and MUST fail with deterministic diagnostics rather than uncontrolled resource exhaustion where practical.

Package or extension content MUST NOT gain filesystem, network, process, or credential access merely by being referenced from source.

## 7. Determinism and Ordering

Later RFCs MUST specify observable ordering for every construct that can produce more than one candidate, driver, transition, artifact, or diagnostic.

When ordering is semantically irrelevant, the compiler MUST still select and document a stable serialization order.

Source order MAY be used when it is explicit and stable. Source order MUST NOT be inferred from filesystem enumeration or unordered dependency discovery.

## 8. Compatibility and Migration

This RFC introduces no stabilized syntax. It establishes review constraints for future syntax and semantics.

Once Accepted, changes to these principles require either:

- an explicit amendment to RFC-0000 with compatibility analysis; or
- a superseding RFC approved through the governance process.

An implementation framework change does not require a language-version change unless observable language behavior changes.

## 9. Safety and Security Considerations

The boundedness rules reduce but do not eliminate industrial-system risk.

External engineering responsibilities include process hazard analysis, safety-integrity allocation, electrical design, commissioning, target-tool qualification, cybersecurity architecture, and regulatory certification unless a specific Accepted RFC and verified tool claim says otherwise.

Profiles and plugins MUST NOT claim certification on behalf of the core compiler without a separately documented assurance case.

## 10. Tooling and Incremental Compilation

Tools SHOULD be able to parse incomplete source, retain precise spans, expose documentation comments, and produce deterministic partial diagnostics.

Language servers and IDEs MUST consume the same language rules as batch compilation. They MUST NOT invent a second compatibility or name-resolution model.

Formatters MUST preserve semantics and SHOULD be idempotent.

## 11. Examples

The examples in this section are conceptual. They do not establish final syntax.

### 11.1 Positive Example: Explicit Composition

```text
Definition: PumpStation
  Instance: main_pump of MotorVfd
  Instance: pressure_sensor of AnalogSensor
  Connection: pressure_sensor.value -> station_pressure
  Constraint: main_pump.enable requires station_pressure < max_pressure
```

The model names definitions, instances, connections, and constraints explicitly.

### 11.2 Negative Example: Hidden Vendor Binding

```text
main_pump.enable := %Q0.0
```

Embedding a target address in a reusable core definition violates vendor neutrality and domain/deployment separation.

### 11.3 Negative Example: Unbounded Behavior

```text
while pressure_error != 0 {
    adjust_output();
}
```

The loop has no statically provable upper bound and is prohibited.

### 11.4 Boundary Example: Reference Spike

A reference spike may support only definitions, instances, four scalar types, connections, and a mock target. It must declare that subset and must not claim conformance to undeveloped RFCs.

## 12. Alternatives Considered

### Grammar-first design

Rejected because parser object structure and framework constraints would become accidental language architecture.

### General-purpose embedded language

Rejected because arbitrary runtime behavior conflicts with bounded analysis, deterministic generation, and target portability.

### Vendor-specific core with portability adapters

Rejected because vendor semantics would contaminate reusable models and Canonical IR.

### Templates as the primary generation abstraction

Rejected because templates cannot safely own type checking, memory planning, validation, or target-independent semantics.

## 13. Resolved and Deferred Decisions

| Topic | Resolution | Owning contract or gate |
| --- | --- | --- |
| Semantic model | Core Semantic Kernel plus Industrial Profiles | RFC-0001A |
| Language-version directive | Required per source file; the manifest may constrain but not override | RFC-0001 and RFC-0001C |
| Expressions and bounded iteration | Must satisfy this RFC's boundedness invariant | RFC-0003 and RFC-0004 |
| Namespaced attributes | No attribute is authorized until a dedicated public contract defines it | Future attribute RFC |
| Version 1.0 stabilization set | Deferred until reference-spike and conformance evidence exist | Stabilization review |
| Deprecated-version support window | Deferred to a published managed support policy | Constitution 2.1 and release policy |

The two stabilization decisions do not alter the pre-1.0 principles in this RFC. They must be resolved before Stabilized status, not before Proposed review.

## 14. Conformance Requirements

A conforming language specification and compiler must demonstrate that:

- no target generation path bypasses Canonical IR;
- parser-framework behavior is not part of language semantics;
- invalid ambiguity produces diagnostics rather than implementation-dependent meaning;
- runtime structure and resource use are statically bounded according to Accepted RFCs;
- clean and incremental compilation are observationally equivalent;
- diagnostics and artifact ordering are deterministic;
- vendor-specific constraints do not silently enter the core semantic model;
- source-to-artifact traceability is preserved.

Conformance fixtures will be added as dependent RFCs define observable syntax and semantics.

## 15. Implementation Notes

This section is non-normative.

An early reference compiler may use Python, textX, and Jinja2 if their ADRs are accepted. Those choices do not change the language principles in this RFC.

The reference spike should prioritize architecture feedback, traceable representations, deterministic snapshots, and high-value negative tests over broad feature coverage.

## 16. Change Log

| Date | Change |
| --- | --- |
| 2026-07-19 | Initial Draft |
| 2026-07-19 | Promoted to Proposed after project-owner audit; resolved foundational decisions and recorded stabilization deferrals |
| 2026-07-19 | Reconciled the dependency and compatibility text with Approved Project Constitution version 2.1 |
