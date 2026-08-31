# LangSmith Monitoring Sample Documentation

## What this demonstrates

This is the **trust/transparency layer** of the pitch — separate from the dashboard (business case) and the n8n POC (mechanism demo). Its job is narrow and specific: prove that the AI's classification decisions are not a black box. Every call is logged with its full reasoning, and every result is scored against a known-correct answer.

This directly answers Chleo's founding fear: *"what is the AI, and how would I know if it's working?"*

## What's actually in it

- **One dataset** in LangSmith (`capstone-spend-classification-sample`): the same 20 transactions used in the n8n live demo, but here paired with their known-correct category — so this run can be scored, not just observed
- **One experiment run**: each transaction sent through the exact same classification prompt/logic as the n8n POC (same model, same system prompt, same output shape — intentionally, so this isn't a second, different AI system, it's an evaluation lens on the same one)
- **One evaluator**: simple exact-match accuracy against the known category — kept deliberately simple so the number is fully explainable if questioned live, rather than an opaque composite score

## What you'll be able to show live / in screenshots

- A traced run showing: the exact input sent to the LLM → the raw model response → the parsed category, confidence, and one-sentence reasoning
- An accuracy score per example and in aggregate across all 20
- Any misclassifications, visible with their reasoning — which is itself a good "here's how you'd catch and correct an error" moment, not something to hide

## Actual results (Round 1 evidence)

The evaluation was run live against OpenAI's `gpt-4o-mini`: **85% accuracy (17 of 20 correct)** against known-correct category labels, zero-shot — no fine-tuning, no few-shot examples in the prompt. Screenshots of the full LangSmith results grid and an expanded individual trace are included in `assets/`.

**The 2 misses, and why they're informative rather than embarrassing:**
- *"gasket set - pump housing, unit 874"* → expected `mro`, predicted `raw_materials`. A genuinely ambiguous case — "pump housing" reads as a material-ish term even though the transaction is really a repair part.
- *"HVAC maintenance contract, visit 40"* → expected `indirect_facilities`, predicted `mro`. Also reasonable — "maintenance" pattern-matches toward MRO even though HVAC upkeep is a facilities cost in this taxonomy.

Both misses reflect boundary cases in the category definitions themselves, not sloppy model behavior — a legitimate Round 2 improvement path is sharpening the category definitions in the prompt, or adding a few labeled boundary examples.

## Setup — run this yourself before presenting

**Environment variables required** (set in your terminal or `.env`, loaded via `python-dotenv` if you prefer):

```
OPENAI_API_KEY=<your key>
LANGCHAIN_API_KEY=<your LangSmith key>
LANGCHAIN_ENDPOINT=<your workspace's API endpoint>
```

**Critical — the EU/US endpoint gotcha:** your LangSmith account lives on the EU workspace. If `LANGCHAIN_ENDPOINT` points to the US endpoint, every call will fail with a 403. Before running this script, go to LangSmith → Settings → API Keys and copy the exact endpoint URL shown there for your workspace — don't guess it.

**Run it:**

```
C:\Users\sindh\miniconda3\envs\bootcamp-env\python.exe langsmith_classification_eval.py
```

(Using the full interpreter path, per your usual pattern, to make sure `openai` and `langsmith` resolve from `bootcamp-env` and not base.)

**If either package is missing:**

```
C:\Users\sindh\miniconda3\envs\bootcamp-env\python.exe -m pip install openai langsmith --break-system-packages
```

(Drop `--break-system-packages` on Windows — that flag's a Linux/Debian-specific requirement; on your Windows conda env it's unnecessary and pip will just ignore or error harmlessly if included, so leave it off.)

## Getting the submission artifact

The `evaluate()` call prints an experiment URL to your terminal when it finishes — that's your shareable LangSmith link for instructors. If your workspace has link-sharing restrictions, take screenshots instead of:
1. The experiment results table (all 20 examples with scores)
2. One expanded individual trace showing the full reasoning
3. The aggregate accuracy score

## Honest limits (state these if asked)

- 20 examples is a sample, not a statistically rigorous validation set — Round 2 would need a larger, more adversarial test set (including edge cases and ambiguous line items) before trusting this at production scale
- Exact-match accuracy doesn't capture "close but reasonable" misclassifications (e.g., a borderline capex/MRO item) — a more nuanced evaluator (or human-reviewed near-misses) would be a natural Round 2 refinement
