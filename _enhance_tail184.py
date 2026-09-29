# -*- coding: utf-8 -*-
"""Enhance 184 tail company pages with Data Snapshot / Products & Specs /
Key Customers & Applications / Competitor Comparison blocks, reusing ONLY
text already present on each page (zero fabrication).

Insertion point: right after the Key Facts table, before FAQ.
Also fills empty Key Facts tables from hero/FAQ-derived fields.
"""
import os, re, io, html, sys

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")

def esc(s):
    return html.escape(s, quote=False)

def strip_tags(s):
    return re.sub(r"<[^>]+>", " ", s)

def find_block(html, h2_text):
    """Find <h2>X</h2> ... up to next <h2> or end; return (inner, start_idx_of_h2, end_idx)."""
    m = re.search(r"<h2>%s</h2>" % re.escape(h2_text), html, re.I)
    if not m:
        return None, -1, -1
    start = m.start()
    nxt = re.search(r"<h2>", html[m.end():])
    end = m.end() + nxt.start() if nxt else len(html)
    return html[m.end():end], start, end

def parse_page(path):
    html = open(path, encoding="utf-8").read()
    d = {"file": os.path.basename(path), "html": html}
    h1 = re.search(r"<h1>([^<]*)</h1>", html)
    d["name"] = h1.group(1).strip() if h1 else ""
    m = re.search(r'<span class="p-cn">([^<]*)</span>', html)
    d["cn"] = strip_tags(m.group(1)).strip() if m else ""
    m = re.search(r"<h2>([^<]*)</h2>", html)
    d["h2"] = strip_tags(m.group(1)).strip() if m else ""
    m = re.search(r"<h2>%s</h2>.*?<h2>" % re.escape(d["name"]), html, re.S)
    focus = ""
    if m:
        seg = html[m.end():]
        nxt = re.search(r"<h2>", seg)
        if nxt:
            focus = strip_tags(seg[:nxt.start()]).strip()
    if not focus and "—" in d["h2"]:
        focus = d["h2"].split("—", 1)[1].strip()
    d["focus"] = focus
    # hero desc: first <p> inside page-hero
    hero_sec = html.split("page-hero", 1)[1] if "page-hero" in html else ""
    m = re.search(r"<p>([^<]*)</p>", hero_sec)
    d["hero"] = strip_tags(m.group(1)).strip() if m else ""
    # hq from FAQ "headquartered in X, China"
    m = re.search(r"headquartered in ([^,<]+),? China", html)
    d["hq"] = m.group(1).strip() if m else ""
    # site url from a.btn-primary
    m = re.search(r'<a class="btn-primary"[^>]*href="([^"]+)"', html)
    d["site"] = m.group(1).strip() if m else ""
    # ticker in hero (e.g. 688400.SH / 300024.SZ / 000425.SZ)
    m = re.search(r"(\d{6}\.(SH|SZ|BJ|HK|AQ|NQ))", d["hero"] + " " + d["cn"])
    d["ticker"] = m.group(1).upper() if m else ""
    # Key Facts table rows
    kf, kf_start, kf_end = find_block(html, "Key Facts")
    d["kf_raw"] = []
    d["kf"] = {}
    if kf is not None:
        for mm in re.finditer(r"<tr><th>(.*?)</th><td>(.*?)</td></tr>", kf, re.S):
            th = strip_tags(mm.group(1)).strip()
            td = strip_tags(mm.group(2)).strip()
            if th and td:
                d["kf_raw"].append((th, td))
                d["kf"][th.lower()] = td
    d["kf_start"] = kf_start
    d["kf_end"] = kf_end
    # FAQ Q2 answer (Competitor Comparison source)
    faq_q2 = re.search(r"<h3>[^<]*compare[^<]*</h3>\s*<p>(.*?)</p>", html, re.S | re.I)
    d["faq_compare"] = strip_tags(faq_q2.group(1)).strip() if faq_q2 else ""
    return d

def split_products(hero, focus):
    """Extract product phrases from hero text; fallback to focus."""
    out = []
    txt = hero
    # patterns: "develops X and Y, targeting Z" / "is ... supplying X to Y" / "specializing in X"
    pats = [
        r"(?:develops|developing|makes|builds|supplies|supplying|produces|offers|exports|provides|makes)\s+(.+?)\s+(?:targeting|serving|for|to|at|,|\.|$)",
        r"specializing in\s+(.+?)\s+(?:\.|$|, targeting)",
    ]
    for p in pats:
        m = re.search(p, txt, re.I)
        if m:
            seg = m.group(1)
            # split on commas / and
            parts = re.split(r",| and | & ", seg)
            for part in parts:
                part = part.strip().rstrip(".")
                if part and len(part) > 2 and any(k in part.lower() for k in
                    ["robot", "arm", "system", "module", "platform", "actuator",
                     "drive", "servo", "inverter", "vision", "motion", "controller",
                     "machine", "line", "cobot", "humanoid", "quadruped", "drone",
                     "exoskeleton", "surgical", "rehab", "clean", "vacuum", "mower"]):
                    if part not in out:
                        out.append(part)
    if not out and focus:
        out = [focus]
    return out[:6]

