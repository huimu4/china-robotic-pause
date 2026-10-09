# -*- coding: utf-8 -*-
"""批量修复 GA4 Measurement ID：G-M63KB9ZNPK -> G-M63KB9ZNFK（官方 ID，2026-10-09 从 GA4 Admin 确认）"""
import io, os, sys

BASE = r"D:\ObsidianVault\机器人精英圈\china-robotic-pause"
OLD = "G-M63KB9ZNPK"
NEW = "G-M63KB9ZNFK"

changed = []
total = 0
for root, dirs, files in os.walk(BASE):
    # 跳过 .git
    dirs[:] = [d for d in dirs if d not in (".git",)]
    for fn in files:
        if not fn.endswith(".html"):
            continue
        p = os.path.join(root, fn)
        total += 1
        with io.open(p, encoding="utf-8") as f:
            c = f.read()
        if OLD in c:
            c2 = c.replace(OLD, NEW)
            with io.open(p, "w", encoding="utf-8", newline="") as f:
                f.write(c2)
            changed.append(p)

print("html_files:", total)
print("changed_files:", len(changed))
# 输出前几个已改文件
for p in changed[:10]:
    print(" -", os.path.relpath(p, BASE))
