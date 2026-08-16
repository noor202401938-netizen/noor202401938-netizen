#!/usr/bin/env python3
"""Generates the Dracula-themed SVG asset set for the GitHub profile README."""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

# ── CRYPT palette — gothic (blood & bone) ─────────────────────────────────────
# Swap this block to retheme everything. Contrast of every text-bearing accent
# against CRYPT (#14141a) is >= 4.2:1, so chips and labels stay readable.
VOID       = "#0b0b0e"   # outermost stone
SEPULCHRE  = "#0e0e13"   # title bars — deeper than the panel
CRYPT      = "#14141a"   # panel fill
MORTAR     = "#332a35"   # borders, rules, grid
BONE       = "#e8e3d9"   # primary text
ASH        = "#7f7480"   # comments, secondary text

BLOOD      = "#d94a5f"   # primary accent  — text-safe crimson
BLOOD_DEEP = "#9b1b30"   # fills, glows, the red title-bar light
CANDLE     = "#c9a227"   # gold highlight
TALLOW     = "#d9b64a"   # pale gold
NIGHTSHADE = "#a487bd"   # muted violet
VERDIGRIS  = "#6faa96"   # aged copper
MOSS       = "#93ae72"   # grave moss

# ── role aliases (the drawing code below speaks in these) ─────────────────────
BG      = VOID
DEEP    = SEPULCHRE
PANEL   = CRYPT
LINE    = MORTAR
FG      = BONE
CMT     = ASH
CYAN    = VERDIGRIS
GREEN   = MOSS
ORANGE  = CANDLE
PINK    = BLOOD
PURPLE  = NIGHTSHADE
RED     = BLOOD_DEEP
YELLOW  = TALLOW

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
    <radialGradient id="glowA" cx="10%" cy="0%" r="68%">
      <stop offset="0%" stop-color="{BLOOD_DEEP}" stop-opacity=".24"/>
      <stop offset="100%" stop-color="{BLOOD_DEEP}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowB" cx="94%" cy="100%" r="62%">
      <stop offset="0%" stop-color="{CANDLE}" stop-opacity=".11"/>
      <stop offset="100%" stop-color="{CANDLE}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{BLOOD}" stop-opacity=".9"/>
      <stop offset="50%" stop-color="{NIGHTSHADE}" stop-opacity=".3"/>
      <stop offset="100%" stop-color="{CANDLE}" stop-opacity="0"/>
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


