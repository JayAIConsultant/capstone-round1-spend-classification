# EU AI Act Compliance Documentation

## Regulatory context (current as of September 2026)

The EU AI Act (Regulation (EU) 2024/1689) entered into force August 1, 2024, with obligations phased in over time rather than all at once. As of this writing: prohibited AI practices have applied since February 2, 2025; obligations for general-purpose AI model providers (relevant to OpenAI, whose models this system uses) have applied since August 2, 2025; and Article 50 transparency obligations took effect August 2, 2026, as originally scheduled. Separately, a "Digital Omnibus on AI" package — politically agreed in May 2026 and formally adopted mid-2026 — deferred the high-risk (Annex III) compliance obligations from their original August 2026 date to December 2, 2027. This deferral is noted for completeness; as the classification below shows, it does not change this system's obligations either way, since it isn't a high-risk system regardless of which deadline applies.

## Risk classification: Minimal Risk

The Act uses a four-tier risk model. Working through each tier in order:

### Tier 1 — Prohibited practices (Article 5)? No.

Checked against the enumerated prohibited practices — manipulative or subliminal techniques causing harm, exploitation of vulnerable groups, social scoring of natural persons by public authorities, real-time remote biometric identification in public spaces for law enforcement, emotion recognition in the workplace, and others. This system does none of these. It classifies procurement transactions and assesses vendor/supplier risk; it has no interaction with the practices this tier addresses.

### Tier 2 — High-risk (Article 6, Annex III)? No.

Annex III enumerates eight specific high-risk domains: biometrics; critical infrastructure management; education and vocational training; employment, worker management, and access to self-employment; access to essential private and public services (including credit scoring and insurance risk assessment for natural persons); law enforcement; migration, asylum, and border control; and administration of justice and democratic processes.

This system falls into none of these. The key distinction worth stating explicitly: Annex III's "access to essential services" category (which includes credit scoring) applies specifically to **natural persons** — an individual's access to credit, insurance, or public benefits. This system assesses **corporate vendor and spend-category risk** (contract compliance, supplier concentration, tariff exposure) — a business analytics function, not a determination about any individual person's access to a service. It also does not manage or evaluate human employees, and does not touch biometric, law enforcement, migration, education, or judicial functions.

### Tier 3 — Limited risk, transparency obligations (Article 50)? No.

Article 50 obligations apply to: systems intended to interact directly with natural persons in a way that could be mistaken for human interaction (e.g., chatbots); systems generating synthetic audio/image/video/text content intended to inform the public (deepfakes); and emotion recognition or biometric categorization systems.

This system is an internal business analytics tool operated by employees who knowingly upload a file and click a button — there is no ambiguity about whether they're interacting with AI, and no public-facing synthetic content is generated. No biometric or emotion data is processed. Article 50 obligations are not triggered as a legal requirement.

**Note:** even though not legally required, this system already exceeds Article 50's transparency spirit voluntarily — every classification shows its reasoning, every risk assessment cites its source context, and every review flag states why it was raised. This is documented further below.

### Tier 4 — Minimal or no risk. Confirmed.

No mandatory obligations apply under the Act. Voluntary adherence to codes of conduct (Article 95) is encouraged for minimal-risk systems, which this documentation addresses in the next section.

## A note on the underlying model provider

This system is built on OpenAI's GPT-4o-mini and text-embedding-3-small models — general-purpose AI (GPAI) models under the Act's Title VIII. The GPAI-level transparency, documentation, and copyright obligations fall on OpenAI as the model **provider**, not on this application as a **deployer** built on top of the API. As a matter of due diligence, this system relies on a GPAI provider with active compliance obligations already in force since August 2025, rather than an unregulated or non-compliant model source.

## Voluntary good practices already in place (mapped to what higher-risk systems would require)

Even though not legally mandated at this risk tier, this system was already built with practices that mirror what a higher-risk system's obligations would demand — worth stating explicitly, since it shows the design wasn't "minimal risk, therefore minimal care":

| Practice | Where it's implemented |
|---|---|
| Transparency of reasoning | Every classification includes the model's stated reasoning, not just a label |
| Human oversight / review routing | Confidence-threshold and keyword-based safety net route uncertain or known-risky classifications to a human, rather than fully automating the decision |
| Documented data provenance | `dataset_documentation.md` states explicitly what's synthetic vs. real, and why |
| Performance evaluation against ground truth | Scored accuracy evaluation (LangSmith, Round 1) and repeated live verification (Round 2), not just an unscored demo |
| Documented limitations | Every module's known limits are stated in `mvp_documentation.md`, not left implicit |
| Grounded, cited outputs (geopolitical risk module) | RAG retrieval over dated, sourced tariff facts rather than the model recalling figures from memory |

## Conformity Assessment Summary

Because this system is classified as minimal risk, **no third-party conformity assessment or CE marking is legally required** under the Act — these apply only to high-risk systems under Article 6(2)/Annex III. This section documents the internal self-assessment basis for the classification above, which would support a re-classification review if the system's scope later expanded into a higher-risk use case (for example, if a future version were used to make binding decisions about individual employees rather than business-level spend patterns).

**Basis for self-assessment:** the four-tier walkthrough above, cross-checked against the system's actual documented scope in `use_case_definition.md` (explicit out-of-scope boundaries already exclude employment decisions, credit/insurance determinations for individuals, and any biometric or law-enforcement function).

## Technical Documentation Outline

Presented as good practice, adapted from the structure Annex IV specifies for high-risk systems, even though not mandated at this risk tier — and mostly already satisfied by existing project documentation rather than written fresh here:

1. **System overview & intended purpose** — see `use_case_definition.md`
2. **Data** — sources, provenance, synthetic vs. real — see `data/dataset_documentation.md`
3. **Models used** — GPT-4o-mini (classification, risk synthesis, insights), text-embedding-3-small (retrieval) — see `mvp/mvp_documentation.md`
4. **Development & testing methodology** — two-level testing approach (mocked logic verification + live ground-truth verification) — see `mvp/mvp_documentation.md`
5. **Performance metrics** — 85% (Round 1, n=20), 93.3%–100% (Round 2, n=60–90) classification accuracy against known-correct labels — see `mvp/mvp_documentation.md`
6. **Human oversight measures** — confidence threshold + keyword safety net + self-consistency voting — see `mvp/mvp_documentation.md`
7. **Known limitations** — stated per-module — see `mvp/mvp_documentation.md`
8. **Risk assessment** — see `roi_risk_assessment.md`
9. **Version/iteration history** — the classification module's full investigation across 8 iterations is documented as a real change log — see `mvp/mvp_documentation.md`

## Summary for non-specialist stakeholders (e.g., Chleo)

This system does not fall into any legally regulated high-risk category under EU AI law — it's an internal spend-analytics tool, not a system that makes binding decisions about people's employment, credit, benefits, or legal rights. No mandatory compliance obligations apply. That said, it was built with the transparency and human-oversight habits a more heavily regulated system would require anyway, because those are simply good practice — not because the law demands it here.
