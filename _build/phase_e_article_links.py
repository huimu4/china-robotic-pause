# -*- coding: utf-8 -*-
"""Phase E: add company official-site cards to the 4 insight articles."""
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARTICLES = {
    'humanoid-robot-race.html': [
        ('Unitree', 'https://www.unitree.com/'),
        ('Agibot', 'https://www.agibot.com/'),
        ('UBTECH', 'https://www.ubtrobot.com/'),
        ('Fourier', 'https://www.fftai.com/'),
        ('EngineAI', 'https://www.engineai.com.cn/'),
        ('Booster', 'https://www.booster.tech/'),
    ],
    'china-robot-vacuums.html': [
        ('Narwal', 'https://www.narwal.com/'),
        ('Gausium', 'https://gausium.com/'),
        ('Roborock', 'https://global.roborock.com/'),
        ('Ecovacs', 'https://www.ecovacs.com/'),
    ],
    'china-industrial-robots.html': [
        ('Estun', 'https://en.estun.com/'),
        ('SIASUN', 'https://www.siasun.com/'),
        ('Inovance', 'https://www.inovance.com/'),
        ('Mech-Mind', 'https://www.mech-mind.com/'),
        ('Topstar', 'https://www.topstarmachine.com/'),
    ],
    'robot-startup-funding.html': [
        ('Unitree', 'https://www.unitree.com/'),
        ('Agibot', 'https://www.agibot.com/'),
        ('EngineAI', 'https://www.engineai.com.cn/'),
    ],
}

for fn, sites in ARTICLES.items():
    path = os.path.join(HERE, fn)
    txt = open(path, encoding='utf-8').read()
    links = ' \u00b7 '.join('<a href="%s" target="_blank" rel="noopener">%s \u2197</a>' % (u, n) for n, u in sites)
    card = (
        '\n        <article class="card">\n'
        '          <h3>Company official sites</h3>\n'
        '          <p>%s</p>\n'
        '          <div class="tag-row"><span class="tag amber">Official links</span></div>\n'
        '        </article>' % links
    )
    marker = '</article>\n      </div>'
    if marker in txt:
        txt = txt.replace(marker, card + marker, 1)
        open(path, 'w', encoding='utf-8').write(txt)
        print('%s: +official-sites card (%d links)' % (fn, len(sites)))
    else:
        print('%s: MARKER NOT FOUND' % fn)
