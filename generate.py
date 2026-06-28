#!/usr/bin/env python3
"""
Galaxy profile SVG generator (self-contained, no external services).
Recreates the vinimlo/galaxy-profile aesthetic: a neuro-galaxy theme with
logarithmic spiral arms, a pulsing core, shooting stars, animated language
bars + rotating radar, and orbital project-constellation cards.

Run:  python3 generate.py
Output: ./assets/*.svg
"""
import math, os, random

random.seed(7)  # stable starfield between runs

# ----- theme -------------------------------------------------------------
T = {
    "void":    "#05060f",
    "void2":   "#0a0c1f",
    "nebula":  "#1b1140",
    "cyan":    "#22d3ee",   # synapse
    "violet":  "#a855f7",   # dendrite
    "amber":   "#fbbf24",   # axon
    "pink":    "#f472b6",
    "text":    "#e8ecff",
    "muted":   "#8b93c4",
    "faint":   "#5b639a",
}
ARMC = [T["cyan"], T["violet"], T["amber"]]

# ----- profile data (edit me) -------------------------------------------
NAME      = "Alpana Nanda"
TAGLINE   = "AI Data Engineer"
PHILOSOPHY= "turning raw data into orbit-ready intelligence"

TECH = [   # (category, [items])  -- from resume
    ("Languages",       ["Python", "SQL", "C++", "JavaScript"]),
    ("AI & LLM",        ["Azure AI Foundry", "Databricks Genie", "LangChain", "OpenAI API", "RAG Pipelines", "Prompt Engineering"]),
    ("Data Engineering",["Azure Databricks", "Azure Data Factory", "PySpark", "Delta Lake", "Azure SQL", "Power BI"]),
    ("Databases",       ["MongoDB", "PostgreSQL", "SQLite"]),
    ("DevOps & Cloud",  ["Azure", "AWS S3", "Docker", "GitHub Actions", "CI/CD"]),
    ("Web",             ["React.js", "Node.js", "Spring Boot", "Django", "Django REST"]),
]

PROJECTS = [  # (name, description, tag)  -- real hackathon highlights
    ("post-discharge-care", "MERN app with AI motion tracking · Dr. Reddy's winner", "AI / Health"),
    ("mentor-match",        "Platform matching students to tailored mentors · Juspay winner", "Full Stack"),
    ("virtual-try-on",      "ML makeup try-on built with Node.js · RAPID runner-up", "ML / Web"),
]

