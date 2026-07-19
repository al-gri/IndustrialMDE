# Current Sprint

**Phase:** Foundational Language Architecture

**Status:** In Progress

**Current Goal:** Establish traceable language governance and a consistent foundational RFC baseline before production compiler implementation.

## Current Tasks

1. Review ADR0004 and the proposed detailed RFC governance contract under Approved Constitution 2.1.
2. Resolve review comments on the initial glossary and RFC template.
3. Review RFC-0000 and the canonical RFC-0001 as Proposed specifications.
4. Review RFC-0001A as a Proposed Core Semantic Kernel and Industrial Profile specification.
5. Draft RFC-0001B identifier, scope, namespace, and import rules.
6. Create RFC-0001C for compilation units, modules, packages, and dependencies.

## Deliverables Under Review

- [`ADR0004_DecisionGovernance.md`](../02_Architecture/ADR/ADR0004_DecisionGovernance.md)
- [`RFC/README.md`](../03_DSL/RFC/README.md)
- [`RFC/RFC-TEMPLATE.md`](../03_DSL/RFC/RFC-TEMPLATE.md)
- [`Glossary.md`](../03_DSL/Glossary.md)
- [`RFC-0000-Language-Design-Principles.md`](../03_DSL/RFC/RFC-0000-Language-Design-Principles.md)
- [`RFC-0001-Core-Language.md`](../03_DSL/RFC/RFC-0001-Core-Language.md)
- [`RFC-0001A-Semantic-Object-Model.md`](../03_DSL/RFC/RFC-0001A-Semantic-Object-Model.md)
- [`06_Foundational_RFC_Review_Decisions.md`](06_Foundational_RFC_Review_Decisions.md)

## Decision Gates

- Verify every foundational RFC against Approved Project Constitution version 2.1 before acceptance.
- Keep version 1.0 stabilization guarantees deferred until reference-spike and conformance evidence exist.
- Define identifier, scope, namespace, qualification, import, and collision rules in RFC-0001B.
- Define the boundary between normative specifications and an experimental reference compiler spike.
- Confirm which implementation choices are accepted after their ADRs contain rationale and consequences.

## Explicitly Deferred

- Production grammar and parser implementation.
- Production compiler phase interfaces.
- Multiple vendor targets, runtime systems, UI, and LSP implementation.
