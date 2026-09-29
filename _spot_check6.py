# -*- coding: utf-8 -*-
import re
for f in ["company-inspire-robots.html", "company-milebot.html", "company-hechuan.html", "company-kepler.html", "company-robosea.html"]:
    try:
        html = open("database/" + f, encoding="utf-8").read()
        h2s = re.findall(r"<h2>(.*?)</h2>", html)
        hero = re.search(r"<section class=\"page-hero\">.*?<p>(.*?)</p>", html, re.S)
        print("=" * 70)
        print(f, "->", [re.sub(r"<[^>]+>", "", h) for h in h2s])
        if hero:
            print("  HERO:", re.sub(r"<[^>]+>", "", hero.group(1)).strip()[:200])
        kf = re.search(r"<h2>Key Facts</h2>(.*?)</table>", html, re.S)
        if kf:
            rows = re.findall(r"<tr><th>(.*?)</th><td>(.*?)</td></tr>", kf.group(1), re.S)
            for th, td in rows:
                print("  KF:", re.sub(r"<[^>]+>", "", th).strip(), "=", re.sub(r"<[^>]+>", " ", td).strip()[:70])
    except FileNotFoundError:
        print(f, "-> FILE MISSING")
