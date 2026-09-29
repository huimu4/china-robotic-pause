# -*- coding: utf-8 -*-
"""Fix two cosmetic artifacts from the enhancer:
1. '<li>both X</li>' -> '<li>X</li>'
2. double-escaped '&amp;amp;' -> '&amp;'
Only touches files that contain a Data Snapshot block (i.e. the 184 enhanced pages).
"""
import os, re, io

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
pages = [f for f in os.listdir(BASE) if f.startswith("company-") and f.endswith(".html")]

fixed = []
for f in sorted(pages):
    p = os.path.join(BASE, f)
    html = open(p, encoding="utf-8").read()
    if "Data Snapshot" not in html:
        continue
    new = html
    new = re.sub(r"<li>both\s+", "<li>", new, flags=re.I)
    new = new.replace("&amp;amp;", "&amp;")
    if new != html:
        io.open(p, "w", encoding="utf-8", newline="\n").write(new)
        fixed.append(f)

print("FIXED:", len(fixed))
