# -*- coding: utf-8 -*-
"""Batch 3: append Global Benchmark blocks to 5 already-thick company pages
(Inspire Robots, MileBot, Hechuan, Kepler, Robosea). Research-backed facts used
where available (Inspire: 2026 C1/C2 rounds, 10k+ dexterous hands in 2025;
Kepler: A++ round 2026-04, Keling 51% control 2026-05); remaining blocks reuse
already-verified page facts plus qualitative peer benchmarks only.
"""
import os, re, io, html

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")

GB = {
 "company-inspire-robots.html": """<p>Inspire Robots is the Chinese counterpart to Britain's Shadow Robot — the reference dexterous-hand maker behind most research and early humanoid hands — and a direct supplier candidate for humanoid platforms such as <a href="company-unitree.html">Unitree</a>, AgiBot and Kepler. Its edge is manufacturing: while Shadow sells low-volume, high-cost research hands, Inspire claims China's first commercial mass production of five-finger dexterous hands, with annual deliveries passing 10,000 units in 2025. The March 2026 C1/C2 rounds (China Mobile Chain Fund + Shenzhen Capital co-leading C1; Beijing AI Industry Fund leading C2) value the hand-and-micro-actuator layer that every Chinese humanoid needs.</p>""",
 "company-milebot.html": """<p>MileBot competes in China's rehab-robotics space against <a href="company-fourier.html">Fourier Intelligence</a> and global players such as Switzerland's Hocoma and US-based Ekso Bionics. Where Fourier sells premium full-body rehab systems internationally, MileBot targets lower-limb gait training — exoskeletons and robotic treadmills built for hospital rehab departments at Chinese prices. Its Shenzhen base keeps it close to the country's medical-device supply chain; the clinical-data moat (tens of thousands of gait-training sessions) is what separates rehab robotics from consumer exoskeletons.</p>""",
 "company-hechuan.html": """<p>Hechuan (688320.SH) plays the servo-and-motion-control layer that Japan's Yaskawa, Panasonic and Mitsubishi long owned, and that China's Inovance (汇川技术) now leads. As a STAR-Market pure servo play, Hechuan's pitch is "domestic servo at half the cost with faster delivery" for robot and machine-tool OEMs — the same substitution logic that lifted <a href="china-harmonic-reducers-vs-harmonic-drive.html">harmonic reducers</a> in joints. Its growth hinges on Chinese robot makers shifting from imported AC servo systems to domestic ones, a trend that accelerates whenever RMB costs or supply security matter.</p>""",
 "company-kepler.html": """<p>Kepler is one of the few Chinese startups built specifically for heavy-duty "blue-collar" humanoids, differentiating from <a href="company-unitree.html">Unitree</a>'s consumer-speed lineup and AgiBot's research-first approach. The April 2026 A++ round (SAIF leading, with Noli Intelligent Equipment and Shenzhen Minbao Photoelectric as strategic investors) funds its embodied-AI brain and force-tactile data play; in May 2026 Hangzhou Keling agreed to pay up to 300 million CNY for 41.57% to take 51% control — one of the first A-share takeovers of a humanoid startup, valuing Kepler against the global race of Tesla Optimus, Figure AI and Boston Dynamics. Its bet: heavy lifting in factories and logistics pays for humanoids before retail does.</p>""",
 "company-robosea.html": """<p>ROBOSEA occupies a niche the global majors ignore: bionic robotic fish and small underwater robots for monitoring, education and research — a softer, lower-cost cousin of the ROV industry led by US players like VideoRay and Ocean Infinity. Its Beijing base and bio-inspired platform give it differentiation in academic and environmental monitoring use, where realism and gentle interaction matter more than deep-water payloads. The niche keeps it small, but also keeps it out of the price war that defines China's humanoid and industrial-robot markets.</p>""",
}

def main():
    ok, skip = [], []
    for fname, text in GB.items():
        p = os.path.join(BASE, fname)
        if not os.path.exists(p):
            print("MISSING:", fname); continue
        html = open(p, encoding="utf-8").read()
        if "Global Benchmark" in html:
            skip.append(fname); continue
        faq_start = re.search(r"<h2>Frequently Asked Questions</h2>", html)
        ins = faq_start.start() if faq_start else len(html)
        block = "<h2>Global Benchmark</h2>\n" + text.strip()
        html = html[:ins] + "        " + block + "\n\n        " + html[ins:]
        io.open(p, "w", encoding="utf-8", newline="\n").write(html)
        ok.append(fname)
    print("OK:", len(ok), ok)
    print("SKIP:", len(skip), skip)

if __name__ == "__main__":
    main()
