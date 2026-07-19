# Current Sprint

**Phase:** Foundational Language Architecture

**Status:** In Progress

**Current Goal:** Establish traceable language governance and a consistent foundational RFC baseline before production compiler implementation.

## Current Tasks

1. Review the proposed Project Constitution version 2.1 amendment.
2. Review ADR0004 and the proposed RFC governance contract.
3. Resolve review comments on the initial glossary and RFC template.
4. Review RFC-0000 and the canonical RFC-0001 Drafts.
5. Draft RFC-0001A around a core semantic kernel with explicit definitions and instances.
6. Draft RFC-0001B identifier, scope, namespace, and import rules.
7. Create RFC-0001C for compilation units, modules, packages, and dependencies.

## Deliverables Under Review

- [`05_Constitution_Amendment_2.1.md`](05_Constitution_Amendment_2.1.md)
- [`ADR0004_DecisionGovernance.md`](../02_Architecture/ADR/ADR0004_DecisionGovernance.md)
- [`RFC/README.md`](../03_DSL/RFC/README.md)
- [`RFC/RFC-TEMPLATE.md`](../03_DSL/RFC/RFC-TEMPLATE.md)
- [`Glossary.md`](../03_DSL/Glossary.md)
- [`RFC-0000-Language-Design-Principles.md`](../03_DSL/RFC/RFC-0000-Language-Design-Principles.md)
- [`RFC-0001-Core-Language.md`](../03_DSL/RFC/RFC-0001-Core-Language.md)

## Decision Gates

- Approve or reject the Core Semantic Kernel + Industrial Profiles direction.
- Define the boundary between normative specifications and an experimental reference compiler spike.
- Confirm which implementation choices are accepted after their ADRs contain rationale and consequences.

## Explicitly Deferred

- Production grammar and parser implementation.
- Production compiler phase interfaces.
- Multiple vendor targets, runtime systems, UI, and LSP implementation.
