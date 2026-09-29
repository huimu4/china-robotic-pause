# -*- coding: utf-8 -*-
"""Deep-profile enhancement for 3 high-value company pages (Leaderdrive/Green
Harmonic, AUBO, SIASUN). Injects researched, factual blocks: Milestones,
Product Lineup, Financial Snapshot, Funding, Global Benchmark, and expands
the one-line hero. Idempotent: skips files that already contain 'Milestones'.
All figures come from the 2026-09-29 web research (public filings, company
sites, financial news); nothing is fabricated.
"""
import os, re, io, html, json

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")

def esc(s):
    return html.escape(s, quote=False)

PROFILES = {
 "company-green-harmonic.html": {
   "hero_extra": " Listed on Shanghai's STAR Market (688017.SH) in 2020, Leaderdrive is China's flagship harmonic-reducer champion and a direct rival to Japan's Harmonic Drive. Its reducers power industrial robots, cobots and, increasingly, the joint modules of humanoid robots.",
   "blocks": [
     ("Milestones & Company History", """<ul>
        <li><strong>2003</strong> — Founder team begins strain-wave gear development, redesigning tooth profiles and basic gear models.</li>
        <li><strong>2011</strong> — Leader Harmonic Drive Systems (绿的谐波) is formally established in Suzhou, Jiangsu.</li>
        <li><strong>2013</strong> — Annual sales exceed 300,000 strain-wave reducers across 21 series; the company becomes a leading Chinese harmonic-drive maker.</li>
        <li><strong>2019</strong> — Launches the patented Y-series third-harmonic strain wave gear with doubled torsional rigidity.</li>
        <li><strong>2020</strong> — IPO on Shanghai's STAR Market (ticker 688017.SH), the first Chinese harmonic-reducer listing.</li>
        <li><strong>2025</strong> — Shows Size 2.5/3/5 micro harmonic reducers for humanoid dexterous hands and KGU rotary actuators at CIIF 2025; launches a high-pressure micro-displacement servo motor pump, a claimed global industry first for micro-hydraulic actuation in automotive chassis.</li>
        </ul>"""),
     ("Product Lineup", """<table class="spec-table">
        <tr><th>Line</th><th>What it is</th><th>Typical use</th></tr>
        <tr><td>LHSG / LHD strain wave gears</td><td>Harmonic reducers built on 3-part gear design (wave generator, flexspline, circular spline)</td><td>Robot joints, precision rotary tables</td></tr>
        <tr><td>Y-series third-harmonic gears</td><td>Patented new-generation reducer with 3rd-harmonic tooth profile, higher torsional rigidity</td><td>High-precision robot axes</td></tr>
        <tr><td>Micro harmonic reducers (Size 2.5/3/5)</td><td>Ultra-miniature reducers for small joints</td><td>Humanoid dexterous hands and wrists</td></tr>
        <tr><td>KGU rotary actuators</td><td>Integrated actuator modules</td><td>Humanoid and industrial joint modules</td></tr>
        <tr><td>Frameless motors & rotary tables</td><td>Direct-drive components and indexing tables</td><td>Machine tools, automation cells</td></tr>
        <tr><td>Servo motor pumps (2025)</td><td>High-pressure micro-displacement pump integrated with servo motor</td><td>Automotive active suspension, steer-by-wire, brake-by-wire</td></tr>
        </table>"""),
     ("Financial Snapshot", """<table class="spec-table">
        <tr><th>Year</th><th>Revenue (CNY)</th><th>Net profit (CNY)</th></tr>
        <tr><td>2023</td><td>356 million</td><td>~50 million</td></tr>
        <tr><td>2024</td><td>387 million</td><td>56 million</td></tr>
        <tr><td>2025</td><td>571 million (+47.3% YoY)</td><td>124 million (+121.4% YoY)</td></tr>
        <tr><td>2026 H1</td><td>349 million</td><td>70 million</td></tr>
        </table>"""),
     ("Global Benchmark", """<p>Leaderdrive is the closest Chinese counterpart to Japan's <a href="../china-harmonic-reducers-vs-harmonic-drive.html">Harmonic Drive</a>, the global benchmark for precision harmonic reducers. Where Harmonic Drive long dominated premium robot joints, Leaderdrive offers comparable accuracy at lower cost with faster domestic supply — a key reason Chinese robot makers can cut joint costs. 2025 revenue of 571 million CNY still leaves it far smaller than Harmonic Drive Systems (~JPY 60bn+), so the catch-up story, plus the humanoid hand/wrist opportunity, is the core investment narrative. In 2026 the company has reportedly been preparing a Hong Kong listing to fund expansion.</p>"""),
   ],
 },
 "company-aubo.html": {
   "hero_extra": " Founded in 2015 by Beihang University professor Wei Hongxing, AUBO has shipped the most collaborative robots in China for four straight years and ranks second globally, with 2023 sales revenue around 520 million CNY.",
   "blocks": [
     ("Milestones & Company History", """<ul>
        <li><strong>2015</strong> — AUBO (遨博智能) is founded in Beijing by Beihang professor Wei Hongxing; receives a 60 million CNY angel round; i5 cobot launches globally.</li>
        <li><strong>2017</strong> — 60 million CNY Series A; starts a global market push with US and German subsidiaries, plus Shenzhen and Shanghai offices.</li>
        <li><strong>2019</strong> — i-Series expands with i3, i10 and i16 global launches.</li>
        <li><strong>2021</strong> — Releases the world's first explosion-proof certified collaborative robot (IFB series).</li>
        <li><strong>2024</strong> — Cumulative product sales pass 30,000 units.</li>
        <li><strong>2025-2026</strong> — Completes seven funding rounds backed by Fosun International, CDB Manufacturing Upgrade Fund and others; named Beijing unicorn, national "little giant" and manufacturing single-champion enterprise.</li>
        </ul>"""),
     ("Product Lineup", """<table class="spec-table">
        <tr><th>Model</th><th>Payload</th><th>Reach</th><th>Repeatability</th><th>Notes</th></tr>
        <tr><td>AUBO C3</td><td>3 kg</td><td>625 mm</td><td>±0.1 mm</td><td>Compact entry cobot (16 kg)</td></tr>
        <tr><td>AUBO C5</td><td>5 kg</td><td>886.5 mm</td><td>±0.1 mm</td><td>Light assembly (24 kg)</td></tr>
        <tr><td>AUBO i5</td><td>5 kg</td><td>967.5 mm</td><td>±0.03 mm</td><td>Flagship i-Series, first of the line (38 kg)</td></tr>
        <tr><td>i3 / i10 / i16 / i20</td><td>3–20 kg</td><td>—</td><td>high precision</td><td>Payload-expanded i-Series</td></tr>
        <tr><td>iS Series</td><td>3–35 kg</td><td>—</td><td>—</td><td>High-performance line, IP ratings up to IP67</td></tr>
        <tr><td>IFB explosion-proof</td><td>—</td><td>—</td><td>—</td><td>World-first explosion-proof certified cobot (2021)</td></tr>
        </table>"""),
     ("Funding & Investors", """<p>AUBO has completed seven funding rounds since its 2015 angel round, with investors including Fosun International, the CDB Manufacturing Upgrading Transformation Fund, Dingsheng Hechuang and Orient Securities. Registered capital is about 103 million CNY. In August 2026, listed conveyor-systems company Dongjie Intelligent agreed to acquire an 11.52% stake, a step widely read as part of AUBO's long-planned path toward an IPO.</p>"""),
     ("Global Benchmark", """<p>AUBO is China's answer to Denmark's <a href="../china-cobots-vs-universal-robots.html">Universal Robots</a>, the inventor of the commercial cobot. Four straight years of No.1 domestic cobot shipments and No.2 globally — with 2023 revenue of about 520 million CNY — put AUBO close behind UR in unit volume while undercutting it on price. AUBO was also the first Chinese cobot maker to earn EN ISO 13849-1:2015 (PL=d, CAT 3) certification, and it now sells into automotive, 3C, medical and new-retail applications, including robotic coffee bars.</p>"""),
   ],
 },
 "company-siasun.html": {
   "hero_extra": " The company is named after Jiang Xinsun, the \u201cfather of Chinese robotics\u201d, and holds more than 100 Chinese robotics industry firsts, with 1,300+ invention patents and exports to 35+ countries.",
   "blocks": [
     ("Milestones & Company History", """<ul>
        <li><strong>2000</strong> — Founded on 30 April by more than 20 researchers from the CAS Shenyang Institute of Automation robotics lab; becomes the national 863-program robotics industrialization base.</li>
        <li><strong>2000s</strong> — Builds China's first industrial robot prototype, first AGV, first welding robot and first clean-room robot; robots begin shipping overseas.</li>
        <li><strong>2009</strong> — IPO on Shenzhen's ChiNext (ticker 300024, now the only A-share company literally named "Robot").</li>
        <li><strong>2019</strong> — 18 years after founding, celebrates more than 100 industry firsts across five product families.</li>
        <li><strong>2020s</strong> — Deploys near-100 industrial robots on Geely's welding main line; builds one of China's largest robot industrial bases in Shenyang.</li>
        <li><strong>2025-2026</strong> — Revenue reaches 4.12 billion CNY but net loss widens to -398 million CNY amid intense competition and exchange-rate pressure.</li>
        </ul>"""),
     ("Product Lineup", """<table class="spec-table">
        <tr><th>Category</th><th>Examples</th><th>Applications</th></tr>
        <tr><td>Industrial robots</td><td>Articulated arms, welding robots</td><td>Automotive welding lines, general manufacturing</td></tr>
        <tr><td>Mobile robots</td><td>AGVs, AMRs, warehouse automation</td><td>Logistics, semiconductors, automotive</td></tr>
        <tr><td>Special robots</td><td>Clean-room robots, inspection robots</td><td>Semiconductor fabs, public security</td></tr>
        <tr><td>Collaborative robots</td><td>Cobots within five product families</td><td>Flexible assembly</td></tr>
        <tr><td>Automation systems</td><td>Welding / assembly / logistics automation</td><td>Complete factory solutions</td></tr>
        </table>"""),
     ("Financial Snapshot", """<table class="spec-table">
        <tr><th>Period</th><th>Revenue (CNY)</th><th>Net profit (CNY)</th></tr>
        <tr><td>2024</td><td>~4.4 billion</td><td>-194 million</td></tr>
        <tr><td>2025</td><td>4.12 billion</td><td>-398 million (gross margin 12.5%)</td></tr>
        <tr><td>2026 H1</td><td>1.45 billion</td><td>-189 million</td></tr>
        </table>"""),
     ("Global Benchmark", """<p>SIASUN is the Chinese counterpart to <a href="../china-robot-arms-vs-abb-kuka.html">ABB, KUKA and FANUC</a> — the incumbent industrial-robot oligopoly. Its scale (4.12 billion CNY revenue) approaches the global majors' China business, and its claim to fame is strategic: SIASUN built China's first domestic industrial robot and AGV, replacing imports across automotive and 3C plants. Unlike profitable global incumbents, SIASUN's margins have compressed sharply in recent years, and 2025's net loss of -398 million CNY shows the price pressure in China's crowded industrial-robot market — the same market where rivals such as Estun and Topstar now compete fiercely.</p>"""),
   ],
 },
}

