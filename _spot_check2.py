# -*- coding: utf-8 -*-
import re
for f in ["company-aubo.html", "company-siasun.html"]:
    html = open("database/" + f, encoding="utf-8").read()
    h2s = re.findall(r"<h2>(.*?)</h2>", html)
    print(f, "->", [re.sub(r"<[^>]+>", "", h) for h in h2s])
