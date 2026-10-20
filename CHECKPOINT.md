# Indonesia shopping research skill

**Verification state:** `CLOUD_VERIFIED`

## Relevant Git commit

Task commit: current `HEAD` (the single shopping-skill commit, rebased onto `origin/main`). Parent: `efb6c40fbea7a595f155a5f21fa4515cf00be5e2`.

## Task objective

Implement a reusable, implicitly discoverable native Codex skill named `indonesia-shopping-research` for read-only, evidence-backed PC hardware price comparison across Shopee Indonesia, Tokopedia, Blibli, and Lazada.

## Approved decisions

- Prioritize lowest reliable purchase cost, after excluding incompatible offers.
- Use public web and read-only browser research by default. Do not install scraping dependencies, require authenticated marketplace sessions, or bypass access controls.
- Record marketplace coverage as checked, blocked, unavailable, or not checked.
- Separate verified listing prices from estimated checkout totals and stale search-index observations.
- Report direct product links, timestamps, seller signals, warranty, stock, shipping/discount information, and ranking reasons.
- Do not purchase, change account settings, or handle login credentials.
- Keep changes limited to the skill and this checkpoint; do not push before user review.

## Completed work

- Added `.agents/skills/indonesia-shopping-research/SKILL.md` with discovery description, workflow, compatibility gate, evidence labels, coverage statuses, suspicious-listing guidance, and standard report tables.
- Added `.agents/skills/indonesia-shopping-research/agents/openai.yaml` with UI metadata and `allow_implicit_invocation: true`.
- Dry-run researched DDR4-3200 2x16 GB desktop RAM. No reliable winner could be selected. Shopee's direct product page showed Rp5,039,000 but the retrieved content was crawled last month and marked sold out. Lazada's search/tag page showed Rp1,850,000 for a Kingston Fury Beast 32GB kit, with 5/5 from 31 ratings and 87 sold, but its direct product page returned no readable details; seller was “Lapak Pendaki Outdoor,” warranty, stock, shipping, and model verification were unavailable, and the title included unrelated wording. This remains an unverified search-index lead, not a recommendation. Blibli product detail requests returned 403; an indexed Crucial 32GB DDR4-3200 UDIMM listing had no usable price. Targeted Tokopedia searches returned no usable attributable product listing. Research timestamp: 2026-10-20 06:01 UTC.

## Test and supporting evidence

- `python /run/codex-environment/codex-home/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/indonesia-shopping-research` — passed (`Skill is valid!`).
- `codex debug prompt-input "Compare DDR4-3200 2x16 GB RAM prices in Indonesia"` — passed discovery check; the new skill appears under available skills with its scoped description.
- Parsed `agents/openai.yaml` with PyYAML and asserted implicit invocation, default prompt, display name, coverage labels, price labels, compatibility gate, warranty, and direct-link requirements — passed.
- Public source evidence: Shopee direct listing `https://shopee.co.id/Corsair-DDR4-Vengeance-LPX-32GB-(2X16GB)-3200-MHz-CMK32GX4M2C3200C18-i.107411941.26302014138`; Lazada tag result `https://www.lazada.co.id/tag/memori-ram-32-gb-ddr4/` and linked product `https://www.lazada.co.id/products/pdp-i5884704188.html`; Blibli direct listing request failed with 403; Tokopedia targeted searches surfaced no usable listing.
- Codex prompt-input lists available skills on both relevant and unrelated prompts, so that diagnostic verifies catalog discoverability but does not prove selective activation behavior.
- No application tests apply; no scraping dependencies were installed or executed.

## Unresolved blockers

- Product compatibility cannot be finalized without the buyer's motherboard/device constraints. No destination was provided, so shipping and delivered totals could not be established.
- No current, in-stock offer had enough verifiable price, seller, warranty, and shipping evidence to rank.

## Exact next action

Recheck that `origin/main` is still `efb6c40fbea7a595f155a5f21fa4515cf00be5e2`, then push `main` with a normal fast-forward push.
