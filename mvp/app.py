"""
AI-Powered Spend Intelligence MVP
Module 1: Spend Category Classification

Uses the exact same classification logic (system prompt, model, temperature)
as the Round 1 n8n POC and LangSmith evaluation, so all three artifacts
demonstrate one consistent mechanism.
"""

import os
import json
import time
import pandas as pd
import streamlit as st
from openai import OpenAI
from pinecone import Pinecone

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Spend Intelligence MVP", layout="wide")

REQUIRED_COLUMNS = ["vendor_name", "line_item_description", "amount_usd"]
CATEGORIES = ["raw_materials", "mro", "packaging", "logistics_freight", "indirect_facilities", "capex_components"]
N_SAMPLES = 3

# LAYER 2 (specific, solved problems): a deterministic safety net for the two systematic
# biases we've already diagnosed through evaluation. This does NOT generalize to new,
# unseen ambiguous items -- that's what Layer 1 (self-consistency, below) is for.
KNOWN_TRICKY_PATTERNS = ["maintenance contract", "safety gloves"]


def matches_known_tricky_pattern(description: str) -> bool:
    d = description.lower()
    return any(p in d for p in KNOWN_TRICKY_PATTERNS)


SYSTEM_PROMPT = (
    "You are a procurement spend classification assistant for an industrial manufacturer. "
    "Classify the purchase transaction into exactly one of: "
    "raw_materials, mro, packaging, logistics_freight, indirect_facilities, capex_components. "
    "\n\n"
    "IMPORTANT distinction between mro and capex_components, since these are commonly confused: "
    "mro means wear parts, spare parts, and maintenance/repair items used to maintain or fix EQUIPMENT "
    "THE COMPANY ALREADY OWNS -- gaskets, bearings, fasteners, drive belts, filters, lubricants, and "
    "hose repairs are mro even though they are mechanical components, because they are consumable "
    "replacement items, not new capital investments. capex_components means acquiring NEW capital "
    "equipment or major assemblies as a capital investment -- robot arms, PLC controllers, linear "
    "actuator systems, CNC spindle units."
    "\n\n"
    "Respond ONLY with valid JSON: {\"reasoning\": string, \"category\": string}. "
    "Base your classification primarily on the line item description, not the vendor name alone -- "
    "vendors sometimes supply across multiple categories."
)

# Few-shot corrections for the two specific, already-diagnosed biases.
FEWSHOT_EXAMPLES = [
    (
        "Vendor: ABC Facilities Co. Description: HVAC maintenance contract, visit 12. Amount: $1200.",
        {"reasoning": "This is a recurring facility upkeep service for building HVAC systems, "
                       "not a repair part for production equipment.", "category": "indirect_facilities"},
    ),
    (
        "Vendor: SafetyFirst Equipment. Description: safety gloves - nitrile, case of 100. Amount: $250.",
        {"reasoning": "Safety gloves are a consumable maintenance/safety supply used in day-to-day "
                       "operations, not a facilities service contract.", "category": "mro"},
    ),
]


