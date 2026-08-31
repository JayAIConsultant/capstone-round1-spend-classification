# User Stories & Acceptance Criteria

These formalize the pitch into testable commitments — each written from the perspective of who benefits, with objective pass/fail criteria rather than prose claims.

## 1. Procurement Analyst — Automated Classification

**As a** procurement analyst, **I want** raw spend transactions automatically classified into standard categories, **so that** I'm not manually tagging thousands of line items.

**Acceptance criteria:**
- [x] Given a batch of unclassified transactions, every transaction receives a category from the six defined types (no transaction left unclassified or dropped)
- [x] Classification accuracy is ≥80% against human-labeled ground truth — **measured: 85% (17/20) in Round 1 evaluation**
- [x] Any classification below 0.7 confidence is routed to human review, never silently accepted into the classified dataset

## 2. Procurement Manager — Concentration & Fragmentation Visibility

**As a** procurement manager, **I want** to see spend concentration and fragmentation by category, **so that** I can identify consolidation opportunities.

**Acceptance criteria:**
- [x] Dashboard displays top-3 supplier share (%) per category
- [x] Dashboard displays distinct supplier count per category
- [x] Both metrics recalculate automatically from the latest classified dataset — no manual pivot-table work required

## 3. Procurement Manager — Contract Leakage Visibility

**As a** procurement manager, **I want** visibility into off-contract spend, **so that** I can quantify and act on contract leakage.

**Acceptance criteria:**
- [x] Dashboard shows % and $ split between under-contract and off-contract spend, overall and by category
- [x] The single largest off-contract exposure category is clearly identifiable at a glance (Round 1 finding: Capex Components, $925K off-contract)

## 4. Compliance Stakeholder — Auditability

**As a** compliance stakeholder, **I want** every AI classification decision to be traceable, **so that** I can verify this is not an unaccountable black box.

**Acceptance criteria:**
- [x] Every classification call is logged with its input, output, confidence score, and stated reasoning
- [x] Logs are queryable and exportable for audit (LangSmith experiment view)
- [x] Accuracy is demonstrated through a scored evaluation against known-correct labels, not asserted from an unscored demo

## 5. Finance Stakeholder — Honest Cost-Benefit Case

**As a** finance stakeholder, **I want** a cost-benefit case with explicit assumptions, **so that** I can approve funding with clear eyes on the risk.

**Acceptance criteria:**
- [x] Cost estimate states its assumptions explicitly (team composition, day rate, scope boundaries)
- [x] Savings estimate is broken into named, independently-defensible levers (not one blended number)
- [x] A go/no-go decision point is defined at a specific week with a specific, measurable success threshold

---

**Note on status:** all Round 1 acceptance criteria above are met using the synthetic dataset and 20-transaction evaluation sample (see `data/dataset_documentation.md` and `langsmith/langsmith_documentation.md` for what's synthetic vs. live). Round 2's pilot (Sprint 3, see `planning/sprint_plan.md`) re-validates these same criteria against one plant's real, live data — the actual bar this system must clear before scaling further.
