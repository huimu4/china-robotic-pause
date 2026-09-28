# -*- coding: utf-8 -*-
import os, re, glob
BASE = r"D:\ObsidianVault\机器人精英圈\china-robotic-pause\database"
files = glob.glob(os.path.join(BASE, "company-*.html"))
no_schema = []
dead = []
for f in files:
    t = open(f, encoding="utf-8").read()
    if "application/ld+json" not in t or "FAQPage" not in t:
        no_schema.append(os.path.basename(f))
    for href in re.findall(r'href="([^"]+\.html)"', t):
        if href.startswith("http"):
            continue
        target = os.path.normpath(os.path.join(BASE, href))
        if not os.path.exists(target):
            dead.append((os.path.basename(f), href))
print("total company pages:", len(files))
print("missing schema:", len(no_schema), no_schema[:5])
print("dead links:", len(dead))
for d in dead[:15]:
    print(" ", d)
