# Decision Index

This file is a concise index. It does not replace the normative RFC or ADR that records rationale, alternatives, consequences, and status.

## Project and Language Direction

| Decision | Status | Record |
| --- | --- | --- |
| Project Constitution version 2.0 | Approved | [`00_Project_Constitution.md`](00_Project_Constitution.md) |
| Project documentation and source material use English | Approved; normative record pending | Project owner decision |
| Language design follows an RFC-first process | Approved direction; governance Proposed | [`RFC/README.md`](../03_DSL/RFC/README.md) |
| Separate language RFCs from implementation ADRs | Proposed | [`ADR0004_DecisionGovernance.md`](../02_Architecture/ADR/ADR0004_DecisionGovernance.md) |
| Amend Project Constitution to version 2.1 | Proposed | [`05_Constitution_Amendment_2.1.md`](05_Constitution_Amendment_2.1.md) |
| Target generation must not bypass the canonical IR | Approved principle | Project Constitution, section 7 |
| Published compiler phase artifacts are immutable | Approved principle; detailed contract pending | Project Constitution, section 3 |

## Implementation Choices Requiring Complete ADRs

| Choice | Current status | ADR |
| --- | --- | --- |
| Python compiler implementation | Recorded; rationale incomplete | [`ADR0001_TechStack.md`](../02_Architecture/ADR/ADR0001_TechStack.md) |
| textX parser framework | Recorded; rationale incomplete | [`ADR0001_TechStack.md`](../02_Architecture/ADR/ADR0001_TechStack.md) |
| Jinja2 template engine | Recorded; rationale incomplete | [`ADR0001_TechStack.md`](../02_Architecture/ADR/ADR0001_TechStack.md) |
| Canonical immutable IR architecture | Approved principle; schema not defined | [`ADR0002_IR_Design.md`](../02_Architecture/ADR/ADR0002_IR_Design.md) |
| Strict plugin extension interfaces | Approved principle; isolation model not defined | [`ADR0003_CompilerArchitecture.md`](../02_Architecture/ADR/ADR0003_CompilerArchitecture.md) |

No implementation choice is considered fully documented until its ADR is substantive and explicitly accepted.
