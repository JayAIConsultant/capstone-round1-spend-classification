# Use Case Definition — AI-Powered Spend Intelligence for Industrial Manufacturers

## Business problem statement

Large industrial manufacturers route 60–70% of their costs through procurement, yet most cannot answer basic questions about that spend — which categories it falls into, which suppliers concentrate risk, which purchases bypass negotiated contracts, or which sourcing origins carry meaningful tariff and geopolitical exposure — without weeks of manual analysis. This isn't a data availability problem; the transaction records exist. It's a *usability* problem: raw ERP exports are messy, inconsistently categorized, and disconnected from the external risk context (tariffs, trade policy) that increasingly determines whether a sourcing decision is still sound.

## Company profile

**Industry:** Industrial goods manufacturing — capital equipment / heavy machinery
**Size:** Large, multi-plant, multi-country (plants in Germany, Mexico, Vietnam, and the US in our working example)
**Current state:** Procurement data exists in ERP systems but lacks consistent categorization, contract-compliance visibility, and any systematic view of geopolitical/tariff exposure across the supplier base. Spend analysis today is manual, slow, and reactive.

## Proposed AI solution and system type

A hybrid AI system, delivered as a self-service web application, combining three distinct AI/analytical approaches rather than one:

1. **Zero-shot LLM classification** — categorizes raw, messy spend transactions into a standard taxonomy without requiring pre-labeled training data (proven in Round 1: 85% accuracy)
2. **Statistical analysis** — supplier concentration/fragmentation metrics, contract-compliance cross-referencing, and freight-cost outlier detection
3. **Retrieval-Augmented Generation (RAG)** — assigns a geopolitical/tariff risk tier to each transaction by retrieving relevant, cited tariff context (product category + vendor country) and having an LLM synthesize a risk assessment with stated reasoning

The application supports two modes: a one-click demo using our synthetic dataset (guaranteed to showcase all five modules), and a bring-your-own-data mode where a user uploads their own spend export (core classification and dashboard always run; contract-compliance and geopolitical modules activate if the user also provides a contract list and/or vendor-country mapping).

## Key stakeholders and interests

| Stakeholder | Interest |
|---|---|
| CEO / executive sponsor | Wants to know: where does our money go, and what's the risk exposure I don't currently see? |
| Procurement manager | Wants actionable visibility: concentration, fragmentation, contract leakage — without manual pulling |
| Compliance / legal officer | Wants assurance the AI is auditable, and visibility into geopolitical/tariff exposure that could create supply continuity risk |
| Finance stakeholder | Wants an honest, assumption-explicit cost-benefit case, not an inflated ROI claim |
| IT / data team | Wants a system that doesn't require live ERP integration or new infrastructure to pilot |

## Success criteria (measurable)

1. **Classification accuracy ≥80%** against human-labeled ground truth, measured via a scored evaluation (not an unscored demo) — Round 1 achieved 85%
2. **Time-to-insight**: categorized spend visibility produced in under 5 minutes for a comparable dataset, versus the "weeks of manual pulling" baseline
3. **Geopolitical risk differentiation**: the RAG module must assign meaningfully different risk tiers across at least 3 distinct country/category combinations with cited reasoning — not a flat, undifferentiated score
4. **Contract-compliance detection**: correctly flags 100% of transactions present in an uploaded contract list as "under contract" (a precision check on the join logic, not a judgment call)

## Out-of-scope boundaries

- No live ERP or procurement-system integration — file upload only
- No comprehensive HS/HTS-code-level customs classification — the geopolitical module uses a curated, dated snapshot of real tariff facts (~20 sources), not the full federal tariff schedule
- No production-grade authentication, multi-tenancy, or enterprise security — this is an MVP, not a production deployment (see `strategic_plan.md` for the production migration path)
- Fixed six-category taxonomy — not user-configurable in this version
- Freight variance uses statistical outlier detection within the dataset itself, not an external cost-benchmarking model (kept distinct from the separate should-cost benchmarking capstone)

## Evolution from Round 1

**Round 1** built and proved one capability: AI-assisted spend category classification, demonstrated via an n8n workflow and scored via a LangSmith evaluation (85% accuracy). Two additional use cases — maverick spend detection and freight cost variance — were explicitly scoped as roadmap items, not built.

**Decision: KEEP.** Feedback on the Round 1 pitch validated the core concept and requested formalization into user stories with acceptance criteria and a sprint-organized delivery plan (see `planning/`) — no change to industry, company size, or core use case.

**Scope expansion for Round 2 (deliberate, not scope creep):** Rather than building only the minimum required MVP (classification + dashboard), the scope was intentionally expanded to include Maverick Spend Detection and Freight Cost Variance — both originally Round 1 roadmap items — plus a new Geopolitical Risk module built on Retrieval-Augmented Generation. This decision was made explicitly, weighing the added build time against the value of a more differentiated, consulting-relevant demonstration, and is judged worth the trade-off given the two-week Round 2 window. The geopolitical risk module in particular directly targets the kind of tariff/supply-chain-diversification problem currently live in global industrial procurement — a deliberate positioning choice, not an arbitrary feature addition.
