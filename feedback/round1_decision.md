# Round 1 Decision

## Feedback summary

- The core concept — AI-assisted spend category classification for a large industrial manufacturer — was well received; the overall idea and approach were validated as a strong fit
- Request to formalize the pitch into user stories with objective acceptance criteria, so a jury can verify claims are testable rather than asserted
- Request to organize the delivery timeline into clearly scoped sprints, with explicit in-scope and deferred items per sprint, rather than a single undifferentiated timeline
- No concerns raised about the industry, company size, or core use case selection itself

## Decision

**KEEP**

## Why

The feedback was entirely about *how the pitch is packaged and defended* — rigor, testability, and delivery discipline — not about the underlying industry, use case, or technical approach. Nothing in the feedback suggested the spend classification use case, the industrial goods sector, or the large-manufacturer company profile needs to change. The core idea (auto-classify messy spend data to surface concentration, fragmentation, and contract leakage) remains the right problem to deepen in Round 2.

## Round 2 focus

**POC improvements:**
- Expand the LangSmith evaluation set beyond 20 transactions, including deliberately harder/ambiguous edge cases
- Move from prompt-only JSON output to structured output / function-calling mode for guaranteed valid parsing (currently has a try/except fallback)
- Add few-shot examples to the classification prompt if accuracy needs improvement beyond the 85% zero-shot baseline

**MVP scope (the one capability that must run):**
- A small Streamlit or FastAPI app where a user uploads a spend CSV and receives back a classified dataset plus the same concentration/fragmentation/contract-leakage view currently built in PowerBI — this is the n8n POC's logic promoted into an actual lightweight product, not a from-scratch rebuild

**Compliance / ROI / strategy priorities:**
- EU AI Act: this is expected to classify as minimal/limited risk (text classification, no Annex III high-risk domain) — confirm this reasoning formally in `compliance/eu_ai_act_compliance.md`
- GDPR: spend/vendor data is predominantly B2B commercial data; DPIA should confirm the minimal personal-data footprint explicitly rather than assuming it
- ROI/risk: validate the Round 1 benchmark-based savings estimate ($104K–$209K) against Sprint 3's real pilot data before presenting it as a finalized number in Round 2
- Formalize `planning/user_stories.md` and `planning/sprint_plan.md` (built in response to this round's feedback) as living documents carried into Round 2 planning
