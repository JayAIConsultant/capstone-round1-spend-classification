# MVP Documentation — AI-Powered Spend Intelligence

## What this is

A self-service Streamlit application that takes raw, messy spend transaction data and produces five layers of analysis: AI classification, a spend dashboard, maverick spend (contract-compliance) detection, freight cost variance detection, and geopolitical/tariff risk scoring via RAG. It's the working product upgrade from Round 1's n8n proof-of-concept — the same core classification mechanism, now generalized so a user can bring their own data rather than a fixed demo sample.

## How to run it

```
cd mvp
pip install -r ../requirements.txt
streamlit run app.py
```

Requires `OPENAI_API_KEY` and `PINECONE_API_KEY` as environment variables (or Streamlit secrets, for a deployed instance). Before first use, run `python setup_pinecone_corpus.py` once to embed and upload the tariff knowledge base — this only needs to happen once, ever, unless `tariff_corpus.py` is edited.

## Two usage modes

- **Try demo data** — samples from the bundled 380-transaction synthetic dataset (same one from Round 1), with a slider to control how many transactions to classify. Because this data has known-correct labels, this mode additionally shows a live accuracy score — something impossible for a real uploaded file with no ground truth.
- **Upload your own data** — requires only `vendor_name`, `line_item_description`, `amount_usd`. Contract list and vendor-country mapping are optional add-on uploads that unlock Maverick Spend Detection and Geopolitical Risk Scoring respectively; if not provided, those sections degrade gracefully with a clear message rather than breaking.

---

## Module 1: Classification — an honest account of what it took to get right

This module went through **eight iterations** before landing on a design that actually works, and the investigation itself is worth documenting because it's a real lesson in AI engineering, not just a build log.

**The original ask:** during a mentor review, the feedback was to have the LLM flag transactions it's genuinely unsure about for human review, rather than relying solely on a confidence threshold.

**Attempts 1–4 (all failed, each for an instructive reason):**
1. **Self-reported boolean `ambiguous` flag**, requested after the category in the JSON schema — never fired once across 60 real transactions, including on known misclassifications. The model had already committed to an answer before reaching that field.
2. **Reordering the schema so reasoning came first** — this genuinely worked for a handful of cases, correctly naming the right alternative category. But adding one *unrelated* prompt clarification later caused it to stop firing on the exact same transaction it had previously caught — proof that single-shot self-report is fragile and holistic, not narrowly controllable.
3. **Scoring all six categories independently** (0–1 each), computing ambiguity from the score gap in our own code rather than trusting a self-report — sounder in principle, but the model ignored the instruction not to give binary 1/0 scores anyway, so every transaction came back with confidence exactly 1.0 and zero ambiguity ever detected.
4. **Self-consistency voting** (3 independent calls per transaction at temperature 0.7) — this is where the real diagnosis emerged: all 3 votes were unanimous on every transaction, *including the wrong ones*. The errors weren't stochastic uncertainty at all — the model was confidently, consistently wrong the same way every time. No amount of resampling reveals a bias that isn't random.

**The actual fix — two separate layers solving two different problems:**

