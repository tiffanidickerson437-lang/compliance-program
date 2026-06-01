# ISO/IEC 42001:2023 alignment

ISO/IEC 42001:2023 is the AI management system (AIMS) standard: the AI-specific counterpart to ISO/IEC 27001. This document maps the owned control set to the clauses and Annex A controls of 42001, and it is named honestly as a forward target. The program demonstrates alignment to the AIMS structure; it does not claim certification. ISO 42001 adoption is still early, and stating alignment as a direction rather than an accomplishment is the accurate position.

Direct catalog crosswalk (real references from `02-controls/framework-crosswalk.yaml`):

| Control | ISO/IEC 42001:2023 references |
|---------|-------------------------------|
| AAT-01 | 5.1, 8.1, A.2.2, A.6.2.2 |

## Management system clauses

ISO 42001 is built on the Annex SL management-system structure (clauses 4 through 10). The program maps to it as follows.

- 5.1 Leadership and commitment: AAT-01 establishes that AI risk policy is defined, owned, and enforced, with a quarterly governance review and a DPIA on material change. Accountability sits with named functions in the AAT-01 RACI.
- 8.1 Operational planning and control: the authorization broker, the human oversight gate, and the model change-management gate are the operational controls that plan and control how AI runs in production. This is where 42001 operation is most concretely satisfied.
- Clauses 4 (context), 6 (planning), 7 (support), 9 (performance evaluation), and 10 (improvement) are partially addressed through the wider program (risk register, governance charter, evaluation gate, and post-incident review) and are named as a forward target for a formal AIMS.

## Annex A controls

Annex A of 42001 organizes AI controls into themes. The table records where the program already has an operating control and where the theme is a forward target.

| Annex A theme | Program position | Where it lives |
|---------------|------------------|----------------|
| A.2 Policies related to AI (incl. A.2.2 AI policy) | Operating: AI acceptable-use policy and AAT-01 govern AI risk | `ai-acceptable-use-policy-summary.md`, AAT-01 |
| A.3 Internal organization | Operating: roles and accountability per AAT-01 RACI | AAT-01, `agent-governance.md` |
| A.4 Resources for AI systems | Forward target: full resource and competence documentation | program governance |
| A.5 Assessing impacts of AI systems | Operating: DPIA and use-case impact mapping | `eu-ai-act-readiness.md`, DPIA |
| A.6 AI system life cycle (incl. A.6.2.2 requirements and specification) | Operating: model change management with eval, drift, rollback, and approval gate | `model-change-management.md` |
| A.7 Data for AI systems | Operating: AI data classification, restricted classes, provenance | `ai-control-set.md`, OWASP LLM04 mapping |
| A.8 Information for interested parties | Operating: customer-facing responsible-AI statement | `responsible-ai-statement.md` |
| A.9 Use of AI systems | Operating: acceptable-use policy and human oversight gates | `ai-acceptable-use-policy-summary.md`, `agent-governance.md` |
| A.10 Third-party and customer relationships | Operating: AI vendor and model-provider risk under TPM-01 | TPM-01, `model-change-management.md` |

## A.6.2.2 in detail

A.6.2.2 (AI system requirements and specification, within the AI system life cycle) is satisfied operationally by `model-change-management.md`. Every model, prompt, and tool-grant change is specified as a tracked work item, evaluated against a held-out suite, drift-checked, and approved through a human gate before it reaches production. The specification and its acceptance criteria are recorded on the change, so the life-cycle requirement is evidenced, not asserted.

## The honest forward-target framing

What is operating today: AI risk policy, agent authorization and least privilege, the human oversight gate, model change management, AI data classification, AI incident response, and AI vendor risk. These map cleanly to 42001 clause 8 operation and several Annex A themes.

What is a forward target: a formally documented and audited AI management system (clauses 4, 6, 7, 9, 10 in full, internal audit of the AIMS, and management review of the AIMS as a system). Reaching that is a maturity step, not a relabeling of what exists. Naming it as a forward target is the difference between a program that can be trusted and one that overstates.

## One control, three AI frameworks

AAT-01 answers ISO 42001, NIST AI RMF, and the EU AI Act from a single definition. The agent spec in `agent-governance.md` is the artifact behind all three. This is the thesis of the program: one owned control, evidence collected once, every framework and audience served.
