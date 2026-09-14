# -*- coding: utf-8 -*-
"""Phase F: CSS additions + news.html + search.html + search.js + search-index.js + sitemap update."""
import os, re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------- 1. CSS additions ----------
CSS_ADD = """

/* ---------- Official site links ---------- */
.site-link {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 0.88rem; font-weight: 700; color: var(--blue-600);
  margin-top: 14px;
}
.site-link:hover { color: var(--blue-500); }
.site-link::after { content: "\\2197"; transition: transform 0.15s ease; }
.site-link:hover::after { transform: translate(2px, -2px); }
.card .site-link { margin-top: 16px; }

/* ---------- Header search box ---------- */
.main-nav li.nav-search { display: flex; align-items: center; }
.search-form { display: flex; align-items: center; }
.search-form input {
  width: 108px; padding: 6px 13px; border: 1px solid var(--line);
  border-radius: 999px; font-size: 0.84rem; background: var(--bg-soft);
  color: var(--ink-700); transition: width 0.2s ease, border-color 0.2s ease, background 0.2s ease;
}
.search-form input::placeholder { color: var(--ink-300); }
.search-form input:focus { outline: none; width: 170px; border-color: var(--blue-600); background: #fff; }
@media (max-width: 1060px) {
  .search-form input { width: 90px; }
  .search-form input:focus { width: 130px; }
}
@media (max-width: 860px) {
  .main-nav li.nav-search { padding: 12px 10px 6px; }
  .search-form input, .search-form input:focus { width: 100%; padding: 10px 14px; }
}

/* ---------- News page ---------- */
.news-item .news-date {
  font-size: 0.78rem; font-weight: 700; color: var(--ink-300);
  text-transform: uppercase; letter-spacing: 0.03em; margin-bottom: 10px; display: block;
}
.news-item h3 { margin-bottom: 8px; }
.news-item h3 a { color: var(--ink-900); }
.news-item h3 a:hover { color: var(--blue-600); }
.news-item .news-src { font-size: 0.84rem; color: var(--ink-300); margin-top: 14px; }
.news-item .news-src a { font-weight: 700; color: var(--ink-500); }
.news-item .news-src a:hover { color: var(--blue-600); }

/* ---------- Search page ---------- */
.search-box { display: flex; gap: 10px; max-width: 680px; margin-bottom: 24px; }
.search-box input {
  flex: 1; padding: 14px 20px; border: 1px solid var(--line); border-radius: 12px;
  font-size: 1.05rem; background: var(--white); color: var(--ink-900); box-shadow: var(--shadow-sm);
}
.search-box input:focus { outline: none; border-color: var(--blue-600); }
.search-count { font-size: 0.92rem; color: var(--ink-500); margin-bottom: 18px; font-weight: 700; }
.search-hit h3 a { color: var(--ink-900); }
.search-hit h3 a:hover { color: var(--blue-600); }
.search-empty { color: var(--ink-400); font-size: 1rem; padding: 14px 0; }
"""

css_path = os.path.join(HERE, 'css', 'style.css')
css = open(css_path, encoding='utf-8').read()
open(css_path, 'w', encoding='utf-8').write(css + CSS_ADD)
print('style.css: +%d chars' % len(CSS_ADD))

# ---------- helper: grab header/footer from an existing page ----------
def grab_template(src):
    txt = open(os.path.join(HERE, src), encoding='utf-8').read()
    head_start = txt.index('<header class="site-header">')
    head_end = txt.index('</header>') + len('</header>')
    head = txt[head_start:head_end]
    foot_start = txt.index('<footer class="site-footer">')
    foot = txt[foot_start:]
    return head, foot

HEAD, FOOT = grab_template('companies.html')

# ---------- 2. news.html ----------
def news_header():
    h = HEAD.replace('href="companies.html" class="active"', 'href="news.html" class="active"')
    return h

