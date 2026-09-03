# Strategic Deployment and Commercialization Plan

## Phases: POC → Pilot → Full Deployment → Scale

### Phase 1 — POC (Complete, Round 1)
n8n classification workflow + LangSmith scored evaluation, proving the core AI mechanism works (85% zero-shot accuracy). No further work needed here.

### Phase 2 — Pilot (Weeks 1–10, one plant)
Full detail already in `cost_estimation/timeline_estimate.md`: discovery → pipeline build → dashboard build → live validation against one plant's real spend data → go/no-go decision at week 10. Cost: $37,500–$56,200.

### Phase 3 — Full Deployment (Months 3–8, ~4–6 months build-out, all plants)
Migration from MVP (Streamlit, single-tenant, no auth) to production architecture: proper database, enterprise SSO, ERP integration across all plants, client-owned cloud infrastructure. Cost: $530,000–$870,000 upfront, $135,000–$200,000/year ongoing (see `roi_risk_assessment.md`).

### Phase 4 — Scale (Month 9+)
Two distinct meanings worth separating, since they have different KPIs and different owners:
- **Scale the engagement** (deepen at the existing client): extend geopolitical risk coverage beyond the US import regime to EU/Mexican/Vietnamese customs (see `mvp_documentation.md`'s stated limit), tighten the classification taxonomy, expand maverick spend detection with richer contract data
- **Scale the practice** (grow beyond this one client): package the methodology for the next manufacturer engagement — this is where the commercialization model below actually gets tested

## Timeline and milestones

| Milestone | Timing | Gate/Decision |
|---|---|---|
| Pilot go/no-go | End of Week 10 | Live accuracy ≥80% on real (not synthetic) plant data — matches the bar already set in `planning/user_stories.md` |
| Full deployment go-live | ~Month 8 | All plants integrated, staff trained |
| First KPI review | ~Month 10–11 (one full quarter post-go-live) | Realized savings tracking against projection |
| Scale decision | ~Month 14 (two quarters post-go-live) | Both scale paths (deepen vs. expand practice) evaluated |

## Go-to-market

**Buyer:** VP of Procurement / Chief Procurement Officer at large industrial manufacturers ($500M–$5B+ revenue, multi-plant, procurement-intensive) — companies structurally similar to the profile used throughout this project. This is a genuinely underserved buyer population: our own Round 1 research found only 8% of procurement teams industry-wide have moved past the pilot stage on AI adoption.

**Channel — leading with the embedded partnership model:** rather than building a standalone sales motion from scratch, the primary channel is **acting as a specialized AI delivery partner embedded within larger strategic sourcing consultancies** (the Inverto model) that already have deep manufacturer relationships but may lack in-house AI engineering capability. Direct-to-manufacturer outreach remains a secondary channel, but the embedded-partnership path is both more realistic for an early-stage practice and more directly aligned with actual career positioning.

**Pricing — a hybrid model, not pure hourly and not pure fixed:**

| Phase | Pricing structure |
|---|---|
| Pilot / Discovery | Fixed fee, $40,000–$60,000 |
| Full Deployment | Fixed implementation fee (cost + 20–30% margin, ~$650,000–$1,100,000), with **hourly billing for anything beyond agreed scope** |
| Ongoing Support | Fixed annual retainer (~$165,000–$260,000), with hourly overflow beyond retainer scope |

**Critical structural decision: the client bears all infrastructure costs directly** (their own OpenAI and Pinecone accounts, billed to them, not passed through the consultant). This is deliberate for two reasons, not just cost protection:
1. **Data governance**: the client's spend data flows directly to their own third-party processor accounts — it never routes through consultant-owned infrastructure, which simplifies the data-processing relationship described in `gdpr_documentation.md` considerably (client ↔ OpenAI directly, not client ↔ consultant ↔ OpenAI)
2. **Cost/risk isolation**: removes the consultant's exposure to API pricing changes or usage spikes entirely — the fixed/retainer fees price the *expertise and delivery*, not a pass-through utility cost

**Differentiator** (against both generic AI consultancies and established procurement software like Coupa, SAP Ariba, Zycus, Ivalua):
1. **Speed** — proof-of-concept to working MVP in weeks, not a 12–18 month enterprise rollout
2. **Domain-specific**, not horizontal generic software — built with genuine manufacturing/operations expertise
3. **Transparency-by-design** — every classification shows its reasoning; every risk score cites its source; this directly answers the "AI is a black box" fear that opened this entire project, and most incumbent procurement software doesn't lead with this
4. **Geopolitical/tariff risk via RAG** — a genuinely novel capability most standard procurement analytics tools don't yet offer

## Commercialization model

**Consulting-led software delivery, not multi-tenant SaaS.** Each engagement is a discrete, client-specific deployment — the *methodology and codebase* are reused across clients (the actual reusable IP), but there is no shared multi-tenant platform at this stage. This is the honest framing given actual production readiness: the MVP is a proven mechanism, not an enterprise SaaS platform, and pretending otherwise would overstate current capability. A shared platform product is a legitimate future evolution, not a Phase 1–4 claim.

## Stakeholder communication plan

| Stakeholder | Update cadence | Content |
|---|---|---|
| CEO / executive sponsor | Phase-gate milestones only (pilot go/no-go, deployment go-live, KPI review) | Business case status, decision asks |
| Procurement manager | Weekly (pilot), bi-weekly (deployment) | Working-level progress, review-queue findings |
| Compliance / legal | Pre-pilot and pre-deployment checkpoints | Compliance posture (`eu_ai_act_compliance.md`, `gdpr_documentation.md`) |
| IT / data team | Integration checkpoints during deployment | Technical integration status, infrastructure ownership confirmation |

## KPIs per phase

- **Pilot → Full Deployment gate:** live classification accuracy ≥80% on real plant data (not synthetic) — the same bar already established in `planning/user_stories.md`
- **Full deployment success (first quarter post-go-live):** realized savings reach at least 80% of the low end of the projected range (~$7.4M of the $9.2M–$18.3M projection) — a deliberately conservative bar for a first-quarter check, given ramp-up
- **Scale decision inputs:** (a) has the existing client requested expansion (deepen path), and/or (b) has a second client engagement been secured via the embedded-partnership channel (practice-growth path) — both are legitimate signals, and the plan doesn't require both to count as success

## Summary for non-specialist stakeholders

This plan sequences a small, cheap proof (already done), a bounded pilot (already costed), and a full rollout whose size is justified by real, measured savings percentages — not invented ones. Commercially, the client owns their own infrastructure and data relationships throughout, which is both a cost protection and a genuine governance improvement, and pricing is structured to reward delivering value, not just billing hours, while still protecting against scope creep.
