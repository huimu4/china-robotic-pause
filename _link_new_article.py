# -*- coding: utf-8 -*-
import os, io

BASE = os.path.dirname(os.path.abspath(__file__))

# 1) sitemap: add new URL after china-robotics-market.html
sp = os.path.join(BASE, "sitemap.xml")
s = io.open(sp, encoding="utf-8").read()
new_loc = "    <loc>https://www.robotichina.com/china-humanoid-market-vs-us-europe.html</loc>"
if "china-humanoid-market-vs-us-europe" in s:
    print("sitemap: already present")
else:
    anchor = "    <loc>https://www.robotichina.com/china-robotics-market.html</loc>"
    s = s.replace(anchor, anchor + "\n" + new_loc, 1)
    io.open(sp, "w", encoding="utf-8", newline="\n").write(s)
    print("sitemap: added")

# 2) articles.html: add card after china-robotics-market card
ap = os.path.join(BASE, "articles.html")
a = io.open(ap, encoding="utf-8").read()
card = '''
        <article class="card">
          <img class="product-photo" src="assets/products/unitree-g1.webp" alt="china vs us humanoid robots" loading="lazy">
          <h3><a href="china-humanoid-market-vs-us-europe.html">China vs. the US &amp; Europe in Humanoid Robots: Who Actually Ships in 2026?</a></h3>
          <p>22,000-36,000 humanoids shipped in H1 2026 — 86-97% of them Chinese. Figure is valued at $39B and Tesla targets 50,000 Optimus units, but China is shipping volume.</p>
          <div class="tag-row"><span class="tag navy">Market</span><span class="tag">Humanoid</span></div>
        </article>
'''
anchor_card = '          <div class="tag-row"><span class="tag navy">Market</span><span class="tag">Data</span></div>\n        </article>'
if "china-humanoid-market-vs-us-europe" in a:
    print("articles: already present")
else:
    a = a.replace(anchor_card, anchor_card + "\n" + card, 1)
    io.open(ap, "w", encoding="utf-8", newline="\n").write(a)
    print("articles: added")
