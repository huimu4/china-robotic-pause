# -*- coding: utf-8 -*-
"""Insert 6 new news cards (Sep 21-29, 2026) at the top of news.html."""
import os, io, html as H

BASE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(BASE, "news.html")
html = open(p, encoding="utf-8").read()

CARDS = [
    ('<span class="news-date">Sep 29, 2026 · Markets</span>',
     'assets/products/us-listed-robotics-stocks.webp',
     'Frost & Sullivan: global humanoid sales hit 36,000 units in H1 2026, Chinese makers sweep top five revenue slots',
     'A new Frost & Sullivan humanoid-robot report (Sep 29) puts global humanoid sales at 36,000 units in H1 2026, with Chinese companies - led by Unitree - taking the top five revenue positions. The data underscores how far China\'s humanoid sector has moved from prototypes toward volume production and consumer shipments.',
     'Source: <a href="https://basic.10jqka.com.cn/176/HK9880/" target="_blank" rel="noopener">Frost & Sullivan via Tonghuashun (Tonghuashun) &#8599;</a>'),
    ('<span class="news-date">Sep 28, 2026 · Deployments</span>',
     'assets/products/agibot-a2.webp',
     'AgiBot deploys 300+ embodied robots at Chimelong Spaceship Park and rolls its 20,000th unit off the line',
     'On Sep 24 AgiBot integrated more than 300 embodied-AI robots across Chimelong Spaceship Park in Zhuhai - billed as the world\'s first large-scale embodied-intelligence theme-park deployment, with robots handling guest services, logistics and show roles - while passing its 20,000th production robot as a milestone.',
     'Source: <a href="https://theroboticsmedia.com/article/agibot-chimelong-spaceship-park-300-embodied-ai-robots-20000th-china-mobile-september-24-2026" target="_blank" rel="noopener">The Robotics Media / AgiBot News &#8599;</a>'),
    ('<span class="news-date">Sep 28, 2026 · Products</span>',
     'assets/products/unitree-g1.webp',
     'Unitree shows GD01 - a mass-produced rider-carrying transforming mech - at the 2026 Global Digital Trade Expo',
     'Unitree unveiled the GD01 at Hangzhou\'s 2026 Global Digital Trade Expo: roughly 3 meters tall and about 500 kg with a rider, it switches between biped and quadruped modes through Unitree\'s own algorithms. The company targets special operations and tourism-culture scenarios for the world\'s first mass-produced rider-carrying transforming mech.',
     'Source: <a href="http://m.toutiao.com/group/7690511707538293284/" target="_blank" rel="noopener">Sing Tao (Singtao) via Toutiao &#8599;</a>'),
    ('<span class="news-date">Sep 28, 2026 · Companies</span>',
     'assets/products/agibot-a2.webp',
     'AgiBot meets Malaysia\'s PM Anwar to expand embodied-AI industry ties in Southeast Asia',
     'On Sep 28 AgiBot held talks with Malaysian Prime Minister Anwar Ibrahim on embodied-intelligence industry cooperation - the clearest signal yet of Chinese humanoid makers building distribution and policy bridges in Southeast Asia as they push overseas.',
     'Source: <a href="https://www.agibot.com.cn/News" target="_blank" rel="noopener">AgiBot News &#8599;</a>'),
    ('<span class="news-date">Sep 24, 2026 · Funding</span>',
     'assets/products/engineai-t800.webp',
     'EngineAI reaches $1.4B valuation in Luxshare-led round, pivoting from viral combat bots',
     'Shenzhen\'s EngineAI has reached a $1.4 billion valuation after a funding round led by Luxshare Precision, signaling a pivot from viral humanoid-fighting entertainment toward industrial and service applications as it scales production of its T-series humanoids.',
     'Source: <a href="https://www.humanoidsdaily.com/authors/default" target="_blank" rel="noopener">Humanoids Daily &#8599;</a>'),
    ('<span class="news-date">Sep 21, 2026 · Policy</span>',
     'assets/products/ubtech-walker.webp',
     'UBTECH issues world\'s first humanoid-robot ethics & governance white paper',
     'UBTECH published what it calls the world\'s first white paper on humanoid-robot technology ethics and governance on Sep 21, building an embodied-intelligence ethics framework - a signal that Chinese leaders of the sector are addressing safety and governance questions as consumer U1 and industrial Walker S robots scale.',
     'Source: <a href="https://www.ubtrobot.com/cn/news-list" target="_blank" rel="noopener">UBTECH News &#8599;</a>'),
]

def esc_attr(s):
    return H.escape(s, quote=True)

def esc_text(s):
    return H.escape(s, quote=False)

def card(date, img, title, summary, src):
    href = src.split('href="')[1].split('"')[0]
    return (
        '        <article class="card news-item">\n'
        '          ' + date + '\n\n'
        '          <img class="product-photo" src="' + img + '" alt="' + esc_attr(title[:60]) + '" loading="lazy">\n'
        '          <h3><a href="' + href + '" target="_blank" rel="noopener">' + esc_text(title) + '</a></h3>\n'
        '          <p>' + esc_text(summary) + '</p>\n'
        '          <div class="news-src">' + src + '</div>\n'
        '        </article>\n'
    )

anchor = '<div class="card-grid">\n'
cards_html = "".join(card(*c) for c in CARDS)
if "Frost &amp; Sullivan" in html:
    print("ALREADY INSERTED, skip")
else:
    html = html.replace(anchor, anchor + cards_html, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(html)
    print("inserted", len(CARDS), "cards")