# ---------------------------------------------------------------------------
# API key resolution: Streamlit Cloud secrets first (for the public demo
# link), falling back to a local .env / environment variable for dev.
# This means visitors to a deployed demo link never need their own key.
# ---------------------------------------------------------------------------
def get_api_key() -> str | None:
    try:
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
    return os.environ.get("OPENAI_API_KEY")


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------
def classify_row(client: OpenAI, vendor_name: str, description: str, amount: float) -> dict:
    """Two-layer approach:
    LAYER 1 (general): self-consistency voting across N_SAMPLES independent calls at
      temperature=0.7 -- catches genuine, previously-UNSEEN ambiguity in real data,
      since a model that's truly unsure will vary its answer across repeated attempts.
    LAYER 2 (specific): few-shot examples correct the two systematic biases we've
      already diagnosed via evaluation, reinforced by a deterministic keyword check
      that guarantees those two specific patterns are always flagged for review,
      regardless of how the vote comes out.
    These solve different problems and neither substitutes for the other."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for example_input, example_output in FEWSHOT_EXAMPLES:
        messages.append({"role": "user", "content": example_input})
        messages.append({"role": "assistant", "content": json.dumps(example_output)})
    messages.append({"role": "user", "content": (
        f"Vendor: {vendor_name}. Description: {description}. Amount: ${amount}."
    )})

    votes = []
    first_reasoning = ""
    for i in range(N_SAMPLES):
        response = client.chat.completions.create(model="gpt-4o-mini", temperature=0.7, messages=messages)
        raw = response.choices[0].message.content
        try:
            parsed = json.loads(raw)
            category = parsed.get("category", "unclassified")
            if category not in CATEGORIES:
                category = "unclassified"
            if i == 0:
                first_reasoning = parsed.get("reasoning", "")
        except (json.JSONDecodeError, TypeError):
            category = "unclassified"
        votes.append(category)

    counts = pd.Series(votes).value_counts()
    top_category, top_count = counts.index[0], counts.iloc[0]
    confidence = top_count / N_SAMPLES
    keyword_hit = matches_known_tricky_pattern(description)

    reasons = []
    if top_count < N_SAMPLES:
        reasons.append(f"model disagreed with itself across {N_SAMPLES} independent attempts")
    if keyword_hit:
        reasons.append("matches a known, previously-diagnosed tricky pattern")
    if top_category == "unclassified":
        reasons.append("could not parse a category")

    return {
        "category": top_category,
        "confidence": confidence,
        "reasoning": first_reasoning,
        "needs_review": bool(reasons),
        "flagged_reason": "; ".join(reasons),
    }


def classify_dataframe(df: pd.DataFrame, client: OpenAI, progress_callback=None) -> pd.DataFrame:
    results = []
    total = len(df)
    for i, row in enumerate(df.itertuples(index=False)):
        result = classify_row(client, row.vendor_name, row.line_item_description, row.amount_usd)
        results.append(result)
        if progress_callback:
            progress_callback((i + 1) / total)
    result_df = pd.DataFrame(results)
    out = pd.concat([df.reset_index(drop=True), result_df], axis=1)
    return out


def validate_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in REQUIRED_COLUMNS if c not in df.columns]


def generate_insight(client: OpenAI, section_title: str, data_summary: str) -> str:
    """Writes a short narrative insight from numbers we've ALREADY computed correctly --
    the LLM's job here is narration only, not calculation, so it can't contradict the
    chart it's describing. Kept crisp and factual, not promotional."""
    prompt = (
        f"You are a procurement data analyst writing for a CEO audience. Based ONLY on the "
        f"computed data below, write a crisp, scientific 2-3 sentence insight. Identify the "
        f"single most decision-relevant pattern (concentration, risk, anomaly, or leakage) "
        f"rather than restating every number. Be precise and factual, no hype language, no "
        f"exclamation points, no invented numbers beyond what's given.\n\n"
        f"Section: {section_title}\nData:\n{data_summary}\n\nInsight:"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", temperature=0.3, messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"(Insight generation unavailable: {e})"


def compute_dashboard_metrics(df: pd.DataFrame) -> dict:
    total_spend = df["amount_usd"].sum()
    cat_spend = df.groupby("category")["amount_usd"].sum().sort_values(ascending=False)

    concentration = {}
    fragmentation = {}
    for cat in df["category"].unique():
        sub = df[df["category"] == cat]
        vendor_totals = sub.groupby("vendor_name")["amount_usd"].sum().sort_values(ascending=False)
        concentration[cat] = vendor_totals.head(3).sum() / vendor_totals.sum() * 100 if vendor_totals.sum() > 0 else 0
        fragmentation[cat] = vendor_totals.shape[0]

    return {
        "total_spend": total_spend,
        "cat_spend": cat_spend,
        "concentration": pd.Series(concentration).sort_values(ascending=False),
        "fragmentation": pd.Series(fragmentation).sort_values(ascending=False),
    }


def normalize_under_contract(series: pd.Series) -> pd.Series:
    """Handle common ways someone might encode a yes/no column in a real upload."""
    truthy = {"true", "yes", "1", "y", "under contract"}
    return series.astype(str).str.strip().str.lower().isin(truthy)


def compute_maverick_metrics(df: pd.DataFrame) -> dict:
    status_spend = df.groupby("contract_status")["amount_usd"].sum()
    off_contract_by_cat = (
        df[df["contract_status"] == "Off-Contract (Maverick)"]
        .groupby("category")["amount_usd"].sum()
        .sort_values(ascending=False)
    )
    return {"status_spend": status_spend, "off_contract_by_cat": off_contract_by_cat}


def compute_freight_variance(df: pd.DataFrame, multiplier: float = 1.5, min_transactions: int = 3) -> dict | None:
    freight = df[df["category"] == "logistics_freight"].copy()
    if len(freight) < min_transactions:
        return None
    median = freight["amount_usd"].median()
    threshold = median * multiplier
    freight["is_variance"] = freight["amount_usd"] > threshold
    freight = freight.sort_values("amount_usd", ascending=False)
    return {
        "freight": freight,
        "median": median,
        "threshold": threshold,
        "flagged_count": int(freight["is_variance"].sum()),
    }


# ---------------------------------------------------------------------------
# Geopolitical Risk (RAG)
# ---------------------------------------------------------------------------
PINECONE_INDEX_NAME = "geopolitical-risk-corpus"
EMBEDDING_MODEL = "text-embedding-3-small"
RISK_TIERS = ["Low", "Medium", "High"]


def get_pinecone_index():
    """Returns a Pinecone Index handle, or None if not configured -- this module
    degrades gracefully rather than crashing the whole app if Pinecone isn't set up."""
    try:
        key = st.secrets["PINECONE_API_KEY"] if "PINECONE_API_KEY" in st.secrets else os.environ.get("PINECONE_API_KEY")
    except Exception:
        key = os.environ.get("PINECONE_API_KEY")
    if not key:
        return None
    try:
        pc = Pinecone(api_key=key)
        return pc.Index(PINECONE_INDEX_NAME)
    except Exception:
        return None


def query_tariff_context(openai_client: OpenAI, pinecone_index, category: str, country: str, top_k: int = 3) -> list:
    """Retrieves the top_k most relevant tariff snippets for a given (category, country)
    pair -- retrieval is scoped to BOTH dimensions, not country alone, since tariff
    exposure genuinely varies by product category within the same country of origin."""
    query_text = f"Tariff and trade risk for {category} products sourced from {country}"
    embedding = openai_client.embeddings.create(model=EMBEDDING_MODEL, input=query_text).data[0].embedding
    results = pinecone_index.query(vector=embedding, top_k=top_k, include_metadata=True)
    return [(m.metadata["text"], m.metadata["source"]) for m in results.matches]


def assess_risk_for_pair(openai_client: OpenAI, category: str, country: str, snippets: list) -> dict:
    """Synthesizes a risk tier from retrieved context -- the LLM's job here is to reason
    over real, retrieved facts, not to recall tariff numbers from memory."""
    context_text = "\n".join(f"- {text} (Source: {source})" for text, source in snippets)
    prompt = (
        f"Based on the following tariff/trade policy context, assess the geopolitical/tariff "
        f"risk tier for sourcing '{category}' from '{country}'.\n\nContext:\n{context_text}\n\n"
        f'Respond ONLY with valid JSON: {{"risk_tier": "Low" or "Medium" or "High", '
        f'"reasoning": string (1-2 sentences, citing the specific context above)}}.'
    )
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini", temperature=0, response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
    )
    try:
        parsed = json.loads(response.choices[0].message.content)
        tier = parsed.get("risk_tier", "Unknown")
        if tier not in RISK_TIERS:
            tier = "Unknown"
        reasoning = parsed.get("reasoning", "")
    except (json.JSONDecodeError, TypeError):
        tier, reasoning = "Unknown", "Could not parse risk assessment."
    return {"risk_tier": tier, "reasoning": reasoning, "sources": [s for _, s in snippets]}