STATS = [  # telemetry card (edit to your real numbers)
    ("Commits",       "—"),
    ("Pull Requests", "—"),
    ("Stars Earned",  "—"),
    ("Repositories",  "—"),
    ("Contributions", "—"),
    ("Followers",     "—"),
]

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# =======================================================================
# 1. GALAXY HEADER
# =======================================================================
def header():
    W, H = 850, 320
    cx, cy = 232, 165         # galaxy core
    MONO = "'JetBrains Mono','Fira Code',Consolas,monospace"
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="Segoe UI,Helvetica,Arial,sans-serif" '
             f'role="img" aria-label="{esc(NAME)} galaxy header">')

    # ---- defs ----
    s.append('<defs>')
    s.append(f'''<radialGradient id="bg" cx="28%" cy="52%" r="85%">
      <stop offset="0%" stop-color="#241652"/>
      <stop offset="42%" stop-color="{T['nebula']}"/>
      <stop offset="78%" stop-color="{T['void2']}"/>
      <stop offset="100%" stop-color="{T['void']}"/></radialGradient>''')
    s.append(f'''<radialGradient id="core-haze" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.95"/>
      <stop offset="22%" stop-color="{T['cyan']}" stop-opacity="0.85"/>
      <stop offset="55%" stop-color="{T['violet']}" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="{T['violet']}" stop-opacity="0"/></radialGradient>''')
    s.append(f'''<radialGradient id="core-inner" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="55%" stop-color="{T['cyan']}"/>
      <stop offset="100%" stop-color="{T['violet']}" stop-opacity="0"/></radialGradient>''')
    s.append('<linearGradient id="shoot" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0%" stop-color="#fff" stop-opacity="0"/>'
             '<stop offset="100%" stop-color="#fff" stop-opacity="0.9"/></linearGradient>')
    s.append('<filter id="blur2"><feGaussianBlur stdDeviation="2"/></filter>')
    s.append('<filter id="blur6"><feGaussianBlur stdDeviation="6"/></filter>')
    s.append('<filter id="blur14"><feGaussianBlur stdDeviation="14"/></filter>')
    s.append('<filter id="bloom" x="-60%" y="-60%" width="220%" height="220%">'
             '<feGaussianBlur stdDeviation="2.4" result="b"/>'
             '<feMerge><feMergeNode in="b"/><feMergeNode in="b"/>'
             '<feMergeNode in="SourceGraphic"/></feMerge></filter>')
    s.append('<filter id="bloomS" x="-30%" y="-30%" width="160%" height="160%">'
             '<feGaussianBlur stdDeviation="1.2" result="b"/>'
             '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    s.append('</defs>')

    # ---- css animations ----
    s.append('<style>'
             '@keyframes tw{0%,100%{opacity:.15}50%{opacity:.95}}'
             '@keyframes twf{0%,100%{opacity:.1}50%{opacity:1}}'
             '@keyframes pc{0%,100%{transform:scale(1);opacity:.9}50%{transform:scale(1.13);opacity:1}}'
             '@keyframes spin{to{transform:rotate(360deg)}}'
             '@keyframes spinr{to{transform:rotate(-360deg)}}'
             '@keyframes shoot{0%{transform:translate(0,0);opacity:0}8%{opacity:1}26%{opacity:0}100%{opacity:0}}'
             '@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}'
             '@keyframes drift{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}'
             '@keyframes rain{0%{transform:translateY(-60px);opacity:0}10%{opacity:.5}90%{opacity:.5}100%{transform:translateY(160px);opacity:0}}'
             '.tw{animation:tw 3.6s ease-in-out infinite}'
             '.twf{animation:twf 1.9s ease-in-out infinite}'
             f'.galaxy{{transform-box:view-box;transform-origin:{cx}px {cy}px;animation:spin 90s linear infinite}}'
             f'.core{{transform-box:view-box;transform-origin:{cx}px {cy}px;animation:pc 4.2s ease-in-out infinite}}'
             '.shoot{animation:shoot 7s linear infinite}'
             '.s2{animation-delay:2.4s}.s3{animation-delay:4.7s}'
             '.cur{animation:blink 1.1s step-end infinite}'
             '.tok{transform-box:fill-box;transform-origin:center;animation:drift 6s ease-in-out infinite}'
             '.rain{animation:rain 5s linear infinite}'
             '</style>')

    s.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>')

    # ---- nebula blobs ----
    for (bx, by, br, col, op) in [(cx, cy, 165, T["violet"], .26),
                                  (cx+55, cy-35, 120, T["cyan"], .20),
                                  (cx-45, cy+45, 130, T["pink"], .14),
                                  (690, 95, 110, T["cyan"], .08),
                                  (610, 240, 90, T["violet"], .07)]:
        s.append(f'<circle cx="{bx}" cy="{by}" r="{br}" fill="{col}" opacity="{op}" filter="url(#blur14)"/>')

    # ---- code nebula (faint IDE text drifting in the background) ----
    snippets = ["def transform(df):", "spark.read.delta(path)", "model.fit(X, y)",
                "SELECT * FROM events", "llm.invoke(prompt)", "df.groupBy(col)",
                "import pyspark", "embeddings = encode(docs)", "@dag(schedule)",
                "0b1011  0xF4  1101", "async def stream():", "pipeline.run()"]
    random.shuffle(snippets)
    for i, snip in enumerate(snippets[:9]):
        x = random.uniform(380, 820); y = random.uniform(28, 300)
        col = random.choice([T["cyan"], T["violet"], T["faint"]])
        s.append(f'<text class="tw" x="{x:.0f}" y="{y:.0f}" fill="{col}" font-size="11" '
                 f'font-family="{MONO}" opacity="0.10" style="animation-duration:{random.uniform(4,7):.1f}s;'
                 f'animation-delay:{random.uniform(0,4):.1f}s">{esc(snip)}</text>')

    # ---- starfield ----
    for i in range(95):
        x = random.uniform(8, W-8); y = random.uniform(8, H-8)
        r = random.uniform(.4, 1.7); op = random.uniform(.2, .9)
        cls = "twf" if random.random() < .35 else "tw"
        dur = random.uniform(2.2, 5.5); dly = random.uniform(0, 5)
        col = "#ffffff" if random.random() < .8 else random.choice(ARMC)
        s.append(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{col}" '
                 f'opacity="{op:.2f}" style="animation-duration:{dur:.1f}s;animation-delay:{dly:.1f}s"/>')

    # ====== THE GALAXY (clean dotted spiral) ======
    def spiral_pts(start_deg, n=34, b=0.30, scale=8.0, flat=0.58):
        return [(cx + scale*math.exp(b*(k*0.30))*math.cos(math.radians(start_deg)+k*0.30),
                 cy + scale*math.exp(b*(k*0.30))*math.sin(math.radians(start_deg)+k*0.30)*flat)
                for k in range(n)]

    for ai, start in enumerate([20, 140, 260]):
        pts = spiral_pts(start)
        d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        col = ARMC[ai]
        # soft wide glow stroke
        s.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="9" '
                 f'opacity="0.10" filter="url(#blur6)"/>')
        # crisp dotted arm
        s.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.6" '
                 f'opacity="0.55" stroke-linecap="round" stroke-dasharray="0.5 5"/>')
        # particles travelling the arm
        for pi in range(2):
            dur = 6 + pi * 2.5 + ai
            s.append(f'<circle r="2.1" fill="#fff">'
                     f'<animateMotion dur="{dur}s" repeatCount="indefinite" '
                     f'begin="{pi*2+ai*0.6}s" path="{d}"/>'
                     f'<animate attributeName="opacity" values="0;1;1;0" dur="{dur}s" '
                     f'begin="{pi*2+ai*0.6}s" repeatCount="indefinite"/></circle>')
        # bright star near the arm tip
        tx, ty = pts[int(len(pts)*0.78)]
        s.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="2.4" fill="{col}" filter="url(#blur2)">'
                 f'<animate attributeName="opacity" values="0.4;1;0.4" dur="{3+ai}s" repeatCount="indefinite"/></circle>')

    # orbital rings
    for (rx, ry, col, dur, rev) in [(74, 32, T["cyan"], 28, 0),
                                    (100, 44, T["violet"], 40, 1),
                                    (126, 56, T["amber"], 54, 0)]:
        anim = "spin" if rev == 0 else "spinr"
        s.append(f'<g style="transform-box:view-box;transform-origin:{cx}px {cy}px;'
                 f'animation:{anim} {dur}s linear infinite">'
                 f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" '
                 f'stroke="{col}" stroke-width="0.8" opacity="0.22" stroke-dasharray="2 7"/></g>')

    # core
    s.append('<g class="core">')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="62" fill="url(#core-haze)"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="url(#core-inner)"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="#ffffff" filter="url(#bloomS)"/>')
    s.append('</g>')

    # ---- shooting stars ----
    for (x, y, cls) in [(560, 55, ""), (720, 120, "s2"), (480, 35, "s3")]:
        s.append(f'<g class="shoot {cls}" transform="translate({x},{y}) rotate(22)">'
                 f'<line x1="0" y1="0" x2="50" y2="0" stroke="url(#shoot)" stroke-width="2"/>'
                 f'<circle cx="50" cy="0" r="1.8" fill="#fff"/></g>')

    # ---- floating code tokens ----
    tokens = [("{ }", T["cyan"]), ("</>", T["violet"]), ("λ", T["amber"]),
              ("()=>", T["cyan"]), ("[ ]", T["pink"]), ("#!", T["violet"])]
    spots = [(470, 90), (810, 70), (640, 285), (790, 250), (455, 270), (835, 160)]
    for (tok, col), (x, y) in zip(tokens, spots):
        s.append(f'<text class="tok" x="{x}" y="{y}" fill="{col}" font-size="16" '
                 f'font-family="{MONO}" opacity="0.45" filter="url(#bloomS)" '
                 f'style="animation-duration:{random.uniform(5,8):.1f}s;'
                 f'animation-delay:{random.uniform(0,3):.1f}s">{esc(tok)}</text>')

    # ====== TEXT BLOCK (right) ======
    tx = 555
    # legibility vignette
    s.append(f'<ellipse cx="{tx}" cy="150" rx="245" ry="92" fill="{T["void"]}" '
             f'opacity="0.34" filter="url(#blur14)"/>')
    # name
    s.append(f'<text x="{tx}" y="128" text-anchor="middle" fill="#ffffff" '
             f'font-size="46" font-weight="800" letter-spacing="1.5">{esc(NAME)}</text>')
    s.append(f'<rect x="{tx-150}" y="144" width="300" height="2.5" rx="1.25" fill="{T["cyan"]}" opacity="0.85"/>')
    # terminal-style tagline with blinking cursor
    term = "> " + TAGLINE.lower().replace(" & ", "_").replace(" ", "_")
    s.append(f'<text x="{tx}" y="178" text-anchor="middle" font-family="{MONO}" '
             f'font-size="16" font-weight="600" fill="{T["cyan"]}" letter-spacing="0.5">{esc(term)}'
             f'<tspan class="cur" dx="2" fill="{T["cyan"]}">▮</tspan></text>')
    # comment line
    s.append(f'<text x="{tx}" y="206" text-anchor="middle" font-family="{MONO}" '
             f'font-size="12" fill="{T["muted"]}" letter-spacing="0.3"># {esc(PHILOSOPHY)}</text>')
    # status chip
    s.append(f'<g transform="translate({tx-72},224)">'
             f'<rect x="0" y="0" width="144" height="22" rx="11" fill="{T["cyan"]}" opacity="0.12"/>'
             f'<circle cx="16" cy="11" r="3.5" fill="#39d98a"><animate attributeName="opacity" '
             f'values="0.3;1;0.3" dur="2s" repeatCount="indefinite"/></circle>'
             f'<text x="28" y="15" font-family="{MONO}" font-size="10.5" fill="{T["text"]}" '
             f'letter-spacing="1">SYSTEMS ONLINE</text></g>')

    s.append('</svg>')
    return "\n".join(s), (W, H)


