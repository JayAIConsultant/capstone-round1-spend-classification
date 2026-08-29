"""
LangSmith Monitoring Sample -- Spend Category Classification
Round 1 Capstone Deliverable

Run this from your bootcamp-env with your own OPENAI_API_KEY and
LANGCHAIN_API_KEY set (see setup notes at the bottom of this file
and in langsmith_documentation.md).

What this does:
1. Creates a small labeled dataset in LangSmith (20 real transactions
   from the same sample used in the n8n POC, with known correct categories)
2. Runs the SAME classification prompt/logic as the n8n workflow against
   each one
3. Scores each prediction against the known-correct category
4. Everything -- the input, the LLM's raw output, the reasoning it gave,
   the score -- lands in LangSmith as an auditable, inspectable trace

This is the "transparency" proof point for Chleo: not just "trust the AI,"
but "here is exactly what it saw, what it concluded, why, and whether it
was right."
"""

import os
import json
from openai import OpenAI
from langsmith import Client
from langsmith.evaluation import evaluate

# ---- Setup check ----
# IMPORTANT: if your LangSmith account is on the EU workspace (eu.smith.langchain.com),
# you MUST set LANGCHAIN_ENDPOINT to the matching EU API endpoint below, or every
# call will fail with a 403. Check Settings -> API Keys in the LangSmith UI for the
# exact endpoint shown for your workspace before running this.
REQUIRED_ENV = ["OPENAI_API_KEY", "LANGCHAIN_API_KEY", "LANGCHAIN_ENDPOINT"]
missing = [v for v in REQUIRED_ENV if not os.environ.get(v)]
if missing:
    raise EnvironmentError(
        f"Missing required environment variables: {missing}. "
        f"Set these before running (see langsmith_documentation.md for the EU/US endpoint note)."
    )

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ.setdefault("LANGCHAIN_PROJECT", "capstone-spend-classification-poc")

openai_client = OpenAI()
langsmith_client = Client()

CATEGORIES = ["raw_materials", "mro", "packaging", "logistics_freight", "indirect_facilities", "capex_components"]

SYSTEM_PROMPT = (
    "You are a procurement spend classification assistant for an industrial manufacturer. "
    "Classify the purchase transaction into exactly one of: "
    "raw_materials, mro, packaging, logistics_freight, indirect_facilities, capex_components. "
    "Respond ONLY with valid JSON: "
    '{"category": string, "confidence": number (0-1), "reasoning": string (one short sentence)}. '
    "Base the classification primarily on the line item description, not the vendor name alone -- "
    "vendors sometimes supply across multiple categories."
)

# ---- Dataset: same 20 transactions as the n8n live demo, with known-correct labels ----
EXAMPLES = [
    {"inputs": {"vendor_name": "Waste Management Ltd", "line_item_description": "HVAC maintenance contract, visit 40", "amount_usd": 3182.87}, "outputs": {"expected_category": "indirect_facilities"}},
    {"inputs": {"vendor_name": "Industrial Supply Co", "line_item_description": "gasket set - pump housing, unit 336", "amount_usd": 4048.00}, "outputs": {"expected_category": "mro"}},
    {"inputs": {"vendor_name": "SteelCore Industries", "line_item_description": "Zinc alloy ingots, lot 854", "amount_usd": 32441.30}, "outputs": {"expected_category": "raw_materials"}},
    {"inputs": {"vendor_name": "Local Electrician Services", "line_item_description": "landscaping services, contract 292", "amount_usd": 2442.63}, "outputs": {"expected_category": "indirect_facilities"}},
    {"inputs": {"vendor_name": "Alloy Dynamics GmbH", "line_item_description": "Titanium plate grade 5, batch 272", "amount_usd": 75436.56}, "outputs": {"expected_category": "raw_materials"}},
    {"inputs": {"vendor_name": "ToolWorks Ltd", "line_item_description": "air filter cartridge, qty 651", "amount_usd": 2406.74}, "outputs": {"expected_category": "mro"}},
    {"inputs": {"vendor_name": "Alloy Dynamics GmbH", "line_item_description": "Aluminum billet 7075-T6, 892kg lot", "amount_usd": 59540.07}, "outputs": {"expected_category": "raw_materials"}},
    {"inputs": {"vendor_name": "ToolWorks Ltd", "line_item_description": "drive belt V-type, 664 pack", "amount_usd": 1545.39}, "outputs": {"expected_category": "mro"}},
    {"inputs": {"vendor_name": "Alloy Dynamics GmbH", "line_item_description": "Bronze bar stock C93200, 592m", "amount_usd": 69602.31}, "outputs": {"expected_category": "raw_materials"}},
    {"inputs": {"vendor_name": "AutomationTech GmbH", "line_item_description": "industrial robot arm - refurbished, unit 362", "amount_usd": 76973.89}, "outputs": {"expected_category": "capex_components"}},
    {"inputs": {"vendor_name": "Belt & Chain Co", "line_item_description": "lubricant - industrial grade, 166L drum", "amount_usd": 174.02}, "outputs": {"expected_category": "mro"}},
    {"inputs": {"vendor_name": "ToolWorks Ltd", "line_item_description": "bearing replacement kit - conveyor line 911", "amount_usd": 3097.40}, "outputs": {"expected_category": "mro"}},
    {"inputs": {"vendor_name": "CartonWorks", "line_item_description": "shrink wrap pallets, 406 units", "amount_usd": 8005.82}, "outputs": {"expected_category": "packaging"}},
    {"inputs": {"vendor_name": "SafetyFirst Equipment", "line_item_description": "gasket set - pump housing, unit 874", "amount_usd": 3645.97}, "outputs": {"expected_category": "mro"}},
    {"inputs": {"vendor_name": "Precision Motion Systems", "line_item_description": "linear actuator system, qty 373", "amount_usd": 7095.51}, "outputs": {"expected_category": "capex_components"}},
    {"inputs": {"vendor_name": "SteelCore Industries", "line_item_description": "Bronze bar stock C93200, 820m", "amount_usd": 65639.44}, "outputs": {"expected_category": "raw_materials"}},
    {"inputs": {"vendor_name": "Office Essentials Co", "line_item_description": "office supplies restock, order 990", "amount_usd": 2469.20}, "outputs": {"expected_category": "indirect_facilities"}},
    {"inputs": {"vendor_name": "Export Crate Co", "line_item_description": "shrink wrap pallets, 894 units", "amount_usd": 1756.78}, "outputs": {"expected_category": "packaging"}},
    {"inputs": {"vendor_name": "Janitorial Partners", "line_item_description": "landscaping services, contract 680", "amount_usd": 1185.55}, "outputs": {"expected_category": "indirect_facilities"}},
    {"inputs": {"vendor_name": "Global Metals Partners", "line_item_description": "6mm HRC steel coil - grade S355, lot 684", "amount_usd": 55214.56}, "outputs": {"expected_category": "raw_materials"}},
]

