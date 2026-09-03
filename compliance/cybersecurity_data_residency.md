# Cybersecurity & Data Residency

## Scope note

This sits alongside `eu_ai_act_compliance.md` (product regulation) and `gdpr_documentation.md` (personal data) as a third, distinct lens: **enterprise information security and data residency** — the questions a CTO or CISO asks, not a regulator. These are genuinely different disciplines, and conflating them is a common mistake worth avoiding explicitly.

## The core concern, stated plainly

The current MVP sends data to two public, third-party API endpoints: OpenAI (vendor name, transaction description, amount — for classification and insight generation) and Pinecone (category and country strings only — for tariff retrieval). For a large MNC with a strict "no proprietary data to public cloud" policy, this is a legitimate blocker as-is, not a minor detail.

## Current MVP posture — honest, and appropriate for its actual purpose

The MVP uses the public OpenAI API and Pinecone's hosted service, with the client supplying and controlling their own API keys (per the infrastructure-ownership decision in `strategic_plan.md`). This is acceptable **for a scoped pilot on a limited plant's data**, where the goal is validating the mechanism, not yet meeting full enterprise security review. It is explicitly **not** the recommended posture for full deployment.

## Production-grade recommendation

### 1. Replace the public OpenAI API with Azure OpenAI Service, deployed in the client's own Azure tenant

This is a materially different security posture, not just a vendor swap. Per Microsoft's own documentation: prompts and completions are not shared with OpenAI and are not used to train any model; data stays isolated to the customer's tenant; deployments can be pinned to a specific region or Data Zone (e.g., EU-only) so processing never leaves that geographic boundary; private networking (VNets, private endpoints) means traffic never needs to touch the public internet; access is controlled via the client's existing Microsoft Entra ID and RBAC; encryption can use customer-managed keys. Azure OpenAI carries SOC, ISO, HIPAA, and GDPR compliance certifications.

**Why this resolves the actual objection, not just a technicality:** most large manufacturers already hold an enterprise agreement with Azure, AWS, or GCP as an *approved* cloud vendor. This isn't introducing a new, unvetted third party into the client's environment — it's using infrastructure their own IT security team has typically already reviewed and trusts, just for a new workload.

### 2. Replace the hosted Pinecone service with a local vector store

The tariff knowledge base is only ~20 snippets — small enough that a hosted vector database isn't actually necessary. A local, in-memory or on-disk vector store (e.g., FAISS) running entirely inside the client's own infrastructure removes this third party from the architecture completely for the retrieval step. No data crosses any external boundary for this function at all.

### 3. An existing design strength worth highlighting explicitly

Even in the current MVP, the RAG module only ever sends **category and country strings** to Pinecone — never vendor names, transaction descriptions, or dollar amounts. This wasn't originally designed for this security conversation, but it directly supports it: the most sensitive fields never reached that third party in the first place, in either the current or the recommended architecture.

## What data crosses which boundary — before and after

| Data | Current MVP (pilot-appropriate) | Production recommendation |
|---|---|---|
| Vendor name, description, amount (classification) | Public OpenAI API | Azure OpenAI Service, client's own tenant, region-pinned |
| Category, country (geopolitical risk retrieval) | Pinecone (hosted, public) | Local vector store, inside client infrastructure |
| Classified output, dashboard, reports | Browser session only, never persisted | Same — no change needed |

## Phased recommendation

- **Pilot phase**: current MVP architecture is acceptable, since it operates on a single plant's data under the client's own API keys, for a bounded validation period — not a full production data flow
- **Full deployment phase**: migrate to Azure OpenAI (client tenant, region-pinned) + local vector store, before any company-wide rollout. This is a stated prerequisite for full deployment, not an optional enhancement.

## Summary for a CTO/CISO audience

Data residency concerns are valid and are addressed by moving from public API endpoints to infrastructure the client already owns and controls — not by weakening the AI capability itself. The classification and risk-scoring logic is identical either way; what changes is where it physically runs. This is a deployment architecture decision, already scoped into the full-deployment cost estimate in `roi_risk_assessment.md`, not a new unbudgeted requirement discovered late.
