---
name: indonesia-shopping-research
description: Research and compare PC hardware offers in Indonesia across Shopee Indonesia, Tokopedia, Blibli, and Lazada. Use for shopping requests that ask to find, compare, rank, or evaluate Indonesian marketplace hardware prices, including exact model lookups and spec-based component searches. Prioritize the lowest reliable purchase cost; never buy or modify accounts.
---

# Indonesia Shopping Research

Research current public listings for PC hardware sold in Indonesia. Use public web search and read-only browser access by default. Return evidence and clearly describe coverage, uncertainty, and the basis for the ranking.

## Boundaries

- Read public pages and search results only. Do not place orders, add items to carts, submit forms, contact sellers, change account settings, or request, use, or expose credentials.
- Do not install scraping tools, use authenticated marketplace sessions, evade bot checks, bypass access controls, or continue when a marketplace blocks access. A blocked source is a coverage result, not a reason to find a workaround.
- Prefer free, official marketplace pages and public documentation. Treat third-party comparison services as discovery aids; verify candidates on marketplace pages when accessible.
- Do not claim a complete comparison if one or more requested marketplaces were not checked or could not be accessed.
- Do not invent prices, seller details, warranty terms, stock, shipping, discounts, or access results. Cite a direct product link for each offer and give the observation time and timezone (default Asia/Jakarta).

## Workflow

1. **Clarify the target only as needed.** Resolve exact brand/model or required specs, quantity, form factor, condition, and compatibility constraints. Ask for the user's motherboard, CPU, or device model if compatibility depends on it. Ask for destination city/postal code when shipping materially affects ranking. If not provided, show shipping as unknown and do not claim a final delivered cost.
2. **Search the four marketplaces separately.** Check Shopee Indonesia, Tokopedia, Blibli, and Lazada. Use public search and publicly accessible listing pages. Record one coverage state for each: `checked` (search/listing evidence reviewed), `blocked` (access control or explicit denial prevented review), `unavailable` (the site or relevant public page failed to load), or `not checked` (not attempted). Include a short explanation and the evidence path for every state. Do not infer `blocked` merely from no search results.
3. **Normalize the requested product.** Convert the request into required and optional specifications. For PC hardware, check component type, model/part number, capacity, module count, interface/generation, form factor, speed, dimensions, condition, and any platform requirements that apply. Manufacturer documentation may resolve specifications, but does not verify a marketplace listing.
4. **Apply a compatibility gate before ranking.** Exclude offers that conflict with any required specification or platform constraint. For RAM, explicitly distinguish DDR generation, UDIMM vs SO-DIMM, kit capacity and stick count, rated speed, and ECC/registered status when relevant. If a necessary compatibility fact is unknown, label the offer `compatibility unconfirmed` and keep it out of the recommended ranking until resolved. Never let price override incompatibility.
5. **Verify each candidate.** Prefer the direct product page. Capture exact listing title/model, price, stock, condition, seller name and visible reputation signals, warranty, shipping, discount/voucher conditions, and page observation time. Note whether each fact comes from the listing itself, a marketplace search/category page, or an external source. If the direct page is inaccessible, retain only clearly labeled search-index evidence and do not present it as a currently verified listing.
6. **Calculate cost without overstating certainty.** Record list price, shipping, unconditional discounts, conditional seller/platform discounts, and unknowns separately. Calculate `estimated delivered cost` only when enough components are visible; state eligibility assumptions. If shipping or voucher eligibility is unknown, report a subtotal or an estimate with missing components, not an exact checkout total. Do not assume coupon stacking or account eligibility.
7. **Flag reliability and discount concerns.** Explain observable signals, not accusations. Flag unusually low prices, incompatible or ambiguous variants, mixed-model listings, used/refurbished condition, missing warranty, weak or sparse seller history, category/name mismatch, low ratings, inconsistent photos/specs, unclear stock, inflated reference prices, or conditional discounts presented as universal. A large crossed-out price alone does not establish a genuine saving.
8. **Rank eligible offers by lowest reliable purchase cost.** Rank only compatible offers with enough evidence to compare. Consider delivered cost where known, stock, seller signals, warranty, and evidence freshness. Explain why each offer ranks where it does. Keep an unverified low-price offer in a separate watchlist rather than making it the recommendation. If no offer clears the evidence threshold, say so.

## Price and evidence labels

- **Verified listing price:** visible on the direct marketplace product page during this research, with direct link and observation timestamp. This label applies only to the listed product price, not shipping or checkout total.
- **Search-index price:** shown in a marketplace search/category snippet but not confirmed on the current direct product page. Include the source and crawl/observation freshness if available; do not call it a verified current listing price.
- **Estimated checkout/delivered total:** calculated from a verified listing price plus visible or assumed costs. Mark the amount as estimated and itemize every unknown or eligibility assumption.
- **Verified checkout total:** use only when the complete applicable total is publicly visible without signing in or proceeding through purchase. Do not sign in or advance checkout to obtain it.
- **Stale/unavailable:** price or listing cannot be confirmed as current. Do not rank it as a live offer.

## Standard report format

Start with the research timestamp and requested compatibility assumptions. Then provide marketplace coverage:

| Marketplace | Coverage | Evidence path / limitation |
|---|---|---|
| Shopee Indonesia | checked / blocked / unavailable / not checked | Search or listing checked; access limitation |
| Tokopedia | checked / blocked / unavailable / not checked | ... |
| Blibli | checked / blocked / unavailable / not checked | ... |
| Lazada | checked / blocked / unavailable / not checked | ... |

For offers, use one row per distinct model/listing:

| Rank | Marketplace and exact model | Compatibility | Listed price and status | Shipping / discounts | Estimated delivered cost | Stock | Seller signals | Warranty | Evidence time | Direct link | Ranking reason / flags |
|---:|---|---|---|---|---|---|---|---|---|---|---|

Put rejected or unranked listings in a separate section with the reason (incompatible, out of stock, stale, blocked, or insufficient evidence). State explicitly whether any price is verified, estimated, or unavailable. End with material unknowns that could change the ranking.

## Dry-run behavior

When access prevents a valid offer comparison, still complete the report skeleton. Mark failed coverage accurately, use only evidence actually retrieved, and conclude that no reliable winner can be selected if applicable. Never fill missing prices with typical market prices or fabricated estimates.
