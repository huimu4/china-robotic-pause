# -*- coding: utf-8 -*-
"""Batch upgrade thin company profile pages to the full template.
Reads each thin page, extracts title/desc/chips/keyfacts, classifies it,
injects Schema JSON-LD + differentiated FAQ + Related Reading, writes back.
"""
import re, os, io, html, sys

BASE = r"D:\ObsidianVault\机器人精英圈\china-robotic-pause\database"
THIN_LIST = r"D:\ObsidianVault\机器人精英圈\china-robotic-pause\_thin-list.txt"

# ---------- classification ----------
def classify(text):
    t = text.lower()
    if any(k in t for k in ["humanoid", "embodied", "biped", "通用人形", "人形"]): return "humanoid"
    if any(k in t for k in ["cobot", "collaborative", "协作"]): return "cobot"
    if any(k in t for k in ["vacuum", "cleaning", "扫地", "清洁", "floor"]): return "cleaning"
    if any(k in t for k in ["gantry", "industrial", "arm", "welding", "spray", "manufacturing", "factory", "cnc", "machine tool", "桁架", "工业", "焊接", "喷涂"]): return "industrial"
    if any(k in t for k in ["agv", "amr", "logistics", "warehouse", "storage", "物流", "仓储"]): return "logistics"
    if any(k in t for k in ["motor", "actuator", "reducer", "sensor", "drive", "component", "encoder", "screw", "harmonic", "bearing", "电机", "减速", "传感器", "丝杠", "轴承", "执行器"]): return "component"
    if any(k in t for k in ["medical", "surgical", "rehab", "exoskeleton", "康复", "医疗", "手术"]): return "medical"
    if any(k in t for k in ["drone", "uav", "无人机"]): return "drone"
    if any(k in t for k in ["education", "steam", "toy", "教育"]): return "education"
    return "general"

