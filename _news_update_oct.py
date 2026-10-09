# -*- coding: utf-8 -*-
"""news.html 插入 10 月上旬（10/1-10/9）中国机器人新闻卡片"""
import html, io, sys, re

PATH = r"D:\ObsidianVault\机器人精英圈\china-robotic-pause\news.html"

cards = [
    {
        "date": "Oct 9, 2026 · Policy & Infrastructure",
        "img": "assets/products/cloud-robotics.webp",
        "alt": "More than 70 embodied-AI training grounds are now operating across China",
        "title": "More than 70 embodied-AI training grounds now operating across China, three regional clusters take shape",
        "url": "https://www.newtimespace.com/en/tech/1451815.html",
        "summary": "More than 70 embodied-intelligence training grounds are completed and operating nationwide, with 40+ more under construction, forming three core clusters in the Yangtze River Delta, Beijing-Tianjin-Hebei and the Pearl River Delta. A Zhongguancun AI firm has built an embodied-intelligence data platform linking human video data with simulated synthetic data from training grounds across the country.",
        "src_name": "NewTimeSpace",
    },
    {
        "date": "Oct 9, 2026 · Manufacturing",
        "img": "assets/products/xpeng-iron-line.webp",
        "alt": "XPENG IRON humanoid rolls into mass production",
        "title": "XPENG's IRON humanoid rolls into mass production, robotics unit valued above $6.3B",
        "url": "https://www.chosun.com/english/industry-en/2026/10/09/AZQ2KB2BRFBADJD6IGJWVUJ2MI/",
        "summary": "On Sep 8 a 178-cm general-purpose humanoid robot named IRON walked off XPENG's new humanoid manufacturing line, with the company targeting 1,000 units a month by year-end by leveraging its EV supply chain. XPENG Robotics separately raised over $900M at a post-money valuation above $6.3B, led by IDG Capital with Tencent and Alibaba as strategic investors.",
        "src_name": "ChosunBiz / XPENG",
    },
    {
        "date": "Oct 8, 2026 · Deployments",
        "img": "assets/products/geekplus.webp",
        "alt": "UBTECH and FAW-Volkswagen team up on humanoid factory-logistics trials",
        "title": "UBTECH and FAW-Volkswagen team up on humanoid factory-logistics trials",
        "url": "https://humanoid.guide/category/news/",
        "summary": "UBTECH has signed a strategic cooperation with FAW-Volkswagen to jointly develop and test embodied-intelligence robots for factory logistics, with demonstration scenarios planned to accelerate humanoid deployment in smart-manufacturing settings.",
        "src_name": "Humanoid Robot Guide",
    },
    {
        "date": "Oct 6, 2026 · Products",
        "img": "assets/products/ubtech-walker.webp",
        "alt": "UBTECH marks first mass delivery of Walker S2",
        "title": "UBTECH marks 'first mass delivery' of Walker S2 with hundreds of units marching in unison",
        "url": "https://www.techshotsapp.com/technology/chinas-first-mass-delivery-of-humanoid-robots",
        "summary": "UBTECH staged a cinematic showcase in which hundreds of Walker S2 humanoids marched in precise unison to mark the first mass delivery of the model, which can reportedly swap its own batteries. The viral demonstration underscores how far China's humanoid sector has moved beyond prototype stage.",
        "src_name": "TechShots",
    },
    {
        "date": "Oct 2, 2026 · Deployments",
        "img": "assets/products/galbot.webp",
        "alt": "Galbot S1 humanoid starts work on CATL production lines",
        "title": "Galbot's S1 humanoid starts work on CATL production lines",
        "url": "https://www.chinadailyasia.com/hk/article/640464",
        "summary": "Galbot's heavy-duty S1 humanoid has entered production lines at battery giant CATL, performing material handling and picking in battery-module and battery-pack production. The machine can carry a combined load of 50 kg with its two arms and operate for up to eight hours, with the partners also working on global deployment and after-sales.",
        "src_name": "China Daily",
    },
    {
        "date": "Oct 1, 2026 · Markets",
        "img": "assets/products/unitree-g1.webp",
        "alt": "IDC: global humanoid shipments jump 432% in H1 2026, China supplies more than 95%",
        "title": "IDC: global humanoid shipments jump 432% in H1 2026, China supplies more than 95%",
        "url": "https://instadatanews.com/articles/2026-10-01-idc-humanoid-shipments-surge-432-percent-china.html",
        "summary": "IDC data shows global humanoid-robot shipments reached nearly 25,000 units in the first half of 2026, up 432.1% year on year, with Chinese vendors supplying more than 95% of them. AgiBot led with more than 8,600 units, roughly 35% of the global market.",
        "src_name": "IDC via InstaDataNews",
    },
]

def esc(s):
    return html.escape(s, quote=False)

with io.open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 已有卡片计数（以 <article class="card news-item"> 计）
existing = content.count('<article class="card news-item">')

block = "\n".join(
    '<article class="card news-item">\n'
    '          <span class="news-date">' + esc(c["date"]) + '</span>\n\n'
    '          <img class="product-photo" src="' + c["img"] + '" alt="' + esc(c["alt"]) + '" loading="lazy">\n'
    '          <h3><a href="' + c["url"] + '" target="_blank" rel="noopener">' + esc(c["title"]) + '</a></h3>\n'
    '          <p>' + esc(c["summary"]) + '</p>\n'
    '          <div class="news-src">Source: <a href="' + c["url"] + '" target="_blank" rel="noopener">' + esc(c["src_name"]) + ' &#8599;</a></div>\n'
    '        </article>'
    for c in cards
)

anchor = '<div class="card-grid">\n'
if anchor in content:
    content = content.replace(anchor, anchor + block + "\n", 1)
    with io.open(PATH, "w", encoding="utf-8") as f:
        f.write(content)
    new_count = content.count('<article class="card news-item">')
    print("OK. cards:", existing, "->", new_count)
else:
    print("ANCHOR NOT FOUND")
    sys.exit(1)
