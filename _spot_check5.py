# -*- coding: utf-8 -*-
import re
for f in ["company-haribit.html", "company-double-ring.html", "company-topstar.html", "company-estun.html"]:
    html = open("database/" + f, encoding="utf-8").read()
    print("=" * 70)
    print(f)
    hero = re.search(r"<section class=\"page-hero\">.*?<p>(.*?)</p>", html, re.S)
    if hero:
        print(" HERO:", re.sub(r"<[^>]+>", "", hero.group(1)).strip()[:220])
    kf = re.search(r"<h2>Key Facts</h2>(.*?)</table>", html, re.S)
    if kf:
        rows = re.findall(r"<tr><th>(.*?)</th><td>(.*?)</td></tr>", kf.group(1), re.S)
        for th, td in rows:
            print("  KF:", re.sub(r"<[^>]+>", "", th).strip(), "=", re.sub(r"<[^>]+>", " ", td).strip()[:80])
    ds = re.search(r"<h2>Data Snapshot</h2>(.*?)</table>", html, re.S)
    if ds:
        rows = re.findall(r"<tr><th>(.*?)</th><td>(.*?)</td></tr>", ds.group(1), re.S)
        for th, td in rows:
            print("  DS:", re.sub(r"<[^>]+>", "", th).strip(), "=", re.sub(r"<[^>]+>", " ", td).strip()[:80])
