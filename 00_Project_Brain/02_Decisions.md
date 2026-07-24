# Decision Index

This file is a concise index. It does not replace the normative RFC or ADR that records rationale, alternatives, consequences, and status.

## Project and Language Direction

| Decision | Status | Record |
| --- | --- | --- |
| Project Constitution version 2.1 | Approved; supersedes 2.0 | [`00_Project_Constitution.md`](00_Project_Constitution.md) |
| Project documentation and source material use English | Approved | Project Constitution, section 16 |
| Language design follows an RFC-first process | Approved direction; governance Proposed | [`RFC/README.md`](../03_DSL/RFC/README.md) |
| Separate language RFCs from implementation ADRs | Approved by Constitution; detailed ADR Proposed | Project Constitution, section 8; [`ADR0004_DecisionGovernance.md`](../02_Architecture/ADR/ADR0004_DecisionGovernance.md) |
| Incorporate Project Constitution version 2.1 | Approved and Incorporated | [`05_Constitution_Amendment_2.1.md`](05_Constitution_Amendment_2.1.md) |
| Promote RFC-0000, RFC-0001, and RFC-0001A to Proposed after architectural audit | Approved | [`06_Foundational_RFC_Review_Decisions.md`](06_Foundational_RFC_Review_Decisions.md) |
| Promote RFC-0001B to Proposed after semantic audit | Approved | [`07_RFC-0001B_Review_Decision.md`](07_RFC-0001B_Review_Decision.md) |
| Promote RFC-0001C to Proposed after independent architectural review and assign public serialization to RFC-0001D | Approved | [`08_RFC-0001C_Review_Decision.md`](08_RFC-0001C_Review_Decision.md) |
| Promote RFC-0002 to Proposed after resolving the binary64 `REAL` domain, Canonical Value Identity, and deterministic evaluation boundary | Approved | [`09_RFC-0002_Review_Decision.md`](09_RFC-0002_Review_Decision.md) |
| Approve `experimental-structural-input/0` and its 44-scenario fixture matrix for a separately gated loader | Approved review gate; contract remains Experimental | [`10_Structural_Input_Contract_Review_Decision.md`](10_Structural_Input_Contract_Review_Decision.md) |
| Accept the audited `experimental-structural-input/0` fixture-loader implementation at PR #15 head `d60fb889` | Accepted implementation gate; compiler remains on HOLD | [`11_Structural_Fixture_Loader_Implementation_Review_Decision.md`](11_Structural_Fixture_Loader_Implementation_Review_Decision.md) |
| Target generation must not bypass the canonical IR | Approved | Project Constitution, section 6 |
| Published compiler phase artifacts are immutable | Approved | Project Constitution, section 7 |
| Core Semantic Kernel with Industrial Profile roles | Proposed | [`RFC-0001A-Semantic-Object-Model.md`](../03_DSL/RFC/RFC-0001A-Semantic-Object-Model.md) |
| Definition, Instance Declaration, and expanded Instance are distinct | Proposed | [`RFC-0001A-Semantic-Object-Model.md`](../03_DSL/RFC/RFC-0001A-Semantic-Object-Model.md) |
| Domain, Application Assembly, and Deployment are separate semantic planes | Proposed | [`RFC-0001A-Semantic-Object-Model.md`](../03_DSL/RFC/RFC-0001A-Semantic-Object-Model.md) |

## Proposed and Draft Directions Under Review

