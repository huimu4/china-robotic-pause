# -*- coding: utf-8 -*-
"""Fix person-*.html: closing-tag bug from phase D insertion."""
import glob, os, re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for path in sorted(glob.glob(os.path.join(HERE, 'person-*.html'))):
    txt = open(path, encoding='utf-8').read()
    orig = txt
    # 1) fix trailing double close from the official-site card
    txt = txt.replace('</article></article>', '</article>')
    # 2) close the previous card before the official-site card (external https link = official site card)
    pat = re.compile(r'(<article class="card">\n          <h3><a href="https://[^"]+" target="_blank" rel="noopener">Official site)')
    m = pat.search(txt)
    if m:
        # insert a closing </article> right before this card if not already closed
        txt = txt[:m.start()] + '        </article>\n' + txt[m.start():]
    if txt != orig:
        open(path, 'w', encoding='utf-8').write(txt)
        print(os.path.basename(path), 'fixed')
    else:
        print(os.path.basename(path), 'no change')
