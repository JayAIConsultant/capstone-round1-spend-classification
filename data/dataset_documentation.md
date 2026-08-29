# Dataset Documentation — Spend Category Analysis

## Source and construction

This is a **synthetic dataset**, built deliberately rather than sourced from Kaggle. Here's why, stated plainly:

Real public procurement/spend datasets reviewed (Kaggle: "Procurement KPI Analysis," "Supplier Stability Dataset," others) either (a) already ship with clean, pre-assigned category labels — which would make the AI classification use case trivial and pointless — or (b) sit behind Kaggle's browser/auth wall in a way this environment couldn't get through. Rather than force-fit a dataset that undermines the use case, this dataset was built to reflect what real ERP spend exports actually look like: vendor name, free-text line-item description, amount, date, plant — **no clean category field**, because in the real world, nobody's kept that up to date consistently.

This is explicitly allowed under the capstone brief ("public or synthetic data only") and is more honest than pretending a clean Kaggle dataset represents the real-world messiness the use case is meant to solve.

## Structure

- **380 transactions** across **4 plants** (Stuttgart DE, Queretaro MX, Haiphong VN, Ohio US) — reflecting a large, multi-country industrial manufacturer
- **48 unique vendors** across **6 categories**: raw materials, MRO, packaging, logistics/freight, indirect/facilities, capex components
- **$7.43M total tracked spend** (12-month window, Sept 2025–Aug 2026)
- Category assignment, vendor concentration patterns, and amount ranges were constructed to reflect realistic industrial-manufacturer patterns (e.g., raw materials and capex dominated by a handful of large suppliers; MRO and indirect spend fragmented across many small vendors) — this is standard, well-documented behavior in real procurement data, not an invented pattern.

## What's real vs. what's simulated — stated explicitly

| Component | Status |
|---|---|
| Transaction records (vendor, description, amount, date, plant) | Synthetic, built to mirror realistic ERP export structure |
| Category labels (`_ground_truth_category`) | Synthetic "true" categories — **not shown to the classification step**; used only to (a) build the dashboard's category view and (b) evaluate classification accuracy |
| Contract/preferred-supplier status | Synthetic, ~60% of vendors marked "under contract," weighted toward higher-spend vendors (realistic pattern) |
| The actual AI classification | **Not run in this environment** — no LLM API key is available in this sandbox. The dashboard's category view uses the ground-truth labels directly, since they represent the intended output of a working classification step. The **live n8n POC demo** runs a real LLM call against a 20-row unclassified sample (`n8n_poc_live_demo_sample.csv`) using Jay's own API credentials, proving the mechanism actually works — that's the part that must be shown live, not simulated. |

**Why this split is the right call, not a shortcut:** Round 1's job is to prove the *mechanism* works (n8n POC) and tell the *business story* credibly (dashboard). Running the full 380-row batch through a live LLM isn't necessary to prove either — a small live sample proves the mechanism, and the target-state category view proves the business value once that mechanism is trusted at scale.

## Files produced

- `data_raw_spend_transactions.csv` — full raw export, no categories (n=380)
- `n8n_poc_live_demo_sample.csv` — 20-row unclassified sample for the live n8n classification demo
- `for_dashboard_classified_spend.csv` — full dataset with category + contract status joined, ready for PowerBI import
- `data_ground_truth_categories.csv` / `data_supplier_contract_status.csv` — underlying reference files
