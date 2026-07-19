# Next Tasks

## P0 — Foundational Consistency

1. Draft and review Project Constitution version 2.1 amendments.
2. Create `03_DSL/RFC/README.md` as the canonical RFC index and governance document.
3. Create a project glossary for language, compiler, and industrial-domain terminology.
4. Create RFC-0000: Language Design Principles.
5. Confirm and create canonical RFC-0001: Core Language and Lexical Structure.
6. Create RFC-0001A: Semantic Object Model.
7. Create RFC-0001B: Identifiers, Scopes, and Namespaces.
8. Create RFC-0001C: Compilation Units, Modules, Packages, and Dependencies.

## P1 — Minimum Executable Specification

1. Define the minimum type-system subset required by a reference spike.
2. Define positive, negative, boundary, and compatibility examples.
3. Specify stable diagnostic codes and deterministic diagnostic ordering.
4. Define source-to-semantic-to-IR traceability requirements.
5. Plan a limited Source → Semantic Model → Canonical IR → Mock Target vertical slice.

## Deferred Until Foundational Review

- Production `plant.tx` grammar.
- Production parser, AST, symbol table, and semantic analyzer.
- Vendor emitters, runtime, UI, LSP, and package registry.
