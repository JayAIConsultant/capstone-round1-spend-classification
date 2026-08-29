# Cost Analysis — Spend Classification Pilot

## Scope of this estimate

This costs **the ask**, not the whole future — a scoped discovery + pilot to validate the spend classification capability against one plant's real data, matching the presentation guide's own advice ("your ask: what you would do in a real next step — pilot design or deeper discovery"). Full multi-plant deployment costing is Round 2 territory, once the pilot has produced real validation data instead of benchmark assumptions.

## Cost breakdown

| Phase | What's included | Estimated cost |
|---|---|---|
| **Discovery & data readiness** | ERP export review, data quality assessment, category taxonomy validation with procurement team | $8,000 – $12,000 |
| **Classification pipeline build** | Prompt/model tuning, confidence-threshold calibration, human-review workflow setup | $14,000 – $20,000 |
| **Dashboard & reporting rollout** | Spend visibility dashboard build (parallel workstream) | $6,000 – $9,000 |
| **Pilot validation (one plant)** | Running the pipeline against a full plant's live spend data, accuracy validation, refinement | $9,000 – $14,000 |
| **Software/infrastructure (pilot period)** | LLM API usage, workflow automation hosting, dashboard licensing | $500 – $1,200 |
| **Total — Discovery through Pilot** | | **$37,500 – $56,200** |

## Assumptions (stated explicitly, as the brief requires)

| Assumption | Basis |
|---|---|
| Consulting team: 1 senior + 1 mid-level consultant, part-time across the engagement | Standard staffing for a scoped pilot of this size |
| Blended day rate: $900 – $1,300/day | Mid-market rate for boutique AI/procurement consulting (not Big 4 premium, not solo-freelancer discount) |
| Client provides ERP data export access and one procurement stakeholder for validation | Client-side dependency, not billed, but a real prerequisite — flagged as a risk if unavailable |
| LLM API costs at pilot scale (thousands, not millions, of transactions/month) are near-negligible | Classification is a short-prompt, short-output task; even generous volume estimates stay under a few hundred dollars/month at current API pricing |
| One plant, not all four, for pilot validation | Standard pilot-before-scale practice — de-risks the investment before committing to full rollout |
| Software costs assume existing licenses (PowerBI, Google Workspace) where the client already has them | Avoids double-counting tools most mid-to-large manufacturers already hold |

## What this number does NOT include

- Full multi-plant deployment (Round 2 strategic plan / ROI assessment covers this)
- Ongoing managed-service costs post-pilot
- EU AI Act / GDPR compliance documentation work (scoped separately in Round 2, though this use case's minimal/limited-risk classification is expected to keep that lift small)
- Change management / training beyond the pilot's core procurement stakeholder

## Why this range, not a single number

A single point estimate before discovery has actually happened would be a worse answer, not a more confident one — real consulting proposals give ranges pre-discovery and narrow them post-discovery. Being asked "why a range" in Q&A is a good moment to say exactly that.
