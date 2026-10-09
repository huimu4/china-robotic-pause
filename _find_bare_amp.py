# -*- coding: utf-8 -*-
import io, re, os

base = r"D:\ObsidianVault\机器人精英圈\china-robotic-pause"
c = io.open(os.path.join(base, "news.html"), encoding="utf-8").read()

# 找裸 &（排除合法实体）带上下文
pat = re.compile(r'.{80}&(?!amp;|#\d+;|nbsp;|quot;|lt;|gt;|copy;|reg;|hellip;|ndash;|mdash;|rsquo;|lsquo;|ldquo;|rdquo;|middot;|times;|8599;).{60}', re.S)
for m in pat.finditer(c):
    s = m.group(0).replace("\n", " ")
    print("---")
    print(s)
