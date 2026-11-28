---
description: Draft eBay listings for items in items/<slug>/ (photos + notes.txt)
argument-hint: "[slug ...]  (omit to draft every item without a listing.md)"
---

Draft eBay listings. Arguments: `$ARGUMENTS`

1. Decide which items to process:
   - If arguments were given, each is a folder name under `items/`.
   - Otherwise, every folder in `items/` (except `_example`) that has no `listing.md` yet.
   If a folder has no photos, skip it and tell me.
2. For each item, run these subagents **in order**, passing the folder path `items/<slug>/`:
   1. `item-identifier`
   2. `price-researcher`
   3. `listing-writer`
   Different items may be processed in parallel, but the three steps for one item must run in sequence.
3. After all are done, verify each `listing.json` against the schema:
   `python3 scripts/validate_listing.py "items/<slug>/listing.json"` (on Windows use `python` if `python3` isn't found; quote paths, folder names may contain spaces)
4. Give me a short table: item, title, suggested price (USD), confidence, number of open questions. Then list the open questions per item so I can answer them (I'll update notes.txt and rerun).
