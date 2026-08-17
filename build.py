#!/usr/bin/env python3
"""
Noor Fatima — GitHub profile assets.

SINGLE-IMAGE layout: the entire profile is ONE svg. Every section lives inside
one background separated by hairlines, so there are no seams and no page
background showing between pieces.

  profile.svg  hero · 01 SYSTEMS · 02 ARSENAL · 03 ACTIVITY
               04 BUILT · 05 PRINCIPLES · 06 NOW · profile.json
  link-*.svg   footer buttons, separate only so the links stay clickable

build.py is the RENDERER; stats.py is the data COLLECTOR. stats.py writes
stats.json, build.py reads it. If stats.json is absent, the activity section
renders a compact "awaiting first run" state rather than empty tiles.
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

# ── CRYPT palette — gothic (blood & bone) ─────────────────────────────────────
# Swap this block to retheme everything. Every text-bearing accent clears
# 4.2:1 contrast against CRYPT (#14141a).
VOID       = "#0b0b0e"   # outermost stone
SEPULCHRE  = "#0e0e13"   # title bar
CRYPT      = "#14141a"   # the slab itself
MORTAR     = "#332a35"   # hairlines, borders, grid
BONE       = "#e8e3d9"   # primary text
ASH        = "#7f7480"   # comments, secondary text

BLOOD      = "#d94a5f"   # primary accent
BLOOD_DEEP = "#9b1b30"   # fills, glows, the red title-bar light
CANDLE     = "#c9a227"   # gold
TALLOW     = "#d9b64a"   # pale gold
NIGHTSHADE = "#a487bd"   # muted violet
VERDIGRIS  = "#6faa96"   # aged copper
MOSS       = "#93ae72"   # grave moss

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,Liberation Mono,monospace"

W    = 860      # slab width
PAD  = 40       # inner horizontal padding
CW   = W - PAD * 2
ADV  = 0.6      # monospace advance ratio


# ── primitives ────────────────────────────────────────────────────────────────
def tw(s, size):
    return len(s) * size * ADV


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def txt(x, y, s, col, size=12.5, weight=None, ls=None, anchor=None, op=None):
    a = f'<text x="{x:.1f}" y="{y:.1f}" xml:space="preserve" font-family="{MONO}" font-size="{size}" fill="{col}"'
    if weight: a += f' font-weight="{weight}"'
    if ls is not None: a += f' letter-spacing="{ls}"'
    if anchor: a += f' text-anchor="{anchor}"'
    if op is not None: a += f' opacity="{op}"'
    return a + f'>{esc(s)}</text>'


def defs(h):
    return f"""<defs>
    <pattern id="grid" width="26" height="26" patternUnits="userSpaceOnUse">
      <path d="M26 0H0V26" fill="none" stroke="{MORTAR}" stroke-width="1" opacity=".2"/>
    </pattern>
    <radialGradient id="glowA" cx="8%" cy="0%" r="55%">
      <stop offset="0%" stop-color="{BLOOD_DEEP}" stop-opacity=".26"/>
      <stop offset="100%" stop-color="{BLOOD_DEEP}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowB" cx="96%" cy="100%" r="45%">
      <stop offset="0%" stop-color="{CANDLE}" stop-opacity=".10"/>
      <stop offset="100%" stop-color="{CANDLE}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{BLOOD}" stop-opacity=".9"/>
      <stop offset="50%" stop-color="{NIGHTSHADE}" stop-opacity=".3"/>
      <stop offset="100%" stop-color="{CANDLE}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="hair" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{MORTAR}" stop-opacity="0"/>
      <stop offset="14%" stop-color="{MORTAR}" stop-opacity=".95"/>
      <stop offset="86%" stop-color="{MORTAR}" stop-opacity=".95"/>
      <stop offset="100%" stop-color="{MORTAR}" stop-opacity="0"/>
    </linearGradient>
    <filter id="soft" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="7" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="dot" x="-160%" y="-160%" width="420%" height="420%">
      <feGaussianBlur stdDeviation="2.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>"""