PLANT_TO_DESTINATION_COUNTRY = {
    "Plant A - Stuttgart, DE": "Germany",
    "Plant B - Queretaro, MX": "Mexico",
    "Plant C - Haiphong, VN": "Vietnam",
    "Plant D - Ohio, US": "USA",
}


def assess_geopolitical_risk(df_with_country: pd.DataFrame, openai_client: OpenAI, pinecone_index, progress_callback=None) -> tuple:
    """Assesses risk ONCE PER UNIQUE (category, country) PAIR, not per transaction --
    tariffs apply at the product-category + origin-country level, so this mirrors
    how the assessment actually works in reality, and is far cheaper than a per-row call.

    IMPORTANT SCOPE LIMIT: the tariff corpus only covers goods entering the US. A
    transaction's real tariff exposure depends on BOTH where it's sourced FROM (vendor
    country) and where it's going TO (destination plant) -- US tariffs are irrelevant
    to a shipment that never crosses into the US. This function therefore only assesses
    transactions destined for the US plant; everything else is explicitly marked
    out of scope rather than shown a misleading US-centric score. See
    mvp_documentation.md for the full explanation and what a production version needs."""
    out = df_with_country.copy()
    out["destination_country"] = out["plant"].map(PLANT_TO_DESTINATION_COUNTRY).fillna("Unknown")

    in_scope = out[out["destination_country"] == "USA"].copy()
    out_of_scope_count = len(out) - len(in_scope)

    unique_pairs = in_scope[["category", "country"]].drop_duplicates().reset_index(drop=True)
    pair_results = {}
    for i, row in unique_pairs.iterrows():
        cat, country = row["category"], row["country"]
        snippets = query_tariff_context(openai_client, pinecone_index, cat, country)
        pair_results[(cat, country)] = assess_risk_for_pair(openai_client, cat, country, snippets)
        if progress_callback:
            progress_callback((i + 1) / max(len(unique_pairs), 1))

    out["risk_tier"] = "Out of scope (non-US destination)"
    out["risk_reasoning"] = out["destination_country"].apply(
        lambda d: f"This module currently only assesses tariff exposure for shipments entering the US. "
                  f"This transaction is destined for a plant in {d}, which needs a different import-tariff "
                  f"regime (EU, Mexican, or Vietnamese customs) not covered by the current corpus."
        if d != "USA" else ""
    )
    for idx in in_scope.index:
        cat, country = out.loc[idx, "category"], out.loc[idx, "country"]
        result = pair_results.get((cat, country))
        if result:
            out.loc[idx, "risk_tier"] = result["risk_tier"]
            out.loc[idx, "risk_reasoning"] = result["reasoning"]

    return out, pair_results, out_of_scope_count


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
st.title("AI-Powered Spend Intelligence")
st.caption(
    "Upload raw, messy spend data and get it classified into procurement categories -- "
    "the same AI mechanism proven in the Round 1 POC (85% zero-shot accuracy)."
)

