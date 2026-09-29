# -*- coding: utf-8 -*-
import re
for f in ["company-estun.html", "company-haribit.html", "company-double-ring.html"]:
    html = open("database/" + f, encoding="utf-8").read()
    has_gb = "Global Benchmark" in html
    cc = re.search(r"<h2>Competitor Comparison</h2>\s*<p>(.*?)</p>", html, re.S)
    cc_text = re.sub(r"<[^>]+>", "", cc.group(1)).strip()[:200] if cc else "(none)"
    print("=" * 70)
    print(f, "| Global Benchmark:", has_gb)
    print(" Competitor Comparison:", cc_text)