def slab_ground(h, r=16):
    """The single continuous background. Top corners rounded, bottom left SQUARE so
    the clickable link bar butts flush against it with no page background between."""
    shape = f"M1 {r} A{r} {r} 0 0 1 {1+r} 1 H{W-1-r} A{r} {r} 0 0 1 {W-1} {r} V{h} H1 Z"
    s = f'<path d="{shape}" fill="{CRYPT}"/>'
    s += f'<path d="{shape}" fill="url(#grid)"/>'
    s += f'<path d="{shape}" fill="url(#glowA)"/>'
    s += f'<path d="{shape}" fill="url(#glowB)"/>'
    s += f'<path d="{shape}" fill="none" stroke="{MORTAR}" stroke-width="1.5"/>'
    return s


def titlebar(label, h=38, r=16):
    return (f'<path d="M1 {r} A{r} {r} 0 0 1 {1+r} 1 H{W-1-r} A{r} {r} 0 0 1 {W-1} {r} V{h} H1 Z" fill="{SEPULCHRE}"/>'
            f'<line x1="1" y1="{h}" x2="{W-1}" y2="{h}" stroke="{MORTAR}" stroke-width="1.5"/>'
            f'<circle cx="24" cy="{h/2}" r="5.5" fill="{BLOOD_DEEP}"/>'
            f'<circle cx="44" cy="{h/2}" r="5.5" fill="{TALLOW}" opacity=".85"/>'
            f'<circle cx="64" cy="{h/2}" r="5.5" fill="{MOSS}" opacity=".85"/>'
            + txt(W/2, h/2 + 4, label, ASH, 12, ls=1, anchor="middle"))


def hairline(y):
    return f'<rect x="{PAD}" y="{y}" width="{CW}" height="1" fill="url(#hair)"/>'


def sec(num, title, note, accent, y):
    """Inline section marker — a label in the flow, NOT a box of its own."""
    s = (f'<rect x="{PAD}" y="{y-17}" width="42" height="26" rx="7" fill="{accent}" fill-opacity=".14" '
         f'stroke="{accent}" stroke-opacity=".45" stroke-width="1.1"/>')
    s += txt(PAD + 21, y + 1, num, accent, 13, weight=700, ls=1, anchor="middle")
    s += txt(PAD + 58, y + 1.5, title, BONE, 16.5, weight=700, ls=3.2)
    tx = PAD + 58 + tw(title, 16.5) + 3.2 * len(title) + 20
    s += f'<rect x="{tx:.0f}" y="{y-4.5}" width="{W-PAD-tx-tw(note,12)-26:.0f}" height="1.5" rx="1" fill="url(#rule)"/>'
    s += txt(W - PAD, y + 1, f"// {note}", ASH, 12, anchor="end")
    return s


def chip(x, y, text, color, size=12, ph=9, h=26):
    w = tw(text, size) + ph * 2
    return (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{color}" '
            f'fill-opacity=".10" stroke="{color}" stroke-opacity=".38" stroke-width="1"/>'
            + txt(x + ph, y + h / 2 + 4.2, text, color, size), w)


def chiprow(x, y, items, color, size=12, gap=9):
    out, cx = "", x
    for it in items:
        g, w = chip(cx, y, it, color, size=size)
        out += g
        cx += w + gap
    return out


