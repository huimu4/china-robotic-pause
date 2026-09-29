# -*- coding: utf-8 -*-
import os, re, io
BASE = os.path.dirname(os.path.abspath(__file__))
files = ["china-robotics-market.html", "china-cloud-robotics.html",
         "china-educational-robots-market.html", "china-clean-room-robots.html"]
for f in files:
    p = os.path.join(BASE, f)
    html = open(p, encoding="utf-8").read()
    html = html.replace('"dateModified": "2026-09-28"', '"dateModified": "2026-09-29"')
    html = re.sub(r'Last updated: Sep 28, 2026', 'Last updated: Sep 29, 2026', html)
    io.open(p, "w", encoding="utf-8", newline="\n").write(html)
    print("timestamped:", f)
