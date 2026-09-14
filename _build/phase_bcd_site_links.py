# -*- coding: utf-8 -*-
"""Phase B/C/D: add official-site links to companies.html, products.html and person-*.html"""
import os, re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# company keyword -> official site (verified earlier via search; English sites preferred)
URLS = {
    'Unitree':   'https://www.unitree.com/',
    'Agibot':    'https://www.agibot.com/',
    'UBTECH':    'https://www.ubtrobot.com/',
    'Fourier':   'https://www.fftai.com/',
    'EngineAI':  'https://www.engineai.com.cn/',
    'AI':        'https://ai2robotics.com/',   # AI² Robotics
    'Booster':   'https://www.booster.tech/',
    'SIASUN':    'https://www.siasun.com/',
    'Estun':     'https://en.estun.com/',
    'Inovance':  'https://www.inovance.com/',
    'Gausium':   'https://gausium.com/',
    'Narwal':    'https://www.narwal.com/',
    'Roborock':  'https://global.roborock.com/',
    'Ecovacs':   'https://www.ecovacs.com/',
    'DJI':       'https://www.dji.com/',
    'Mech-Mind': 'https://www.mech-mind.com/',
    'Zhongding': 'https://www.zhongdinggroup.com/',
    'Lingyi':    'https://www.lingyiitech.com/',
    'Tianji':    'https://www.tianjizn.com/',
    'Topstar':   'https://www.topstarmachine.com/',
    'Benmo':     'https://directdrive.com/',
    'XbotPark':  'https://www.xbotpark.com/',
}

def url_for(block):
    for key, url in URLS.items():
        if key in block:
            return url
    return None

# ---- Phase B: companies.html ----
def phase_b():
    path = os.path.join(HERE, 'companies.html')
    txt = open(path, encoding='utf-8').read()
    art_pat = re.compile(r'<article class="profile-card">.*?</article>', re.S)
    count = 0
    def repl(m):
        nonlocal count
        block = m.group(0)
        url = url_for(block)
        if not url:
            return block
        count += 1
        link = '\n          <a class="site-link" href="%s" target="_blank" rel="noopener">Official site</a>' % url
        return block.replace('</article>', link + '\n        </article>', 1)
    txt = art_pat.sub(repl, txt)
    open(path, 'w', encoding='utf-8').write(txt)
    print('companies.html: +%d links' % count)

# ---- Phase C: products.html ----
def phase_c():
    path = os.path.join(HERE, 'products.html')
    txt = open(path, encoding='utf-8').read()
    art_pat = re.compile(r'<article class="card">.*?</article>', re.S)
    count = 0
    def repl(m):
        nonlocal count
        block = m.group(0)
        url = url_for(block)
        if not url:
            return block
        count += 1
        link = '\n          <a class="site-link" href="%s" target="_blank" rel="noopener">Official site</a>' % url
        return block.replace('</article>', link + '\n        </article>', 1)
    txt = art_pat.sub(repl, txt)
    open(path, 'w', encoding='utf-8').write(txt)
    print('products.html: +%d links' % count)

# ---- Phase D: person-*.html ----
PERSON_SITE = {
    'person-jiang-xinsong':   ('SIASUN', 'https://www.siasun.com/'),
    'person-qu-daokui':       ('SIASUN', 'https://www.siasun.com/'),
    'person-li-zexiang':      ('XbotPark', 'https://www.xbotpark.com/'),
    'person-wang-tao':        ('DJI', 'https://www.dji.com/'),
    'person-wang-xingxing':   ('Unitree Robotics', 'https://www.unitree.com/'),
    'person-peng-zhihui':     ('Agibot', 'https://www.agibot.com/'),
    'person-zhou-jian':       ('UBTECH', 'https://www.ubtrobot.com/'),
    'person-gu-jie':          ('Fourier Intelligence', 'https://www.fftai.com/'),
    'person-zhao-tongyang':   ('EngineAI', 'https://www.engineai.com.cn/'),
    'person-guo-yandong':     ('AI\u00b2 Robotics', 'https://ai2robotics.com/'),
    'person-shao-tianlan':    ('Mech-Mind', 'https://www.mech-mind.com/'),
    'person-cheng-haotian':   ('Gausium', 'https://gausium.com/'),
    'person-xia-yingsong':    ('Zhongding Co.', 'https://www.zhongdinggroup.com/'),
    'person-zeng-fangqin':    ('Lingyi iTech', 'https://www.lingyiitech.com/'),
}

def phase_d():
    for base, (company, url) in PERSON_SITE.items():
        path = os.path.join(HERE, base + '.html')
        txt = open(path, encoding='utf-8').read()
        card = (
            '\n        <article class="card">\n'
            '          <h3><a href="%s" target="_blank" rel="noopener">Official site \u00b7 %s \u2197</a></h3>\n'
            '          <p>The company website for %s \u2014 products, news, careers and more.</p>\n'
            '        </article>' % (url, company, company)
        )
        # insert before the closing </div> of the last card-grid (Related reading)
        marker = '</article>\n      </div>'
        if marker in txt:
            txt = txt.replace(marker, card + marker, 1)
            open(path, 'w', encoding='utf-8').write(txt)
            print('%s: +Official site card (%s)' % (base, company))
        else:
            print('%s: MARKER NOT FOUND' % base)

if __name__ == '__main__':
    phase_b()
    phase_c()
    phase_d()
