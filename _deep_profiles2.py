# -*- coding: utf-8 -*-
"""Batch 2 deep profiles.
- Topstar: full deep profile (Key Facts enrich + hero + Milestones + Product
  Lineup + Financial Snapshot + Global Benchmark). All figures from 2026-09-29
  research (annual report, SEC filings, company site, securities press).
- Estun / HariBit / Double-Ring: append a Global Benchmark block only (their
  pages are already thick). Facts reused from page content / same research.
Idempotent on 'Global Benchmark' / 'Milestones & Company History'.
"""
import os, re, io, html

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")

def esc(s):
    return html.escape(s, quote=False)

TOPS = {
 "hero_extra": " Founded in 2007 and listed on Shenzhen's ChiNext in 2017 (300607.SZ), Topstar is one of China's few robot makers to also build its own injection-molding machines (90-2,800t), CNC machines and servo drives — a vertically integrated play on factory automation.",
 "kf_extra": [
   ("Full Name", "Guangdong Topstar Technology Co., Ltd."),
   ("Chinese Name", "广东拓斯达科技股份有限公司"),
   ("Founded", "2007"),
   ("Headquarters", "Dongguan, Guangdong, China"),
   ("Listing", "300607.SZ (Shenzhen ChiNext, 2017)"),
   ("Focus", "Industrial robots & injection automation"),
   ("Status", "Vertically integrated factory-automation maker"),
   ("Official Site", None),
 ],
 "blocks": [
   ("Milestones & Company History", """<ul>
        <li><strong>2007</strong> — Topstar is founded in Dongguan, Guangdong.</li>
        <li><strong>2015</strong> — Self-developed Cartesian (linear-axis) robots begin exporting to Southeast Asia, Europe and South America.</li>
        <li><strong>2017</strong> — IPO on the Shenzhen ChiNext board (300607.SZ).</li>
        <li><strong>2025</strong> — Robot product shipments reach 12,000 units for the year; annual revenue 2.51 billion CNY with a return to profit (net 74 million CNY).</li>
        <li><strong>Oct 2025</strong> — Global Open Day unveils "Xiao Tuo", Topstar's first humanoid robot, co-developed with Zhipu AI and validated in injection-molding workshops — an industry first for humanoids in injection molding.</li>
        <li><strong>2026 H1</strong> — Robot orders booked near 7,000 units in the half year.</li>
        </ul>"""),
   ("Product Lineup", """<table class="spec-table">
        <tr><th>Line</th><th>What it is</th><th>Typical use</th></tr>
        <tr><td>Injection molding machines</td><td>Servo, hybrid and all-electric machines, 90-2,800t clamping force</td><td>Plastics manufacturing</td></tr>
        <tr><td>Cartesian / take-out robots</td><td>3-5 axis AC-servo linear robots</td><td>Injection-mold extraction, sprue removal</td></tr>
        <tr><td>6-axis articulated robots</td><td>Industrial arms</td><td>Handling, sorting, PVC pipe, general automation</td></tr>
        <tr><td>Delta / parallel robots</td><td>High-speed sorting arms</td><td>Food & packaging pick-and-place</td></tr>
        <tr><td>CNC machines & controllers</td><td>CNC centers plus drives/controllers</td><td>Metalworking cells</td></tr>
        <tr><td>Xiao Tuo humanoid (2025)</td><td>Embodied-AI humanoid co-built with Zhipu AI</td><td>Injection-molding shop-floor tasks</td></tr>
        </table>"""),
   ("Financial Snapshot", """<table class="spec-table">
        <tr><th>Period</th><th>Revenue (CNY)</th><th>Net profit (CNY)</th></tr>
        <tr><td>2024</td><td>2.87 billion</td><td>-239 million</td></tr>
        <tr><td>2025</td><td>2.51 billion (-12.6% YoY)</td><td>74 million (+130.1%, back to profit; gross margin 28.25%)</td></tr>
        <tr><td>2026 H1</td><td>1.29 billion</td><td>106 million</td></tr>
        </table>"""),
   ("Global Benchmark", """<p>Topstar sits between China's industrial-robot majors and the Japanese machine-tool ecosystem: unlike <a href="../china-robot-arms-vs-abb-kuka.html">ABB, KUKA or FANUC</a>, which sell robots plus peripherals, Topstar builds the injection-molding machines themselves — the same model as Japan's Yushin and Star Seiki in mold take-out robots. That vertical integration, plus 12,000 robot units shipped in 2025, lets it win cost-sensitive plastics and 3C factories across the Pearl River Delta. The Xiao Tuo humanoid, launched with Zhipu AI in October 2025, is an early bet that humanoids will first earn their keep inside existing factories, not on public streets.</p>"""),
 ],
}

