# eBay listing agents

This repo turns photos + short notes of things I own into ready-to-paste eBay listing drafts.

## Seller defaults (edit these if they change)
- Seller location: **Malaysia**
- Marketplace: **ebay.com (EBAY_US)** — biggest buyer pool, open to Malaysian sellers
- Currency: **USD**
- Shipping: **worldwide** from Malaysia (Pos Malaysia / courier). Buyer pays shipping unless noted.
- Returns: suggest "No returns" for low-value items (< USD 30), "30-day returns, buyer pays" otherwise.
- Listing format: Buy It Now with Best Offer enabled, unless notes say "auction".

## How it works
- Each item lives in `items/<slug>/` with photos (`.jpg/.jpeg/.png/.webp/.heic`) and `notes.txt`.
- `/list-item <slug>` (or `/list-item` for all un-drafted items) runs three subagents in order:
  1. `item-identifier` → `identification.json`
  2. `price-researcher` → `pricing.json`
  3. `listing-writer` → `listing.md` + `listing.json`
- `listing.json` must follow `templates/listing.schema.json` (shaped like eBay's Inventory API so automated posting can be added later).

## Rules for all agents
- Never invent specs, accessories or condition details not visible in photos or stated in notes. Put doubts under "Open questions".
- eBay titles are max **80 characters**. Count them.
- Always disclose flaws in the condition description.
- Prices are estimates and must cite sources.
- Don't commit photos or personal info; `items/` is gitignored except `items/_example/`.