api_key = get_api_key()
if not api_key:
    st.error(
        "No OpenAI API key found. Set OPENAI_API_KEY as a Streamlit secret (for deployment) "
        "or as an environment variable / .env file (for local runs)."
    )
    st.stop()

client = OpenAI(api_key=api_key)

mode = st.radio("Choose a data source", ["Try demo data", "Upload your own data"], horizontal=True)

input_df = None
contract_df = None
is_demo = False

if mode == "Try demo data":
    is_demo = True
    st.info(
        "Samples from the Round 1 dataset (380 real-looking synthetic transactions). "
        "Because this is our own labeled data, we can also show live accuracy against "
        "known-correct answers -- something we can't do for a real uploaded file with no ground truth."
    )
    full_demo_df = pd.read_csv("data/demo_spend_full.csv")
    n_demo = st.slider(
        "Number of demo transactions to classify", min_value=20, max_value=len(full_demo_df),
        value=60, step=10,
        help="More transactions = a richer dashboard, but a longer wait (roughly 1-1.5 seconds per transaction).",
    )
    input_df = full_demo_df.sample(n=n_demo, random_state=42).reset_index(drop=True)
    contract_df = pd.read_csv("data/demo_contract_status.csv")
    contract_df["under_contract"] = normalize_under_contract(contract_df["under_contract"])
    country_df = pd.read_csv("data/vendor_country_mapping.csv")
    st.dataframe(input_df.head(10), use_container_width=True, height=200)

