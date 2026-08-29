# Timeline Estimate — Discovery Through Pilot

## Phase timeline (8–10 weeks total)

| Weeks | Phase | Key activities | Dependencies |
|---|---|---|---|
| 1–2 | Discovery & data readiness | ERP export pull, data quality review, category taxonomy sign-off with procurement | Client provides data access + stakeholder time |
| 2–5 | Classification pipeline build | Prompt tuning, confidence calibration, human-review routing setup, integration with client's spend data format | Runs partly in parallel with dashboard build |
| 3–5 | Dashboard & reporting rollout | Build spend visibility dashboard on classified output | Needs early pipeline output to build against |
| 6–9 | Pilot validation | Run against one full plant's live spend, measure accuracy, refine thresholds and edge cases | Needs a real plant's cooperation and live data feed |
| 9–10 | Pilot readout & go/no-go | Present validated results, decide: expand to full deployment, adjust scope, or pause | Client decision point |

## Why this pacing

- **Discovery isn't rushed** — a classification system built on unvalidated assumptions about the category taxonomy fails quietly later, not loudly now. Two weeks upfront avoids a much more expensive rebuild in week 6.
- **Dashboard build runs parallel to pipeline build**, not sequentially after — no reason to wait for pipeline perfection before starting the visualization layer against early output.
- **The pilot is scoped to one plant, not all four** — proving the mechanism works on real, messy, single-plant data is the actual test; scaling to four plants before that proof exists would just multiply any undiscovered problems by four.

## What could compress or extend this

**Could compress to ~6 weeks if:** data is already well-structured and export-ready, and one procurement stakeholder is dedicated (not shared) for validation.

**Could extend to ~12–14 weeks if:** ERP data requires significant cleanup, multiple procurement stakeholders need to align on taxonomy definitions, or the pilot plant's spend patterns surface edge cases (e.g., heavily bundled invoices) not represented in the discovery sample.

## Next milestone after this timeline

A go/no-go decision at week 10, informed by real pilot accuracy data — not benchmark assumptions. That decision, and the resulting scope, is what Round 2's strategic deployment plan builds from.
