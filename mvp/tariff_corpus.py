"""
Curated Tariff & Geopolitical Risk Knowledge Base

~20 snippets, hand-picked and dated -- NOT the full US Harmonized Tariff
Schedule. This is a deliberate scope decision (see use_case_definition.md):
real tariff policy changes monthly, so a comprehensive ingestion would be
stale within weeks regardless of effort. This snapshot is honest about being
a snapshot, dated to when it was compiled, covering only the six countries
and product categories relevant to this dataset.

Sources are real and cited in the 'source' field -- this is not invented
data, though rates should be re-verified before any real business decision.
Compiled: September 2026.
"""

TARIFF_CORPUS = [
    # --- China ---
    {"id": "cn-1", "country": "China", "category": "raw_materials",
     "text": "China-origin steel, aluminum, and copper products face Section 232 duties of up to 50% "
             "in addition to standing Section 301 tariffs, making raw metal imports from China the "
             "highest-tariff-exposure combination in this dataset.",
     "source": "Section 232/301 tariff actions, compiled Sept 2026"},
    {"id": "cn-2", "country": "China", "category": "general",
     "text": "China remains subject to Section 301 tariffs layered on top of any general baseline "
             "rate, and is treated as a distinct, elevated-risk case rather than following the "
             "standard baseline applied to most other trading partners.",
     "source": "USTR Section 301 status, compiled Sept 2026"},
    {"id": "cn-3", "country": "China", "category": "capex_components",
     "text": "Machinery, automation equipment, and electronic components from China can carry "
             "combined duties exceeding 25-35% depending on the specific product line, with some "
             "strategic technology categories facing significantly higher rates.",
     "source": "Section 301 product exclusion lists, compiled Sept 2026"},
    {"id": "cn-4", "country": "China", "category": "mro",
     "text": "Spare parts and MRO components from China are generally subject to the same Section "
             "301 tariff structure as other manufactured goods, though duty rates vary significantly "
             "by the specific HS classification of the part.",
     "source": "USTR tariff schedule notes, compiled Sept 2026"},
    {"id": "cn-5", "country": "China", "category": "packaging",
     "text": "Packaging materials (corrugated board, films, foam) from China are typically assessed "
             "at standard Section 301 rates without the elevated Section 232 treatment reserved for "
             "metals, placing this category at moderate rather than severe exposure.",
     "source": "Section 301 tariff structure, compiled Sept 2026"},

    # --- Vietnam ---
    {"id": "vn-1", "country": "Vietnam", "category": "general",
     "text": "Following a February 2026 Supreme Court ruling that struck down the prior tariff "
             "structure, Vietnam and most other Asian trading partners sit at a 10% baseline duty "
             "rate rather than the higher country-specific rates previously in effect.",
     "source": "Post-ruling baseline tariff structure, compiled Sept 2026"},
    {"id": "vn-2", "country": "Vietnam", "category": "raw_materials",
     "text": "Vietnam has faced increased scrutiny for transshipment of Chinese-origin steel and "
             "metals rerouted through Vietnamese ports, meaning some raw material shipments may "
             "carry elevated risk of enforcement action beyond the standard baseline rate.",
     "source": "Trade enforcement notices on transshipment, compiled Sept 2026"},
    {"id": "vn-3", "country": "Vietnam", "category": "packaging",
     "text": "Vietnam-origin packaging materials are assessed at the standard 10% baseline rate, "
             "with no elevated sector-specific duties currently applied to this category.",
     "source": "Baseline tariff structure, compiled Sept 2026"},
    {"id": "vn-4", "country": "Vietnam", "category": "mro",
     "text": "Vietnam-origin spare parts and MRO components fall under the standard 10% baseline "
             "rate applicable to most manufactured goods from the region.",
     "source": "Baseline tariff structure, compiled Sept 2026"},

    # --- Mexico ---
    {"id": "mx-1", "country": "Mexico", "category": "general",
     "text": "Mexico receives preferential tariff treatment for many product categories under USMCA, "
             "but this preference does not extend uniformly across all goods.",
     "source": "USMCA implementation guidance, compiled Sept 2026"},
    {"id": "mx-2", "country": "Mexico", "category": "raw_materials",
     "text": "Steel, aluminum, and automotive-related raw materials from Mexico continue to carry "
             "Section 232 duties of 25% regardless of USMCA preferential status, since these specific "
             "product categories were carved out of the general USMCA exemption.",
     "source": "Section 232 USMCA carve-out notices, compiled Sept 2026"},
    {"id": "mx-3", "country": "Mexico", "category": "logistics_freight",
     "text": "Cross-border trucking and logistics services between Mexico and the US are governed "
             "primarily by USMCA transportation provisions rather than tariff schedules, since "
             "freight/logistics services themselves are not typically subject to import duties.",
     "source": "USMCA transportation provisions, compiled Sept 2026"},
    {"id": "mx-4", "country": "Mexico", "category": "packaging",
     "text": "Packaging materials from Mexico generally qualify for USMCA preferential treatment, "
             "resulting in minimal to no duty exposure for this category.",
     "source": "USMCA rules of origin, compiled Sept 2026"},

    # --- Germany / EU ---
    {"id": "de-1", "country": "Germany", "category": "general",
     "text": "The European Union, including Germany, operates under a flat 15% all-inclusive tariff "
             "rate for most goods entering the US, a rate negotiated as a comprehensive ceiling "
             "rather than a sector-by-sector schedule.",
     "source": "US-EU trade framework, compiled Sept 2026"},
    {"id": "de-2", "country": "Germany", "category": "capex_components",
     "text": "German-origin automation and precision machinery is subject to the standard 15% EU "
             "rate, with no additional sector-specific surcharge currently applied to industrial "
             "automation equipment.",
     "source": "US-EU trade framework, compiled Sept 2026"},
    {"id": "de-3", "country": "Germany", "category": "raw_materials",
     "text": "Specialty alloys and raw materials from Germany fall under the 15% EU baseline, though "
             "steel and aluminum specifically may still be subject to Section 232 treatment "
             "depending on the exact product classification.",
     "source": "US-EU trade framework and Section 232 notes, compiled Sept 2026"},

    # --- India ---
    {"id": "in-1", "country": "India", "category": "general",
     "text": "India sits at the standard 10% baseline tariff rate applicable to most trading "
             "partners following the February 2026 restructuring, though India has separately faced "
             "scrutiny in ongoing forced-labor and supply chain compliance investigations that could "
             "affect specific shipments.",
     "source": "Baseline tariff structure and compliance notices, compiled Sept 2026"},
    {"id": "in-2", "country": "India", "category": "capex_components",
     "text": "Industrial automation components from India are assessed at the standard 10% baseline "
             "rate, positioning India as a moderate-risk, moderate-cost sourcing alternative to China "
             "for this category.",
     "source": "Baseline tariff structure, compiled Sept 2026"},

    # --- USA (domestic) ---
    {"id": "us-1", "country": "USA", "category": "general",
     "text": "Domestically sourced goods and services carry no import tariff exposure, since tariffs "
             "apply only to goods crossing the US border -- domestic vendors represent zero direct "
             "tariff risk regardless of product category.",
     "source": "General customs principle, compiled Sept 2026"},

    # --- Cross-cutting: services/facilities generally exempt ---
    {"id": "general-1", "country": "any", "category": "indirect_facilities",
     "text": "Facility services such as janitorial work, landscaping, HVAC maintenance, and office "
             "supplies are typically domestically procured labor/services rather than imported "
             "goods, and are not subject to import tariffs regardless of the vendor's location.",
     "source": "General customs principle -- services vs. goods, compiled Sept 2026"},
]

if __name__ == "__main__":
    print(f"Corpus size: {len(TARIFF_CORPUS)} snippets")
    countries = set(c["country"] for c in TARIFF_CORPUS)
    print(f"Countries covered: {sorted(countries)}")
