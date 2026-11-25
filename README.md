# eBay listing agents

Claude Code subagents that turn photos of your stuff into ready-to-paste eBay listings.
Defaults: sell on **ebay.com in USD**, shipping **worldwide from Malaysia** (change in `CLAUDE.md`).

## Use it
1. Make a folder per item: `items/sony-xm4/`
2. Put in 4–12 photos (whole item, angles, flaws, labels/serial) and a `notes.txt` — see `items/_example/notes.txt`.
3. Open this repo in Claude Code and run:
   ```
   /list-item sony-xm4        # one item
   /list-item                 # every item that doesn't have a listing yet
   ```
4. Open `items/sony-xm4/listing.md` and copy each block into eBay's **Sell an item** form. Upload photos in the suggested order.
5. Answer any **Open questions** by adding to `notes.txt`, delete `listing.md`, and rerun.

## The agents
| Step | Agent | Output |
|---|---|---|
| 1 | `item-identifier` — reads photos + notes, works out exact model, condition, flaws | `identification.json` |
| 2 | `price-researcher` — searches sold/active prices, estimates shipping from Malaysia | `pricing.json` |
| 3 | `listing-writer` — title (≤80 chars), category, item specifics, description, price | `listing.md`, `listing.json` |

`items/` is gitignored (except the example) so your photos stay off GitHub.

Check a draft: `python3 scripts/validate_listing.py items/<slug>/listing.json`

## Phase 2: automatic posting (later)
`listing.json` already follows eBay's Inventory API shape. To post automatically we'll add `scripts/ebay_post.py`
(upload photos → `createOrReplaceInventoryItem` → `createOffer` → `publishOffer`). You'll need, all free:
1. An eBay Developer Program account (developer.ebay.com) and production app keys.
2. A one-time OAuth login to get a user refresh token (valid ~18 months).
3. Business policies (shipping, returns, payment) enabled on your seller account, plus an inventory location in Malaysia.