def split_apps(hero, focus):
    out = []
    m = re.search(r"targeting\s+(.+?)(?:\.|$)", hero, re.I)
    if m:
        for part in re.split(r",| and ", m.group(1)):
            part = part.strip().rstrip(".")
            if part and len(part) > 2:
                out.append(part)
    if not out:
        m = re.search(r"serving\s+(.+?)(?:\.|$)", hero, re.I)
        if m:
            for part in re.split(r",| and ", m.group(1)):
                part = part.strip().rstrip(".")
                if part and len(part) > 2:
                    out.append(part)
    if not out:
        m = re.search(r"for\s+(.+?)(?:\.|$)", hero, re.I)
        if m and len(m.group(1)) < 80:
            for part in re.split(r",| and ", m.group(1)):
                part = part.strip().rstrip(".")
                if part and len(part) > 2:
                    out.append(part)
    if not out and focus:
        out = [focus]
    return out[:5]

def build_blocks(d):
    blocks = []
    kf = d["kf"]
    # ---- fill empty Key Facts table ----
    kf_html = ""
    if not d["kf_raw"]:
        rows = []
        if d["cn"]:
            rows.append(("<tr><th>Chinese Name</th><td>%s</td></tr>" % esc(d["cn"])))
        if d["hq"]:
            rows.append(("<tr><th>Headquarters</th><td>%s, China</td></tr>" % esc(d["hq"])))
        if d["ticker"]:
            rows.append(("<tr><th>Listing</th><td>%s</td></tr>" % esc(d["ticker"])))
        if d["focus"]:
            rows.append(("<tr><th>Focus</th><td>%s</td></tr>" % esc(d["focus"])))
        if d["site"]:
            rows.append(('<tr><th>Official Site</th><td><a href="%s" target="_blank" rel="noopener">%s</a></td></tr>' % (esc(d["site"]), esc(d["site"]))))
        if rows:
            kf_html = "\n".join("        " + r for r in rows) + "\n"
    # ---- Data Snapshot ----
    snap_rows = []
    if d["name"]:
        snap_rows.append(("<tr><th>Company</th><td>%s</td></tr>" % esc(d["name"])))
    if d["cn"]:
        snap_rows.append(("<tr><th>Chinese Name</th><td>%s</td></tr>" % esc(d["cn"])))
    if d["hq"]:
        snap_rows.append(("<tr><th>Headquarters</th><td>%s, China</td></tr>" % esc(d["hq"])))
    if d["ticker"]:
        snap_rows.append(("<tr><th>Listing</th><td>%s</td></tr>" % esc(d["ticker"])))
    if d["focus"]:
        snap_rows.append(("<tr><th>Core Products</th><td>%s</td></tr>" % esc(d["focus"])))
    if d["site"]:
        snap_rows.append(('<tr><th>Official Site</th><td><a href="%s" target="_blank" rel="noopener">%s</a></td></tr>' % (esc(d["site"]), esc(d["site"]))))
    if snap_rows:
        blocks.append("<h2>Data Snapshot</h2>\n<table class=\"spec-table\">\n%s\n        </table>" % ("\n".join("        " + r for r in snap_rows)))
    # ---- Products & Specs ----
    prods = split_products(d["hero"], d["focus"])
    if prods:
        lis = "\n".join("        <li>%s</li>" % esc(p) for p in prods)
        blocks.append("<h2>Products & Specs</h2>\n<ul>\n%s\n        </ul>" % lis)
    # ---- Key Customers & Applications ----
    apps = split_apps(d["hero"], d["focus"])
    if apps:
        lis = "\n".join("        <li>%s</li>" % esc(a) for a in apps)
        blocks.append("<h2>Key Customers & Applications</h2>\n<ul>\n%s\n        </ul>" % lis)
    # ---- Competitor Comparison (from FAQ Q2, page's own text) ----
    if d["faq_compare"]:
        blocks.append("<h2>Competitor Comparison</h2>\n<p>%s</p>" % esc(d["faq_compare"]))
    return kf_html, blocks

def main():
    pages = [f for f in os.listdir(BASE) if f.startswith("company-") and f.endswith(".html")]
    targets = []
    for f in sorted(pages):
        html = open(os.path.join(BASE, f), encoding="utf-8").read()
        if "Data Snapshot" in html or "Products & Specs" in html:
            continue  # already thick
        targets.append(f)
    print("TARGETS:", len(targets))

    ok, fail = [], []
    for f in targets:
        p = os.path.join(BASE, f)
        try:
            d = parse_page(p)
            kf_fill, blocks = build_blocks(d)
            if not kf_fill and not blocks:
                ok.append(f); continue  # nothing to add
            html = d["html"]
            # 1) fill empty Key Facts
            if kf_fill:
                kf_inner, s, e = find_block(html, "Key Facts")
                if kf_inner is not None and not re.search(r"<tr>", kf_inner):
                    html = html[:s] + "<h2>Key Facts</h2>\n<table class=\"spec-table\">\n" + kf_fill + "        </table>" + html[e:]
            # 2) append blocks after Key Facts table, before FAQ
            faq_start = re.search(r"<h2>Frequently Asked Questions</h2>", html)
            if not faq_start:
                faq_start = re.search(r"<h2>Related Reading</h2>", html)
            if not faq_start:
                raise RuntimeError("no insertion anchor")
            ins = faq_start.start()
            added = "\n\n        " + "\n\n        ".join(blocks)
            html = html[:ins] + added + "\n\n        " + html[ins:]
            with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(html)
            ok.append(f)
        except Exception as ex:
            fail.append((f, str(ex)))
    print("ENHANCED:", len(ok))
    if fail:
        print("FAILED:", len(fail))
        for n, e in fail[:20]:
            print(" ", n, e)

if __name__ == "__main__":
    main()
