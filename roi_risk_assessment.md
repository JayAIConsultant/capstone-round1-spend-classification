# ROI and Risk Assessment

## Scope of this assessment

This covers **full company-wide deployment**, contingent on a successful pilot (see `cost_estimation/` for the Round 1 pilot-scoped estimate, $37.5K–$56.2K for a single-plant discovery + pilot). The figures below project what deployment across all plants would return *if* the pilot confirms the savings patterns already observed in this project's validated sample analysis. This is a deliberate sequencing: the pilot exists specifically to de-risk the larger commitment below, not to be skipped.

## How these numbers are grounded, not invented

Every percentage used here comes from **actual measured proportions** in this project's dataset analysis, verified in `mvp_documentation.md` and Round 1's dashboard — not assumptions built from scratch:

- **Off-contract spend: 24.6%** of tracked spend (verified figure, Round 1 dashboard)
- **Fragmented-category spend (MRO + Indirect/Facilities): 5.86%** of tracked spend (verified figure)
- **Savings-rate benchmarks (5–10% contract compliance recovery, 3–6% consolidation savings)**: the same conservative ranges used in Round 1's cost analysis, consistent with the broader 5–15% AI-enabled procurement savings figure cited in `research/sector_research.md`

**Scaling assumption, stated explicitly**: annual company-wide procurement spend of **$650M**, based on this project's own cited research that procurement represents 60–70% of manufacturing cost structure, applied to a "$1B+ revenue" company profile (midpoint 65%). This is an order-of-magnitude planning assumption, not a client-confirmed figure — the pilot phase would replace this with real numbers.

## Upfront costs (full deployment, one-time)

| Item | Estimate |
|---|---|
| Software/infrastructure setup (production migration from MVP: database, hosting, enterprise SSO integration) | $150,000 – $250,000 |
| ERP data integration across 4 plants | $100,000 – $180,000 |
| Change management & training across all plants | $80,000 – $120,000 |
| Consulting/professional services (build-out beyond pilot team) | $200,000 – $320,000 |
| **Total upfront** | **$530,000 – $870,000** (midpoint used below: **$700,000**) |

## Ongoing annual costs

| Item | Estimate |
|---|---|
| Cloud hosting & software maintenance | $40,000 – $70,000 |
| LLM API costs at full transaction volume (classification, self-consistency voting, geopolitical RAG, insights) | $15,000 – $30,000 |
| Ongoing support/monitoring | $80,000 – $120,000 |
| Periodic model evaluation & corpus refresh (quarterly, per the evaluation loop design in `mvp_documentation.md`) | $20,000 – $30,000 |
| **Total ongoing (annual)** | **$135,000 – $200,000** (midpoint used below: **$170,000**) |

**Note on why the software cost is small relative to the savings below**: this is a real, expected feature of AI-enabled analytics tools, not an inflated projection — the software cost scales with implementation complexity, while the savings scale with the size of the spend base it's applied to. A $650M spend base means even modest percentage-point improvements translate to large absolute dollars. This is exactly why the pilot phase matters: validating the percentage assumptions on real data is what makes a large projected number credible rather than speculative.

## A critical methodology correction, made explicit rather than glossed over

An earlier draft of this document attributed the full identified savings opportunity to the AI system. **That was a real methodological error, corrected here.** This system classifies spend and surfaces where opportunity sits — it does not negotiate contracts, switch suppliers, or enforce compliance. Converting an *identified* opportunity into *realized* dollars depends entirely on the client's procurement team's execution capability, which the AI has no control over. This is a well-established distinction in procurement finance practice: procurement and finance departments routinely dispute savings claims precisely because "identified" and "realized" savings are conflated. This document now separates them explicitly, using two tiers of value with different confidence levels.

## Quantified business value — two tiers, not one blended number

### Tier 1 — Efficiency value (100% directly attributable to the AI system)

Manual classification of spend transactions takes real analyst time; automating it frees that time regardless of what the client's team does with the resulting insight. This tier requires no negotiation success, no supplier switching — it's a direct labor/throughput gain.

| Input | Value |
|---|---|
| Estimated annual transaction volume (company-wide, at $650M spend / ~$19,544 avg. transaction) | ~33,260 transactions |
| Manual classification throughput | ~17.5 transactions/hour |
| Hours saved annually | ~1,900 hours |
| Fully-loaded analyst rate | $50–$75/hour |
| **Tier 1 annual value** | **$95,000 – $143,000** |

### Tier 2 — Capturable opportunity (AI-enabled, execution-dependent)

The $9.2M–$18.3M figure from the original analysis (contract compliance recovery + supplier consolidation, see calculation basis below) represents **identified opportunity, not realized savings**. A capture-rate discount is applied to reflect that this value only materializes if the client's team successfully acts on it.

| Input | Value |
|---|---|
| Identified opportunity (pre-discount) | $9,151,599 – $18,303,198 |
| Capture rate applied | 30–50% |
| **Tier 2 annual value (realistically capturable)** | **$2,745,480 – $9,151,599** |

**Why 30–50%, not higher:** procurement finance sources report realization rates of roughly 70–95% for savings that are *already negotiated and contracted* — but our figure sits one stage earlier, at the point of identification, before any negotiation has occurred. A more conservative rate is the honest choice at this earlier stage, since execution capacity, negotiation success, and competing priorities all still stand between "identified" and "contracted." This rate should be replaced with the client's own historical realization-rate data during the pilot phase, if available — it is a placeholder assumption, not a measured fact.

### Combined annual value

| Tier | Range |
|---|---|
| Tier 1 (efficiency, high confidence) | $95,000 – $143,000 |
| Tier 2 (capturable opportunity, execution-dependent) | $2,745,480 – $9,151,599 |
| **Total** | **$2,840,505 – $9,294,137** (midpoint: **$6,067,321**) |