def main():
    ok, skip, fail = [], [], []
    for fname, prof in PROFILES.items():
        p = os.path.join(BASE, fname)
        if not os.path.exists(p):
            fail.append((fname, "file missing")); continue
        html = open(p, encoding="utf-8").read()
        if "Milestones & Company History" in html:
            skip.append(fname); continue
        # 1) expand hero one-liner
        hero = re.search(r'(<section class="page-hero">.*?<p>)(.*?)(</p>)', html, re.S)
        if hero:
            new_hero = hero.group(2).strip() + " " + prof["hero_extra"]
            html = html[:hero.start()] + hero.group(1) + new_hero + hero.group(3) + html[hero.end():]
        # 2) also expand the Company Overview paragraph
        ov = re.search(r'(<h2>Company Overview</h2>\s*<p>)(.*?)(</p>)', html, re.S)
        if ov and "Milestones" not in ov.group(2):
            html = html[:ov.start()] + ov.group(1) + ov.group(2).strip() + " " + prof["hero_extra"] + ov.group(3) + html[ov.end():]
        # 3) insert blocks after Data Snapshot table, before FAQ
        faq_start = re.search(r"<h2>Frequently Asked Questions</h2>", html)
        if not faq_start:
            faq_start = re.search(r"<h2>Related Reading</h2>", html)
        if not faq_start:
            fail.append((fname, "no FAQ anchor")); continue
        ins = faq_start.start()
        blocks_html = []
        for title, body in prof["blocks"]:
            blocks_html.append("<h2>%s</h2>\n%s" % (esc(title), body.strip()))
        added = "\n\n        " + "\n\n        ".join(blocks_html)
        html = html[:ins] + added + "\n\n        " + html[ins:]
        io.open(p, "w", encoding="utf-8", newline="\n").write(html)
        ok.append(fname)
    print("DEEPENED:", len(ok), ok)
    print("SKIPPED (already thick):", len(skip), skip)
    print("FAILED:", len(fail), fail)

if __name__ == "__main__":
    main()
