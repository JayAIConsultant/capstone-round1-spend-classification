# Round 1 Presentation — Speaker Script & Slide Outline
Target: 5–7 minutes presenting to teaching staff

---

## Slide 1: Title (included in the ~1 min context block)
**AI-Powered Spend Visibility for Industrial Manufacturers**
[Your name] | Industrial Goods Manufacturing — Large, multi-plant capital equipment producer

---

## Slide 2: The Big Picture (context opener, ~20–30 sec of the 1-min context block)

> "Before we get to your company specifically — here's why this matters at all."

- Procurement is 60–70% of a manufacturer's cost structure — not a side function
- Manufacturing lags AI adoption broadly (58% production use vs. 94% in tech)
- Inside procurement specifically: industry AI maturity scores 1.8/5 — only 8% past pilot stage
- Where it's been done: 5–15% spend reduction, 23% higher profitability
- **The gap between what procurement costs and how little AI maturity exists there — that's the opportunity**

*(Speaker note: land this fast, 3-4 sentences max, then pivot: "Now let's make that concrete for your company.")*

---

## Slide 3: Chleo's Company + The Problem (rest of context block, ~30-40 sec)

- Large industrial equipment manufacturer, multiple plants, multiple countries
- Years of fragmented sourcing decisions → nobody can answer "where does our money actually go" without weeks of manual pulling
- Input cost volatility + supply chain diversification pressure make this urgent now, not eventually

**Three use cases proposed** (name all three, flag which one you're proving today):
1. **Spend category classification** ← today's proof of concept
2. Maverick spend / contract-leakage detection *(roadmap)*
3. Inbound freight/logistics cost variance *(roadmap)*

---

## Slide 4: Dashboard Walkthrough (~2 min)

*(Live dashboard or screenshots — stay in business language throughout, no AI/model talk here)*

Walk through in this order:
1. **Total spend by category** — "$7.4M in tracked spend, and here's the breakdown you probably haven't seen this clearly before"
2. **Supplier concentration** — "Capex components: 83% of spend sits with your top 3 suppliers. That's a single-source risk if any one of them has a problem"
3. **Supplier fragmentation** — "MRO: spread across 15 different suppliers. That's the opposite problem — missed consolidation leverage"
4. **Off-contract spend** — "$925K in capex spend is running off-contract. That's not a small number"
5. **Addressable savings** — "$104K–$209K a year, and I can show you exactly how we got that number, not just that we did"

*(Speaker note: the concentration/fragmentation contrast — Capex vs. MRO — is your best visual moment. Don't rush past it.)*

---

## Slide 5: POC + Monitoring (~2 min)

**Run the n8n workflow live** (or play the backup recording):
- "This is the trigger — a batch of raw, messy spend transactions, no clean category field, the way real ERP exports actually look"
- "Here the AI is reading each line item and classifying it — not just looking at the vendor name, because vendors don't map cleanly to one category" *(the Local Electrician Services / landscaping example is a great concrete moment here if it comes up in the sample)*
- "And this is the output — classified, plus a confidence score. Anything below our threshold gets routed for human review instead of silently accepted"

**Then, LangSmith:**
- "Same classification logic, but here it's being scored against known-correct answers — [X out of 20] correct, and every single decision is traceable: what it saw, what it concluded, why"
- "This is what 'AI transparency' actually looks like in practice — not a promise, an audit trail"

**Be honest about limits:** "This proves the mechanism works on a real sample. Scaling to your full transaction volume, validating against a larger dataset, integrating with your actual ERP — that's exactly what the pilot in the next slide is for."

---

## Slide 6: Cost, Timeline, and the Ask (~1 min)

- Discovery + one-plant pilot: **$37,500–$56,200**
- **8–10 weeks** to a validated go/no-go decision
- "I'm not asking you to commit to a full rollout today. I'm asking for a scoped pilot — one plant, real data, a validated accuracy number instead of a benchmark estimate — and a clear decision point at the end of it."

---

## Slide 7: Close (~15–30 sec)

- One sentence: "Your procurement function is your biggest cost lever, and right now almost nobody in this industry has real visibility into it — this pilot gets you there first."
- **What you most want feedback on:** *(fill in your own honest answer — e.g., "whether the use case sequencing is right, or whether contract-leakage should be the lead story instead of classification")*

---

## Timing check
| Section | Target time |
|---|---|
| Title + Big Picture + Company context | ~1 min |
| Dashboard walkthrough | ~2 min |
| POC + monitoring | ~2 min |
| Cost/timeline + ask | ~1 min |
| Close | ~0.5 min |
| **Total** | **~6.5 min** |

## Before you present
- Rehearse once with a timer — the guide explicitly recommends this
- Have the n8n recording ready as backup even if you plan to run it live
- Know your two savings-lever numbers separately (contract compliance vs. consolidation) — don't let Q&A catch you with only the blended total
- Know your LangSmith accuracy number cold — if it's not 20/20, have a one-sentence honest read on the misses ready, not a defensive one
