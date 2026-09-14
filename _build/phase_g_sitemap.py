# -*- coding: utf-8 -*-
"""Add news.html to sitemap.xml"""
import os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(HERE, 'sitemap.xml')
txt = open(path, encoding='utf-8').read()
entry = (
'  <url>\n'
'    <loc>https://www.robotichina.com/news.html</loc>\n'
'    <lastmod>2026-08-26</lastmod>\n'
'    <changefreq>weekly</changefreq>\n'
'    <priority>0.9</priority>\n'
'  </url>\n'
)
if 'news.html' not in txt:
    marker = '  </url>\n  <url>\n    <loc>https://www.robotichina.com/about.html'
    txt = txt.replace(marker, entry + '  </url>\n  <url>\n    <loc>https://www.robotichina.com/about.html', 1)
    open(path, 'w', encoding='utf-8').write(txt)
    print('sitemap.xml: news.html added')
else:
    print('sitemap.xml: news.html already present')
