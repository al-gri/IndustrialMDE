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

1. Review Proposed RFC-0002 conformance and diagnostic matrices before acceptance; its `REAL` exceptional-value Draft-to-Proposed gates are resolved.
2. Review Draft RFC-0005's Structural/Runtime split and confirm that its Spike A layer has no RFC-0003 or RFC-0004 dependency.
3. Review Draft RFC-0006 and RFC-0007 composition, occurrence-identity, multiple-root, and explicit Assembly-selection contracts.
4. Review `experimental-structural-snapshot/0`, its nine-step validation pipeline, all-or-nothing publication rule, and `SPIKEA` diagnostic domain.
5. Define a separate experimental input grammar or fixture contract limited to Definitions, Instances, Endpoints, Connections, and Application Assemblies, with expressions explicitly excluded.
6. Approve positive, negative, boundary, randomized-order, limit, and referential-integrity fixtures for the structural subset.
7. After the documentation gates are approved, authorize a bounded implementation Task Envelope for the non-conforming Structural Reference Spike A.

## Deferred Until Foundational Review

- Production `plant.tx` grammar.
- Production parser, AST, symbol table, and semantic analyzer.
- Vendor emitters, runtime, UI, LSP, and package registry.
