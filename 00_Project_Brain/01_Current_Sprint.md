# Current Sprint

**Phase:** Foundational Language Architecture

**Status:** In Progress

**Current Goal:** Establish traceable language governance and a consistent foundational RFC baseline before production compiler implementation.

## Current Tasks

1. Review ADR0004 and the proposed detailed RFC governance contract under Approved Constitution 2.1.
2. Resolve review comments on the initial glossary and RFC template.
3. Review RFC-0000 and the canonical RFC-0001 as Proposed specifications.
4. Review RFC-0001A as a Proposed Core Semantic Kernel and Industrial Profile specification.
5. Review RFC-0001B conformance and acceptance gates as a Proposed specification.
6. Review Proposed RFC-0001C compilation-unit, module, package, dependency, lock, and visibility contracts.
7. Review Draft RFC-0001D strict JSON schema `0.1` as the public Project, Package, and Dependency Lock serialization contract.
8. Review Proposed RFC-0002 intrinsic domains, canonical value identity, compatibility, deterministic `REAL` boundaries, and conformance matrix.

## Deliverables Under Review

- [`ADR0004_DecisionGovernance.md`](../02_Architecture/ADR/ADR0004_DecisionGovernance.md)
- [`RFC/README.md`](../03_DSL/RFC/README.md)
- [`RFC/RFC-TEMPLATE.md`](../03_DSL/RFC/RFC-TEMPLATE.md)
- [`Glossary.md`](../03_DSL/Glossary.md)
- [`RFC-0000-Language-Design-Principles.md`](../03_DSL/RFC/RFC-0000-Language-Design-Principles.md)
- [`RFC-0001-Core-Language.md`](../03_DSL/RFC/RFC-0001-Core-Language.md)
- [`RFC-0001A-Semantic-Object-Model.md`](../03_DSL/RFC/RFC-0001A-Semantic-Object-Model.md)
- [`RFC-0001B-Identifiers-Scopes-and-Namespaces.md`](../03_DSL/RFC/RFC-0001B-Identifiers-Scopes-and-Namespaces.md)
- [`RFC-0001C-Compilation-Units-Modules-Packages-and-Dependencies.md`](../03_DSL/RFC/RFC-0001C-Compilation-Units-Modules-Packages-and-Dependencies.md)
- [`RFC-0001D-Project-Package-and-Dependency-Lock-Serialization.md`](../03_DSL/RFC/RFC-0001D-Project-Package-and-Dependency-Lock-Serialization.md)
- [`RFC-0002-Type-System.md`](../03_DSL/RFC/RFC-0002-Type-System.md)
- [`06_Foundational_RFC_Review_Decisions.md`](06_Foundational_RFC_Review_Decisions.md)
- [`07_RFC-0001B_Review_Decision.md`](07_RFC-0001B_Review_Decision.md)
- [`08_RFC-0001C_Review_Decision.md`](08_RFC-0001C_Review_Decision.md)
- [`09_RFC-0002_Review_Decision.md`](09_RFC-0002_Review_Decision.md)

## Decision Gates

- Verify every foundational RFC against Approved Project Constitution version 2.1 before acceptance.
- Keep version 1.0 stabilization guarantees deferred until reference-spike and conformance evidence exist.
- Resolve the package-boundary, visibility, import-cycle, naming-severity, and resource-limit gates identified by Proposed RFC-0001B.
- Review RFC-0001D serialization independently and resolve RFC-0001C package-authority ownership, public-signature closure, fingerprint-schema, and production-limit acceptance gates.
- Review the Proposed minimal Type System conformance matrix; the `REAL` exceptional-value Draft-to-Proposed gates are resolved.
- Define composition, connection, application-root, experimental grammar, and structural IR contracts before a full Structural Reference Spike.
- Define the boundary between normative specifications and an experimental reference compiler spike.
- Confirm which implementation choices are accepted after their ADRs contain rationale and consequences.

## Explicitly Deferred

- Production grammar and parser implementation.
- Production compiler phase interfaces.
- Multiple vendor targets, runtime systems, UI, and LSP implementation.