else:
    uploaded = st.file_uploader("Upload a spend CSV", type=["csv"])
    if uploaded is not None:
        try:
            input_df = pd.read_csv(uploaded)
        except Exception as e:
            st.error(f"Could not read that file as a CSV: {e}")
            st.stop()

        missing = validate_columns(input_df)
        if missing:
            st.error(
                f"Missing required column(s): {', '.join(missing)}. "
                f"Your file needs at minimum: {', '.join(REQUIRED_COLUMNS)}."
            )
            st.stop()

        st.success(f"Loaded {len(input_df)} transactions.")
        st.dataframe(input_df.head(10), use_container_width=True)

    with st.expander("Optional: add a vendor-country mapping to unlock Geopolitical Risk Scoring"):
        st.caption("Needs two columns: vendor_name, country")
        country_upload = st.file_uploader("Upload a vendor-country mapping", type=["csv"], key="country_upload")
        if country_upload is not None:
            try:
                country_df = pd.read_csv(country_upload)
                if "vendor_name" not in country_df.columns or "country" not in country_df.columns:
                    st.error("File needs both 'vendor_name' and 'country' columns.")
                    country_df = None
                else:
                    st.success(f"Loaded country data for {len(country_df)} vendors.")
            except Exception as e:
                st.error(f"Could not read that file as a CSV: {e}")
                country_df = None
        else:
            country_df = None

    with st.expander("Optional: add a contract list to unlock Maverick Spend Detection"):
        st.caption("Needs two columns: vendor_name, under_contract (True/False, Yes/No, or 1/0)")
        contract_upload = st.file_uploader("Upload a contract/preferred-supplier list", type=["csv"], key="contract_upload")
        if contract_upload is not None:
            try:
                contract_df = pd.read_csv(contract_upload)
                if "vendor_name" not in contract_df.columns or "under_contract" not in contract_df.columns:
                    st.error("Contract file needs both 'vendor_name' and 'under_contract' columns.")
                    contract_df = None
                else:
                    contract_df["under_contract"] = normalize_under_contract(contract_df["under_contract"])
                    st.success(f"Loaded contract status for {len(contract_df)} vendors.")
            except Exception as e:
                st.error(f"Could not read that file as a CSV: {e}")
                contract_df = None

