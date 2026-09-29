# -*- coding: utf-8 -*-
import re
for f in ["company-topstar.html", "company-estun.html", "company-haribit.html", "company-double-ring.html"]:
    try:
        html = open("database/" + f, encoding="utf-8").read()
        h2s = re.findall(r"<h2>(.*?)</h2>", html)
        print(f, "->", [re.sub(r"<[^>]+>", "", h) for h in h2s])
        kf = re.search(r"<h2>Key Facts</h2>(.*?)</table>", html, re.S)
        if kf:
            print("  KeyFacts:", re.findall(r"<th>(.*?)</th>", kf.group(1)))
    except FileNotFoundError:
        print(f, "-> FILE MISSING")
