# -*- coding: utf-8 -*-
"""Inject FAQ block + FAQPage schema into full-template pages that lack it.
Does NOT rewrite existing content — only adds FAQ section before Related Reading
(or before end of prose) and adds FAQPage JSON-LD into <head>.
"""
import os, re, glob, html, io

BASE = r"D:\ObsidianVault\机器人精英圈\china-robotic-pause\database"

# reuse classification + FAQ from the upgrade script
import importlib.util
spec = importlib.util.spec_from_file_location("up", r"D:\ObsidianVault\机器人精英圈\china-robotic-pause\_upgrade_thin.py")
up = importlib.util.module_from_spec(spec)
spec.loader.exec_module(up)


def extract(d):
    """Get name/cn/focus/hq from a full-template page."""
    name = ""
    m = re.search(r"<h1>([^<]*)</h1>", d)
    if m: name = m.group(1).strip()
    cn = ""
    m = re.search(r'<span class="p-cn">([^<]*)</span>', d)
    if m: cn = m.group(1).strip()
    focus = ""
    m = re.search(r"<tr><th>Core Products?</th><td>([^<]*)</td></tr>", d)
    if m: focus = m.group(1).strip()
    if not focus:
        m = re.search(r"<tr><th>Focus</th><td>([^<]*)</td></tr>", d)
        if m: focus = m.group(1).strip()
    if not focus:
        chips = re.findall(r"<span class=\"chip\">([^<]*)</span>", d)
        if chips: focus = chips[0].strip()
    hq = "China"
    m = re.search(r"<tr><th>Headquarters?</th><td>([^<]*)</td></tr>", d)
    if m: hq = m.group(1).strip()
    return name, cn, focus, hq


def esc(s):
    return html.escape(s, quote=False)


def esc_json(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()


def build_faq_html(faqs):
    blocks = []
    for q, a in faqs:
        blocks.append('<h3>%s</h3>\n        <p>%s</p>' % (esc(q), esc(a)))
    return "\n\n".join(blocks)


def build_faq_json(faqs):
    objs = []
    for q, a in faqs:
        objs.append('{"@type": "Question", "name": "%s", "acceptedAnswer": {"@type": "Answer", "text": "%s"}}'
                    % (esc_json(q), esc_json(a)))
    return ",\n      ".join(objs)


def main():
    files = glob.glob(os.path.join(BASE, "company-*.html"))
    injected = []
    skipped = []
    for f in files:
        t = io.open(f, encoding="utf-8").read()
        if "FAQPage" in t:
            continue
        name, cn, focus, hq = extract(t)
        if not name:
            skipped.append((os.path.basename(f), "no-name"))
            continue
        cat = up.classify(focus + " " + name)
        faqs = []
        for q, a in up.FAQ[cat]:
            faqs.append((q.format(name=name, cn=cn, focus=focus, hq=hq),
                         a.format(name=name, cn=cn, focus=focus, hq=hq)))
        faq_block = ('\n        <h2>Frequently Asked Questions</h2>\n        '
                     + build_faq_html(faqs) + "\n")
        faq_json = build_faq_json(faqs)
        # 1) inject FAQPage schema into <head> before </head>
        schema = ('<script type="application/ld+json">\n  {\n    "@context": "https://schema.org",\n'
                  '    "@type": "FAQPage",\n    "mainEntity": [\n      ' + faq_json + '\n    ]\n  }\n  </script>\n')
        if "</head>" in t:
            t = t.replace("</head>", schema + "</head>", 1)
        # 2) inject FAQ block before "Related Reading" h2, else before end of prose
        anchor = '<h2>Related Reading</h2>'
        if anchor in t:
            t = t.replace(anchor, faq_block + "        " + anchor, 1)
        else:
            # insert before last closing of prose container
            m = re.search(r"\n(\s*)</div>\s*\n\s*</div>\s*\n\s*</section>", t)
            if m:
                t = t[:m.start()] + faq_block + t[m.start():]
            else:
                skipped.append((os.path.basename(f), "no-anchor"))
                continue
        io.open(f, "w", encoding="utf-8", newline="\n").write(t)
        injected.append(os.path.basename(f))
    print("INJECTED FAQ:", len(injected))
    if skipped:
        print("SKIPPED:", len(skipped))
        for n, r in skipped[:10]:
            print(" ", n, r)


if __name__ == "__main__":
    main()
