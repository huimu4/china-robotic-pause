# -*- coding: utf-8 -*-
"""Final structural check: tag balance across all HTML files + list all external official-site links."""
import glob, os, re, urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print('--- Tag balance check ---')
issues = 0
for f in sorted(glob.glob(os.path.join(HERE, '*.html'))):
    txt = open(f, encoding='utf-8').read()
    for tag in ['article', 'div', 'section', 'nav', 'header', 'footer', 'form', 'ul', 'li']:
        opens = len(re.findall(r'<%s[\s>]' % tag, txt))
        closes = len(re.findall(r'</%s>' % tag, txt))
        if opens != closes:
            print('%s: <%s> open=%d close=%d' % (os.path.basename(f), tag, opens, closes))
            issues += 1
print('issues:', issues)

print('\n--- Official-site links present ---')
links = set()
for f in sorted(glob.glob(os.path.join(HERE, '*.html'))):
    txt = open(f, encoding='utf-8').read()
    for m in re.finditer(r'<a class="site-link" href="([^"]+)"', txt):
        links.add(m.group(1))
    for m in re.finditer(r'<a href="(https://[^"]+)" target="_blank" rel="noopener">Official site', txt):
        links.add(m.group(1))
for u in sorted(links):
    print(u)

print('\n--- Verify a sample of official links return 200 ---')
sample = sorted(links)
import ssl
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
for u in sample:
    try:
        req = urllib.request.Request(u, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=12, context=ctx) as r:
            print(u, '->', r.status)
    except Exception as e:
        try:
            req = urllib.request.Request(u, method='GET', headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=12, context=ctx) as r:
                print(u, '->', r.status)
        except Exception as e2:
            print(u, '-> FAIL', e2)