def vampire(x, y, s=1.0):
    """Engraving-style vampire in a 100 x 124 local box."""
    g = f'<g transform="translate({x},{y}) scale({s})">'
    g += f'<ellipse cx="50" cy="66" rx="46" ry="54" fill="{BLOOD_DEEP}" opacity=".14" filter="url(#soft)"/>'
    g += (f'<path d="M37 59 C26 51 19 35 16 11 C26 29 35 45 42 56 Z" fill="{BLOOD_DEEP}"/>'
          f'<path d="M63 59 C74 51 81 35 84 11 C74 29 65 45 58 56 Z" fill="{BLOOD_DEEP}"/>')
    g += (f'<path d="M50 57 C31 57 23 66 19 80 L9 118 Q20 110 30 118 Q40 110 50 118 '
          f'Q60 110 70 118 Q80 110 91 118 L81 80 C77 66 69 57 50 57 Z" '
          f'fill="{VOID}" stroke="{BLOOD_DEEP}" stroke-width="1.4" stroke-opacity=".8"/>')
    g += f'<path d="M41 56 L50 63 L59 56 L62 84 L38 84 Z" fill="#221d24"/>'
    g += f'<path d="M50 62 L54.5 70 L50 78 L45.5 70 Z" fill="{BLOOD}"/>'
    g += f'<ellipse cx="50" cy="40" rx="13.6" ry="16.4" fill="#ded8ce"/>'
    g += (f'<path d="M50 22.6 C60 22.6 64.2 30 64.2 40.5 C64.2 33.2 60.4 29.2 56.6 29.2 L50 37.6 '
          f'L43.4 29.2 C39.6 29.2 35.8 33.2 35.8 40.5 C35.8 30 40 22.6 50 22.6 Z" fill="{VOID}"/>')
    g += (f'<path d="M41.6 37.8 L47.4 40.2 L47 41.5 L41.4 39.3 Z" fill="{VOID}" opacity=".55"/>'
          f'<path d="M58.4 37.8 L52.6 40.2 L53 41.5 L58.6 39.3 Z" fill="{VOID}" opacity=".55"/>')
    g += (f'<circle cx="44.6" cy="43.2" r="1.6" fill="{BLOOD}"/>'
          f'<circle cx="55.4" cy="43.2" r="1.6" fill="{BLOOD}"/>')
    g += (f'<path d="M45.4 50 Q50 51.4 54.6 50" fill="none" stroke="{VOID}" stroke-width="1.1" '
          f'stroke-linecap="round" opacity=".8"/>')
    g += (f'<path d="M47.1 50.6 L48.6 50.7 L47.9 55.2 Z" fill="#f2eee7"/>'
          f'<path d="M51.4 50.7 L52.9 50.6 L52.1 55.2 Z" fill="#f2eee7"/>')
    return g + "</g>"


def svg(h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
            f'viewBox="0 0 {W} {h}" fill="none" role="img">\n  {defs(h)}\n  {body}\n</svg>\n')


def write(name, content):
    # encoding is explicit: Windows defaults to cp1252, which cannot encode the
    # arrows/dashes used here and would silently mis-encode the rest.
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  assets/{name}")


# ── 03 ACTIVITY: charts ───────────────────────────────────────────────────────
# Categorical order is FIXED and validated for colour-vision deficiency:
#   passes lightness band, chroma floor, CVD separation, normal-vision floor and
#   contrast against the dark surface. Do not reorder or extend these by eye —
#   the UI accents FAIL the check (verdigris/moss are ΔE 6.4 apart).
SERIES = ["#d94a5f", "#9b6fc4", "#009b80", "#b8871a"]


def tile(x, y, w, value, label, accent):
    b = f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="76" rx="11" fill="{VOID}" fill-opacity=".45"/>'
    b += (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="76" rx="11" fill="none" '
          f'stroke="{MORTAR}" stroke-width="1"/>')
    b += f'<rect x="{x+14:.1f}" y="{y+16}" width="3" height="20" rx="1.5" fill="{accent}" opacity=".9"/>'
    b += txt(x + 26, y + 40, value, BONE, 27, weight=700)
    b += txt(x + 26, y + 60, label, ASH, 10, ls=1.8)
    return b


