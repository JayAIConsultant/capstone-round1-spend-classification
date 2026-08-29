# Capstone Round 1 — AI-Powered Spend Visibility for Industrial Manufacturers

**Author:** Jay Ramamoorthi | Ironhack AI Engineering Bootcamp (ACFT July 2026)
**Sector:** Industrial Goods Manufacturing — Large, multi-plant capital equipment producer
**Use case (built):** AI-assisted spend category classification

## Overview

This project pitches an AI solution to "Chleo" — a CEO of a large industrial equipment manufacturer worried that AI is an opaque black box. The pitch centers on **spend category classification**: using an LLM to turn raw, messy transactional spend data into a usable category structure, surfacing supplier concentration, fragmentation, and off-contract spend that leadership currently can't see.

Two additional use cases (maverick spend detection, freight cost variance) are proposed as roadmap items but not built in Round 1 — see `research/use_cases.md` for the scope rationale.

## Repo structure

```
├── README.md                          # this file
├── requirements.txt
├── .env.example
├── research/
│   ├── sector_research.md             # market context + company profile
│   ├── opportunities_risks.md
│   └── use_cases.md                   # 3 use cases; only #1 is built
├── data/
│   ├── dataset_documentation.md       # IMPORTANT: read this first — explains synthetic data rationale
│   ├── data_raw_spend_transactions.csv        # raw, unclassified (380 txns)
│   ├── for_dashboard_classified_spend.csv     # classified + contract status, ready for PowerBI
│   ├── n8n_poc_live_demo_sample.csv           # 20-row sample for the live n8n demo
│   ├── data_ground_truth_categories.csv       # reference labels (eval only)
│   └── data_supplier_contract_status.csv      # reference contract status
├── dashboard/
│   └── dashboard_documentation.md     # metric rationale + PowerBI build steps
│   └── dashboard.pbix                 # [ADD: your built PowerBI file]
├── n8n/
│   ├── workflow.json                  # importable n8n workflow
│   └── workflow_documentation.md
├── langsmith/
│   ├── langsmith_classification_eval.py
│   └── langsmith_documentation.md
├── cost_estimation/
│   ├── cost_analysis.md
│   └── timeline_estimate.md
├── presentation/
│   └── presentation_script.md         # full speaker script, slide-by-slide
│   └── presentation.pdf               # [ADD: your final slide deck]
└── feedback/
    └── round1_decision.md             # [ADD: after presenting to teaching staff]
```

## Setup

1. Clone/download this repo
2. Install Python dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your own API keys (never commit `.env`)
4. See individual `*_documentation.md` files in each folder for tool-specific setup (n8n import steps, LangSmith endpoint configuration, PowerBI import steps)

## How to view/run each piece

- **Dashboard:** Open `dashboard/dashboard.pbix` in PowerBI Desktop (build steps in `dashboard/dashboard_documentation.md` if reproducing from scratch)
- **n8n POC:** Import `n8n/workflow.json` into your n8n instance, add your own OpenAI + Google Sheets credentials (see `n8n/workflow_documentation.md`)
- **LangSmith:** Run `langsmith/langsmith_classification_eval.py` with your own API keys set as environment variables (see `langsmith/langsmith_documentation.md` — includes an important EU/US endpoint note)

## Key honest caveats (stated upfront, not buried)

- The transactional dataset is **synthetic**, built to reflect realistic messy ERP export conditions — not sourced from a real company. Full rationale in `data/dataset_documentation.md`.
- The dashboard's category view represents the *target output* of the classification pipeline; the *live, real* classification mechanism is proven separately and specifically in the n8n POC (20-row sample) and the LangSmith evaluation (same 20 rows, scored against known-correct labels, ~85% zero-shot accuracy).
- Cost and savings estimates are conservative, benchmark-based projections for a scoped pilot — not a company-specific ROI. Round 2 would refine these against real validation data.

## Status

Round 1 deliverable, presented to teaching staff. See `feedback/round1_decision.md` for the keep/change decision once available.
