#!/usr/bin/env python3
"""Validate an items/<slug>/listing.json against templates/listing.schema.json.

Uses the `jsonschema` package if installed; otherwise falls back to the key checks.
Usage: python3 scripts/validate_listing.py items/<slug>/listing.json [...]
"""
import json
import sys
from pathlib import Path

SCHEMA = Path(__file__).resolve().parent.parent / "templates" / "listing.schema.json"


def basic_checks(data, folder):
    errors = []
    for key in ("sku", "marketplaceId", "product", "condition", "offer", "imageFiles"):
        if key not in data:
            errors.append(f"missing '{key}'")
    product = data.get("product", {})
    title = product.get("title", "")
    if not title:
        errors.append("product.title is empty")
    elif len(title) > 80:
        errors.append(f"title is {len(title)} chars (max 80)")
    if not product.get("description"):
        errors.append("product.description is empty")
    offer = data.get("offer", {})
    if not isinstance(offer.get("price"), (int, float)) or offer.get("price", 0) <= 0:
        errors.append("offer.price must be a positive number")
    allowed = json.loads(SCHEMA.read_text())["properties"]["condition"]["enum"]
    if data.get("condition") not in allowed:
        errors.append(f"condition must be one of {allowed}")
    for name in data.get("imageFiles", []):
        if not (folder / name).exists():
            errors.append(f"image not found: {name}")
    return errors


def main(paths):
    if not paths:
        print(__doc__)
        return 2
    try:
        import jsonschema  # optional
    except ImportError:
        jsonschema = None
    schema = json.loads(SCHEMA.read_text())
    failed = False
    for p in map(Path, paths):
        try:
            data = json.loads(p.read_text())
        except (OSError, json.JSONDecodeError) as e:
            print(f"FAIL {p}: {e}")
            failed = True
            continue
        errors = basic_checks(data, p.parent)
        if jsonschema:
            errors += [e.message for e in jsonschema.Draft202012Validator(schema).iter_errors(data)]
        if errors:
            failed = True
            print(f"FAIL {p}")
            for e in dict.fromkeys(errors):
                print(f"  - {e}")
        else:
            print(f"OK   {p}  ({len(data['product']['title'])}-char title, {data['offer']['currency']} {data['offer']['price']})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
