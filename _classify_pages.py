# -*- coding: utf-8 -*-
"""Classify company pages by data density."""
import os, re, json

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
pages = [f for f in os.listdir(DB) if f.startswith("company-") and f.endswith(".html")]

thick, mid, thin, no_faq = [], [], [], []
for f in sorted(pages):
    p = os.path.join(DB, f)
    html = open(p, encoding="utf-8").read()
    has_data_snapshot = "Data Snapshot" in html
    has_prod_specs = "Products & Specs" in html
    has_faq_page = "FAQPage" in html
    has_key_facts = "Key Facts" in html
    word_count = len(re.sub(r"<[^>]+>", " ", html).split())
    if has_data_snapshot or has_prod_specs:
        thick.append(f)
    elif has_key_facts and has_faq_page:
        mid.append(f)
    else:
        thin.append(f)
        if not has_faq_page:
            no_faq.append(f)

print("TOTAL:", len(pages))
print("THICK (Data Snapshot/Products & Specs):", len(thick))
print("MID (Key Facts + FAQ, no snapshot):", len(mid))
print("THIN (no Key Facts or no FAQ):", len(thin))
print("  of which NO FAQPage JSON-LD:", len(no_faq))
print("\n--- THIN sample (first 40) ---")
for f in thin[:40]:
    print(" ", f)
