# n8n POC Documentation — Spend Category Classification

## What this workflow does

Takes raw, unclassified spend transactions (vendor, line-item description, amount) and classifies each into one of six procurement categories using an LLM, then routes the result based on classification confidence: high-confidence classifications get written straight to a "Classified" sheet, low-confidence ones get flagged to a "Needs Review" sheet for human review.

This is a live, real classification run — not simulated — on `n8n_poc_live_demo_sample.csv` (20 transactions), the same file referenced in `dataset_documentation.md`.

## Why it's built this way (design decisions worth being able to defend)

- **Sample is embedded in the workflow, not read from a file.** The Round 2 presentation guide is explicit: *"if your demo fails live: have a backup recording ready."* Better than that — removing the file-read step removes an entire failure category before it can happen. Nothing to path-mismatch, nothing to fail to upload mid-demo.
- **Confidence threshold routes to human review, not just accepts everything.** This directly answers the "what happens if the AI is wrong" risk from the opportunities/risks doc — low-confidence outputs never silently enter the classified data; they're flagged for a person to check.
- **Classification reads the description, not just the vendor name.** The prompt explicitly instructs this, because the dataset itself proves why it matters — e.g., "Local Electrician Services" billing for "landscaping services": a vendor-name lookup would misclassify it; reading the actual line item gets it right. Worth pointing this out live if you get the chance — it's a concrete, visible reason the AI step adds value over a simple lookup table.
- **temperature: 0** — for a classification task, you want consistency, not creativity. Worth knowing this if asked why.

## Node-by-node

| Node | Type | What it does |
|---|---|---|
| When clicking 'Execute workflow' | Manual Trigger | Starts the demo on command (production version would trigger on new PO/invoice batch landing in the ERP export folder or via webhook) |
| Load Sample Transactions | Code | Emits the 20 demo transactions as individual workflow items |
| Classify Spend Category (LLM) | HTTP Request | Calls OpenAI's chat completions endpoint per transaction with a system prompt defining the 6 categories and requiring structured JSON output (category, confidence, reasoning) |
| Parse LLM Response | Code | Parses the LLM's JSON response; if parsing fails, defaults to `unclassified` + flags for review rather than guessing |
| Confidence Check | IF | Routes on `confidence < 0.7` |
| Write to Needs Review / Write to Classified | Google Sheets | Appends results to the corresponding tab |

## What this proves vs. what it doesn't (say this out loud in the pitch)

**Proves:** the classification mechanism genuinely works on messy, real-looking free text, with a built-in safety valve for uncertain cases.

**Doesn't prove:** performance at full scale (380+ transactions, ongoing), integration with a real ERP export, or accuracy against a large validation set — that's Round 2 territory (stronger POC + working MVP).

## How to reproduce / set up

1. Import `workflow.json` into your n8n instance (Workflows → Import from File)
2. Add your OpenAI API credential to the "Classify Spend Category (LLM)" node (Credentials → OpenAI API)
3. Create a Google Sheet with two tabs: `Classified` and `Needs_Review`, matching columns: `transaction_id, date, plant, vendor_name, line_item_description, amount_usd, ai_category, ai_confidence, ai_reasoning, needs_review`
4. Replace `REPLACE_WITH_GOOGLE_SHEET_ID` in both Google Sheets nodes with your sheet's ID, and attach your Google Sheets credential
5. Click "Execute workflow" — should complete in well under a minute for 20 rows
6. **Before presenting:** run it once ahead of time to confirm no credential/quota issues, and have a screen-recording of a successful run as backup, per the presentation guide's own advice

## Note on model choice

Built against OpenAI's API (`gpt-4o-mini`) since that's what's configured in this environment's credentials setup — swapping to Anthropic's API is a one-node change (same JSON-structured-output pattern) if preferred.
