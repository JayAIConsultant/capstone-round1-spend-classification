# GDPR Documentation

## Scope note, stated upfront

This document is intentionally short. The system processes B2B procurement and vendor spend data — not personal data about identifiable individuals, in the overwhelming majority of its fields. Where personal data *could* incidentally appear (explained below), it's handled explicitly rather than ignored. A short, honest GDPR document reflecting genuinely low exposure is a stronger answer here than an artificially padded one.

## Data flow map

```
Vendor/spend data (CSV upload or demo dataset)
        |
        v
AI classification (OpenAI API call -- vendor name, line-item description, amount)
        |
        v
Dashboard / Maverick Spend / Freight Variance computation (local, in-memory)
        |
        v
Geopolitical Risk assessment (Pinecone retrieval + OpenAI synthesis -- category + country only, no vendor-identifying data sent)
        |
        v
Displayed to user in-browser; optional CSV download
        |
        v
Session ends -- no data persisted anywhere
```

**Third parties in this flow:** OpenAI (processes vendor names, line-item descriptions, and amounts via API calls for classification and insight generation) and Pinecone (receives only category and country strings for retrieval — never vendor names, amounts, or any transaction-level data).

## Processing activities register

| Activity | Data involved | Legal basis | Retention | Recipients |
|---|---|---|---|---|
| Spend classification | Vendor company name, transaction description, amount | Legitimate interest (internal business operations analytics) | None — session memory only, cleared on close | OpenAI (processor, API call only) |
| Dashboard/Maverick/Freight computation | Same, aggregated | Legitimate interest | None — session memory only | None (local computation) |
| Geopolitical risk assessment | Product category + country (no vendor identifiers) | Legitimate interest | None — session memory only | OpenAI, Pinecone (processors) |

**Note on "vendor company name":** in nearly every case, this is a company/legal entity name (e.g., "SteelCore Industries"), not a natural person's name. GDPR applies to personal data about identifiable natural persons — a company name alone is not personal data under the Regulation. The narrow exception is addressed next.

## Where personal data could actually appear, and how it's handled

The one realistic scenario: a small business operating under an individual's name (a sole proprietorship, e.g., "John Smith Consulting") could make a vendor field indirectly identify a natural person. This system does not detect or filter for this case automatically in the current MVP — a stated, honest limitation, not a hidden gap.

**What this means practically:** the risk is narrow (affects a small subset of vendor records, only for certain business structures) and the processing purpose (spend classification, not profiling of the individual) is unrelated to anything about that person specifically. This is a legitimate item for the DPIA below rather than something requiring a redesign.

## Short DPIA (Data Protection Impact Assessment)

**Is a full DPIA legally required?** Under GDPR Article 35, a DPIA is mandatory only where processing is "likely to result in a high risk" to individuals' rights — e.g., large-scale profiling, special category data, systematic monitoring. This system does neither: it doesn't profile individuals, doesn't process special category data (health, biometric, etc.), and the incidental sole-proprietor edge case above is narrow and non-systematic. A full statutory DPIA is not triggered. This short-form assessment is provided as good practice regardless.

**Nature of processing:** Automated classification of business transaction records; no automated decision-making with legal or similarly significant effects on any individual (Article 22 is not engaged, since no individual is being scored, evaluated, or denied anything by this system).

**Necessity and proportionality:** Processing is limited to what's needed for spend classification (vendor name, description, amount) — no excess data collection, no special category data.

**Risk to individuals:** Low. In the rare sole-proprietor edge case, the only "processing" occurring is categorizing a business transaction into a procurement category — not evaluating, scoring, or making any decision about the individual themselves.

**Mitigations already in place:** no data persistence beyond the browser session; no special category data collected; third-party processors (OpenAI, Pinecone) are established providers with their own GDPR-compliant data processing terms.

**Residual risk:** Low. Recommended before any production deployment: add an explicit check/warning if a vendor field pattern suggests an individual's name rather than a company name, and extend the contract with OpenAI/Pinecone to a formal Data Processing Agreement (DPA) — both are Round 2→production items, listed in `strategic_plan.md`.

## Data subject rights

Given the low personal-data footprint, most GDPR data subject rights (access, rectification, erasure, portability) have minimal practical scope in this system — there is no persistent personal data store to query, correct, or export. In the narrow sole-proprietor edge case, a rights request would be handled by locating and removing the specific vendor record from any downstream export the user retained (the application itself retains nothing after the session ends).

## Third-party and cross-border transfers

- **OpenAI**: US-based provider; transaction descriptions and vendor names are sent via API for classification. OpenAI's standard API terms include data processing commitments; a production deployment should formalize this with a signed DPA and confirm OpenAI's current EU-US data transfer mechanism (e.g., EU-U.S. Data Privacy Framework participation) before processing any real company's data.
- **Pinecone**: receives only category and country strings for the geopolitical risk module — no vendor-identifying or transaction-level data crosses this boundary at all, by design.

## Summary for non-specialist stakeholders

This system's GDPR exposure is genuinely low because it processes business transaction data, not personal data, in nearly all cases. The one narrow edge case (sole-proprietor vendor names) is documented honestly rather than ignored, with a clear, low-cost fix identified for a production version. No full DPIA is legally required, but this document provides one anyway as good practice.
