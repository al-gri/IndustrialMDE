# Proposed Amendment: IndustrialMDE Project Constitution 2.1

**Proposal Version:** 0.1

**Status:** Proposed

**Target Document:** `00_Project_Constitution.md`, version 2.0

**Proposed Target Version:** 2.1

**Created:** 2026-07-19

## 1. Authority and Effect

This document is an architectural review proposal. It is not normative and does not modify the authority or status of Project Constitution version 2.0.

If this proposal is explicitly accepted by the project owner, its approved clauses will be incorporated into Project Constitution version 2.1 in a separate patch. Until that acceptance and incorporation occur, Constitution version 2.0 remains the governing document.

## 2. Purpose

The amendment replaces absolute or underspecified promises with testable contracts and reconciles the Constitution with the approved language-first development direction.

The amendment is intended to:

- define a reproducibility envelope rather than treating source text as the only build input;
- distinguish the source model from the canonical IR;
- make diagnostics a cross-cutting subsystem;
- place target lowering before target-specific memory planning;
- distinguish language RFCs from implementation ADRs;
- define managed compatibility rather than perpetual unconditional compatibility;
- limit formal-verification claims to properties the platform can actually analyze;
- define bounded execution and static resource expectations;
- describe plugin isolation according to an explicit trust and process model;
- replace universal diagnostic fix requirements with tiered requirements;
- treat performance budgets as measured engineering targets;
- make Definition of Done evidence-based rather than pre-checked.

## 3. Proposed Normative Keywords

The following meanings are proposed for the Constitution, RFCs, ADRs, and public specifications:

- **MUST** and **MUST NOT** define mandatory requirements.
- **SHOULD** and **SHOULD NOT** define strong recommendations that require documented justification when not followed.
- **MAY** defines an optional capability.

Normative keywords apply only when written in uppercase.

## 4. Proposed Product Claims

Replace claims of absolute vendor independence, universal mathematical verification, and elimination of human error with the following contract:

> IndustrialMDE MUST maintain a vendor-neutral core semantic model and MUST preserve sufficient semantic information for static analysis, traceability, and formal verification where the modeled property and selected target permit it. The platform reduces classes of manual engineering error but does not claim to eliminate process, integration, configuration, or operator error.

Vendor-specific constraints MUST enter through target profiles, target lowering, target IR, or explicitly namespaced target extensions. They MUST NOT silently redefine core language semantics.

## 5. Proposed Reproducibility Contract

A reproducible build is defined by the complete build input set:

- source contents and normalized logical source paths;
- project manifest and effective language version;
- compiler and standard-library versions;
- dependency lock and resolved package contents;
- plugin identities, versions, and declared capabilities;
- target profile and target-toolchain identity;
- compiler configuration;
- normalized environment inputs explicitly declared by the build contract.

Given an identical complete build input set, the compiler MUST produce:

- structurally and semantically identical compiler representations;
- deterministic symbol, node, allocation, and artifact ordering;
- deterministic generated identifiers;
- deterministic diagnostic codes, locations, related information, and ordering;
- byte-identical artifacts for formats fully controlled by IndustrialMDE.

Concurrency, hash-map iteration, file discovery order, host operating system, and locale MUST NOT change observable compiler results after normalization.

Vendor tools that post-process IndustrialMDE output MAY produce non-byte-identical files. Such processing is outside the byte-identity boundary and MUST be declared in the artifact manifest with the relevant tool version and known non-deterministic fields.

## 6. Proposed Compiler Pipeline Contract

Replace the existing simplified pipeline with:

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

## 7. Proposed Authority of Source and IR

Replace “IR is the Single Source of Truth” with:

> The source model and its declared build inputs are the authoritative user input. Canonical IR is the sole authoritative input to target lowering and artifact generation.

Emitters, exporters, templates, memory planners, and target plugins MUST NOT read source text, parser objects, or AST nodes as an alternative semantic channel.

Source spans and source-level structure MAY remain available through immutable traceability records for diagnostics, tooling, and generated-artifact mapping.

## 8. Proposed Phase Immutability Contract

Published output from a completed compiler phase MUST be immutable to downstream phases and plugins.

Mutable builders MAY be used inside a phase, provided that they:

- do not escape the phase;
- are not retained as published artifacts;
- cannot mutate previously published compiler state.

Stable identities MUST be derived deterministically from declared build inputs. Random UUIDs MUST NOT be used for persistent semantic or IR identity unless their value is explicitly supplied as an input.

## 9. Proposed RFC and ADR Governance

The governance hierarchy is proposed as:

1. Project Constitution;
2. Accepted language and public-contract RFCs;
3. Accepted implementation ADRs;
4. compiler and tooling specifications;
5. implementation and tests.

RFCs MUST define language syntax, language semantics, user-visible validation rules, compatibility contracts, and public language-extension contracts.

ADRs MUST record implementation choices, including implementation language, parser framework, internal serialization, process topology, and concrete library selection.

An RFC or ADR MUST NOT silently conflict with a higher-level normative document. A conflict requires rejection of the proposal or an explicit amendment to the higher-level document.

The repository MUST contain a canonical RFC index that records status, dependencies, supersession, and implementation state. Conversation history alone MUST NOT establish normative status.

## 10. Proposed Compatibility Contract

Replace unconditional perpetual compatibility with managed compatibility:

