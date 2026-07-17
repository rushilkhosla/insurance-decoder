# Insurance Decoder — Product Plan

## The problem
Indians buy insurance they don't understand. The evidence:
- **Mis-selling dominates IRDAI complaint data** — especially "investment + insurance" products sold as fixed deposits, and health policies whose exclusions surface only at claim time.
- **Claim-time shock is the norm in health**: room-rent proportionate deductions, disease sub-limits, 2–4 year waiting periods, consumables exclusions, co-pays hidden in the wording.
- **Motor**: buyers don't know their IDV, depreciation slabs, or that a missing zero-dep add-on halves their payout; many don't know third-party-only vs comprehensive.
- Policy wordings are 40–80 pages of legal English; most buyers never read them, and agents are incentivized not to explain.

## The product (MVP — built)
A tool where you upload your policy PDF and get, in English or Hindi:
1. Plain-language summary of what the product fundamentally is
2. What's covered / what's NOT covered
3. Limits, waiting periods, sub-limits, caps — with the actual numbers
4. Red flags ranked by severity (things that shrink or kill claims)
5. Jargon glossary
6. Specific questions to ask the agent/insurer

Scope: **Health + Motor** first (highest volume, highest pain). ULIPs/endowment later — that's where mis-selling money is, but it needs returns math (IRR of illustrated benefits), a natural v2.

## Regulatory line (important)
- Explaining a document = fine. **Recommending buy/sell/switch = regulated advice** (IRDAI licensing for brokers/agents; SEBI RIA if framed as investment advice for ULIPs). The app's prompt already enforces "explain, never recommend."
- Keep a visible disclaimer (done). If this becomes a business, get legal review before adding any comparison/recommendation features, or partner with a licensed broker (the Ditto model — Ditto is a licensed broker owned by Zerodha).

## Competition
- **Ditto** — human advisors + content, licensed broker, free advice monetized by commission. Strong brand.
- **Beshak** — community/reviews/education content. No document-level tool.
- **PolicyX / Policybazaar** — comparison marketplaces, incentive-conflicted.
- **Gap this fills**: nobody does *"upload YOUR actual policy and get it decoded, in Hindi."* Post-purchase understanding (free-look period! 15–30 days to cancel) is an unserved wedge.

## Wedge & GTM
1. **Free-look window angle**: "Just bought a policy? You have 15 days to cancel. Decode it first." Very shareable.
2. **Claim-rejection angle**: decode before you claim — know your room-rent cap before choosing a hospital room.
3. Distribution: Hindi YouTube/Instagram finance creators, r/IndiaInvestments, Twitter finance circles; each decoded policy generates shareable "red flags found" content.

## Monetization options (later)
- Free decode → paid deep-dive or human review (partner with licensed advisors)
- B2B: HR teams decoding group-health policies for employees
- Broker referral (careful: reintroduces the conflict of interest that created the problem)

## Roadmap
- **v1 (done)**: PDF upload → decoded report, EN/HI, health + motor, local Flask app
- **v1.1**: OCR for scanned PDFs (many insurers email scans); compare "what agent told you" vs "what document says" — user types agent's claims, app fact-checks against the wording
- **v2**: ULIP/endowment decoder with IRR calculation on benefit illustrations; more languages (Tamil, Telugu, Bengali, Marathi)
- **v3**: hosted web app, WhatsApp bot (where the target user actually is), policy-vs-policy comparison

## Costs
~₹3–8 per decode (Claude Sonnet, 40–80 page wording). Cheap enough to give away free while validating.