| Direction | Status | Record |
| --- | --- | --- |
| One `.plant` source file is one Compilation Unit in language version 0.1 | Proposed | [`RFC-0001C`](../03_DSL/RFC/RFC-0001C-Compilation-Units-Modules-Packages-and-Dependencies.md) |
| Package Identity excludes version, content digest, alias, origin, and checkout path | Proposed | [`RFC-0001C`](../03_DSL/RFC/RFC-0001C-Compilation-Units-Modules-Packages-and-Dependencies.md) |
| A Project resolves at most one Package Revision per Package Identity | Proposed | [`RFC-0001C`](../03_DSL/RFC/RFC-0001C-Compilation-Units-Modules-Packages-and-Dependencies.md) |
| Package and Module dependency graphs are acyclic and use deterministic dependency-first scheduling | Proposed | [`RFC-0001C`](../03_DSL/RFC/RFC-0001C-Compilation-Units-Modules-Packages-and-Dependencies.md) |
| Cross-package access uses direct dependency aliases without transitive visibility or implicit re-export | Proposed | [`RFC-0001C`](../03_DSL/RFC/RFC-0001C-Compilation-Units-Modules-Packages-and-Dependencies.md) |
| Top-level declarations are private by default and Package exports require an exported Module | Proposed | [`RFC-0001C`](../03_DSL/RFC/RFC-0001C-Compilation-Units-Modules-Packages-and-Dependencies.md) |
| Language version `0.1` has one Project-wide version and no implicit prelude | Proposed | [`RFC-0001B`](../03_DSL/RFC/RFC-0001B-Identifiers-Scopes-and-Namespaces.md), [`RFC-0001C`](../03_DSL/RFC/RFC-0001C-Compilation-Units-Modules-Packages-and-Dependencies.md) |
| Public Project, Package, and Dependency Lock serialization uses strict JSON schema `0.1` | Draft | [`RFC-0001D`](../03_DSL/RFC/RFC-0001D-Project-Package-and-Dependency-Lock-Serialization.md) |
| Intrinsic type designators remain Identifier tokens and resolve through an explicit type-context rule rather than an implicit prelude | Proposed | [`RFC-0002`](../03_DSL/RFC/RFC-0002-Type-System.md) |
| Intrinsic Type Identity includes Language Version; build-local handles additionally retain Project resolution context | Proposed | [`RFC-0002`](../03_DSL/RFC/RFC-0002-Type-System.md) |
| `INT` and `TIME` use exact signed 64-bit-range semantic domains that target lowering must preserve without silent narrowing | Proposed | [`RFC-0002`](../03_DSL/RFC/RFC-0002-Type-System.md) |
| Minimum type compatibility is exact identity; declaration inference and all cross-type conversions are unsupported | Proposed | [`RFC-0002`](../03_DSL/RFC/RFC-0002-Type-System.md) |
| `REAL` uses binary64 with signed zeros, signed infinities, one canonical quiet NaN, and no signaling-NaN Semantic Model value | Proposed | [`RFC-0002`](../03_DSL/RFC/RFC-0002-Type-System.md) |
| `REAL` Canonical Value Identity is distinct from numeric equality; signed zeros remain distinct and quiet-NaN payloads canonicalize | Proposed | [`RFC-0002`](../03_DSL/RFC/RFC-0002-Type-System.md) |
| RFC-0003 must provide bit-exact binary64 compile-time evaluation and cannot defer a compile-time Constant to Target IR | Proposed | [`RFC-0002`](../03_DSL/RFC/RFC-0002-Type-System.md), [`09_RFC-0002_Review_Decision.md`](09_RFC-0002_Review_Decision.md) |
| RFC-0005 separates a Spike A Structural Layer from a Runtime Layer gated by RFC-0003 and RFC-0004 | Draft | [`RFC-0005`](../03_DSL/RFC/RFC-0005-Signals-Ports-and-Connections.md) |
| Expanded Instance, Endpoint, and Connection occurrence identities are typed tuples rather than delimiter-concatenated strings | Draft | [`RFC-0006`](../03_DSL/RFC/RFC-0006-Composition-and-Interfaces.md) |
| Application Assembly selection is an explicit extralinguistic root-Package build input with no source-order or implicit-main fallback | Draft | [`RFC-0007`](../03_DSL/RFC/RFC-0007-Application-and-Deployment.md) |
| Spike A uses an explicitly non-conforming and non-interoperable Experimental Structural Snapshot instead of Canonical IR | Experimental | [`Spike_A_Experimental_Snapshot.md`](../02_Architecture/Spike_A_Experimental_Snapshot.md) |
| Spike A receives expression-free Collected Structural Input through the closed, non-conforming `experimental-structural-input/0` fixture contract | Experimental | [`Spike_A_Experimental_Input.md`](../02_Architecture/Spike_A_Experimental_Input.md) |
| Spike A step 1 produces immutable `experimental-resolved-structural-model/0` with no-winner collision groups, structured identities, resolved or explicit invalid references, and closure-neutral diagnostics | Experimental design; implementation HOLD | [`Spike_A_Step_1_Resolution.md`](../02_Architecture/Spike_A_Step_1_Resolution.md) |

## Implementation Choices Requiring Complete ADRs

| Choice | Current status | ADR |
| --- | --- | --- |
| Python compiler implementation | Recorded; rationale incomplete | [`ADR0001_TechStack.md`](../02_Architecture/ADR/ADR0001_TechStack.md) |
| textX parser framework | Recorded; rationale incomplete | [`ADR0001_TechStack.md`](../02_Architecture/ADR/ADR0001_TechStack.md) |
| Jinja2 template engine | Recorded; rationale incomplete | [`ADR0001_TechStack.md`](../02_Architecture/ADR/ADR0001_TechStack.md) |
| Canonical immutable IR architecture | Approved principle; schema not defined | [`ADR0002_IR_Design.md`](../02_Architecture/ADR/ADR0002_IR_Design.md) |
| Strict plugin extension interfaces | Approved principle; isolation model not defined | [`ADR0003_CompilerArchitecture.md`](../02_Architecture/ADR/ADR0003_CompilerArchitecture.md) |
| Disposable Structural Spike A fixture-loader stack | Accepted after `AUDIT-PR14-PHASE-A`; Phase B implementation accepted after `AUDIT-PR15-PHASE-B`; compiler HOLD | [`ADR0005_StructuralSpikeFixtureLoader.md`](../02_Architecture/ADR/ADR0005_StructuralSpikeFixtureLoader.md), [`11_Structural_Fixture_Loader_Implementation_Review_Decision.md`](11_Structural_Fixture_Loader_Implementation_Review_Decision.md) |
| Disposable Structural Spike A Step-1 resolver stack | Proposed; requires independent Phase A audit and explicit acceptance; Phase B HOLD | [`ADR0006_StructuralSpikeStep1Resolver.md`](../02_Architecture/ADR/ADR0006_StructuralSpikeStep1Resolver.md) |

No implementation choice is considered fully documented until its ADR is substantive and explicitly accepted.
