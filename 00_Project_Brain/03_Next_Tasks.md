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
5. Input-contract review complete: `experimental-structural-input/0` received `GO` at exact head `7fdbfbc`; see `10_Structural_Input_Contract_Review_Decision.md`.
6. Fixture gate complete: all 44 positive, negative, boundary, randomized-order, limit, and referential-integrity scenarios are approved for the structural subset.
7. ADR0005 review complete: `AUDIT-PR14-PHASE-A` returned `GO` against exact Phase A head `9bffef77`, and explicit Project Owner acceptance is recorded in the ADR.
8. Fixture Loader Phase B review complete: `AUDIT-PR15-PHASE-B` returned `IMPLEMENTATION GO / COMPILER HOLD` against exact head `d60fb889`, and the Project Owner accepted the result in `11_Structural_Fixture_Loader_Implementation_Review_Decision.md`.
9. Structural Reference Spike A step-1 Phase A design is prepared in `Spike_A_Step_1_Resolution.md` and Proposed ADR0006 against exact authorized base `1c48928`; request independent `AUDIT-STEP1-PHASE-A`. No source, fixture, test, dependency, or lock implementation is authorized.
10. After a positive Phase A audit, require explicit Project Owner acceptance recorded at the exact reviewed head, then require `AUTHORIZE TE-STRUCTURAL-SPIKE-STEP-1 PHASE B AT <accepted-gate-a-commit>` before implementation. Step 2a and every later phase remain on HOLD.

## Deferred Until Foundational Review

- Production `plant.tx` grammar.
- Production parser, AST, symbol table, and semantic analyzer.
- Vendor emitters, runtime, UI, LSP, and package registry.
