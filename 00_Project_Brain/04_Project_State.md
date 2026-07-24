# Project State

**Phase:** Foundational Language Architecture

**Last Reconciled:** 2026-07-24

Percent-complete estimates are intentionally omitted until measurable acceptance criteria exist.

| Area | State | Evidence or next requirement |
| --- | --- | --- |
| Repository structure | Present | Initial project backbone committed |
| Project Constitution | Approved, version 2.1 | Highest normative document; version 2.0 is Superseded |
| Constitution 2.1 amendment | Accepted and Incorporated | Historical approval and supersession record retained |
| Project Brain | Present | Current focus and backlog reconciled with repository reality |
| README | Present | Describes current scope and repository map |
| RFC governance and index | Proposed, version 0.1 | Not normative until governance review is accepted |
| RFC template | Draft | Initial review artifact present |
| Project glossary | Draft, version 0.1 | Terms remain subordinate to Accepted RFCs |
| Foundational language RFCs | Partially Proposed and Draft | RFC-0000, RFC-0001, RFC-0001A, RFC-0001B, RFC-0001C, and RFC-0002 are Proposed; RFC-0001D, RFC-0005, RFC-0006, and RFC-0007 are Draft |
| Architecture specifications | Experimental contracts present; Step-1 design under review | `Spike_A_Experimental_Snapshot.md` and `experimental-structural-input/0` remain the reviewed boundaries; `experimental-resolved-structural-model/0` now has a Phase A design requiring independent audit; Canonical IR and production pipeline contracts remain undefined |
| ADRs | Incomplete | ADR0001–ADR0003 are empty; ADR0004 and spike-only Step-1 ADR0006 are Proposed; spike-only fixture-loader ADR0005 is Accepted |
| Language examples | Not present | Add after foundational syntax and semantics are drafted |
| Grammar and parser | Production parser not implemented; experimental fixture loader accepted | `AUDIT-PR15-PHASE-B` and Project Owner acceptance cover only the expression-free JSON fixture boundary at reviewed head `d60fb889`; `.plant` grammar, production parsing, and compiler steps remain on HOLD |
| Compiler core and canonical IR | Not implemented; experimental Step-1 design proposed | `Spike_A_Step_1_Resolution.md` defines only the disposable identity/resolution boundary; ADR0006 is not Accepted and Phase B remains on HOLD; Canonical IR is undefined |
| Target lowering and emitters | Not implemented | Target model not yet defined |
| Tests and conformance suite | Experimental loader evidence accepted | `78` locked-environment tests execute all 44 reviewed scenarios with the exact 35-success/9-failure loader partition; `AUDIT-PR15-PHASE-B` accepted this evidence without creating production language conformance |
