# -*- coding: utf-8 -*-
import io, re
h = io.open(r"D:\ObsidianVault\机器人精英圈\china-robotic-pause\news.html", encoding="utf-8").read()
print("news-item count:", len(re.findall(r'class="card news-item"', h)))
titles = re.findall(r'<h3><a[^>]*>(.*?)</a></h3>', h, re.S)
print("total titles:", len(titles))
for t in titles[:8]:
    print(" -", t.strip()[:90])
# check amp escaping
print("has raw & in titles:", bool(re.search(r'<h3><a[^>]*>[^<]*&(?!amp;|#)', h, re.S)))
# check dates order (first 8)
dates = re.findall(r'<span class="news-date">(.*?)</span>', h, re.S)
print("dates[:8]:", [d.strip()[:20] for d in dates[:8]])