NEWS_ITEMS = [
    {
        'date': 'Aug 25, 2026', 'cat': 'Events',
        'title': "China's humanoid robots break records at World Humanoid Robot Games",
        'url': 'http://www.globaltimes.cn/page/202608/1369001.shtml',
        'src': 'Global Times',
        'body': "Beijing's \u201cTiangong\u201d humanoid clocked 8.86 seconds in the 100-metre sprint at the World Humanoid Robot Games in Beijing \u2014 beating the human men's world record \u2014 in a games that drew global attention to China's robot athletics.",
    },
    {
        'date': 'Aug 25, 2026', 'cat': 'Events',
        'title': 'Humanoid robots shattered human records in the 100m and 400m',
        'url': 'http://www.chinaview.cn/20260825/6cbdd8e20a9d4e3a9eff6cc0d1da89f8/c.html',
        'src': 'Xinhua',
        'body': 'At the second World Humanoid Robot Games (Aug 22\u201326), humanoid robots broke human records on the track \u2014 a striking leap from last year, when viral clips showed robots freezing at the starting line or veering off course.',
    },
    {
        'date': 'Aug 26, 2026', 'cat': 'Products',
        'title': 'Your future tennis partner may be a robot',
        'url': 'http://www.xinhuanet.com/20260826/323c391046bd4563a23d9224ffe90447/c.html',
        'src': 'Xinhua',
        'body': 'Galaxy General\u2019s humanoid played tennis with former pro Zheng Jie at the games\u2019 opening. Founder Wang He says the robot can serve, return, save and lob \u2014 and it gets back up on its own after falling.',
    },
    {
        'date': 'Aug 21, 2026', 'cat': 'Events',
        'title': '2026 World Robot Conference opens; Galaxy General unveils bipedal humanoid Galbot ET1',
        'url': 'http://www.xinhuanet.com/digital/20260821/e172222483dc4d75a357145caa74d9d0/c.html',
        'src': 'Xinhua',
        'body': 'With 300+ exhibitors and 150+ new products, the 2026 World Robot Conference in Beijing showcased the industry\u2019s momentum. Galaxy General debuted its bipedal Galbot ET1 humanoid and its self-developed \u201cGalaxy Brain\u201d embodied foundation model.',
    },
    {
        'date': 'Aug 21, 2026', 'cat': 'Industry',
        'title': 'China leads global humanoid robot growth: report',
        'url': 'https://www.cctvplus.com/news/20260821/8495403.shtml',
        'src': 'CCTV+',
        'body': 'In the first half of 2026, China\u2019s humanoid robot shipments accounted for 97 percent of the global total, according to a report covered by CCTV+, which also highlighted China\u2019s push on standards, talent, cooperation and innovation infrastructure.',
    },
    {
        'date': 'Aug 25, 2026', 'cat': 'Companies',
        'title': "IPO, athletic feats and mass deployment show China's robot momentum",
        'url': 'http://en.people.cn/n3/2026/0825/c90000-20492071.html',
        'src': "People's Daily Online",
        'body': 'Unitree\u2019s revenue neared 1.7 billion yuan in 2025 and reached ~1.15 billion yuan in H1 2026, up 48.5% year on year \u2014 with the company vertically integrating motors, reducers, controllers and LiDAR in-house.',
    },
    {
        'date': 'Aug 23, 2026', 'cat': 'Deployments',
        'title': "China's humanoid robots move from exhibition floors to real-world applications",
        'url': 'http://www.china.org.cn/2026-08/23/content_118660262.shtml',
        'src': 'China.org.cn',
        'body': 'Use cases are expanding into emergency response, household services, industrial production and pharma logistics \u2014 including the LINGLOONG v2.0, described as the world\u2019s first firefighting humanoid robot.',
    },
]

def news_card(item):
    return (
        '<article class="card news-item">\n'
        '          <span class="news-date">%s \u00b7 %s</span>\n'
        '          <h3><a href="%s" target="_blank" rel="noopener">%s</a></h3>\n'
        '          <p>%s</p>\n'
        '          <div class="news-src">Source: <a href="%s" target="_blank" rel="noopener">%s \u2197</a></div>\n'
        '        </article>'
    ) % (item['date'], item['cat'], item['url'], item['title'], item['body'], item['url'], item['src'])

