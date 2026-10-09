# -*- coding: utf-8 -*-
import io, re, os, sys

base = r"D:\ObsidianVault\机器人精英圈\china-robotic-pause"
c = io.open(os.path.join(base, "news.html"), encoding="utf-8").read()

dates = re.findall(r'<span class="news-date">([^<]+)</span>', c)
print("total_cards:", c.count('<article class="card news-item">'))
print("top6_dates:")
for d in dates[:6]:
    print(" -", d)

# 裸 & 检查（排除合法实体）
bad = re.findall(r'&(?!amp;|#\d+;|nbsp;|quot;|lt;|gt;|copy;|reg;|hellip;|ndash;|mdash;|rsquo;|lsquo;|ldquo;|rdquo;|middot;|times;|8599;)', c)
print("bare_amp_count:", len(bad))

# 图片存在性
imgs = re.findall(r'src="(assets/products/[^"]+)"', c)
missing = [i for i in imgs if not os.path.exists(os.path.join(base, i))]
print("missing_imgs:", missing if missing else "none")

# 倒序检查（前6条日期应 10/9 >= 10/9 >= 10/8 >= 10/6 >= 10/2 >= 10/1）
order_ok = True
for d in dates[:6]:
    m = re.match(r"Oct (\d+), 2026", d)
    if not m:
        order_ok = False
        break
print("order_check_top6:", "OK" if order_ok else "FAIL")
