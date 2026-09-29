# -*- coding: utf-8 -*-
"""Verify local href/src targets in the three market pages."""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
FILES = ["china-robotics-market.html", "china-cloud-robotics.html", "china-clean-room-robots.html"]

issues = []
for f in FILES:
    p = os.path.join(ROOT, f)
    html = open(p, encoding="utf-8").read()
    links = re.findall(r'(?:href|src)="([^"]+)"', html)
    for l in links:
        if l.startswith(("http://", "https://", "mailto:", "#", "tel:")):
            continue
        if "?" in l:
            l = l.split("?")[0]
        if l.startswith("#"):
            continue
        target = os.path.normpath(os.path.join(ROOT, l))
        if not os.path.exists(target):
            issues.append((f, l, "MISSING"))

for f in FILES:
    html = open(os.path.join(ROOT, f), encoding="utf-8").read()
    # anchor targets
    anchors = set(re.findall(r'id="([^"]+)"', html))
    for href in re.findall(r'href="#([^"]+)"', html):
        if href not in anchors:
            issues.append((f, "#" + href, "NO-ANCHOR"))

if issues:
    for it in issues:
        print("ISSUE:", it)
    sys.exit(1)
print("OK: all local links/images resolve in %d files" % len(FILES))
