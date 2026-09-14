# -*- coding: utf-8 -*-
import re, os
HERE = r'D:\ObsidianVault\机器人精英圈\china-robotics-site'
for fn in ['companies.html', 'products.html']:
    txt = open(os.path.join(HERE, fn), encoding='utf-8').read()
    arts = re.findall(r'<article class="(?:profile-card|card)">.*?</article>', txt, re.S)
    print('===', fn, '===')
    for a in arts:
        name_m = re.search(r'<div class="pname">([^<]+)', a)
        if not name_m:
            h3 = re.search(r'<h3>(.*?)</h3>', a, re.S)
            name = re.sub(r'<[^>]+>', '', h3.group(1)).strip() if h3 else '?'
        else:
            name = name_m.group(1).strip()
        link_m = re.search(r'<a class="site-link" href="([^"]+)"', a)
        print(('%-28s' % name[:28]), '->', link_m.group(1) if link_m else '(no link)')