# ---------- FAQ templates (differentiated per category) ----------
FAQ = {
 "humanoid": [
  ("What does {name} do?",
   "{name} ({cn}) is a Chinese robotics company whose focus is {focus}. It sits in the fast-moving Chinese humanoid and embodied-AI segment, where companies compete on joint actuation, perception and manufacturing cost."),
  ("How does {name} compare with humanoid leaders such as Unitree, Fourier or Tesla Optimus?",
   "China's humanoid field is crowded. {name} is part of that ecosystem, competing against better-known names such as Unitree and Fourier and international programs like Tesla Optimus. Differentiation usually comes from {focus}, plus supply-chain and cost advantages common to Chinese builders."),
  ("Where is {name} based?",
   "{name} ({cn}) is headquartered in {hq}, China, one of the country's robot-industry clusters."),
 ],
 "cobot": [
  ("What does {name} do?",
   "{name} ({cn}) is a Chinese maker of collaborative robots. Its focus is {focus}, serving manufacturing and education customers that need safe, easy-to-deploy 6-axis arms."),
  ("How does {name} compare with Universal Robots or Doosan?",
   "Chinese cobot makers such as {name} compete with Universal Robots and Doosan on price, local support and fast iteration. {name}'s edge comes from {focus}, at a cost structure global brands often cannot match."),
  ("Where is {name} based?",
   "{name} ({cn}) is headquartered in {hq}, China."),
 ],
 "cleaning": [
  ("What does {name} do?",
   "{name} ({cn}) is a Chinese home-robot company focused on {focus}. The category is dominated by Chinese brands, which now ship most of the world's robot vacuums."),
  ("How does {name} compete with Roborock, Ecovacs or Dreame?",
   "The Chinese cleaning-robot market is fiercely competitive, with Roborock, Ecovacs and Dreame leading globally. {name} differentiates on {focus}, a segment where Chinese supply chains keep costs and feature cycles aggressive."),
  ("Where is {name} based?",
   "{name} ({cn}) is headquartered in {hq}, China."),
 ],
 "industrial": [
  ("What does {name} do?",
   "{name} ({cn}) is a Chinese industrial-automation company focused on {focus}. It serves factories that need reliable, cost-effective robotic and automation systems."),
  ("How does {name} compare with ABB, KUKA or FANUC?",
   "Chinese industrial-robot makers such as {name} are closing the gap with ABB, KUKA and FANUC in price-sensitive segments. {name} competes mainly on {focus}, local integration speed and supply-chain cost."),
  ("Where is {name} based?",
   "{name} ({cn}) is headquartered in {hq}, China, near its main manufacturing customers."),
 ],
 "logistics": [
  ("What does {name} do?",
   "{name} ({cn}) is a Chinese logistics-robotics company focused on {focus}. Chinese AMR and AGV makers now supply warehouses globally with flexible, low-cost automation."),
  ("How does {name} compete with global AMR leaders?",
   "{name} competes with international AMR/AGV vendors on {focus}, leveraging China's electronics supply chain and deployment speed. Global players still lead in large enterprise integrations, while Chinese vendors win on price and iteration."),
  ("Where is {name} based?",
   "{name} ({cn}) is headquartered in {hq}, China."),
 ],
 "component": [
  ("What does {name} do?",
   "{name} ({cn}) is a Chinese robotics-component supplier focused on {focus}. Core components — motors, reducers, sensors, screws and drives — are where China is rapidly building self-sufficiency."),
  ("How does {name} compare with global component leaders like Harmonic Drive or Maxon?",
   "Chinese component makers such as {name} are challenging incumbents like Harmonic Drive (reducers) and Maxon (motors) on price and delivery. {name} differentiates on {focus}, often with comparable specs at lower cost."),
  ("Where is {name} based?",
   "{name} ({cn}) is headquartered in {hq}, China."),
 ],
 "medical": [
  ("What does {name} do?",
   "{name} ({cn}) is a Chinese company focused on {focus} in the medical and rehabilitation robotics space, a sector where China is investing heavily."),
  ("How does {name} compare with Intuitive Surgical or global rehab-robot makers?",
   "Chinese medical-robotics players such as {name} are developing alternatives to established systems like Intuitive's da Vinci. {name} focuses on {focus}, with domestic approval pipelines and cost advantages."),
  ("Where is {name} based?",
   "{name} ({cn}) is headquartered in {hq}, China."),
 ],
 "drone": [
  ("What does {name} do?",
   "{name} ({cn}) is a Chinese company focused on {focus} in the drone/UAV industry, which China's Shenzhen ecosystem largely leads worldwide."),
  ("How does {name} compare with DJI?",
   "DJI dominates consumer and commercial drones. {name} focuses on {focus}, finding niches — industrial inspection, logistics or specialized platforms — where it can differentiate."),
  ("Where is {name} based?",
   "{name} ({cn}) is headquartered in {hq}, China."),
 ],
 "education": [
  ("What does {name} do?",
   "{name} ({cn}) is a Chinese company focused on {focus} in the educational-robotics market, which is expanding rapidly with China's push for STEM curricula."),
  ("How does {name} compete in the education-robot market?",
   "Educational robotics in China is a fast-growing, price-sensitive market. {name} focuses on {focus}, competing with domestic rivals and global brands like LEGO Education and Makeblock."),
  ("Where is {name} based?",
   "{name} ({cn}) is headquartered in {hq}, China."),
 ],
 "general": [
  ("What does {name} do?",
   "{name} ({cn}) is a Chinese robotics company focused on {focus}. It is part of China's fast-growing robotics ecosystem, which spans industrial, service and humanoid robots."),
  ("How does {name} fit into China's robotics industry?",
   "China's robotics sector is broad and competitive. {name} focuses on {focus}, competing with domestic peers and international companies through cost, integration and speed."),
  ("Where is {name} based?",
   "{name} ({cn}) is headquartered in {hq}, China."),
 ],
}

