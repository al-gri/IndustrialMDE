# IndustrialMDE

IndustrialMDE is a model-driven engineering platform for declaratively describing industrial automation systems and deterministically generating target artifacts.

The project is currently establishing its language architecture and governance. It is not yet a working compiler.

## Current Status

- The repository structure and Project Brain exist.
- [Project Constitution version 2.1](00_Project_Brain/00_Project_Constitution.md) is Approved and supersedes version 2.0.
- The Constitution 2.1 amendment is Accepted and Incorporated; detailed RFC lifecycle rules remain Proposed for review.
- [RFC-0000](03_DSL/RFC/RFC-0000-Language-Design-Principles.md), the canonical [RFC-0001](03_DSL/RFC/RFC-0001-Core-Language.md), [RFC-0001A](03_DSL/RFC/RFC-0001A-Semantic-Object-Model.md), and [RFC-0001B](03_DSL/RFC/RFC-0001B-Identifiers-Scopes-and-Namespaces.md) are Proposed review artifacts.
- [RFC-0001C](03_DSL/RFC/RFC-0001C-Compilation-Units-Modules-Packages-and-Dependencies.md) is a Proposed review artifact.
- [RFC-0001D](03_DSL/RFC/RFC-0001D-Project-Package-and-Dependency-Lock-Serialization.md) is a Draft public-serialization review artifact.
- [RFC-0002](03_DSL/RFC/RFC-0002-Type-System.md) is a Proposed minimal Type System review artifact.
- Compiler source code, grammar, emitters, and tests have not been implemented.

The authoritative status is maintained in [Project State](00_Project_Brain/04_Project_State.md). Current work is listed in [Current Sprint](00_Project_Brain/01_Current_Sprint.md) and [Next Tasks](00_Project_Brain/03_Next_Tasks.md).

## Current Direction

The immediate objective is to establish a consistent foundational language package before production compiler development:

1. review and accept RFC lifecycle and indexing details under Approved Constitution 2.1;
2. review the Proposed language-principles and lexical contracts;
3. review the Proposed core semantic model and the Proposed identifier, scope, namespace, and import rules;
4. review the Proposed compilation-unit, module, package, dependency, lock, and visibility contracts;
5. review the Draft strict JSON Project, Package, and Dependency Lock serialization contract;
6. review the Proposed minimum Type System conformance matrix and define the structural companion slices required by a deliberately limited reference compiler spike.

## Repository Map

- [`00_Project_Brain/`](00_Project_Brain/) — project constitution, current focus, decisions, backlog, and state.
- [`01_Documentation/`](01_Documentation/) — engineering and quality documentation placeholders.
- [`02_Architecture/`](02_Architecture/) — architecture specifications and ADR placeholders.
- [`03_DSL/`](03_DSL/) — proposed RFC governance, glossary, future language RFCs, examples, and grammar specifications.
- `04_Compiler/` — future compiler implementation.
- `09_Testing/` — future conformance and implementation tests.

## Governance

- Project and source documentation is written in English.
- Language behavior is specified through RFCs.
- Implementation architecture is justified through ADRs.
- Fundamental changes require review and explicit approval before implementation.
- Target generation must use the canonical intermediate representation rather than bypassing it through source- or template-specific logic.