GB = {
 "company-estun.html": """<p>ESTUN is China's closest challenger to the global industrial-robot oligopoly of <a href="../china-robot-arms-vs-abb-kuka.html">ABB, KUKA and FANUC</a>. Per MIR Databank it took No.1 in China robot shipments in 2025 (10.6% share) — the first time a Chinese brand has overtaken foreign incumbents in the domestic market. Where the global majors built on decades of servo and motion-control heritage, ESTUN did the same in-house ("ALL Made By Estun") and added Germany's Cloos (2020) for premium welding, Trio and M.A.i for the global portfolio. Its 2026 A+H listing (02715.HK) funds the push from China's No.1 toward the global top three.</p>""",
 "company-haribit.html": """<p>HariBit competes in the same legged-robot arena as <a href="company-unitree.html">Unitree</a>, Deep Robotics and, internationally, Boston Dynamics' Spot. Its differentiation is academic: spun out of the Beijing Institute of Technology with a research-led, high-fidelity motion approach, HariBit targets labs, education and demonstration use rather than mass consumer shipping — closer in spirit to a robotics institute with a product line than to Unitree's consumer-first playbook. In China's crowded humanoid field, that BIT-rooted technical depth is both its moat and its scale ceiling.</p>""",
 "company-double-ring.html": """<p>Double-Ring is China's answer to Japan's <a href="../china-harmonic-reducers-vs-harmonic-drive.html">Nabtesco</a>, the near-monopolist of precision RV reducers. Where Nabtesco still dominates premium six-axis industrial joints, Double-Ring (002470.SZ) has built domestic RV scale, precision gears and — critically for the current cycle — planetary roller screws for humanoid actuators. Its bet mirrors the harmonic-drive story of Leaderdrive (绿的谐波): win the Chinese joint-component market on price and delivery as robot volumes explode, then ride the humanoid joint demand that could need dozens of precision reducers and screws per unit.</p>""",
}

def main():
    ok, skip = [], []
    # 1) Topstar full deep profile
    p = os.path.join(BASE, "company-topstar.html")
    html = open(p, encoding="utf-8").read()
    if "Milestones & Company History" not in html:
        # enrich Key Facts (replace existing table rows: drop Official Site None logic)
        kf_sec = re.search(r"(<h2>Key Facts</h2>\s*<table class=\"spec-table\">)(.*?)(</table>)", html, re.S)
        if kf_sec:
            rows = []
            for label, val in TOPS["kf_extra"]:
                if val is None:
                    continue
                rows.append("        <tr><th>%s</th><td>%s</td></tr>" % (esc(label), esc(val)))
            # append official site from existing page
            site = re.search(r'<tr><th>Official Site</th><td><a href="([^"]+)"', html)
            if site:
                rows.append('        <tr><th>Official Site</th><td><a href="%s" target="_blank" rel="noopener">%s</a></td></tr>' % (esc(site.group(1)), esc(site.group(1))))
            html = html[:kf_sec.start()] + kf_sec.group(1) + "\n" + "\n".join(rows) + "\n        " + kf_sec.group(3) + html[kf_sec.end():]
        # hero extra
        hero = re.search(r'(<section class="page-hero">.*?<p>)(.*?)(</p>)', html, re.S)
        if hero:
            html = html[:hero.start()] + hero.group(1) + hero.group(2).strip() + " " + TOPS["hero_extra"] + hero.group(3) + html[hero.end():]
        ov = re.search(r'(<h2>Company Overview</h2>\s*<p>)(.*?)(</p>)', html, re.S)
        if ov:
            html = html[:ov.start()] + ov.group(1) + ov.group(2).strip() + " " + TOPS["hero_extra"] + ov.group(3) + html[ov.end():]
        # blocks before FAQ
        faq_start = re.search(r"<h2>Frequently Asked Questions</h2>", html)
        ins = faq_start.start() if faq_start else len(html)
        blocks = ["<h2>%s</h2>\n%s" % (esc(t), b.strip()) for t, b in TOPS["blocks"]]
        added = "\n\n        " + "\n\n        ".join(blocks)
        html = html[:ins] + added + "\n\n        " + html[ins:]
        io.open(p, "w", encoding="utf-8", newline="\n").write(html)
        ok.append("company-topstar.html (full deep profile)")
    else:
        skip.append("company-topstar.html")
    # 2) Global Benchmark blocks for the other three
    for fname, text in GB.items():
        p = os.path.join(BASE, fname)
        html = open(p, encoding="utf-8").read()
        if "Global Benchmark" in html:
            skip.append(fname); continue
        faq_start = re.search(r"<h2>Frequently Asked Questions</h2>", html)
        ins = faq_start.start() if faq_start else len(html)
        block = "<h2>Global Benchmark</h2>\n" + text.strip()
        html = html[:ins] + "        " + block + "\n\n        " + html[ins:]
        io.open(p, "w", encoding="utf-8", newline="\n").write(html)
        ok.append(fname)
    print("OK:", len(ok))
    for x in ok: print("  ", x)
    print("SKIP:", len(skip), skip)

if __name__ == "__main__":
    main()
