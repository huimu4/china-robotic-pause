# -*- coding: utf-8 -*-
"""Phase A: add News nav item + header search box to every HTML page."""
import glob, os, re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = sorted(glob.glob(os.path.join(HERE, '*.html')))

def add_news(txt):
    pat = re.compile(r'(<li><a href="articles\.html"[^>]*>Insights</a></li>)')
    m = pat.search(txt)
    if not m:
        return txt, False
    txt = pat.sub(lambda mm: mm.group(0) + '\n        <li><a href="news.html">News</a></li>', txt, count=1)
    return txt, True

SEARCH_LI = (
'        <li class="nav-search">\n'
'          <form class="search-form" action="search.html" method="get" role="search">\n'
'            <input type="search" name="q" placeholder="Search\u2026" aria-label="Search this site">\n'
'          </form>\n'
'        </li>\n'
)
def add_search(txt):
    pat = re.compile(r'(\n      </ul>\n    </nav>)')
    if not pat.search(txt):
        return txt, False
    txt = pat.sub(lambda mm: '\n' + SEARCH_LI + '      </ul>\n    </nav>', txt, count=1)
    return txt, True

for f in files:
    with open(f, encoding='utf-8') as fh:
        txt = fh.read()
    orig = txt
    txt, ok1 = add_news(txt)
    txt, ok2 = add_search(txt)
    if txt != orig:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(txt)
    print(os.path.basename(f), '| news:', ok1, '| search:', ok2)