# =======================================================================
# 2. TECH STACK  (animated language bars + rotating radar)
# =======================================================================
def tech():
    W = 850
    pad = 28
    palette = [T["cyan"], T["violet"], T["amber"], T["pink"], T["cyan"], T["violet"]]
    body = []
    chip_i = 0
    y = 64
    for ci, (cat, items) in enumerate(TECH):
        col = palette[ci % len(palette)]
        y += 30 if ci else 18
        # category header: accent bar + label
        body.append(f'<rect x="{pad}" y="{y-11}" width="3.5" height="15" rx="2" fill="{col}"/>')
        body.append(f'<text x="{pad+12}" y="{y+1}" fill="{T["text"]}" font-size="13.5" '
                    f'font-weight="700" letter-spacing="1.5">{esc(cat.upper())}</text>')
        y += 20
        cx = pad
        for it in items:
            w = int(len(it) * 7.4) + 26
            if cx + w > W - pad:
                cx = pad; y += 34
            body.append(f'<g class="chip" style="animation-delay:{chip_i*0.05:.2f}s">')
            body.append(f'<rect x="{cx}" y="{y}" width="{w}" height="27" rx="13.5" '
                        f'fill="{col}" opacity="0.12"/>')
            body.append(f'<rect x="{cx+0.5}" y="{y+0.5}" width="{w-1}" height="26" rx="13" '
                        f'fill="none" stroke="{col}" stroke-opacity="0.45"/>')
            body.append(f'<circle cx="{cx+13}" cy="{y+13.5}" r="2.4" fill="{col}"/>')
            body.append(f'<text x="{cx+24}" y="{y+17.5}" fill="{T["text"]}" '
                        f'font-size="12">{esc(it)}</text>')
            body.append('</g>')
            cx += w + 8
            chip_i += 1
        y += 34
    H = y + 14

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="Segoe UI,Helvetica,Arial,sans-serif" role="img" '
         f'aria-label="Tech stack">']
    s.append('''<style>
      @keyframes pop{from{transform:scale(.6);opacity:0}to{transform:scale(1);opacity:1}}
      .chip{transform-box:fill-box;transform-origin:left center;animation:pop .5s ease-out backwards}
    </style>''')
    s.append(f'<rect width="{W}" height="{H}" rx="14" fill="{T["void2"]}"/>')
    s.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="13.5" fill="none" '
             f'stroke="{T["violet"]}" stroke-opacity="0.25"/>')
    s.append(f'<text x="28" y="42" fill="{T["text"]}" font-size="16" font-weight="700" '
             f'letter-spacing="2" font-family="monospace">TECH STACK</text>')
    s.append(f'<circle cx="20" cy="37" r="4" fill="{T["cyan"]}"><animate attributeName="opacity" '
             f'values="0.3;1;0.3" dur="2s" repeatCount="indefinite"/></circle>')
    # faint starfield
    for i in range(22):
        sx = random.uniform(10, W-10); sy = random.uniform(50, H-10)
        body.insert(0, f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{random.uniform(.3,.9):.2f}" '
                       f'fill="#fff" opacity="{random.uniform(.05,.2):.2f}"/>')
    s.extend(body)
    s.append('</svg>')
    return "\n".join(s), (W, H)