# ---------- related reading per category ----------
RELATED = {
 "humanoid": ("../humanoid-robot-bom-cost-breakdown.html", "../humanoid-robot-race.html",
              "company-unitree.html", "company-fourier.html"),
 "cobot": ("../china-cobots-vs-universal-robots.html", "../china-robot-arms-vs-abb-kuka.html",
           "company-flexiv.html", "company-jaka.html"),
 "cleaning": ("../china-robot-vacuums.html", "../unitree-go2-vs-xiaomi-cyberdog.html",
              "company-roborock.html", "company-ecovacs.html"),
 "industrial": ("../china-industrial-robots.html", "../china-robot-arms-vs-abb-kuka.html",
                "company-siasun.html", "company-estun.html"),
 "logistics": ("../china-amr-agv-suppliers.html", "../china-industrial-robots.html",
               "company-geekplus.html", "company-visionnav.html"),
 "component": ("../china-humanoid-actuator-suppliers.html", "../china-harmonic-drive-suppliers.html",
               "company-sanhua.html", "company-qinchuan.html"),
 "medical": ("../china-surgical-robots-vs-intuitive-davinci.html", "../china-exoskeleton-robots.html",
             "company-elite-robots.html", "company-medbot.html"),
 "drone": ("../china-industrial-robots.html", "../humanoid-robot-race.html",
           "company-dji.html", "company-siasun.html"),
 "education": ("../china-educational-robots.html", "../china-industrial-robots.html",
               "company-dobot.html", "company-ai-squared.html"),
 "general": ("../china-industrial-robots.html", "../humanoid-robot-race.html",
             "company-siasun.html", "company-unitree.html"),
}

KICKER = {
 "humanoid": "Humanoid & Embodied AI", "cobot": "Collaborative Robots",
 "cleaning": "Home & Cleaning Robots", "industrial": "Industrial Automation",
 "logistics": "Logistics & Mobile Robots", "component": "Core Components & Supply Chain",
 "medical": "Medical & Rehabilitation", "drone": "Drones & UAV",
 "education": "Educational Robotics", "general": "Robotics",
}

# ---------- template ----------
TMPL = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>$title</title>
  <meta name="description" content="$meta_desc">
  <meta name="keywords" content="$keywords">
  <link rel="canonical" href="https://www.robotichina.com/database/$fname">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="China Robotics Insider">
  <meta property="og:title" content="$name — Company Profile">
  <meta property="og:description" content="$og_desc">
  <meta property="og:url" content="https://www.robotichina.com/database/$fname">
  <meta property="og:image" content="https://www.robotichina.com/assets/og-default.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="../css/style.css">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "$name",
    "alternateName": "$cn",
    "description": "$meta_desc",
    "url": "$site_url",
    "publisher": {"@type": "Organization", "name": "China Robotics Insider"},
    "mainEntityOfPage": {"@type": "WebPage", "@id": "https://www.robotichina.com/database/$fname"}
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.robotichina.com/"},
      {"@type": "ListItem", "position": 2, "name": "Database", "item": "https://www.robotichina.com/database/index.html"},
      {"@type": "ListItem", "position": 3, "name": "$name", "item": "https://www.robotichina.com/database/$fname"}
    ]
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      $faq_json
    ]
  }
  </script>
  <link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon-32.png">
  <link rel="shortcut icon" href="../assets/favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="../assets/apple-touch-icon.png">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-M63KB9ZNPK"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-M63KB9ZNPK');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5339038392744176" crossorigin="anonymous"></script>
</head>
<body>

<header class="site-header">
  <div class="container nav-wrap">
    <a class="brand" href="../index.html" aria-label="China Robotics Insider home">
      <svg class="logo-mark" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect x="8" y="16" width="24" height="15" rx="4" fill="#2563eb"/>
        <rect x="5" y="12" width="4" height="9" rx="2" fill="#f59e0b"/>
        <rect x="31" y="12" width="4" height="9" rx="2" fill="#f59e0b"/>
        <rect x="13" y="20" width="4" height="4" rx="1" fill="#fff"/>
        <rect x="23" y="20" width="4" height="4" rx="1" fill="#fff"/>
        <rect x="18" y="27" width="4" height="4" rx="1" fill="#fff"/>
        <circle cx="9" cy="30" r="2.4" fill="#0d9488"/>
        <circle cx="31" cy="30" r="2.4" fill="#0d9488"/>
      </svg>
      <span>China Robotics <b>Insider</b></span>
    </a>
    <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav class="main-nav" aria-label="Primary">
      <ul>
        <li><a href="../index.html">Home</a></li>
        <li><a href="../history.html">History</a></li>
        <li><a href="../people.html">People</a></li>
        <li><a href="../companies.html">Companies</a></li>
        <li><a href="../products.html">Products</a></li>
        <li><a href="../articles.html">Insights</a></li>
        <li><a href="../news.html">News</a></li>
        <li><a href="./index.html" class="active">Database</a></li>
        <li><a href="../about.html">About</a></li>
        <li class="nav-search">
          <form class="search-form" action="../search.html" method="get" role="search">
            <input type="search" name="q" placeholder="Search…" aria-label="Search this site">
          </form>
        </li>
      </ul>
    </nav>
  </div>
