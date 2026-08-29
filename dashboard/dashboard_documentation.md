# Dashboard Documentation — Spend Visibility Dashboard

## What this dashboard is (and isn't) for

This is the **business communication layer** — it shows Chleo what's happening in spend, in plain business language. It does NOT talk about AI, models, or classification confidence. That story lives in the n8n POC and LangSmith sample instead. (See the Round 1 dashboard-scope discussion for why this separation matters.)

Data source: `for_dashboard_classified_spend.csv` (already computed and ready to import).

## Page 1 — Market Context (the "big picture" opener)

Three callout cards, not charts — this is scene-setting before zooming into the company:
- "Procurement = 60–70% of manufacturing cost structure"
- "Procurement AI maturity: 1.8/5 industry-wide — only 8% past pilot stage"
- "Where deployed: 5–15% spend reduction, 23% higher profitability"

## Page 2 — Company Spend Overview

| # | Metric | Why a CEO/ops lead cares | PowerBI build |
|---|---|---|---|
| 1 | **Total spend by category** | "Where is our money actually going" — the most basic question leadership usually can't answer fast | Bar chart, `category` on axis, `SUM(amount_usd)` |
| 2 | **Top-3 supplier share per category** | Flags single-source/concentration risk — Capex at 83% is a real exposure story | Bar or matrix, `category` × top-3 vendor SUM / category SUM |
| 3 | **Supplier count per category** | Flags fragmentation — MRO's 15 suppliers is a consolidation opportunity | Bar chart, `DISTINCTCOUNT(vendor_name)` by category |
| 4 | **% spend under contract vs. off-contract** | Direct compliance/leakage signal | Donut or gauge, `under_contract` split |
| 5 | **Off-contract spend by category** | Shows *where* the leakage concentrates (Capex is the standout at $925K) | Bar chart, filtered `under_contract = False`, by category |
| 6 | **Estimated addressable savings** | The number that answers "so what do we do about it" | Callout card: $104K–$209K annually (two-lever calculation, see below) |

**On metric 6 — don't just state the number, be ready to explain the two levers separately:**
- Contract compliance recovery: 5–10% of off-contract spend ($1.83M base) → $91K–$183K
- Supplier consolidation on fragmented categories (MRO, Indirect): 3–6% of $435K base → $13K–$26K

This split matters for Q&A — a single blended number invites "how did you get that?" with no good answer. Two small, separately-justified levers survive scrutiny.

## PowerBI build steps

1. Open PowerBI Desktop → Get Data → Text/CSV → import `for_dashboard_classified_spend.csv`
2. Verify column types: `date` as Date, `amount_usd` as Decimal Number, `under_contract` as True/False — **don't let auto-detect assume comma decimals** if your locale defaults to that (known issue: use "Change Type with Locale (en-US)" if numbers look wrong)
3. Build Page 1 (context cards) using static text/card visuals — this page doesn't need the dataset at all
4. Build Page 2 visuals per the table above
5. Add a category slicer at the top of Page 2 so you can filter live during the presentation if asked "what about just Capex?"
6. Screenshot each page for `dashboard_documentation.md` once built (embed below this section)

## Assumptions and limits (state these honestly in the pitch)

- Data is synthetic, built to reflect realistic ERP messiness — not a live company export (see `dataset_documentation.md`)
- Category labels shown here represent the *target output* of the AI classification step, not a live classification run at this scale — the live classification mechanism is demonstrated separately in the n8n POC on a small sample
- Savings estimates are conservative, benchmark-based projections, not a company-specific ROI — Round 2 would refine these against real data
