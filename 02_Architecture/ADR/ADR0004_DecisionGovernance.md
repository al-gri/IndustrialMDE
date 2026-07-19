# ADR0004: Separate Language RFCs from Implementation ADRs

**Status:** Proposed

**Date:** 2026-07-19

## Context

Approved Project Constitution version 2.1 establishes separate authority for language and public-contract RFCs and for implementation ADRs. This ADR documents the detailed application of that constitutional boundary.

Using implementation ADRs as the complete language specification would mix user-visible language contracts with replaceable compiler choices. Using RFCs for every internal library or framework choice would make the language process depend on implementation details.

## Problem

IndustrialMDE needs a single, reviewable rule that determines:

- which decisions belong in RFCs;
- which decisions belong in ADRs;
- how Project Constitution amendments are handled;
- how status is established;
- how conflicts between records are resolved.

## Decision

Adopt the split governance model required by Approved Project Constitution version 2.1:

- **RFCs** define language syntax, language semantics, user-visible validation behavior, compatibility guarantees, and public language or target-extension contracts.
- **ADRs** record replaceable implementation decisions such as implementation language, parser framework, internal serialization, process topology, and concrete library selection.
- **Constitution amendments** are versioned proposals that have no normative effect until explicitly accepted and incorporated into the approved Constitution.
- **Compiler specifications** elaborate accepted RFCs and ADRs but cannot override them.

The Project Constitution remains the highest project-level normative authority.

The canonical RFC index records each RFC’s decision status and implementation status. A conversation, issue, or draft pull request does not establish `Accepted` status without explicit project-owner approval recorded in the repository.

## Alternatives Considered

### ADR-only governance

Rejected because implementation decisions and public language contracts have different audiences, lifecycles, and compatibility consequences.

### RFC-only governance

Rejected because replaceable implementation choices should not become language contracts.

### Informal separation without a governing record

Rejected because status and authority would remain ambiguous.

## Consequences

### Positive

- Language semantics remain independent of parser and compiler frameworks.
- Implementation choices can change without rewriting language specifications.
- Status, dependencies, and supersession become traceable.
- Public compatibility decisions receive an explicit review path.

### Negative

- Some features require both an RFC and one or more ADRs.
- Reviewers must verify that documents do not duplicate or contradict each other.
- Governance adds initial documentation overhead.

## Compliance

If accepted:

- `03_DSL/RFC/README.md` becomes the canonical RFC index and lifecycle definition;
- every RFC and ADR must carry an explicit status;
- a record conflicting with the Constitution must remain Proposed or be rejected until the Constitution is amended;
- implementation-specific notes inside RFCs must be clearly marked non-normative.

## Supersession

This ADR does not supersede an earlier substantive ADR. It replaces only the current undocumented assumption that ADRs alone can govern both language and implementation decisions.
