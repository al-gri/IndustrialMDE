# Next Tasks

## P0 — Foundational Consistency

1. Review ADR0004 and the proposed detailed RFC governance contract.
2. Review Proposed RFC-0000 against Approved Project Constitution version 2.1 before acceptance.
3. Review Proposed RFC-0001 conformance cases before acceptance.
4. Review Proposed RFC-0001A conformance cases before acceptance.
5. Review Proposed RFC-0001B conformance cases and resolve its delegated gates before acceptance.
6. Review Proposed RFC-0001C conformance cases and resolve its delegated acceptance gates.
7. Review Draft RFC-0001D schema `0.1`, including duplicate handling, canonical serialization, diagnostics, and migration.

## P1 — Minimum Executable Specification

1. Review Draft RFC-0002, resolve its `REAL` exceptional-value gates, and verify its conformance matrix before Proposed consideration.
2. Define the minimum RFC-0005, RFC-0006, and RFC-0007 structural slices required for Endpoint, Connection, composition, and Application Assembly roots.
3. Define explicit experimental grammar and structural IR snapshot contracts without representing them as Accepted syntax or Canonical IR.
4. Define positive, negative, boundary, compatibility, randomized-order, and integrity examples.
5. Specify stable diagnostic codes and deterministic diagnostic ordering.
6. Define source-to-semantic-to-IR traceability requirements.
7. Plan a limited Source → Semantic Model → structural IR snapshot → Mock Structural Target vertical slice.

## Deferred Until Foundational Review

- Production `plant.tx` grammar.
- Production parser, AST, symbol table, and semantic analyzer.
- Vendor emitters, runtime, UI, LSP, and package registry.
