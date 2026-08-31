# Sprint Plan — Discovery Through Pilot Decision

The 8–10 week engagement (see `cost_estimation/timeline_estimate.md`) organized into five 2-week sprints, each with an explicit in-scope list, an explicit deferred list, and an exit criterion. Deferring items on purpose — not vaguely "later" — is what keeps each sprint honest and reviewable.

| Sprint | Weeks | Scope (in) | Explicitly deferred | Exit criteria |
|---|---|---|---|---|
| **Sprint 0 — Discovery** | 1–2 | ERP export review, data quality assessment, category taxonomy sign-off with procurement stakeholder | Any pipeline or dashboard build work | Taxonomy signed off; sample data extract validated as usable |
| **Sprint 1 — Core Build** | 3–4 | Classification pipeline (prompt design, confidence calibration), LangSmith evaluation harness | Dashboard visuals, human review UI, live plant data | Pipeline runs end-to-end on sample data; ≥80% accuracy on golden evaluation set |
| **Sprint 2 — Dashboard & Review Flow** | 5–6 | PowerBI dashboard (6 metrics), human review queue for low-confidence items | Any live plant integration | Dashboard live and demoable; review queue functional with real routing logic |
| **Sprint 3 — Pilot Execution** | 7–8 | Run the full pipeline against one plant's live, real spend data; measure real-world accuracy | Multi-plant rollout, additional use cases (maverick spend, freight variance) | Live accuracy measured and documented; edge cases and failure modes catalogued |
| **Sprint 4 — Readout & Decision** | 9–10 | Compile pilot results, present ROI/risk findings, facilitate go/no-go decision with stakeholders | Any further development pending the decision | Go/no-go decision made and documented; Round 2 scope adjusted based on real pilot data if needed |

## Why sprints, not just a timeline

A single 10-week bar chart hides where scope could creep. Naming what's explicitly *out* of each sprint is the actual discipline — it means if someone asks "can we also add maverick spend detection in week 4," the answer is a documented "no, that's Sprint 3+ territory" rather than an improvised yes that quietly extends the whole timeline.

## How this connects to the user stories

Each sprint's exit criteria map directly to the acceptance criteria in `planning/user_stories.md`:
- Sprint 1's exit criterion is User Story 1's accuracy bar
- Sprint 2's exit criterion is User Stories 2 and 3's dashboard requirements
- Sprint 3's exit criterion re-validates User Story 1 against real (not synthetic) data — the true test
- Sprint 4's exit criterion is User Story 5's decision-point requirement

## What changes if Sprint 1 or Sprint 3 runs long

Two realistic risk points, both already logged in `research/opportunities_risks.md`:
- **Sprint 1 risk:** if classification accuracy on the golden set falls short of 80%, this sprint extends for prompt iteration rather than proceeding to Sprint 2 with a weak foundation.
- **Sprint 3 risk:** live plant data is messier than any curated sample — if real-world accuracy is meaningfully lower than the golden-set number, Sprint 4's readout reports that honestly rather than the optimistic Round 1 figure.
