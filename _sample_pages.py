# -*- coding: utf-8 -*-
"""Sample hero desc / focus / hq patterns from 8 thin pages to calibrate extraction."""
import os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
samples = ["company-58-intelligence.html","company-aubo.html","company-cursor-infi.html",
           "company-droidup.html","company-hans-robot.html","company-luster.html",
           "company-siasun.html","company-topstar.html","company-veichi.html","company-xcmg.html"]
for f in samples:
    html = open(os.path.join(DB, f), encoding="utf-8").read()
    h1 = re.search(r"<h1>([^<]*)</h1>", html)
    h2 = re.search(r"<h2>([^<]*)</h2>", html)
    hero = re.search(r'<p>([^<]*)</p>', html.split("page-hero")[1]) if "page-hero" in html else None
    faq_hq = re.search(r"headquartered in ([^,<]+),? China", html)
    print("="*80)
    print(f)
    print(" H1:", h1.group(1).strip() if h1 else None)
    print(" H2:", h2.group(1).strip() if h2 else None)
    print(" HERO:", hero.group(1).strip()[:160] if hero else None)
    print(" HQ:", faq_hq.group(1).strip() if faq_hq else None)