def vampire(x, y, s=1.0):
    """Small engraving-style vampire: caped figure, high collar, blood eyes.
    Drawn in a 100 x 124 local box, then translated/scaled into place."""
    g = f'<g transform="translate({x},{y}) scale({s})">'

    # ambient blood haze behind the figure
    g += f'<ellipse cx="50" cy="66" rx="46" ry="54" fill="{BLOOD_DEEP}" opacity=".14" filter="url(#soft)"/>'

    # cape lining / high collar — the two sweeping points behind the head
    g += (f'<path d="M37 59 C26 51 19 35 16 11 C26 29 35 45 42 56 Z" fill="{BLOOD_DEEP}"/>'
          f'<path d="M63 59 C74 51 81 35 84 11 C74 29 65 45 58 56 Z" fill="{BLOOD_DEEP}"/>')

    # cape body, scalloped hem
    g += (f'<path d="M50 57 C31 57 23 66 19 80 L9 118 Q20 110 30 118 Q40 110 50 118 '
          f'Q60 110 70 118 Q80 110 91 118 L81 80 C77 66 69 57 50 57 Z" '
          f'fill="{VOID}" stroke="{BLOOD_DEEP}" stroke-width="1.4" stroke-opacity=".8"/>')

    # shirt front + blood cravat
    g += f'<path d="M41 56 L50 63 L59 56 L62 84 L38 84 Z" fill="#221d24"/>'
    g += f'<path d="M50 62 L54.5 70 L50 78 L45.5 70 Z" fill="{BLOOD}"/>'

    # head — pallid, not glowing
    g += f'<ellipse cx="50" cy="40" rx="13.6" ry="16.4" fill="#ded8ce"/>'
    # hair with widow's peak
    g += (f'<path d="M50 22.6 C60 22.6 64.2 30 64.2 40.5 C64.2 33.2 60.4 29.2 56.6 29.2 L50 37.6 '
          f'L43.4 29.2 C39.6 29.2 35.8 33.2 35.8 40.5 C35.8 30 40 22.6 50 22.6 Z" fill="{VOID}"/>')
    # sunken brow — this is what makes him sinister rather than cute
    g += (f'<path d="M41.6 37.8 L47.4 40.2 L47 41.5 L41.4 39.3 Z" fill="{VOID}" opacity=".55"/>'
          f'<path d="M58.4 37.8 L52.6 40.2 L53 41.5 L58.6 39.3 Z" fill="{VOID}" opacity=".55"/>')
    # eyes
    g += (f'<circle cx="44.6" cy="43.2" r="1.6" fill="{BLOOD}"/>'
          f'<circle cx="55.4" cy="43.2" r="1.6" fill="{BLOOD}"/>')
    # grim mouth + fangs
    g += (f'<path d="M45.4 50 Q50 51.4 54.6 50" fill="none" stroke="{VOID}" stroke-width="1.1" '
          f'stroke-linecap="round" opacity=".8"/>')
    g += (f'<path d="M47.1 50.6 L48.6 50.7 L47.9 55.2 Z" fill="#f2eee7"/>'
          f'<path d="M51.4 50.7 L52.9 50.6 L52.1 55.2 Z" fill="#f2eee7"/>')
    return g + "</g>"


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
          f'letter-spacing="2" fill="{BLOOD}" opacity=".34" filter="url(#soft)">NOOR FATIMA</text>')
    b += (f'<text x="{x}" y="146" font-family="{MONO}" font-size="46" font-weight="700" '
          f'letter-spacing="2" fill="{FG}">NOOR FATIMA</text>')

    # role line
    roles = [("SOFTWARE ENGINEER", BLOOD), ("FOUNDER", CANDLE), ("BUILDER", NIGHTSHADE)]
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
    lk, _ = chiprow(x, 232, ["SixtyHours.tech", "Autometiq.com"], [BLOOD, VERDIGRIS], size=12.5)
    b += lk

    # the resident vampire — sits in the gap between the text block and the status rail
    b += vampire(472, 86, 0.92)

    # status column (right)
    b += f'<line x1="596" y1="62" x2="596" y2="{h-30}" stroke="{LINE}" stroke-width="1" opacity=".7"/>'
    b += (f'<text x="628" y="86" font-family="{MONO}" font-size="11" letter-spacing="2.2" '
          f'fill="{CMT}">&#8250; STATUS</text>')
    for i, (t, c) in enumerate([("BUILDING", MOSS), ("SHIPPING", BLOOD), ("LEARNING", VERDIGRIS)]):
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
    # These carry their own dark ground — without it the bone text is invisible
    # on GitHub's LIGHT theme, which is the one place a transparent SVG breaks.
    b = frame(W, h, r=11)
    # number badge
    b += (f'<rect x="14" y="12" width="52" height="34" rx="8" fill="{accent}" fill-opacity=".14" '
          f'stroke="{accent}" stroke-opacity=".45" stroke-width="1.2"/>')
    b += (f'<text x="40" y="34.5" text-anchor="middle" font-family="{MONO}" font-size="14" '
          f'font-weight="700" letter-spacing="1" fill="{accent}">{num}</text>')
    b += (f'<text x="82" y="35" font-family="{MONO}" font-size="17" font-weight="700" '
          f'letter-spacing="3.2" fill="{FG}">{title}</text>')

    tx = 82 + tw(title, 17) + 3.2 * len(title) + 22
    b += f'<rect x="{tx:.0f}" y="28.5" width="{W-tx-175:.0f}" height="1.6" rx="1" fill="url(#rule)"/>'
    b += (f'<text x="{W-18}" y="34" text-anchor="end" font-family="{MONO}" font-size="12" '
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
    b += f'<path d="M1 15 A14 14 0 0 1 15 1 H6 V{h-1} H15 A14 14 0 0 1 1 {h-15} Z" fill="{BLOOD}" opacity=".95"/>'
    b += f'<rect x="5" y="1" width="2" height="{h-2}" fill="{BLOOD}" opacity=".95"/>'
    b += (f'<text x="46" y="54" font-family="{MONO}" font-size="11.5" letter-spacing="2.4" '
          f'fill="{CMT}">// CORE AXIOM</text>')
    q = "Systems &#62; shortcuts. Always."
    b += (f'<text x="46" y="106" font-family="{MONO}" font-size="33" font-weight="700" '
          f'letter-spacing="0.5" fill="{CANDLE}" opacity=".28" filter="url(#soft)">{q}</text>')
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
        ("AUTOMETIQ",  "revenue engine",   BLOOD),
        ("SIXTYHOURS", "talent pipeline",  CANDLE),
        ("PK AI INFRA","the long game",    NIGHTSHADE),
        ("CONTENT",    "compounding",      VERDIGRIS),
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
        ("STATUS",   "Building",             MOSS),
        ("FOCUS",    "AI  ×  SMEs  ×  Automation", VERDIGRIS),
        ("OPEN TO",  "Collaborations  ·  Consulting  ·  Speaking", BLOOD),
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
# 7b. CODE PANELS
# GitHub styles ``` fenced blocks with its own syntax theme, which fights the
# palette. These render the same content as SVG so the whole page is one surface.
# ══════════════════════════════════════════════════════════════════════════════
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def codepanel(fname, title, lines, fs=12.5, pad=26, lh=20):
    """lines: list of [(text, colour), ...] segment lists. [] renders a blank line."""
    h = 36 + pad + len(lines) * lh + pad - 6
    b = frame(W, h)
    b += titlebar(W, title)
    for i, segs in enumerate(lines):
        y = 36 + pad + fs + i * lh
        x = 32.0
        for text, col in segs:
            if text.strip():
                b += (f'<text x="{x:.1f}" y="{y:.1f}" xml:space="preserve" font-family="{MONO}" '
                      f'font-size="{fs}" fill="{col}">{esc(text)}</text>')
            x += len(text) * fs * ADV
    write(fname, svg(W, h, b))


def built_console():
    P = [("noor@github", MOSS), (" ~ ", ASH), ("$", BLOOD)]
    entries = [
        ("voice-agent-core/",    "telephony + STT + LLM + TTS loop, sub-second turn-taking"),
        ("n8n-sme-workflows/",   "reusable automation blueprints for non-technical teams"),
        ("sixtyhours-platform/", "cohort, submissions and mentor tooling"),
        ("retrieval-lab/",       "BM25 + FAISS from scratch, no LangChain"),
    ]
    lines = [P + [(" ls -1 built/", BONE)], []]
    for name, note in entries:
        lines.append([("  " + name.ljust(23), CANDLE), ("# " + note, ASH)])
    lines += [[], P + [("  # replace these with your real repos — one line, one truth", ASH)]]
    codepanel("built-console.svg", "~/noor — ls -1 built/", lines)


def principles_yml():
    def kv(s):
        return [("  - ", BLOOD), (f'"{s}"', BONE)]
    lines = [
        [("# ~/noor/principles.yml", ASH)], [],
        [("build:", BLOOD)],
        kv("Ship the ugly version that runs. Beauty is a refactor away; usage isn't."),
        kv("If it needs me awake to work, it isn't finished."),
        kv("Read the source before the tutorial."), [],
        [("teach:", CANDLE)],
        kv("Write the algorithm before importing it. Once. Then import forever."),
        kv("A student who can explain it out loud has actually learned it."), [],
        [("business:", VERDIGRIS)],
        kv("Pakistani SMEs don't need AI. They need their Tuesday back."),
        kv("Automate the boring thing first — trust is earned on small wins."),
    ]
    codepanel("principles-yml.svg", "~/noor — cat principles.yml", lines)


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
    built_console()
    principles_yml()

    linkbtn("link-autometiq.svg",  "AUTOMETIQ",  VERDIGRIS)
    linkbtn("link-sixtyhours.svg", "SIXTYHOURS", BLOOD)
    linkbtn("link-email.svg",      "EMAIL",      CANDLE)
    linkbtn("link-linkedin.svg",   "LINKEDIN",   NIGHTSHADE)
    print("\ndone.")