def area_chart(x, y, w, h, series):
    """Single series → no legend; the title names it. Peak is direct-labelled."""
    vals = [c for _, c in series]
    hi = max(vals)
    scale = hi or 1
    step = w / max(len(vals) - 1, 1)

    b = txt(x, y - 22, "CONTRIBUTION SIGNAL — LAST 91 DAYS", ASH, 10.5, ls=1.8)
    for f in (0.5, 1.0):
        gy = y + h - h * f
        b += (f'<line x1="{x}" y1="{gy:.1f}" x2="{x+w}" y2="{gy:.1f}" stroke="{MORTAR}" '
              f'stroke-width="1" opacity=".55" stroke-dasharray="3 5"/>')
    b += txt(x + w, y - 4, str(hi), ASH, 10, anchor="end")

    pts = [(x + i * step, y + h - (v / scale) * h) for i, v in enumerate(vals)]
    d = " ".join(f"{'M' if i == 0 else 'L'}{px:.1f} {py:.1f}" for i, (px, py) in enumerate(pts))
    b += f'<path d="{d} L{x+w:.1f} {y+h} L{x} {y+h} Z" fill="{SERIES[0]}" fill-opacity=".16"/>'
    b += (f'<path d="{d}" fill="none" stroke="{SERIES[0]}" stroke-width="2" '
          f'stroke-linejoin="round" stroke-linecap="round"/>')
    b += f'<line x1="{x}" y1="{y+h}" x2="{x+w}" y2="{y+h}" stroke="{MORTAR}" stroke-width="1"/>'

    if hi:
        pi = vals.index(hi)
        px, py = pts[pi]
        b += (f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{SERIES[0]}" '
              f'stroke="{CRYPT}" stroke-width="2"/>')
        lbl = f"peak {hi} · {series[pi][0]}"
        anchor = "end" if px > x + w - 130 else "start"
        ly = py + 18 if py - 12 < y else py - 11   # flip below when hugging the top
        b += txt(px + (-9 if anchor == "end" else 9), ly, lbl, BONE, 10.5, anchor=anchor)

    b += txt(x, y + h + 15, series[0][0], ASH, 10)
    b += txt(x + w, y + h + 15, series[-1][0], ASH, 10, anchor="end")
    return b


def lang_bars(x, y, w, langs):
    b = txt(x, y, "LANGUAGE MIX — BY BYTES ACROSS PUBLIC REPOS", ASH, 10.5, ls=1.8)
    labw, valw = 140, 54
    barw = w - labw - valw
    hi = max((p for _, p in langs), default=1)
    for i, (name, pct) in enumerate(langs):
        ly = y + 26 + i * 26
        col = ASH if name == "Other" else SERIES[i % len(SERIES)]
        b += txt(x, ly + 9, name[:20], BONE, 12)      # text token, never the series colour
        b += f'<rect x="{x+labw}" y="{ly}" width="{barw:.1f}" height="12" rx="6" fill="{MORTAR}" fill-opacity=".45"/>'
        b += f'<rect x="{x+labw}" y="{ly}" width="{max(barw*(pct/hi),8):.1f}" height="12" rx="6" fill="{col}"/>'
        b += txt(x + w, ly + 9, f"{pct:.1f}%", ASH, 11, anchor="end")
    return b


