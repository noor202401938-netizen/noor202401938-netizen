#!/usr/bin/env python3
"""Generates the Dracula-themed SVG asset set for the GitHub profile README."""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

# ── Dracula palette ────────────────────────────────────────────────────────────
BG      = "#282a36"
DEEP    = "#1e1f29"
PANEL   = "#21222c"
LINE    = "#44475a"
FG      = "#f8f8f2"
CMT     = "#6272a4"
CYAN    = "#8be9fd"
GREEN   = "#50fa7b"
ORANGE  = "#ffb86c"
PINK    = "#ff79c6"
PURPLE  = "#bd93f9"
RED     = "#ff5555"
YELLOW  = "#f1fa8c"

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,Liberation Mono,monospace"

W = 860          # full content width
ADV = 0.6        # monospace advance ratio


def tw(s, size):
    """Approximate rendered width of a monospace string."""
    return len(s) * size * ADV


def defs(extra=""):
    return f"""<defs>
    <pattern id="grid" width="26" height="26" patternUnits="userSpaceOnUse">
      <path d="M26 0H0V26" fill="none" stroke="{LINE}" stroke-width="1" opacity=".22"/>
    </pattern>
    <radialGradient id="glowA" cx="12%" cy="0%" r="65%">
      <stop offset="0%" stop-color="{PURPLE}" stop-opacity=".20"/>
      <stop offset="100%" stop-color="{PURPLE}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowB" cx="92%" cy="100%" r="60%">
      <stop offset="0%" stop-color="{CYAN}" stop-opacity=".13"/>
      <stop offset="100%" stop-color="{CYAN}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{PURPLE}" stop-opacity=".85"/>
      <stop offset="55%" stop-color="{PINK}" stop-opacity=".35"/>
      <stop offset="100%" stop-color="{CYAN}" stop-opacity="0"/>
    </linearGradient>
    <filter id="soft" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="7" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="dot" x="-160%" y="-160%" width="420%" height="420%">
      <feGaussianBlur stdDeviation="2.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>{extra}
  </defs>"""


