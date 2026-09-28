# -*- coding: utf-8 -*-
"""Verify internal hrefs of the two new market articles resolve to existing files."""
import os, re, sys

ROOT = r"D:\ObsidianVault\机器人精英圈\china-robotic-pause"
FILES = ["china-robotics-market.html", "china-educational-robots-market.html"]

problems = []
for f in FILES:
    path = os.path.join(ROOT, f)
    html = open(path, encoding="utf-8").read()
    hrefs = re.findall(r'href="([^"]+)"', html)
    for h in hrefs:
        if h.startswith(("http", "#", "mailto:", "javascript:")):
            continue
        h_clean = h.split("#")[0]
        if not h_clean:
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(path), h_clean))
        if not os.path.exists(target):
            problems.append(f"{f}: MISSING {h}")

# check referenced images exist
for f in FILES:
    path = os.path.join(ROOT, f)
    html = open(path, encoding="utf-8").read()
    imgs = re.findall(r'src="([^"]+)"', html)
    for im in imgs:
        if im.startswith(("http", "data:")):
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(path), im))
        if not os.path.exists(target):
            problems.append(f"{f}: MISSING IMG {im}")

if problems:
    print("PROBLEMS:")
    for p in problems:
        print(" ", p)
    sys.exit(1)
else:
    print(f"OK: {len(FILES)} files, all internal hrefs and images resolve.")
