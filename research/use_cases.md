# Use Case Proposals

## Use Case 1 — AI-Assisted Spend Category Classification *(BUILT — Round 1 POC + dashboard foundation)*

**What it does:** Takes raw, messy transactional spend data (vendor name, line-item description, amount — no reliable existing category field) and uses an LLM to classify each line into a standard procurement category structure, flagging anything it can't classify with confidence for human review.

**Why it fits a large industrial manufacturer:** At scale, spend data lives across multiple plants and ERP instances with no consistent tagging discipline. Manual classification doesn't scale; this does.

**Round 1 proof:** n8n workflow processing 20 real transactions, ~85% zero-shot accuracy against known-correct labels (see LangSmith evaluation), with low-confidence items correctly routed to human review.

## Use Case 2 — Maverick Spend / Contract-Leakage Detection *(DESCRIBED ONLY — Round 1 narrative, candidate for Round 2 deepening)*

**What it does:** Once spend is reliably categorized, cross-reference transactions against negotiated contract terms/preferred supplier lists to flag off-contract purchases.

**Why it fits:** A direct, quantifiable savings lever — and a natural "what's next" once classification exists.

## Use Case 3 — Inbound Freight / Logistics Cost Variance Analysis *(DESCRIBED ONLY — roadmap/phase 2)*

**What it does:** Extends spend visibility beyond "what did we buy" to "what did it cost to get here" — flagging categories or lanes where freight cost runs above expected variance.

**Why it fits:** Rounds out the story into full total-cost-of-ownership visibility — closer to how a procurement/supply chain consultancy would actually scope this engagement.

---

**Scope discipline note:** Only Use Case 1 is built end-to-end in Round 1. Use Cases 2 and 3 are deliberately described-only — they're the roadmap, not padding.