news_main = (
'<main>\n'
'  <section class="page-hero">\n'
'    <div class="container ph-inner">\n'
'      <span class="kicker">News</span>\n'
'      <h1>China Robotics News</h1>\n'
'      <p>Fresh dispatches on China\u2019s robotics industry \u2014 events, company milestones, products and deployments. Each headline links straight to the original report.</p>\n'
'    </div>\n'
'  </section>\n'
'\n'
'  <section class="section">\n'
'    <div class="container">\n'
'      <div class="section-head">\n'
'        <span class="eyebrow">Latest dispatches</span>\n'
'        <h2>This week in Chinese robotics</h2>\n'
'        <p>Curated from Chinese and international press, with direct links to the original sources.</p>\n'
'      </div>\n'
'      <div class="card-grid">\n'
+ '\n'.join('        ' + news_card(i) for i in NEWS_ITEMS) + '\n'
'      </div>\n'
'    </div>\n'
'  </section>\n'
'\n'
'  <section class="section">\n'
'    <div class="container">\n'
'      <div class="cta-band">\n'
'        <div>\n'
'          <h3>Context for the headlines</h3>\n'
'          <p>News moves fast. Our guides explain the companies and the people behind the headlines.</p>\n'
'        </div>\n'
'        <a class="btn btn-primary" href="articles.html">Read the insights</a>\n'
'      </div>\n'
'    </div>\n'
'  </section>\n'
'</main>\n'
)

news_page = (
'<!DOCTYPE html>\n'
'<html lang="en">\n'
'<head>\n'
'  <meta charset="UTF-8">\n'
'  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
'  <title>China Robotics News \u2014 Latest Industry Dispatches | China Robotics Insider</title>\n'
'  <meta name="description" content="The latest news on China\u2019s robotics industry \u2014 humanoid events, company milestones, products and real-world deployments, with links to original reports.">\n'
'  <link rel="canonical" href="https://www.robotichina.com/news.html">\n'
'  <meta property="og:type" content="article">\n'
'  <meta property="og:site_name" content="China Robotics Insider">\n'
'  <meta property="og:title" content="China Robotics News">\n'
'  <meta property="og:url" content="https://www.robotichina.com/news.html">\n'
'  <link rel="stylesheet" href="css/style.css">\n'
'</head>\n'
'<body>\n'
'\n'
+ news_header() + '\n'
'\n'
+ news_main + '\n'
'\n'
+ FOOT + '\n'
'\n'
'<script src="js/main.js"></script>\n'
'</body>\n'
'</html>\n'
)
open(os.path.join(HERE, 'news.html'), 'w', encoding='utf-8').write(news_page)
print('news.html created')

# ---------- 3. search.html ----------
def search_header():
    # keep About as default active? Set no active for search page
    return HEAD.replace(' class="active"', '', 1)  # removes first active (Companies)

search_main = (
'<main class="search-page">\n'
'  <section class="page-hero">\n'
'    <div class="container ph-inner">\n'
'      <span class="kicker">Search</span>\n'
'      <h1>Search the site</h1>\n'
'      <p>Find companies, founders, products and articles across China Robotics Insider.</p>\n'
'    </div>\n'
'  </section>\n'
'\n'
'  <section class="section">\n'
'    <div class="container">\n'
'      <form class="search-box" action="search.html" method="get" role="search">\n'
'        <input type="search" id="search-input" name="q" placeholder="Try \u201cUnitree\u201d, \u201cWang Xingxing\u201d, \u201chumanoid\u201d\u2026" aria-label="Search query">\n'
'      </form>\n'
'      <p class="search-count" id="search-count"></p>\n'
'      <div class="card-grid" id="search-results"></div>\n'
'    </div>\n'
'  </section>\n'
'</main>\n'
)

search_page = (
'<!DOCTYPE html>\n'
'<html lang="en">\n'
'<head>\n'
'  <meta charset="UTF-8">\n'
'  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
'  <title>Search \u2014 China Robotics Insider</title>\n'
'  <meta name="description" content="Search China Robotics Insider for companies, founders, products, history and news.">\n'
'  <meta name="robots" content="noindex, follow">\n'
'  <link rel="stylesheet" href="css/style.css">\n'
'</head>\n'
'<body>\n'
'\n'
+ search_header() + '\n'
'\n'
+ search_main + '\n'
'\n'
+ FOOT + '\n'
'\n'
'<script src="js/search-index.js"></script>\n'
'<script src="js/search.js"></script>\n'
'<script src="js/main.js"></script>\n'
'</body>\n'
'</html>\n'
)
open(os.path.join(HERE, 'search.html'), 'w', encoding='utf-8').write(search_page)
print('search.html created')

print('done phase_f part 1')