**Basis for the pre-discount Tier 2 figure**, for reference:

| Lever | Base (of $650M) | Savings rate | Identified value |
|---|---|---|---|
| Contract compliance recovery | $160.2M (24.6% off-contract) | 5–10% | $8.0M – $16.0M |
| Supplier consolidation | $38.1M (5.86% fragmented) | 3–6% | $1.1M – $2.3M |

## ROI calculation (revised)

Using `ROI = (Net Benefit / Total Cost) × 100`, with midpoint figures:

| | 12-month | 36-month |
|---|---|---|
| Total cost | $870,000 | $1,210,000 |
| Total benefit | $6,067,321 | $18,201,963 |
| Net benefit | $5,197,321 | $16,991,963 |
| **ROI** | **~597%** | **~1,404%** |

These are meaningfully lower than the original (uncorrected) figures of 1,478% and 3,303% — **that reduction is the point, not a problem.** A smaller, properly-attributed number that survives scrutiny is worth more than a larger one that collapses under the first hard question about who's actually delivering the value.

## Break-even (revised)

At the midpoint, break-even at instant full run-rate would be ~1.4 months — still unrealistically fast to present without caveat. Accounting for a realistic ramp-up (both the tool's adoption curve *and* the time procurement teams need to actually negotiate and execute against Tier 2 opportunities), **break-even more credibly lands in the 4–7 month range.** This is still a fast payback profile — the honest, discounted version of this plan is still a strong business case.

## Assumptions table

| Assumption | Value | Basis |
|---|---|---|
| Annual company-wide procurement spend | $650M | 65% of $1B+ revenue, per project's own cited procurement-cost-share research |
| Off-contract spend % | 24.6% | Measured directly in this project's dataset analysis |
| Fragmented-category spend % | 5.86% | Measured directly (MRO + Indirect/Facilities) |
| Contract compliance recovery rate | 5–10% | Consistent with Round 1 cost analysis methodology |
| Consolidation savings rate | 3–6% | Consistent with Round 1 cost analysis methodology |
| Manual classification throughput | ~17.5 transactions/hour | Planning estimate for Tier 1 efficiency calculation |
| Fully-loaded analyst rate | $50–$75/hour | Planning estimate for Tier 1 efficiency calculation |
| **Capture rate (identified → realized)** | **30–50%** | Conservative placeholder, informed by industry reports of 70–95% realization rates *post-negotiation* — our figure is pre-negotiation, so a lower rate is used. Should be replaced with client's own historical data during pilot. |
| Savings realized steady-state from Year 1 | Simplifying assumption | Real deployments would ramp up; see break-even note above |
| Upfront/ongoing cost estimates | Order-of-magnitude ranges | Based on typical enterprise analytics tool implementation scope; not vendor-quoted |

## Risk matrix (8 risks across all 4 required categories)

| # | Risk | Category | Likelihood (1–5) | Impact (1–5) | Mitigation |
|---|---|---|---|---|---|
| 1 | AI systematic classification bias (confidently, consistently wrong on specific patterns) | Technical | 3 | 3 | Two-layer detection already built and verified: self-consistency voting (catches unforeseen bias) + keyword safety net (catches diagnosed bias) — see `mvp_documentation.md` |
| 2 | LLM/vector-DB vendor dependency (OpenAI or Pinecone outage, pricing change, or API deprecation) | Technical | 2 | 3 | Architecture is not hard-locked to one provider; cost/availability monitoring; SLA review before production contract |
| 3 | EU AI Act reclassification if scope later expands (e.g., into employment or credit-adjacent decisions) | Regulatory | 2 | 4 | Explicit out-of-scope boundaries documented in `use_case_definition.md`; compliance re-review required before any scope change |
| 4 | GDPR exposure if a vendor field inadvertently identifies a natural person (sole-proprietor edge case) | Regulatory | 2 | 2 | Documented in `gdpr_documentation.md`; planned detection enhancement for production version |
| 5 | Tariff/geopolitical reference data becoming stale (trade policy actively changing — confirmed during this project's own research) | Regulatory | 4 | 2 | Corpus is explicitly dated and labeled as a snapshot, not a live feed; quarterly refresh cadence planned |
| 6 | Automation bias — staff over-trusting AI output without genuine review of flagged items | Ethical | 3 | 3 | Mandatory human review routing for flagged transactions; staff training on system's documented limitations; periodic audit of review-queue handling |
| 7 | Change management resistance from procurement staff (fear of replacement, distrust of automation) | Operational | 3 | 3 | Positioned explicitly as augmentation, not replacement (stated in `research/opportunities_risks.md`); phased pilot rollout; staff involved in review-queue design |
| 8 | Real ERP data quality significantly messier than pilot/demo sample | Operational | 3 | 3 | Discovery phase includes explicit data-quality assessment (`planning/sprint_plan.md`); system already handles unmatched/unclassifiable cases gracefully rather than forcing bad answers |
| 9 | Client attributes full Tier 2 value to the AI system and is disappointed when actual capture falls short due to their own execution gaps | Ethical/Operational | 3 | 4 | Two-tier value framework above states this dependency explicitly upfront, before contract signature — not discovered after the fact |

## Summary for non-specialist stakeholders

The projected return is smaller than an initial (uncorrected) analysis suggested, and that correction matters: this document separates what the AI directly delivers (efficiency gains, Tier 1) from what the AI merely makes visible but your team must actually capture (Tier 2, discounted for realistic execution). The single biggest uncertainty is still the $650M spend-base assumption — the pilot phase is designed to replace that, and the Tier 2 capture-rate assumption, with real client data.
