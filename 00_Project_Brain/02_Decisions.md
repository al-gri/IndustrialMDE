# Decision Index

This file is a concise index. It does not replace the normative RFC or ADR that records rationale, alternatives, consequences, and status.

## Project and Language Direction

| Decision | Status | Record |
| --- | --- | --- |
| Project Constitution version 2.1 | Approved; supersedes 2.0 | [`00_Project_Constitution.md`](00_Project_Constitution.md) |
| Project documentation and source material use English | Approved | Project Constitution, section 16 |
| Language design follows an RFC-first process | Approved direction; governance Proposed | [`RFC/README.md`](../03_DSL/RFC/README.md) |
| Separate language RFCs from implementation ADRs | Approved by Constitution; detailed ADR Proposed | Project Constitution, section 8; [`ADR0004_DecisionGovernance.md`](../02_Architecture/ADR/ADR0004_DecisionGovernance.md) |
| Incorporate Project Constitution version 2.1 | Approved and Incorporated | [`05_Constitution_Amendment_2.1.md`](05_Constitution_Amendment_2.1.md) |
| Promote RFC-0000, RFC-0001, and RFC-0001A to Proposed after architectural audit | Approved | [`06_Foundational_RFC_Review_Decisions.md`](06_Foundational_RFC_Review_Decisions.md) |
| Target generation must not bypass the canonical IR | Approved | Project Constitution, section 6 |
| Published compiler phase artifacts are immutable | Approved | Project Constitution, section 7 |
| Core Semantic Kernel with Industrial Profile roles | Proposed | [`RFC-0001A-Semantic-Object-Model.md`](../03_DSL/RFC/RFC-0001A-Semantic-Object-Model.md) |
| Definition, Instance Declaration, and expanded Instance are distinct | Proposed | [`RFC-0001A-Semantic-Object-Model.md`](../03_DSL/RFC/RFC-0001A-Semantic-Object-Model.md) |
| Domain, Application Assembly, and Deployment are separate semantic planes | Proposed | [`RFC-0001A-Semantic-Object-Model.md`](../03_DSL/RFC/RFC-0001A-Semantic-Object-Model.md) |

## Implementation Choices Requiring Complete ADRs

| Choice | Current status | ADR |
| --- | --- | --- |
| Python compiler implementation | Recorded; rationale incomplete | [`ADR0001_TechStack.md`](../02_Architecture/ADR/ADR0001_TechStack.md) |
| textX parser framework | Recorded; rationale incomplete | [`ADR0001_TechStack.md`](../02_Architecture/ADR/ADR0001_TechStack.md) |
| Jinja2 template engine | Recorded; rationale incomplete | [`ADR0001_TechStack.md`](../02_Architecture/ADR/ADR0001_TechStack.md) |
| Canonical immutable IR architecture | Approved principle; schema not defined | [`ADR0002_IR_Design.md`](../02_Architecture/ADR/ADR0002_IR_Design.md) |
| Strict plugin extension interfaces | Approved principle; isolation model not defined | [`ADR0003_CompilerArchitecture.md`](../02_Architecture/ADR/ADR0003_CompilerArchitecture.md) |

No implementation choice is considered fully documented until its ADR is substantive and explicitly accepted.
