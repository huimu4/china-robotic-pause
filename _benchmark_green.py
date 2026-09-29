# -*- coding: utf-8 -*-
"""Add only a Global Benchmark block to green-harmonic (already a thick page)."""
import os, re, io

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
p = os.path.join(BASE, "company-green-harmonic.html")
html = open(p, encoding="utf-8").read()
if "Global Benchmark" in html:
    print("already has Global Benchmark, skip")
else:
    block = ('<h2>Global Benchmark</h2>\n'
             '<p>Leaderdrive is the closest Chinese counterpart to Japan\'s <a href="../china-harmonic-reducers-vs-harmonic-drive.html">Harmonic Drive</a>, '
             'the global benchmark for precision harmonic reducers. Where Harmonic Drive long dominated premium robot joints, Leaderdrive offers comparable '
             'accuracy at lower cost and faster domestic supply - a key reason Chinese robot and humanoid makers can cut joint costs. Its 2025 revenue of '
             'RMB 571M still leaves it far smaller than Harmonic Drive Systems (JPY 60bn+ scale), so the catch-up story plus the humanoid hand/wrist '
             'opportunity is the core narrative; an A+H Hong Kong listing was filed in August 2026 to fund expansion.</p>')
    faq_start = re.search(r"<h2>Frequently Asked Questions</h2>", html)
    ins = faq_start.start() if faq_start else len(html)
    html = html[:ins] + "        " + block + "\n\n        " + html[ins:]
    io.open(p, "w", encoding="utf-8", newline="\n").write(html)
    print("added Global Benchmark to green-harmonic")