| Layer | Problem it solves | Mechanism |
|---|---|---|
| **General** | Unknown, unforeseen ambiguous items in real data | Self-consistency voting (restored, since it's the right tool for *genuine* stochastic uncertainty) |
| **Specific** | Two confirmed, diagnosed systematic biases (HVAC/maintenance → wrong category; safety gloves → wrong category) | Few-shot correction examples + a deterministic keyword safety net that forces review regardless of model confidence |

This distinction — **systematic bias vs. stochastic uncertainty require different fixes** — is the central finding from this module. Verified with a targeted test proving both layers work independently: a brand-new, never-seen ambiguous item gets caught by voting alone (no keyword match needed), and a known bias gets caught by the safety net even when votes are unanimous (proving it doesn't depend on voting disagreement at all).

**Result:** 100% accuracy on a 90-transaction verification batch, with all flagged rows correctly matching known-diagnosed patterns, plus evidence of the voting layer catching at least one genuinely new item unprompted during testing.

**Honest limit:** the keyword safety net only covers the two biases we've specifically diagnosed through evaluation. It is not a general solution — that's what the voting layer is for. A production version would need this list to grow over time as new systematic biases are discovered through ongoing evaluation.

---

## Module 2: Spend Dashboard

Computes total spend by category, top-3 supplier concentration (%), and distinct supplier count (fragmentation) — direct ports of the Round 1 PowerBI logic, now computed live from whatever was just classified. Verified against hand-calculated values on synthetic test data before trusting it on real output.

**Consistent finding across multiple independent samples:** Capex Components shows the highest supplier concentration and lowest fragmentation; MRO shows the opposite. This pattern held across at least three different random samples, suggesting it's a real structural feature of the data, not sampling noise.

## Module 3: Maverick Spend Detection

Cross-references classified spend against an uploaded contract/preferred-supplier list. Vendors not found in the contract list are shown as their own explicit "Unknown" category — not assumed compliant or non-compliant. Boolean parsing handles common real-world encodings (True/False, Yes/No, 1/0).

**Honest limit:** relies entirely on vendor *name* matching — a real system would need fuzzy matching or a vendor ID system to handle naming inconsistencies between the spend data and contract records.

## Module 4: Freight Cost Variance

Deliberately lean by design: flags freight transactions costing more than 1.5x the category's own median *within the current sample* — a statistical outlier check, not a comparison against an external cost benchmark. This keeps the module distinct from the separate should-cost benchmarking capstone project. Requires at least 3 freight transactions to compute a meaningful threshold; below that, it says so rather than showing a misleading result from too little data.

## Module 5: Geopolitical Risk (RAG)

Retrieves relevant tariff context (via Pinecone vector search, scoped to both product category *and* vendor country) from a curated corpus of ~20 real, cited, dated tariff facts, then has an LLM synthesize a risk tier with reasoning grounded in that retrieved context — not recalled from the model's training data.

**A real design bug found and fixed during testing:** the initial version assessed every transaction's risk assuming the destination was always the US. But this company has four plants (Germany, Mexico, Vietnam, USA), and a shipment to the Germany plant never touches US customs at all — a US tariff score for it is meaningless, not just imprecise. The fix: map each transaction's `plant` field to its real destination country, and only assess transactions actually bound for the US (the one regime this corpus covers). Everything else is explicitly labeled "Out of scope" with an explanation, rather than given a confident-looking but wrong number. Verified with a test proving the *same* category/country combination gets a real score when US-bound and is correctly excluded when it isn't.

**Honest, significant limit:** this covers exactly one of four relevant import regimes. A complete version needs three more dated, cited corpora — EU import rules, Mexican customs, Vietnamese customs — each built the same way as the US one. This is a legitimate, well-defined next step, documented here rather than glossed over.

**Corpus scope:** ~20 snippets, hand-curated and dated (compiled September 2026), not the full tariff schedule — tariff policy changes monthly, so a comprehensive ingestion would be stale within weeks regardless of effort. This is a deliberate, stated snapshot, not a live feed.

## Insights Layer

Each of the four analytical sections (Dashboard, Maverick Spend, Freight Variance, Geopolitical Risk) gets a short natural-language insight generated by an LLM — but critically, the LLM is given the exact numbers we've already computed and verified, and instructed only to narrate them, not calculate anything. This separation means the insight text cannot contradict the chart it sits below, since it has no ability to compute a different number than what's already on screen.

---

## Testing approach used throughout

Every module was verified at two levels before being trusted:
1. **Logic verification with mocked responses** — column validation, merge logic, threshold math, and edge cases (malformed JSON, missing vendors, insufficient data) were tested deterministically, without needing a live API call, wherever the logic allowed it.
2. **Live verification against ground truth** — actual runs were cross-checked against Round 1's known-correct labels and hand-calculated expected values, not just eyeballed for plausibility.

This two-level approach is what caught every real bug in this MVP — including the classification investigation above and the geopolitical risk destination-scoping error — before they became invisible flaws in a finished-looking product.

## Overall honest limits (stated upfront, not buried)

- No live ERP integration — file upload only, by design (see `use_case_definition.md`)
- No production authentication, multi-tenancy, or enterprise security — see `strategic_plan.md` for the production migration path
- Fixed six-category taxonomy, not user-configurable
- Geopolitical risk scoped to one of four relevant import regimes
- The keyword safety net for classification covers two specifically diagnosed biases, not a general defense
