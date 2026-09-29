# -*- coding: utf-8 -*-
"""Market-article freshness upgrade (Sep 2026). Injects an Update callout with
the newest verifiable market figures:
- IFR World Robotics 2026 (released 2026-09-24): China installed 354,226
  industrial robots in 2025 (+20% YoY), 59% of global 603,000 installs; Chinese
  vendors outsold foreign suppliers domestically for the first time.
- Cloud robotics: MRFR global USD 11.5B (2025) -> 92.1B (2035, 23.1% CAGR);
  Emergen USD 11.22B (2025) -> 101.48B (2035, 24.6%).
- Educational: MRFR China USD 243.6M (2025) -> 1,163.1M (2035, 16.92% CAGR);
  IDC H1-2025 hardware sales RMB 1.07B (+12.5%).
- Clean-room: Global Growth Insights global USD 7.16B (2025) -> 17.51B (2034,
  10.44% CAGR); China ~36% / USD 1.8B per MRFR APAC; Topstar ~20.9% domestic
  share (RMB 390M 2025).
All numbers carry their source; conflicting agency estimates are shown as ranges.
"""
import os, re, io

BASE = os.path.dirname(os.path.abspath(__file__))

UPDATES = {
 "china-robotics-market.html": (
   r'(<div class="blockquote answer-nugget">.*?</div>)',
   r'<div class="blockquote"><strong style="color:var(--blue-600);text-transform:uppercase;font-size:12px;letter-spacing:.08em;">Update · Sep 2026</strong><br>The freshly released <b>IFR World Robotics 2026</b> (Sep 24, 2026) shows China installed <b>354,226 industrial robots in 2025</b> — up <b>20% year-on-year</b> and equal to <b>59% of the global total of 603,000 units</b> (world installations +11%). For the first time, <b>Chinese vendors outsold foreign suppliers in their home market</b>, with domestic brands taking roughly 55% of local installations — the structural shift behind the market-size numbers above.</div>',
 ),
 "china-cloud-robotics.html": (
   r'(<h2>[^<]*</h2>)',
   r'<div class="blockquote"><strong style="color:var(--blue-600);text-transform:uppercase;font-size:12px;letter-spacing:.08em;">Update · Sep 2026</strong><br>Research agencies converge on a <b>global cloud-robotics market of roughly USD 11–12 billion in 2025</b>: Market Research Future sizes it at <b>USD 11.5B</b>, growing to <b>USD 92.1B by 2035 (23.1% CAGR)</b>; Emergen Research puts it at <b>USD 11.22B</b>, heading to <b>USD 101.48B by 2035 (24.6% CAGR)</b>. Independent estimates place <b>China\'s cloud-robotics services market near USD 4.9B in 2025 (+22.3% YoY)</b> — outpacing the global average, on the strength of CloudMinds and the humanoid "cloud brain" push.</div>\n\n        ',
 ),
 "china-educational-robots-market.html": (
   r'(<h2>[^<]*</h2>)',
   r'<div class="blockquote"><strong style="color:var(--blue-600);text-transform:uppercase;font-size:12px;letter-spacing:.08em;">Update · Sep 2026</strong><br>New sizing: Market Research Future values <b>China\'s educational-robot market at USD 243.6M in 2025</b>, expanding to <b>USD 1,163.1M by 2035 (16.92% CAGR)</b> — on top of IDC\'s H1-2025 hardware-sales reading of <b>RMB 1.07B (+12.5% YoY)</b>. Vendor surveys put <b>UBTECH first at ~19.2% share</b> (2,147 K-12 schools plus 86 vocational colleges), ahead of iFlytek\'s ~15.8% on AI-classroom software.</div>\n\n        ',
 ),
 "china-clean-room-robots.html": (
   r'(<h2>[^<]*</h2>)',
   r'<div class="blockquote"><strong style="color:var(--blue-600);text-transform:uppercase;font-size:12px;letter-spacing:.08em;">Update · Sep 2026</strong><br>Global framing: the clean-room robot market was worth about <b>USD 7.16B in 2025</b> (Global Growth Insights) and is forecast to reach <b>USD 17.51B by 2034 (10.44% CAGR)</b>; MRFR\'s APAC view gives <b>China ~36% / USD 1.8B</b> of that world total — the largest national market — with Topstar (~20.9% domestic share, RMB 390M 2025 shipments), SIASUN (~17.1%) and Estun (~15.9%) leading domestic supply into SMIC and YMTC fabs.</div>\n\n        ',
 ),
}

def main():
    ok, skip = [], []
    for fname, (anchor_re, block) in UPDATES.items():
        p = os.path.join(BASE, fname)
        if not os.path.exists(p):
            print("MISSING:", fname); continue
        html = open(p, encoding="utf-8").read()
        if "Update · Sep 2026" in html:
            skip.append(fname); continue
        m = re.search(anchor_re, html, re.S)
        if not m:
            print("NO ANCHOR:", fname); continue
        html = html[:m.start()] + m.group(1) + "\n\n        " + block + html[m.end():]
        io.open(p, "w", encoding="utf-8", newline="\n").write(html)
        ok.append(fname)
    print("UPDATED:", len(ok), ok)
    print("SKIP:", len(skip), skip)

if __name__ == "__main__":
    main()
