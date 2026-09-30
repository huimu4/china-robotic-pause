# -*- coding: utf-8 -*-
import io, re
p = r"D:\ObsidianVault\机器人精英圈\china-robotic-pause\news.html"
h = io.open(p, encoding="utf-8").read()
# extract article blocks in order
blocks = re.findall(r'<article class="card news-item">.*?</article>', h, re.S)
idx = {b: i for i, b in enumerate(blocks)}
sep22 = [b for b in blocks if "Sep 22, 2026" in b]
sep21 = [b for b in blocks if "Sep 21, 2026" in b]
if sep22 and sep21:
    a, b = sep22[0], sep21[0]
    if idx[a] > idx[b]:
        blocks.remove(a)
        blocks.insert(idx[b], a)
        new_h = h
        # rebuild the card-grid section only
        grid_start = new_h.index('<div class="card-grid">')
        grid_end = new_h.index('</div>', new_h.index('card-grid') + 100)
        # find the closing </div> of card-grid: use the next '</section>' fallback
        sec_end = new_h.index('</section>', grid_start)
        new_card_grid = '<div class="card-grid">\n' + "\n".join(blocks) + "\n        </div>"
        new_h = new_h[:grid_start] + new_card_grid + new_h[sec_end:]
        io.open(p, "w", encoding="utf-8", newline="\n").write(new_h)
        print("order fixed, sep22 moved before sep21")
    else:
        print("order already correct")
else:
    print("blocks not found", bool(sep22), bool(sep21))