DATASET_NAME = "capstone-spend-classification-sample"


def ensure_dataset():
    """Create the dataset in LangSmith if it doesn't already exist."""
    existing = list(langsmith_client.list_datasets(dataset_name=DATASET_NAME))
    if existing:
        print(f"Dataset '{DATASET_NAME}' already exists -- reusing it.")
        return existing[0]
    dataset = langsmith_client.create_dataset(
        dataset_name=DATASET_NAME,
        description="20 spend transactions (vendor, description, amount) with known-correct "
                     "procurement category labels. Used to evaluate the classification step "
                     "shared with the n8n POC workflow.",
    )
    langsmith_client.create_examples(
        inputs=[ex["inputs"] for ex in EXAMPLES],
        outputs=[ex["outputs"] for ex in EXAMPLES],
        dataset_id=dataset.id,
    )
    print(f"Created dataset '{DATASET_NAME}' with {len(EXAMPLES)} examples.")
    return dataset


def classify(inputs: dict) -> dict:
    """The target function LangSmith evaluates. This is the SAME classification
    logic as the n8n POC's HTTP Request node -- same prompt, same model, same
    output shape -- so the two deliverables demonstrate one consistent mechanism,
    not two different ones."""
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": (
                f"Vendor: {inputs['vendor_name']}. "
                f"Description: {inputs['line_item_description']}. "
                f"Amount: ${inputs['amount_usd']}."
            )},
        ],
    )
    raw = response.choices[0].message.content
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = {"category": "unclassified", "confidence": 0.0, "reasoning": "Model did not return valid JSON."}
    return {
        "predicted_category": parsed.get("category"),
        "confidence": parsed.get("confidence"),
        "reasoning": parsed.get("reasoning"),
    }


def category_accuracy(run, example) -> dict:
    """Evaluator: exact-match accuracy against the known-correct category.
    Kept simple and legible on purpose -- for a Round 1 sample, a transparent,
    explainable metric beats a more elaborate one nobody can sanity-check live."""
    predicted = run.outputs.get("predicted_category")
    expected = example.outputs.get("expected_category")
    return {"key": "category_accuracy", "score": int(predicted == expected)}


if __name__ == "__main__":
    ensure_dataset()

    results = evaluate(
        classify,
        data=DATASET_NAME,
        evaluators=[category_accuracy],
        experiment_prefix="spend-classification",
        metadata={"use_case": "Round 1 capstone - spend category classification"},
    )

    print("\nEvaluation complete. Open the LangSmith UI to inspect:")
    print("- Each individual trace (input -> LLM call -> reasoning -> output)")
    print("- The category_accuracy score per example")
    print("- The aggregate accuracy across all 20 examples")
    print(f"\nExperiment URL will be printed above by the `evaluate()` call itself.")