if input_df is not None:
    if st.button("Run classification", type="primary"):
        progress_bar = st.progress(0, text="Classifying transactions...")

        def update_progress(fraction):
            progress_bar.progress(fraction, text=f"Classifying transactions... {int(fraction * 100)}%")

        start = time.time()
        classified_df = classify_dataframe(input_df, client, progress_callback=update_progress)
        elapsed = time.time() - start

        progress_bar.empty()
        st.session_state["classified_df"] = classified_df
        st.session_state["is_demo"] = is_demo
        st.session_state["contract_df"] = contract_df
        st.session_state["country_df"] = country_df

        st.success(f"Classified {len(classified_df)} transactions in {elapsed:.1f} seconds.")

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
if "classified_df" in st.session_state:
    st.divider()
    st.subheader("Classification results")

    result = st.session_state["classified_df"]

    metric_cols = st.columns(4) if st.session_state.get("is_demo") else st.columns(3)
    metric_cols[0].metric("Total transactions", len(result))
    metric_cols[1].metric("Flagged for review", int(result["needs_review"].sum()))
    metric_cols[2].metric("Avg. confidence", f"{result['confidence'].mean():.0%}")

    if st.session_state.get("is_demo"):
        gt = pd.read_csv("data/demo_ground_truth.csv")
        scored = result.merge(gt, on="transaction_id", how="left")
        accuracy = (scored["category"] == scored["_ground_truth_category"]).mean()
        metric_cols[3].metric("Accuracy vs. known-correct", f"{accuracy:.0%}")

    def highlight_review(row):
        return ["background-color: #fdecea" if row["needs_review"] else "" for _ in row]

    st.dataframe(
        result.style.apply(highlight_review, axis=1),
        use_container_width=True,
    )

    csv_bytes = result.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download classified data (CSV)",
        data=csv_bytes,
        file_name="classified_spend.csv",
        mime="text/csv",
    )

    st.caption(
        "Rows highlighted in red were flagged for one of two distinct reasons, shown in "
        "'flagged_reason': the model disagreed with itself across 3 independent attempts "
        "(catches genuinely new, unforeseen ambiguity) or the description matched a specific "
        "bias we've already diagnosed through evaluation (guaranteed via a code-level check, "
        "not AI self-judgment). See mvp_documentation.md for why both layers are necessary -- "
        "one alone does not generalize to real, previously-unseen data."
    )

    # -----------------------------------------------------------------
    # Dashboard
    # -----------------------------------------------------------------
    st.divider()
    st.subheader("Spend Dashboard")

    metrics = compute_dashboard_metrics(result)

    st.metric("Total spend classified", f"${metrics['total_spend']:,.0f}")

    dash_col1, dash_col2 = st.columns(2)

    with dash_col1:
        st.markdown("**Spend by Category**")
        st.bar_chart(metrics["cat_spend"], horizontal=True)

    with dash_col2:
        st.markdown("**Top-3 Supplier Concentration (%)**")
        st.bar_chart(metrics["concentration"], horizontal=True)

    st.markdown("**Supplier Fragmentation (Distinct Suppliers per Category)**")
    st.bar_chart(metrics["fragmentation"], horizontal=True)

    st.caption(
        "Concentration and fragmentation are computed from whatever was just classified above -- "
        "small sample sizes (e.g. a 20-transaction demo) will show thinner, less representative "
        "patterns than a larger sample or a full real dataset."
    )

    dashboard_data_summary = (
        f"Total spend: ${metrics['total_spend']:,.0f}. "
        f"Spend by category: {metrics['cat_spend'].round(0).to_dict()}. "
        f"Top-3 supplier concentration by category (%): {metrics['concentration'].round(1).to_dict()}. "
        f"Distinct supplier count by category: {metrics['fragmentation'].to_dict()}."
    )
    with st.spinner("Generating insight..."):
        dashboard_insight = generate_insight(client, "Spend Dashboard", dashboard_data_summary)
    st.info(f"**Insight:** {dashboard_insight}")

    # -----------------------------------------------------------------
    # Maverick spend detection
    # -----------------------------------------------------------------
    st.divider()
    st.subheader("Maverick Spend Detection")

    contract_df = st.session_state.get("contract_df")

    if contract_df is None:
        st.info(
            "Upload a contract/preferred-supplier list (see the optional uploader above) to unlock this section. "
            "It cross-references classified spend against negotiated contracts to flag leakage."
        )
    else:
        with_status = result.merge(contract_df[["vendor_name", "under_contract"]], on="vendor_name", how="left")
        with_status["contract_status"] = with_status["under_contract"].map(
            {True: "Under Contract", False: "Off-Contract (Maverick)"}
        )
        with_status["contract_status"] = with_status["contract_status"].fillna("Unknown (vendor not in contract list)")

        maverick_metrics = compute_maverick_metrics(with_status)
        status_spend = maverick_metrics["status_spend"]
        total = status_spend.sum()
        off_contract_total = status_spend.get("Off-Contract (Maverick)", 0)

        mv_col1, mv_col2, mv_col3 = st.columns(3)
        mv_col1.metric("Off-contract spend", f"${off_contract_total:,.0f}")
        mv_col2.metric("% off-contract", f"{off_contract_total/total*100:.1f}%" if total else "0%")
        unknown_amt = status_spend.get("Unknown (vendor not in contract list)", 0)
        mv_col3.metric("Unmatched vendor spend", f"${unknown_amt:,.0f}",
                        help="Spend from vendors not found in the uploaded contract list -- neither confirmed compliant nor flagged, shown separately rather than guessed.")

        mv_chart_col1, mv_chart_col2 = st.columns(2)
        with mv_chart_col1:
            st.markdown("**Spend by Contract Status**")
            st.bar_chart(status_spend, horizontal=True)
        with mv_chart_col2:
            if not maverick_metrics["off_contract_by_cat"].empty:
                st.markdown("**Off-Contract Spend by Category**")
                st.bar_chart(maverick_metrics["off_contract_by_cat"], horizontal=True)
            else:
                st.markdown("**Off-Contract Spend by Category**")
                st.caption("No off-contract spend detected in this sample.")

        st.caption(
            "\"Unknown\" vendors are shown as their own category rather than assumed compliant or "
            "non-compliant -- an honest gap, not a guess."
        )

        maverick_data_summary = (
            f"Total spend: ${total:,.0f}. Off-contract (maverick) spend: ${off_contract_total:,.0f} "
            f"({off_contract_total/total*100:.1f}% of total). "
            f"Off-contract spend by category: {maverick_metrics['off_contract_by_cat'].round(0).to_dict()}. "
            f"Unmatched vendor spend (not in contract list): ${unknown_amt:,.0f}."
        )
        with st.spinner("Generating insight..."):
            maverick_insight = generate_insight(client, "Maverick Spend Detection", maverick_data_summary)
        st.info(f"**Insight:** {maverick_insight}")

    # -----------------------------------------------------------------
    # Freight cost variance
    # -----------------------------------------------------------------
    st.divider()
    st.subheader("Freight Cost Variance")

    freight_result = compute_freight_variance(result)

    if freight_result is None:
        st.info(
            "Not enough logistics/freight transactions in this sample (need at least 3) "
            "to compute a meaningful variance threshold."
        )
    else:
        fr_col1, fr_col2, fr_col3 = st.columns(3)
        fr_col1.metric("Category median cost", f"${freight_result['median']:,.0f}")
        fr_col2.metric("Variance threshold (1.5x median)", f"${freight_result['threshold']:,.0f}")
        fr_col3.metric("Flagged as high variance", freight_result["flagged_count"])

        freight_df = freight_result["freight"][["vendor_name", "line_item_description", "amount_usd", "is_variance"]]

        def highlight_variance(row):
            return ["background-color: #fff4e5" if row["is_variance"] else "" for _ in row]

        st.dataframe(freight_df.style.apply(highlight_variance, axis=1), use_container_width=True)

        st.caption(
            "Flags freight transactions costing more than 1.5x the category's own median in this sample -- "
            "a statistical outlier check, not a comparison against an external cost benchmark. "
            "Small samples produce noisier medians; this threshold becomes more meaningful with more data."
        )

        flagged_list = freight_result["freight"][freight_result["freight"]["is_variance"]][["vendor_name", "amount_usd"]].to_dict("records")
        freight_data_summary = (
            f"Category median freight cost: ${freight_result['median']:,.0f}. "
            f"Variance threshold (1.5x median): ${freight_result['threshold']:,.0f}. "
            f"Number of transactions flagged as high variance: {freight_result['flagged_count']}. "
            f"Flagged transactions: {flagged_list if flagged_list else 'none'}."
        )
        with st.spinner("Generating insight..."):
            freight_insight = generate_insight(client, "Freight Cost Variance", freight_data_summary)
        st.info(f"**Insight:** {freight_insight}")

    # -----------------------------------------------------------------
    # Geopolitical risk (RAG)
    # -----------------------------------------------------------------
    st.divider()
    st.subheader("Geopolitical Risk (RAG)")

    country_df = st.session_state.get("country_df")
    pinecone_index = get_pinecone_index()

    if country_df is None:
        st.info(
            "Upload a vendor-country mapping (see the optional uploader above) to unlock this section. "
            "It retrieves relevant tariff context per product category + sourcing country and assesses risk."
        )
    elif pinecone_index is None:
        st.warning(
            "Pinecone is not configured. Set PINECONE_API_KEY as a Streamlit secret or environment "
            "variable, and run setup_pinecone_corpus.py once first. See mvp_documentation.md."
        )
    else:
        with_country = result.merge(country_df, on="vendor_name", how="left")
        unmapped = with_country["country"].isna().sum()
        with_country["country"] = with_country["country"].fillna("Unknown")

        if unmapped > 0:
            st.caption(f"Note: {unmapped} transaction(s) had no matching vendor in the country mapping and are shown as 'Unknown'.")

        if st.button("Assess Geopolitical Risk", type="secondary"):
            openai_client_for_rag = OpenAI(api_key=api_key)
            geo_progress = st.progress(0, text="Retrieving tariff context and assessing risk...")

            def update_geo_progress(fraction):
                geo_progress.progress(fraction, text=f"Assessing risk... {int(fraction * 100)}%")

            geo_result, pair_results, out_of_scope_count = assess_geopolitical_risk(
                with_country, openai_client_for_rag, pinecone_index, progress_callback=update_geo_progress
            )
            geo_progress.empty()
            st.session_state["geo_result"] = geo_result
            st.session_state["pair_results"] = pair_results
            st.session_state["out_of_scope_count"] = out_of_scope_count

        if "geo_result" in st.session_state:
            geo_result = st.session_state["geo_result"]
            pair_results = st.session_state["pair_results"]
            out_of_scope_count = st.session_state.get("out_of_scope_count", 0)

            if out_of_scope_count > 0:
                st.warning(
                    f"{out_of_scope_count} transaction(s) are destined for non-US plants (Germany, "
                    f"Mexico, or Vietnam) and are marked 'Out of scope' below -- this module's tariff "
                    f"corpus currently only covers goods entering the US. Assessing EU, Mexican, or "
                    f"Vietnamese import tariffs would need a separate corpus for each regime."
                )

            in_scope_result = geo_result[geo_result["risk_tier"] != "Out of scope (non-US destination)"]
            risk_spend = in_scope_result.groupby("risk_tier")["amount_usd"].sum()
            high_risk_spend = risk_spend.get("High", 0)
            total_geo_spend = risk_spend.sum()

            geo_col1, geo_col2, geo_col3 = st.columns(3)
            geo_col1.metric("High-risk spend exposure", f"${high_risk_spend:,.0f}")
            geo_col2.metric("% of in-scope spend at High risk", f"{high_risk_spend/total_geo_spend*100:.1f}%" if total_geo_spend else "0%")
            geo_col3.metric("Out-of-scope transactions", out_of_scope_count,
                             help="Destined for a non-US plant -- not assessed, not guessed.")

            if not risk_spend.empty:
                st.markdown("**Spend by Risk Tier (US-destined transactions only)**")
                st.bar_chart(risk_spend, horizontal=True)
            else:
                st.info("No US-destined transactions in this sample to assess.")

            st.markdown("**Risk Assessment by Category + Country (US-destined only)**")
            pair_table = pd.DataFrame([
                {"category": cat, "country": country, "risk_tier": v["risk_tier"], "reasoning": v["reasoning"]}
                for (cat, country), v in pair_results.items()
            ])
            if not pair_table.empty:
                pair_table = pair_table.sort_values(["risk_tier", "category"])
            st.dataframe(pair_table, use_container_width=True)

            st.caption(
                "Risk tiers are synthesized by an LLM reasoning over retrieved, dated tariff facts "
                "(~20 curated sources, compiled Sept 2026) -- not the full federal tariff schedule, "
                "and not a live feed. Assessed once per unique category+country combination, not per "
                "transaction, since tariffs apply at that level. Scoped to US-destined transactions "
                "only -- see the warning above and mvp_documentation.md for why, and what a full "
                "multi-region production version would need."
            )

            if not risk_spend.empty:
                geo_data_summary = (
                    f"Spend by risk tier (US-destined only): {risk_spend.round(0).to_dict()}. "
                    f"High-risk spend: ${high_risk_spend:,.0f} ({high_risk_spend/total_geo_spend*100:.1f}% of in-scope spend). "
                    f"Out-of-scope (non-US-destined) transactions: {out_of_scope_count}. "
                    f"Category/country assessments: {[(cat, country, v['risk_tier']) for (cat, country), v in pair_results.items()]}."
                )
                with st.spinner("Generating insight..."):
                    geo_insight = generate_insight(client, "Geopolitical Risk", geo_data_summary)
                st.info(f"**Insight:** {geo_insight}")

