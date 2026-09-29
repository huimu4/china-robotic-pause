# -*- coding: utf-8 -*-
"""Analyze Key Facts table headers across MID pages to build a compatible enhancer."""
import os, re, collections, json

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
pages = [f for f in os.listdir(DB) if f.startswith("company-") and f.endswith(".html")]

field_counter = collections.Counter()
variants = {}   # slug -> {fields: [...], overview_lis: n, faq_q: n}
mid = []

for f in sorted(pages):
    html = open(os.path.join(DB, f), encoding="utf-8").read()
    if ("Data Snapshot" in html) or ("Products & Specs" in html):
        continue
    # Key Facts table rows
    kf = re.search(r"<h2>Key Facts</h2>\s*<table[^>]*>(.*?)</table>", html, re.S)
    fields = []
    if kf:
        for m in re.finditer(r"<tr><th>(.*?)</th><td>(.*?)</td></tr>", kf.group(1), re.S):
            th = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            td = re.sub(r"<[^>]+>", " ", m.group(2)).strip()
            fields.append((th, td))
        for th, _ in fields:
            field_counter[th] += 1
    # Overview lis
    ov = re.search(r"<h2>Company Overview</h2>\s*<ul>(.*?)</ul>", html, re.S)
    n_li = len(re.findall(r"<li>", ov.group(1))) if ov else 0
    # FAQ questions
    n_faq = len(re.findall(r"<h3>", html))
    variants[f] = {"fields": [f[0] for f in fields], "n_li": n_li, "n_faq": n_faq}
    mid.append(f)

print("MID count:", len(mid))
print("\nKey Facts header frequency:")
for k, v in field_counter.most_common(25):
    print(f"  {v:4d}  {k}")

# pages lacking typical headers
print("\nPages with odd Key Facts structures (no Full Name / no Headquarters):")
for f, v in variants.items():
    fs = v["fields"]
    if not fs or ("Full Name" not in fs and "Headquarters" not in fs):
        print(" ", f, "->", fs, "| overview_li:", v["n_li"], "| faq:", v["n_faq"])

print("\nDistribution of overview li counts:", collections.Counter(v["n_li"] for v in variants.values()).most_common())
print("Distribution of faq counts:", collections.Counter(v["n_faq"] for v in variants.values()).most_common())