def load_stats():
    try:
        with open(os.path.join(os.path.dirname(OUT), "stats.json"), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def activity(y):
    """Returns (body, height). Renders a compact empty state when there's no data."""
    body = sec("03", "ACTIVITY", "the receipts", VERDIGRIS, y)
    y0, y = y, y + 40
    s = load_stats()

    if not s:
        body += (f'<rect x="{PAD}" y="{y}" width="{CW}" height="64" rx="11" fill="{VOID}" '
                 f'fill-opacity=".45" stroke="{MORTAR}" stroke-width="1"/>')
        body += txt(PAD + 24, y + 27, "awaiting first workflow run", BONE, 13)
        body += txt(PAD + 24, y + 46,
                    "Actions ▸ profile stats ▸ Run workflow — then this fills with live data",
                    ASH, 11)
        return body, y + 64 - y0

    gap, n = 20, 4
    tw_ = (CW - gap * (n - 1)) / n
    for i, (v, lab, c) in enumerate([
        (s["contributions"], "CONTRIBUTIONS · 12 MO", SERIES[0]),
        (s["repos"],         "PUBLIC REPOS",          SERIES[1]),
        (s["stars"],         "STARS EARNED",          SERIES[2]),
        (s["streak"],        "DAY STREAK",            SERIES[3])]):
        body += tile(PAD + i * (tw_ + gap), y, tw_, str(v), lab, c)
    y += 76 + 26
    body += hairline(y)
    y += 46
    body += area_chart(PAD, y, CW, 132, [(d, c) for d, c in s["series"]])
    y += 132 + 30
    body += hairline(y)
    y += 40
    body += lang_bars(PAD, y, CW, [(n_, p) for n_, p in s["langs"]])
    y += 26 + len(s["langs"]) * 26 + 14
    body += txt(PAD, y, f"longest streak {s['longest']} days · {s['followers']} followers", ASH, 11)
    body += txt(W - PAD, y, f"self-hosted · regenerated {s['stamp']}", ASH, 11, anchor="end")
    return body, y + 6 - y0


# ══════════════════════════════════════════════════════════════════════════════
# THE PROFILE — one continuous image
# ══════════════════════════════════════════════════════════════════════════════
def hero(y):
    b = txt(PAD, y + 40, "›", MOSS, 14) + txt(PAD + 18, y + 40, "whoami", VERDIGRIS, 14)
    b += txt(PAD, y + 100, "NOOR FATIMA", BLOOD, 46, weight=700, ls=2, op=".34").replace(
        "<text", '<text filter="url(#soft)"', 1)
    b += txt(PAD, y + 100, "NOOR FATIMA", BONE, 46, weight=700, ls=2)

    cx = PAD
    for i, (t, c) in enumerate([("SOFTWARE ENGINEER", BLOOD), ("FOUNDER", CANDLE), ("BUILDER", NIGHTSHADE)]):
        b += txt(cx, y + 130, t, c, 13, ls=2.4)
        cx += tw(t, 13) + 2.4 * len(t) + 10
        if i < 2:
            b += txt(cx, y + 130, "/", MORTAR, 13)
            cx += 20

    b += txt(PAD, y + 166, "Building AI-first systems for Pakistani SMEs.", BONE, 14.5, op=".85")
    c1, w1 = chip(PAD, y + 186, "SixtyHours.tech", BLOOD, size=12.5)
    c2, _ = chip(PAD + w1 + 10, y + 186, "Autometiq.com", VERDIGRIS, size=12.5)
    b += c1 + c2

    b += vampire(470, y + 34, 0.9)

    b += f'<line x1="600" y1="{y+16}" x2="600" y2="{y+216}" stroke="{MORTAR}" stroke-width="1" opacity=".8"/>'
    b += txt(632, y + 40, "› STATUS", ASH, 11, ls=2.2)
    for i, (t, c) in enumerate([("BUILDING", MOSS), ("SHIPPING", BLOOD), ("LEARNING", VERDIGRIS)]):
        yy = y + 72 + i * 30
        b += f'<circle cx="637" cy="{yy-4}" r="4.2" fill="{c}" filter="url(#dot)"/>'
        b += txt(654, yy, t, BONE, 13, ls=1.6, op=".92")
    b += f'<line x1="632" y1="{y+176}" x2="{W-PAD}" y2="{y+176}" stroke="{MORTAR}" stroke-width="1" opacity=".7"/>'
    b += txt(632, y + 202, "Faisalabad, PK — UTC+5", ASH, 11.5)
    return b, 234


def product_col(x, y, name, domain, tagline, lines, stack, status, status_col, accent):
    b = txt(x, y, name, accent, 21, weight=700, ls=1.2, op=".35").replace(
        "<text", '<text filter="url(#soft)"', 1)
    b += txt(x, y, name, BONE, 21, weight=700, ls=1.2)
    b += txt(x + tw(name, 21) + 1.2 * len(name) + 14, y, domain, ASH, 11.5)
    b += txt(x, y + 22, tagline, accent, 11.5, ls=1.5)
    for i, ln in enumerate(lines):
        b += txt(x, y + 52 + i * 20, ln, BONE, 12.5, op=".8")
    sy = y + 52 + len(lines) * 20 + 12
    b += txt(x, sy, "STACK", ASH, 10, ls=2)
    b += chiprow(x, sy + 10, stack[0], accent, size=11)
    if len(stack) > 1:
        b += chiprow(x, sy + 40, stack[1], accent, size=11)
    fy = sy + 82
    b += f'<circle cx="{x+5}" cy="{fy-4}" r="4" fill="{status_col}" filter="url(#dot)"/>'
    b += txt(x + 19, fy, status, status_col, 11, ls=1.4)
    return b, fy - y + 10


def part_a(y):
    body, hh = hero(y + 18)
    y += 18 + hh

    y += 26
    body += hairline(y)
    y += 40

    body += sec("01", "SYSTEMS", "things that run without me", BLOOD, y)
    y += 44

    colw = (CW - 52) / 2
    lx, rx = PAD, PAD + colw + 52
    a, ha = product_col(lx, y + 18, "SIXTYHOURS", "sixtyhours.tech",
                        "ENGINEERING TALENT, BUILT FROM SCRATCH",
                        ["An 8-week, build-it-yourself program across",
                         "ML/AI and Software Dev tracks. Students write",
                         "the algorithms, not just the imports."],
                        [["Next.js", "FastAPI", "Supabase"], ["Slack API", "Claude"]],
                        "COHORT LIVE", MOSS, BLOOD)
    c, hc = product_col(rx, y + 18, "AUTOMETIQ", "autometiq.com",
                        "AI OPERATIONS FOR PAKISTANI SMES",
                        ["Voice agents, workflow automation and internal",
                         "tooling for businesses that never had an",
                         "engineering team to begin with."],
                        [["n8n", "Twilio", "Deepgram"], ["ElevenLabs", "Claude", "Redis"]],
                        "SHIPPING", VERDIGRIS, VERDIGRIS)
    body += a + c
    colh = max(ha, hc)
    body += (f'<line x1="{PAD+colw+26}" y1="{y+6}" x2="{PAD+colw+26}" y2="{y+colh+18}" '
             f'stroke="{MORTAR}" stroke-width="1" opacity=".75"/>')
    y += 18 + colh

    y += 22
    body += hairline(y)
    y += 40

    body += sec("02", "ARSENAL", "tools, not trophies", NIGHTSHADE, y)
    y += 40

    rows = [
        ("LANGUAGES",       ["Python", "TypeScript", "JavaScript", "SQL"],              BLOOD),
        ("AI / AUTOMATION", ["Claude", "n8n", "Twilio", "Deepgram", "ElevenLabs"],      NIGHTSHADE),
        ("BACKEND",         ["FastAPI", "Fastify", "Supabase", "PostgreSQL", "Redis"],  MOSS),
        ("FRONTEND",        ["Next.js", "React", "Tailwind", "shadcn/ui"],              VERDIGRIS),
        ("INFRA",           ["Docker", "Vercel", "Railway", "GitHub Actions"],          CANDLE),
    ]
    for i, (label, items, col) in enumerate(rows):
        ry = y + 22 + i * 50
        body += f'<rect x="{PAD}" y="{ry-13}" width="3" height="26" rx="1.5" fill="{col}" opacity=".8"/>'
        body += txt(PAD + 16, ry + 4, label, col, 11, ls=1.8)
        body += chiprow(PAD + 212, ry - 13, items, col, size=12)
    y += 22 + len(rows) * 50

    return body, y


# ══════════════════════════════════════════════════════════════════════════════
# SLAB B — 04 BUILT · 05 PRINCIPLES · 06 NOW · profile.json
# ══════════════════════════════════════════════════════════════════════════════
def part_b(y):
    body = sec("04", "BUILT", "shipped, not screenshotted", MOSS, y)
    y += 42

    P = [("noor@github", MOSS), (" ~ ", ASH), ("$", BLOOD)]
    entries = [
        ("voice-agent-core/",    "telephony + STT + LLM + TTS loop, sub-second turn-taking"),
        ("n8n-sme-workflows/",   "reusable automation blueprints for non-technical teams"),
        ("sixtyhours-platform/", "cohort, submissions and mentor tooling"),
        ("retrieval-lab/",       "BM25 + FAISS from scratch, no LangChain"),
    ]
    lines = [P + [(" ls -1 built/", BONE)], []]
    for n, note in entries:
        lines.append([("  " + n.ljust(23), CANDLE), ("# " + note, ASH)])
    lines += [[], P + [("  # replace these with your real repos — one line, one truth", ASH)]]
    for i, segs in enumerate(lines):
        ly, lx = y + 12 + i * 20, float(PAD)
        for t, c in segs:
            if t.strip():
                body += txt(lx, ly, t, c, 12.5)
            lx += len(t) * 12.5 * ADV
    y += 12 + len(lines) * 20

    y += 20
    body += hairline(y)
    y += 40
    body += sec("05", "PRINCIPLES", "how I make decisions", CANDLE, y)
    y += 40

    q = "Systems > shortcuts. Always."
    body += f'<rect x="{PAD}" y="{y+4}" width="3" height="66" rx="1.5" fill="{BLOOD}" opacity=".9"/>'
    body += txt(PAD + 18, y + 20, "// CORE AXIOM", ASH, 11.5, ls=2.4)
    body += txt(PAD + 18, y + 56, q, CANDLE, 31, weight=700, op=".28").replace(
        "<text", '<text filter="url(#soft)"', 1)
    body += txt(PAD + 18, y + 56, q, BONE, 31, weight=700)
    body += txt(PAD + 18, y + 78, "A thing that works once is a demo. "
                                  "A thing that works unattended is a product.", ASH, 12)
    y += 104

    def kv(s):
        return [("  - ", BLOOD), (f'"{s}"', BONE)]
    yml = [
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
    for i, segs in enumerate(yml):
        ly, lx = y + i * 20, float(PAD)
        for t, c in segs:
            if t.strip():
                body += txt(lx, ly, t, c, 12.5)
            lx += len(t) * 12.5 * ADV
    y += len(yml) * 20

    y += 16
    body += hairline(y)
    y += 40
    body += sec("06", "NOW", "what has my attention", TALLOW, y)
    y += 36

    nodes = [("AUTOMETIQ", "revenue engine", BLOOD), ("SIXTYHOURS", "talent pipeline", CANDLE),
             ("PK AI INFRA", "the long game", NIGHTSHADE), ("CONTENT", "compounding", VERDIGRIS)]
    gap, n = 26, 4
    bw = (CW - gap * (n - 1)) / n
    for i, (t, sub, c) in enumerate(nodes):
        x = PAD + i * (bw + gap)
        body += (f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="52" rx="10" fill="{c}" '
                 f'fill-opacity=".08" stroke="{c}" stroke-opacity=".42" stroke-width="1.2"/>')
        body += txt(x + bw / 2, y + 23, t, c, 12.5, weight=700, ls=1.2, anchor="middle")
        body += txt(x + bw / 2, y + 40, sub, ASH, 10.5, anchor="middle")
        if i < n - 1:
            ax = x + bw + gap / 2
            body += (f'<path d="M{ax-7:.1f} {y+26} H{ax+4:.1f} M{ax:.1f} {y+22} l4 4 l-4 4" fill="none" '
                     f'stroke="{MORTAR}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    y += 76

    for i, (k, rest) in enumerate([
        ("Autometiq",         "voice agents and workflow automation in production for SME clients."),
        ("SixtyHours",        "running the current cohort across the ML/AI and Software Dev tracks."),
        ("PK AI infrastructure", "local-context tooling that doesn't assume a US-shaped business."),
        ("Content",           "writing up what actually works, so the next person skips a month."),
    ]):
        ly = y + i * 22
        body += f'<circle cx="{PAD+3}" cy="{ly-4}" r="2.6" fill="{BLOOD}" opacity=".8"/>'
        body += txt(PAD + 16, ly, k, BONE, 12.5, weight=700)
        body += txt(PAD + 16 + tw(k, 12.5) + 10, ly, "— " + rest, ASH, 12.5)
    y += 4 * 22

    y += 18
    body += hairline(y)
    y += 40

    for i, (k, v, c) in enumerate([
        ("LOCATION", "Faisalabad, Pakistan", BONE),
        ("STATUS",   "Building", MOSS),
        ("FOCUS",    "AI  ×  SMEs  ×  Automation", VERDIGRIS),
        ("OPEN TO",  "Collaborations  ·  Consulting  ·  Speaking", BLOOD),
    ]):
        ry = y + i * 28
        body += txt(PAD, ry, k, ASH, 11, ls=2)
        body += txt(PAD + 136, ry, v, c, 13)
    y += 4 * 28

    body += txt(PAD, y + 4, "CRYPT · #14141a — no falling bats, no snake on the graph.", ASH, 11.5)
    body += txt(W - PAD, y + 4, "› thanks for reading the source", ASH, 11.5, anchor="end")
    return body, y + 24


def profile():
    """Compose every section into ONE image — no seams, no page background."""
    y = 38
    a, y = part_a(y)

    y += 26
    a += hairline(y)
    y += 46
    act, ah = activity(y)
    y += ah

    y += 26
    a += hairline(y)
    y += 46
    b, y = part_b(y)

    write("profile.svg", svg(y, slab_ground(y) + titlebar("~/noor/profile — zsh") + a + act + b))


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER LINK BUTTONS — separate files only so the <a> links stay clickable
# ══════════════════════════════════════════════════════════════════════════════
def linkbtn(fname, label, color, bl=False, br=False):
    """One cell of the footer bar. 4 × 215 = 860 — exactly the profile width, so the
    row reads as the bottom edge of the image rather than four floating buttons.
    bl / br round the outer bottom corners only; every other edge is square."""
    global W
    keep, W = W, 215
    h, r = 52, 16
    d = f"M0 0 H{W}"
    d += f" V{h-r} A{r} {r} 0 0 1 {W-r} {h}" if br else f" V{h}"
    d += f" H{r} A{r} {r} 0 0 1 0 {h-r}" if bl else " H0"
    d += " Z"
    b = (f'<path d="{d}" fill="{CRYPT}"/><path d="{d}" fill="url(#grid)"/>'
         f'<path d="{d}" fill="url(#glowB)"/>'
         f'<path d="{d}" fill="none" stroke="{MORTAR}" stroke-width="1.5"/>'
         f'<rect x="0" y="0" width="{W}" height="2" fill="{color}" opacity=".5"/>'
         f'<circle cx="26" cy="{h/2+1}" r="4" fill="{color}" filter="url(#dot)"/>'
         + txt(44, h / 2 + 5.5, label, color, 12.5, ls=1.8)
         + txt(W - 20, h / 2 + 5.5, "→", ASH, 12.5, anchor="end"))
    write(fname, svg(h, b))
    W = keep


if __name__ == "__main__":
    profile()
    linkbtn("link-autometiq.svg",  "AUTOMETIQ",  VERDIGRIS,  bl=True)
    linkbtn("link-sixtyhours.svg", "SIXTYHOURS", BLOOD)
    linkbtn("link-email.svg",      "EMAIL",      CANDLE)
    linkbtn("link-linkedin.svg",   "LINKEDIN",   NIGHTSHADE, br=True)
    print("\ndone.")