- every compilation MUST have an unambiguous effective language version;
- each compiler release MUST publish its supported language-version range;
- accepted behavior MUST NOT change silently within the same language version;
- deprecation MUST precede ordinary removal by at least one minor release cycle;
- ordinary breaking changes MUST occur only at a major language-version boundary;
- removals MUST include migration documentation and SHOULD include migration tooling when mechanical migration is practical;
- dependency, standard-library, plugin, and target-profile versions MUST participate in compatibility checks;
- unsupported legacy language versions MAY be removed only according to a published support policy.

An urgent safety or security correction MAY use an expedited compatibility process, but it MUST include a documented rationale, impact assessment, diagnostic, and migration path.

## 11. Proposed Diagnostic Contract

Every diagnostic MUST provide:

- a stable diagnostic code;
- severity;
- a human-readable message;
- a primary source span or an explicit non-source origin;
- deterministic ordering relative to other diagnostics.

A diagnostic SHOULD provide, when applicable:

- related source spans;
- an explanation or contextual notes;
- a stable documentation reference.

A diagnostic MAY provide:

- a fix suggestion;
- an automated fix-it;
- an IDE code action.

The compiler MUST NOT silently modify erroneous source. Automated fixes require an explicit user action or an explicitly selected migration command.

## 12. Proposed Bounded-Semantics Contract

IndustrialMDE source is not interpreted on the target. It declaratively defines bounded runtime behavior that is compiled into target control logic.

The core language MUST NOT permit:

- unbounded recursion or mutually recursive execution;
- runtime object creation or dynamic memory allocation;
- unbounded runtime collections;
- loops without a statically provable upper bound;
- uncontrolled thread or task creation;
- self-modifying configuration or runtime code generation;
- dispatch whose possible targets cannot be statically bounded.

State machines and execution graphs MUST be finite. Storage allocation MUST be resolvable before deployment. Resource-cost analysis SHOULD be available for properties supported by the selected target profile.

Detailed scan-cycle, event, state-transition, initialization, side-effect, and scheduling semantics remain the responsibility of an Accepted Execution Model RFC.

## 13. Proposed Verification Scope

The compiler MUST distinguish between:

- syntax validation;
- name and type correctness;
- connectivity and mapping validation;
- bounded-resource checks;
- state-machine and data-flow analyses;
- target capability validation;
- formally verified properties;
- properties that remain external engineering responsibilities.

IndustrialMDE MUST NOT describe generated systems as safe, correct, or certified solely because compilation succeeded.

## 14. Proposed Plugin Contract

Plugins MUST interact with the compiler only through published extension interfaces and declared capabilities. They MUST NOT depend on undocumented compiler internals.

Artifacts passed to plugins MUST be immutable. Plugin discovery and execution ordering MUST be deterministic.

In-process API boundaries provide architectural isolation but MUST NOT be described as security isolation. Security isolation requires an explicit trust model and, where required, an out-of-process or sandboxed execution boundary.

Plugin filesystem, network, process, and credential access MUST be governed by declared capabilities and host policy.

## 15. Proposed Security and Traceability Contract

Source files, manifests, packages, plugins, and imported metadata MUST be treated as untrusted input.

The compiler and package tooling MUST define and enforce limits for applicable resources, including:

- source-file size and nesting depth;
- syntax, semantic, and dependency graph size;
- expression and type-instantiation complexity;
- emitted diagnostic count and related-span count;
- package and archive extraction size;
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

## 16. Proposed Performance Policy

Performance requirements MUST identify:

- benchmark corpus or workload shape;
- hardware and operating environment;
- cold or warm cache state;
- concurrency configuration;
- measured compiler phase;
- percentile or maximum being evaluated.

Unqualified performance numbers SHOULD move from the Constitution to `Performance_Budget.md`, where they can be versioned and supported by repeatable benchmarks.

## 17. Proposed Definition of Done

Definition of Done items MUST be unchecked requirements, not pre-completed claims.

A change is complete only when all applicable requirements have recorded evidence. A requirement MAY be marked not applicable only with a short justification.

No task may claim tests, static analysis, review, or documentation completion unless those activities actually occurred.

## 18. Proposed Roadmap Principle

Language semantics and compilation-unit contracts MUST precede production grammar and compiler implementation.

A deliberately limited reference spike MAY be developed before the full language is specified when its purpose is to test an explicit architectural hypothesis. Such a spike MUST:

- declare its supported subset;
- avoid claiming language conformance;
- remain replaceable;
- produce conformance fixtures and architecture feedback;
- trigger review of any RFC assumptions it disproves.

## 19. Decisions Explicitly Not Made by This Amendment

This proposal does not decide:

- the Core Semantic Kernel + Industrial Profiles model;
- the exact definition/instance metamodel;
- the type system;
- execution scheduling semantics;
- the attribute system;
- package resolution;
- plugin process topology;
- parser or template framework selection.

Those decisions require their respective RFCs or ADRs.

## 20. Acceptance Procedure

Acceptance requires:

1. architectural review of this proposal;
2. resolution or explicit deferral of recorded objections;
3. explicit project-owner approval recorded in the repository;
4. a separate patch incorporating accepted clauses into Constitution version 2.1;
5. an amendment entry identifying version 2.0 as superseded.

Until all five steps are complete, Project Constitution version 2.0 remains Approved and authoritative.