</header>

<main>
  <section class="page-hero">
    <div class="container ph-inner">
      <span class="kicker">Database · $kicker</span>
      <h1>$name</h1>
      <p>$hero_desc</p>
      <div class="p-chips">$chips_html</div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="person-head">
        <div class="p-h-meta">
          <span class="p-cn">$cn</span>
          <h2>$name — $focus_headline</h2>
          <p><a class="btn-primary" target="_blank" rel="noopener noreferrer" href="$site_url">Official site ↗</a></p>
        </div>
      </div>

      <div class="prose" style="max-width:860px;">
        <h2>Company Overview</h2>
        <p>$hero_desc</p>

        <h2>Key Facts</h2>
        <table class="spec-table">
$keyfacts_html
        </table>

        <h2>Frequently Asked Questions</h2>
$faq_html

        <h2>Related Reading</h2>
        <ul>
$related_html
        </ul>
      </div>
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <h4>Navigation</h4>
      <ul>
        <li><a href="../index.html">Home</a></li>
        <li><a href="../history.html">History</a></li>
        <li><a href="../people.html">People</a></li>
        <li><a href="../companies.html">Companies</a></li>
        <li><a href="../products.html">Products</a></li>
        <li><a href="../articles.html">Insights</a></li>
        <li><a href="../news.html">News</a></li>
        <li><a href="./index.html">Database</a></li>
      </ul>
    </div>
    <div>
      <h4>Resources</h4>
      <ul>
        <li><a href="../privacy.html">Privacy Policy</a></li>
        <li><a href="../about.html">About Us</a></li>
      </ul>
    </div>
  </div>
</footer>