# =======================================================================
# 3. PROJECTS CONSTELLATION
# =======================================================================
def projects():
    W, H = 850, 230
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="Segoe UI,Helvetica,Arial,sans-serif" role="img" '
         f'aria-label="Featured systems">']
    s.append('<defs><filter id="ph"><feGaussianBlur stdDeviation="4"/></filter></defs>')
    s.append('''<style>
      @keyframes orb{to{transform:rotate(360deg)}}
      @keyframes pls{0%,100%{r:5;opacity:.6}50%{r:6.4;opacity:1}}
      @keyframes appr{from{transform:translateY(12px)}to{transform:translateY(0)}}
      @keyframes scan{0%{transform:translateY(0);opacity:0}10%{opacity:.5}90%{opacity:.5}100%{transform:translateY(150px);opacity:0}}
      .card{transform-box:fill-box;animation:appr .6s ease-out backwards}
      .orb{transform-box:fill-box;transform-origin:center;animation:orb 12s linear infinite}
      .pls{animation:pls 3s ease-in-out infinite}
    </style>''')
    s.append(f'<rect width="{W}" height="{H}" rx="14" fill="{T["void"]}"/>')
    # corner brackets
    for (cxr, cyr, sx, sy) in [(16,16,1,1),(W-16,16,-1,1),(16,H-16,1,-1),(W-16,H-16,-1,-1)]:
        s.append(f'<path d="M {cxr} {cyr+14*sy} L {cxr} {cyr} L {cxr+14*sx} {cyr}" '
                 f'fill="none" stroke="{T["cyan"]}" stroke-opacity="0.4" stroke-width="1.4"/>')
    # faint grid
    for gy in range(40, H, 40):
        s.append(f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}" stroke="{T["faint"]}" stroke-opacity="0.06"/>')
    for gx in range(80, W, 80):
        s.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}" stroke="{T["faint"]}" stroke-opacity="0.06"/>')
    # starfield
    for i in range(28):
        x=random.uniform(10,W-10); y=random.uniform(10,H-10); r=random.uniform(.3,1.1)
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.2f}" fill="#fff" opacity="{random.uniform(.1,.4):.2f}"/>')
    # header
    s.append(f'<text x="28" y="40" fill="{T["text"]}" font-size="14" font-weight="700" '
             f'letter-spacing="3" font-family="monospace">FEATURED SYSTEMS</text>')
    s.append(f'<circle cx="20" cy="35" r="4" fill="{T["cyan"]}"><animate attributeName="opacity" '
             f'values="0.4;1;0.4" dur="2s" repeatCount="indefinite"/></circle>')
    n = len(PROJECTS)
    s.append(f'<text x="{W-28}" y="40" text-anchor="end" fill="{T["muted"]}" font-size="11" '
             f'font-family="monospace" opacity="0.7">SYS {n}/{n} ONLINE</text>')

    cardw = 248; gap = (W - 56 - cardw*n) / max(1, n-1) if n > 1 else 0
    cy0 = 62; cardh = 142
    conn_y = cy0 + 30
    # connection line
    s.append(f'<line x1="{28+cardw/2}" y1="{conn_y}" x2="{W-28-cardw/2}" y2="{conn_y}" '
             f'stroke="{T["violet"]}" stroke-opacity="0.3" stroke-width="1" stroke-dasharray="3 5"/>')

    for i, (name, desc, tag) in enumerate(PROJECTS):
        x = 28 + i*(cardw+gap)
        col = ARMC[i % 3]
        s.append(f'<g class="card" style="animation-delay:{i*0.25:.2f}s">')
        s.append(f'<rect x="{x}" y="{cy0}" width="{cardw}" height="{cardh}" rx="10" '
                 f'fill="{T["void2"]}" stroke="{col}" stroke-opacity="0.4"/>')
        # orbital star
        ox = x + cardw/2; oy = cy0 + 26
        s.append(f'<circle cx="{ox}" cy="{oy}" r="13" fill="none" stroke="{col}" '
                 f'stroke-opacity="0.5" stroke-dasharray="2 4" class="orb"/>')
        s.append(f'<circle cx="{ox}" cy="{oy}" r="9" fill="{col}" opacity="0.4" filter="url(#ph)"/>')
        s.append(f'<circle class="pls" cx="{ox}" cy="{oy}" r="5" fill="{col}"/>')
        s.append(f'<circle cx="{ox}" cy="{oy}" r="2" fill="#fff"/>')
        # name
        s.append(f'<text x="{ox}" y="{cy0+68}" text-anchor="middle" fill="{T["text"]}" '
                 f'font-size="15" font-weight="700">{esc(name)}</text>')
        # description (wrap to 2 lines)
        words = desc.split(); lines=[""];
        for w in words:
            if len(lines[-1]) + len(w) > 30: lines.append("")
            lines[-1] += (" " if lines[-1] else "") + w
        for li, ln in enumerate(lines[:2]):
            s.append(f'<text x="{ox}" y="{cy0+88+li*15}" text-anchor="middle" fill="{T["muted"]}" '
                     f'font-size="11">{esc(ln)}</text>')
        # tag pill
        pw = 8 + len(tag)*7
        s.append(f'<rect x="{ox-pw/2}" y="{cy0+cardh-30}" width="{pw}" height="19" rx="9.5" '
                 f'fill="{col}" opacity="0.16"/>')
        s.append(f'<text x="{ox}" y="{cy0+cardh-17}" text-anchor="middle" fill="{col}" '
                 f'font-size="10" font-weight="600" letter-spacing="0.5">{esc(tag.upper())}</text>')
        s.append('</g>')
    s.append('</svg>')
    return "\n".join(s), (W, H)