def frame(w, h, r=14, grid=True, glow=True, fill=PANEL):
    """Rounded panel with grid + ambient glow."""
    s = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="{fill}"/>'
    if grid:
        s += f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="url(#grid)"/>'
    if glow:
        s += (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="url(#glowA)"/>'
              f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="url(#glowB)"/>')
    s += f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="none" stroke="{LINE}" stroke-width="1.5"/>'
    return s


def titlebar(w, label, y=0, h=36, r=14):
    """macOS-ish terminal title bar."""
    return f"""<g transform="translate(0,{y})">
    <path d="M1 {r} A{r} {r} 0 0 1 {1+r} 1 H{w-1-r} A{r} {r} 0 0 1 {w-1} {r} V{h} H1 Z" fill="{DEEP}"/>
    <line x1="1" y1="{h}" x2="{w-1}" y2="{h}" stroke="{LINE}" stroke-width="1.5"/>
    <circle cx="22" cy="{h/2}" r="5.5" fill="{RED}" opacity=".9"/>
    <circle cx="42" cy="{h/2}" r="5.5" fill="{YELLOW}" opacity=".9"/>
    <circle cx="62" cy="{h/2}" r="5.5" fill="{GREEN}" opacity=".9"/>
    <text x="{w/2}" y="{h/2+4}" text-anchor="middle" font-family="{MONO}" font-size="12"
          fill="{CMT}" letter-spacing="1">{label}</text>
  </g>"""


def svg(w, h, body, extra_defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" fill="none" role="img">\n  {defs(extra_defs)}\n  {body}\n</svg>\n')


def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)
    print(f"  wrote assets/{name}")


def chip(x, y, text, color, size=12, ph=9, h=26):
    """Rounded tag."""
    w = tw(text, size) + ph * 2
    return (f'<g><rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" '
            f'fill="{color}" fill-opacity=".10" stroke="{color}" stroke-opacity=".38" stroke-width="1"/>'
            f'<text x="{x+ph:.1f}" y="{y+h/2+4.2}" font-family="{MONO}" font-size="{size}" '
            f'fill="{color}">{text}</text></g>', w)


def chiprow(x, y, items, colors, size=12, gap=9):
    out, cx = "", x
    for i, it in enumerate(items):
        g, w = chip(cx, y, it, colors[i % len(colors)], size=size)
        out += g
        cx += w + gap
    return out, cx - x - gap


# ══════════════════════════════════════════════════════════════════════════════
# 1. HERO
# ══════════════════════════════════════════════════════════════════════════════
def hero():
    h = 300
    b = frame(W, h)
    b += titlebar(W, "~/noor/profile — zsh")

    x = 40
    b += f'<text x="{x}" y="86" font-family="{MONO}" font-size="14" fill="{GREEN}">&#8250;</text>'
    b += f'<text x="{x+18}" y="86" font-family="{MONO}" font-size="14" fill="{CYAN}">whoami</text>'

    # name
    b += (f'<text x="{x}" y="146" font-family="{MONO}" font-size="46" font-weight="700" '
          f'letter-spacing="2" fill="{PURPLE}" opacity=".30" filter="url(#soft)">NOOR FATIMA</text>')
    b += (f'<text x="{x}" y="146" font-family="{MONO}" font-size="46" font-weight="700" '
          f'letter-spacing="2" fill="{FG}">NOOR FATIMA</text>')

    # role line
    roles = [("SOFTWARE ENGINEER", PURPLE), ("FOUNDER", PINK), ("BUILDER", CYAN)]
    cx = x
    for i, (t, c) in enumerate(roles):
        b += (f'<text x="{cx:.1f}" y="176" font-family="{MONO}" font-size="13" letter-spacing="2.4" '
              f'fill="{c}">{t}</text>')
        cx += tw(t, 13) + 2.4 * len(t) + 10
        if i < len(roles) - 1:
            b += f'<text x="{cx:.1f}" y="176" font-family="{MONO}" font-size="13" fill="{LINE}">/</text>'
            cx += 20

    b += (f'<text x="{x}" y="212" font-family="{MONO}" font-size="14.5" fill="{FG}" opacity=".82">'
          f'Building AI-first systems for Pakistani SMEs.</text>')

    # links
    lk, _ = chiprow(x, 232, ["SixtyHours.tech", "Autometiq.com"], [PINK, CYAN], size=12.5)
    b += lk

    # status column (right)
    b += f'<line x1="596" y1="62" x2="596" y2="{h-30}" stroke="{LINE}" stroke-width="1" opacity=".7"/>'
    b += (f'<text x="628" y="86" font-family="{MONO}" font-size="11" letter-spacing="2.2" '
          f'fill="{CMT}">&#8250; STATUS</text>')
    for i, (t, c) in enumerate([("BUILDING", GREEN), ("SHIPPING", PINK), ("LEARNING", CYAN)]):
        yy = 118 + i * 30
        b += f'<circle cx="633" cy="{yy-4}" r="4.2" fill="{c}" filter="url(#dot)"/>'
        b += (f'<text x="650" y="{yy}" font-family="{MONO}" font-size="13" letter-spacing="1.6" '
              f'fill="{FG}" opacity=".9">{t}</text>')

    b += f'<line x1="628" y1="204" x2="{W-40}" y2="204" stroke="{LINE}" stroke-width="1" opacity=".6"/>'
    b += (f'<text x="628" y="232" font-family="{MONO}" font-size="11.5" fill="{CMT}">'
          f'Faisalabad, PK &#8212; UTC+5</text>')

    # prompt + blinking cursor
    b += f'<text x="{x}" y="{h-26}" font-family="{MONO}" font-size="13.5" fill="{GREEN}">&#8250;</text>'
    b += (f'<rect x="{x+18}" y="{h-38}" width="9" height="16" fill="{FG}" opacity=".85">'
          f'<animate attributeName="opacity" values="0;0;.9;.9" dur="1.1s" repeatCount="indefinite"/></rect>')

    write("hero.svg", svg(W, h, b))


# ══════════════════════════════════════════════════════════════════════════════
# 2. SECTION HEADERS
# ══════════════════════════════════════════════════════════════════════════════
def section(num, title, note, accent, fname):
    h = 58
    b = ""
    # number badge
    b += (f'<rect x="1" y="12" width="52" height="34" rx="8" fill="{accent}" fill-opacity=".12" '
          f'stroke="{accent}" stroke-opacity=".45" stroke-width="1.2"/>')
    b += (f'<text x="27" y="34.5" text-anchor="middle" font-family="{MONO}" font-size="14" '
          f'font-weight="700" letter-spacing="1" fill="{accent}">{num}</text>')
    b += (f'<text x="68" y="35" font-family="{MONO}" font-size="17" font-weight="700" '
          f'letter-spacing="3.2" fill="{FG}">{title}</text>')

    tx = 68 + tw(title, 17) + 3.2 * len(title) + 22
    b += f'<rect x="{tx:.0f}" y="28.5" width="{W-tx-160:.0f}" height="1.6" rx="1" fill="url(#rule)"/>'
    b += (f'<text x="{W-1}" y="34" text-anchor="end" font-family="{MONO}" font-size="12" '
          f'fill="{CMT}">// {note}</text>')
    write(fname, svg(W, h, b))


# ══════════════════════════════════════════════════════════════════════════════
# 3. PRODUCT CARDS
# ══════════════════════════════════════════════════════════════════════════════
def product(fname, name, domain, tagline, lines, stack, status, status_color, accent):
    w, h = 418, 342
    b = frame(w, h, r=13)
    b += titlebar(w, domain, h=32, r=13)

    b += (f'<text x="24" y="70" font-family="{MONO}" font-size="21" font-weight="700" '
          f'letter-spacing="1.2" fill="{accent}" opacity=".35" filter="url(#soft)">{name}</text>')
    b += (f'<text x="24" y="70" font-family="{MONO}" font-size="21" font-weight="700" '
          f'letter-spacing="1.2" fill="{FG}">{name}</text>')
    b += (f'<text x="24" y="92" font-family="{MONO}" font-size="11.5" letter-spacing="1.5" '
          f'fill="{accent}">{tagline}</text>')
    b += f'<line x1="24" y1="106" x2="{w-24}" y2="106" stroke="{LINE}" stroke-width="1"/>'

    for i, ln in enumerate(lines):
        b += (f'<text x="24" y="{130+i*20}" font-family="{MONO}" font-size="12" fill="{FG}" '
              f'opacity=".78">{ln}</text>')

    sy = 130 + len(lines) * 20 + 10
    b += (f'<text x="24" y="{sy+10}" font-family="{MONO}" font-size="10" letter-spacing="2" '
          f'fill="{CMT}">STACK</text>')
    row1, _ = chiprow(24, sy + 20, stack[0], [accent], size=11)
    b += row1
    if len(stack) > 1:
        row2, _ = chiprow(24, sy + 20 + 30, stack[1], [accent], size=11)
        b += row2

    b += f'<line x1="24" y1="{h-44}" x2="{w-24}" y2="{h-44}" stroke="{LINE}" stroke-width="1" opacity=".7"/>'
    b += f'<circle cx="30" cy="{h-25}" r="4" fill="{status_color}" filter="url(#dot)"/>'
    b += (f'<text x="44" y="{h-21}" font-family="{MONO}" font-size="11" letter-spacing="1.4" '
          f'fill="{status_color}">{status}</text>')
    b += (f'<text x="{w-24}" y="{h-21}" text-anchor="end" font-family="{MONO}" font-size="11" '
          f'fill="{CMT}">&#8250; visit &#8594;</text>')
    write(fname, svg(w, h, b))


# ══════════════════════════════════════════════════════════════════════════════
# 4. ARSENAL
# ══════════════════════════════════════════════════════════════════════════════
def arsenal():
    rows = [
        ("LANGUAGES",      ["Python", "TypeScript", "JavaScript", "SQL"],                     PINK),
        ("AI / AUTOMATION",["Claude", "n8n", "Twilio", "Deepgram", "ElevenLabs"],             PURPLE),
        ("BACKEND",        ["FastAPI", "Fastify", "Supabase", "PostgreSQL", "Redis"],         GREEN),
        ("FRONTEND",       ["Next.js", "React", "Tailwind", "shadcn/ui"],                     CYAN),
        ("INFRA",          ["Docker", "Vercel", "Railway", "GitHub Actions"],                 ORANGE),
    ]
    h = 74 + (len(rows) - 1) * 54 + 44
    b = frame(W, h)
    b += titlebar(W, "~/noor/arsenal — cat stack.toml")

    for i, (label, items, color) in enumerate(rows):
        y = 74 + i * 54
        b += f'<rect x="32" y="{y-14}" width="3" height="28" rx="1.5" fill="{color}" opacity=".75"/>'
        b += (f'<text x="48" y="{y+4}" font-family="{MONO}" font-size="11" letter-spacing="1.8" '
              f'fill="{color}">{label}</text>')
        row, _ = chiprow(252, y - 13, items, [color], size=12)
        b += row
        if i < len(rows) - 1:
            b += (f'<line x1="32" y1="{y+27}" x2="{W-32}" y2="{y+27}" stroke="{LINE}" '
                  f'stroke-width="1" opacity=".55"/>')
    write("arsenal.svg", svg(W, h, b))


# ══════════════════════════════════════════════════════════════════════════════
# 5. PRINCIPLES SPOTLIGHT
# ══════════════════════════════════════════════════════════════════════════════
def principles():
    h = 166
    b = frame(W, h)
    b += f'<path d="M1 15 A14 14 0 0 1 15 1 H6 V{h-1} H15 A14 14 0 0 1 1 {h-15} Z" fill="{PURPLE}" opacity=".9"/>'
    b += f'<rect x="5" y="1" width="2" height="{h-2}" fill="{PURPLE}" opacity=".9"/>'
    b += (f'<text x="46" y="54" font-family="{MONO}" font-size="11.5" letter-spacing="2.4" '
          f'fill="{CMT}">// CORE AXIOM</text>')
    q = "Systems &#62; shortcuts. Always."
    b += (f'<text x="46" y="106" font-family="{MONO}" font-size="33" font-weight="700" '
          f'letter-spacing="0.5" fill="{PURPLE}" opacity=".35" filter="url(#soft)">{q}</text>')
    b += (f'<text x="46" y="106" font-family="{MONO}" font-size="33" font-weight="700" '
          f'letter-spacing="0.5" fill="{FG}">{q}</text>')
    b += (f'<text x="46" y="136" font-family="{MONO}" font-size="12" fill="{CMT}">'
          f'A thing that works once is a demo. A thing that works unattended is a product.</text>')
    write("principles.svg", svg(W, h, b))


# ══════════════════════════════════════════════════════════════════════════════
# 6. NOW PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
def now():
    h = 138
    nodes = [
        ("AUTOMETIQ",  "revenue engine",   PINK),
        ("SIXTYHOURS", "talent pipeline",  PURPLE),
        ("PK AI INFRA","the long game",    CYAN),
        ("CONTENT",    "compounding",      GREEN),
    ]
    b = frame(W, h)
    b += (f'<text x="32" y="36" font-family="{MONO}" font-size="11" letter-spacing="2.2" '
          f'fill="{CMT}">// CURRENT TRAJECTORY</text>')

    pad, gap = 32, 26
    bw = (W - pad * 2 - gap * (len(nodes) - 1)) / len(nodes)
    for i, (t, sub, c) in enumerate(nodes):
        x = pad + i * (bw + gap)
        b += (f'<rect x="{x:.1f}" y="60" width="{bw:.1f}" height="52" rx="10" fill="{c}" '
              f'fill-opacity=".08" stroke="{c}" stroke-opacity=".42" stroke-width="1.2"/>')
        b += (f'<text x="{x+bw/2:.1f}" y="83" text-anchor="middle" font-family="{MONO}" '
              f'font-size="12.5" font-weight="700" letter-spacing="1.2" fill="{c}">{t}</text>')
        b += (f'<text x="{x+bw/2:.1f}" y="100" text-anchor="middle" font-family="{MONO}" '
              f'font-size="10.5" fill="{CMT}">{sub}</text>')
        if i < len(nodes) - 1:
            ax = x + bw + gap / 2
            b += (f'<path d="M{ax-7:.1f} 86 H{ax+4:.1f} M{ax:.1f} 82 l4 4 l-4 4" fill="none" '
                  f'stroke="{LINE}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    write("now.svg", svg(W, h, b))


# ══════════════════════════════════════════════════════════════════════════════
# 7. PROFILE / FOOTER CARD
# ══════════════════════════════════════════════════════════════════════════════
def profilecard():
    h = 206
    b = frame(W, h)
    b += titlebar(W, "~/noor — cat profile.json")

    rows = [
        ("LOCATION", "Faisalabad, Pakistan", FG),
        ("STATUS",   "Building",             GREEN),
        ("FOCUS",    "AI  ×  SMEs  ×  Automation", CYAN),
        ("OPEN TO",  "Collaborations  ·  Consulting  ·  Speaking", PINK),
    ]
    for i, (k, v, c) in enumerate(rows):
        y = 76 + i * 30
        b += (f'<text x="40" y="{y}" font-family="{MONO}" font-size="11" letter-spacing="2" '
              f'fill="{CMT}">{k}</text>')
        b += f'<text x="176" y="{y}" font-family="{MONO}" font-size="13" fill="{c}">{v}</text>'

    b += (f'<text x="{W-40}" y="{h-24}" text-anchor="end" font-family="{MONO}" font-size="11.5" '
          f'fill="{CMT}">&#8250; thanks for reading the source</text>')
    write("profile-card.svg", svg(W, h, b))


# ══════════════════════════════════════════════════════════════════════════════
# 8. FOOTER LINK BUTTONS
# ══════════════════════════════════════════════════════════════════════════════
def linkbtn(fname, label, color):
    w, h = 204, 46
    b = (f'<rect x="1.5" y="1.5" width="{w-3}" height="{h-3}" rx="10" fill="{PANEL}"/>'
         f'<rect x="1.5" y="1.5" width="{w-3}" height="{h-3}" rx="10" fill="url(#grid)"/>'
         f'<rect x="1.5" y="1.5" width="{w-3}" height="{h-3}" rx="10" fill="none" '
         f'stroke="{color}" stroke-opacity=".45" stroke-width="1.5"/>')
    b += f'<circle cx="24" cy="{h/2}" r="4" fill="{color}" filter="url(#dot)"/>'
    b += (f'<text x="42" y="{h/2+4.5}" font-family="{MONO}" font-size="12.5" letter-spacing="1.8" '
          f'fill="{color}">{label}</text>')
    b += (f'<text x="{w-18}" y="{h/2+4.5}" text-anchor="end" font-family="{MONO}" font-size="12.5" '
          f'fill="{CMT}">&#8594;</text>')
    write(fname, svg(w, h, b))


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    hero()
    section("01", "SYSTEMS",    "things that run without me", PINK,   "s01-systems.svg")
    section("02", "ARSENAL",    "tools, not trophies",        PURPLE, "s02-arsenal.svg")
    section("03", "ACTIVITY",   "the receipts",               CYAN,   "s03-activity.svg")
    section("04", "BUILT",      "shipped, not screenshotted", GREEN,  "s04-built.svg")
    section("05", "PRINCIPLES", "how I make decisions",       ORANGE, "s05-principles.svg")
    section("06", "NOW",        "what has my attention",      YELLOW, "s06-now.svg")

    product("card-sixtyhours.svg", "SIXTYHOURS", "sixtyhours.tech",
            "ENGINEERING TALENT, BUILT FROM SCRATCH",
            ["An 8-week, build-it-yourself program",
             "across ML/AI and Software Dev tracks.",
             "Students write the algorithms, not",
             "just the imports."],
            [["Next.js", "FastAPI", "Supabase"], ["Slack API", "Claude"]],
            "COHORT LIVE", GREEN, PINK)

    product("card-autometiq.svg", "AUTOMETIQ", "autometiq.com",
            "AI OPERATIONS FOR PAKISTANI SMES",
            ["Voice agents, workflow automation and",
             "internal tooling for businesses that",
             "never had an engineering team to",
             "begin with."],
            [["n8n", "Twilio", "Deepgram"], ["ElevenLabs", "Claude", "Redis"]],
            "SHIPPING", CYAN, CYAN)

    arsenal()
    principles()
    now()
    profilecard()

    linkbtn("link-autometiq.svg",  "AUTOMETIQ",  CYAN)
    linkbtn("link-sixtyhours.svg", "SIXTYHOURS", PINK)
    linkbtn("link-email.svg",      "EMAIL",      PURPLE)
    linkbtn("link-linkedin.svg",   "LINKEDIN",   GREEN)
    print("\ndone.")