</body>
</html>
"""

def esc(s):
    return html.escape(s, quote=False)

def parse_thin(path):
    with io.open(path, "r", encoding="utf-8") as f:
        t = f.read()
    fname = os.path.basename(path)
    m = re.search(r"<title>(.*?)</title>", t)
    title = m.group(1) if m else fname
    m = re.search(r"<meta name='description' content='(.*?)'>", t)
    meta_desc = m.group(1) if m else ""
    m = re.search(r"<h1>([^<]*)</h1>", t)
    name = m.group(1).strip() if m else ""
    m = re.search(r"<h1>.*?</h1><p>(.*?)</p>", t, re.S)
    hero_desc = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else meta_desc
    chips = re.findall(r"<span class='chip'>([^<]*)</span>", t)
    kf_raw = re.findall(r"<tr><th>(.*?)</th><td>(.*?)</td></tr>", t, re.S)
    kf = {}
    for k, v in kf_raw:
        kk = re.sub(r"<[^>]+>", "", k).strip().lower()
        vv = re.sub(r"<[^>]+>", "", v).strip()
        kf[kk] = vv
    cn = kf.get("chinese name", "")
    hq = kf.get("headquarters", "China")
    focus = kf.get("focus", chips[0] if chips else "robotics")
    site_url = kf.get("official site", "")
    return dict(fname=fname, title=title, meta_desc=meta_desc, name=name,
                hero_desc=hero_desc, chips=chips, kf=kf, cn=cn, hq=hq,
                focus=focus, site_url=site_url)

def build(d):
    cat = classify(d["focus"] + " " + " ".join(d["chips"]))
    d["kicker"] = KICKER[cat]
    d["focus_headline"] = d["focus"][0].upper() + d["focus"][1:] if d["focus"] else "Robotics"
    # chips html
    chips_html = " ".join("<span class='chip'>%s</span>" % esc(c) for c in d["chips"]) or "<span class='chip'>Robotics</span>"
    # keyfacts rows: keep Chinese name, Headquarters, Focus, Official site + any extra
    rows = []
    seen = set()
    order = [("chinese name", "Chinese Name"), ("headquarters", "Headquarters"),
             ("focus", "Focus"), ("official site", "Official Site")]
    for key, label in order:
        v = d["kf"].get(key, "")
        if v and key not in seen:
            seen.add(key)
            if key == "official site" and d.get("site_url"):
                rows.append("<tr><th>%s</th><td><a href=\"%s\" target=\"_blank\" rel=\"noopener\">%s</a></td></tr>" % (label, esc(d["site_url"]), esc(d["site_url"])))
            else:
                rows.append("<tr><th>%s</th><td>%s</td></tr>" % (label, esc(v)))
    # extra keyfacts not in order list
    for k, v in d["kf"].items():
        if k not in seen and v:
            label = " ".join(w.capitalize() for w in k.split())
            rows.append("<tr><th>%s</th><td>%s</td></tr>" % (esc(label), esc(v)))
    keyfacts_html = "\n".join("        " + r for r in rows)
    # faq
    faq_objs = []
    faq_blocks = []
    for q, a in FAQ[cat]:
        qq = q.format(name=d["name"], cn=d["cn"], focus=d["focus"], hq=d["hq"])
        aa = a.format(name=d["name"], cn=d["cn"], focus=d["focus"], hq=d["hq"])
        faq_objs.append('{"@type": "Question", "name": "%s", "acceptedAnswer": {"@type": "Answer", "text": "%s"}}' % (esc_json(qq), esc_json(aa)))
        faq_blocks.append('<h3>%s</h3>\n<p>%s</p>' % (esc(qq), esc(aa)))
    d["faq_json"] = ",\n      ".join(faq_objs)
    d["faq_html"] = "\n\n".join("        " + b for b in faq_blocks)
    # related
    a1, a2, c1, c2 = RELATED[cat]
    rel = []
    rel.append('<li><a href="%s">%s</a></li>' % (a1, a1.split("/")[-1].replace(".html", "").replace("-", " ").title()))
    rel.append('<li><a href="%s">%s</a></li>' % (a2, a2.split("/")[-1].replace(".html", "").replace("-", " ").title()))
    # company anchors: only if file exists
    for c in (c1, c2):
        if os.path.exists(os.path.join(BASE, c)):
            cname = c.replace("company-", "").replace(".html", "").replace("-", " ").title()
            rel.append('<li><a href="%s">%s Profile</a></li>' % (c, cname))
    rel.append('<li><a href="companies-directory.html">Full Company Directory</a></li>')
    d["related_html"] = "\n".join("          " + r for r in rel)
    # assemble
    out = TMPL
    for key in ["title", "meta_desc", "name", "cn", "site_url", "fname",
                "hero_desc", "kicker", "chips_html", "keyfacts_html",
                "faq_json", "faq_html", "related_html", "focus_headline"]:
        out = out.replace("$" + key, str(d.get(key, "")))
    d["keywords"] = ", ".join([d["name"], d["cn"], d["focus"]] + d["chips"])
    out = out.replace("$keywords", d["keywords"])
    og_desc = (d["hero_desc"] or d["meta_desc"])[:155]
    out = out.replace("$og_desc", esc(og_desc))
    return out

def esc_json(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()

def main():
    with io.open(THIN_LIST, "r", encoding="utf-8") as f:
        names = [l.strip() for l in f if l.strip()]
    ok, fail = [], []
    for n in names:
        p = os.path.join(BASE, n)
        try:
            d = parse_thin(p)
            out = build(d)
            with io.open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(out)
            ok.append(n)
        except Exception as e:
            fail.append((n, str(e)))
    print("UPGRADED: %d" % len(ok))
    if fail:
        print("FAILED: %d" % len(fail))
        for n, e in fail:
            print(" ", n, e)

if __name__ == "__main__":
    main()