# =======================================================================
# 4. STATS / TELEMETRY CARD
# =======================================================================
def stats():
    W = 850; cols = 3; rows = 2
    cw = (W - 56 - 24*(cols-1)) / cols; ch = 78; top = 70
    H = top + ch*rows + 24*(rows-1) + 24
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}" font-family="Segoe UI,Helvetica,Arial,sans-serif" role="img" '
       f'aria-label="Mission telemetry">']
    s.append(f'<rect width="{W}" height="{H}" rx="14" fill="{T["void2"]}"/>')
    s.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="13.5" fill="none" '
             f'stroke="{T["cyan"]}" stroke-opacity="0.22"/>')
    s.append(f'<text x="28" y="42" fill="{T["text"]}" font-size="16" font-weight="700" '
             f'letter-spacing="2" font-family="monospace">MISSION TELEMETRY</text>')
    s.append(f'<circle cx="20" cy="37" r="4" fill="{T["amber"]}"><animate attributeName="opacity" '
             f'values="0.3;1;0.3" dur="2s" repeatCount="indefinite"/></circle>')
    for i,(lab,val) in enumerate(STATS):
        r=i//cols; c=i%cols
        x=28 + c*(cw+24); y=top + r*(ch+24)
        col=ARMC[i%3]
        s.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="10" '
                 f'fill="{T["void"]}" stroke="{col}" stroke-opacity="0.3"/>')
        s.append(f'<rect x="{x}" y="{y}" width="3.5" height="{ch}" rx="2" fill="{col}" opacity="0.8"/>')
        s.append(f'<text x="{x+20}" y="{y+34}" fill="{col}" font-size="26" font-weight="700" '
                 f'font-family="monospace">{esc(val)}</text>')
        s.append(f'<text x="{x+20}" y="{y+58}" fill="{T["muted"]}" font-size="12" '
                 f'letter-spacing="1">{esc(lab.upper())}</text>')
    s.append('</svg>')
    return "\n".join(s),(W,H)


# ----- write all --------------------------------------------------------
# Note: tech stack is now a local logo wall in assets/logos/ (see README).
# The telemetry, tech-stack, and projects-constellation panels were removed by request.
for fn, gen in [("galaxy-header.svg", header)]:
    svg, _ = gen()
    with open(os.path.join(OUT, fn), "w") as f:
        f.write(svg)
    print("wrote", fn)
print("done ->", OUT)
