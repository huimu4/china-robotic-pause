# -*- coding: utf-8 -*-
"""Fix: remove wrong site-links, then re-insert with exact company-name matching."""
import os, re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

URLS = {
    'Unitree Robotics': 'https://www.unitree.com/',
    'Agibot':           'https://www.agibot.com/',
    'UBTECH':           'https://www.ubtrobot.com/',
    'Fourier Intelligence': 'https://www.fftai.com/',
    'EngineAI':         'https://www.engineai.com.cn/',
    'AI\u00b2 Robotics': 'https://ai2robotics.com/',
    'Booster Robotics': 'https://www.booster.tech/',
    'SIASUN':           'https://www.siasun.com/',
    'Estun':            'https://en.estun.com/',
    'Inovance':         'https://www.inovance.com/',
    'Gausium':          'https://gausium.com/',
    'Narwal':           'https://www.narwal.com/',
    'Roborock':         'https://global.roborock.com/',
    'Ecovacs':          'https://www.ecovacs.com/',
    'DJI':              'https://www.dji.com/',
    'Mech-Mind':        'https://www.mech-mind.com/',
    'Zhongding Co.':    'https://www.zhongdinggroup.com/',
    'Lingyi iTech':     'https://www.lingyiitech.com/',
    'Tianji Intelligent': 'https://www.tianjizn.com/',
    'Topstar':          'https://www.topstarmachine.com/',
    'Benmo':            'https://directdrive.com/',
    'XbotPark':         'https://www.xbotpark.com/',
}

def clean_links(txt):
    """Remove any existing site-link anchors (with surrounding whitespace)."""
    pat = re.compile(r'\n          <a class="site-link"[^>]*>Official site</a>')
    return pat.sub('', txt)

def insert_link(block, url):
    link = '\n          <a class="site-link" href="%s" target="_blank" rel="noopener">Official site</a>' % url
    return block.replace('</article>', link + '\n        </article>', 1)

def pname_of(block):
    m = re.search(r'<div class="pname">([^<]+)', block)
    return m.group(1).strip() if m else None

def h3_of(block):
    m = re.search(r'<h3>(.*?)</h3>', block, re.S)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ''

# ---- rebuild companies.html ----
COMPANY_ORDER = [
    'Unitree Robotics', 'Agibot', 'UBTECH', 'Fourier Intelligence', 'EngineAI',
    'AI\u00b2 Robotics', 'LiberAI', 'Booster Robotics', 'OriginFlow', 'SIASUN',
    'Estun', 'Inovance', 'Gausium', 'Narwal', 'Roborock', 'Ecovacs', 'DJI',
    'Yingkan Zhiyi', 'Mech-Mind', 'Zhongding Co.', 'Lingyi iTech',
    'Tianji Intelligent', 'Topstar', 'Benmo', 'XbotPark',
]

def rebuild(path, art_pat, resolver):
    txt = open(path, encoding='utf-8').read()
    txt = clean_links(txt)
    arts = art_pat.findall(txt)
    out = []
    idx = 0
    def repl(m):
        nonlocal idx
        block = m.group(0)
        url = resolver(block, idx)
        idx += 1
        return insert_link(block, url) if url else block
    txt = art_pat.sub(repl, txt)
    open(path, 'w', encoding='utf-8').write(txt)
    return idx

# companies.html: exact order match on pname
def resolver_company(block, idx):
    name = pname_of(block)
    return URLS.get(name)

n = rebuild(os.path.join(HERE, 'companies.html'),
            re.compile(r'<article class="profile-card">.*?</article>', re.S),
            resolver_company)
print('companies.html rebuilt, %d cards processed' % n)

# products.html: keyword match on h3 (no cross-card pollution because each card only names itself)
PROD_RULES = [
    ('Unitree', 'https://www.unitree.com/'),
    ('Agibot',  'https://www.agibot.com/'),
    ('UBTECH',  'https://www.ubtrobot.com/'),
    ('Fourier', 'https://www.fftai.com/'),
    ('EngineAI','https://www.engineai.com.cn/'),
    ('Booster', 'https://www.booster.tech/'),
    ('Benmo',   'https://directdrive.com/'),
    ('AlphaBot','https://ai2robotics.com/'),
    ('Estun',   'https://en.estun.com/'),
    ('Mech-Mind','https://www.mech-mind.com/'),
    ('Tianji',  'https://www.tianjizn.com/'),
    ('Zhongding','https://www.zhongdinggroup.com/'),
    ('Gausium', 'https://gausium.com/'),
    ('Narwal',  'https://www.narwal.com/'),
    ('DJI',     'https://www.dji.com/'),
]
def resolver_product(block, idx):
    h3 = h3_of(block)
    for kw, url in PROD_RULES:
        if kw in h3:
            return url
    return None

n = rebuild(os.path.join(HERE, 'products.html'),
            re.compile(r'<article class="card">.*?</article>', re.S),
            resolver_product)
print('products.html rebuilt, %d cards processed' % n)
