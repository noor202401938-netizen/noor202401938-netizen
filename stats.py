#!/usr/bin/env python3
"""
Generates assets/stats.svg — the 03 / ACTIVITY section — from live GitHub data.

Run by .github/workflows/stats.yml on a schedule. Uses the workflow's built-in
GITHUB_TOKEN (no personal access token required) to read PUBLIC data about the
user via the GraphQL API. Nothing here depends on a third-party widget service.

Local dry run:   GITHUB_TOKEN=ghp_xxx GH_USER=noor202401938-netizen python3 stats.py
No token        -> renders a "pending" placeholder rather than failing the build.

Chart decisions follow the dataviz method:
  · stat tiles for single headline numbers (not a chart)
  · one area chart for change-over-time, single series so no legend is needed
  · horizontal bars for magnitude, 5th+ languages folded into "Other"
  · categorical order is FIXED and validated for colour-vision deficiency:
      #d94a5f -> #9b6fc4 -> #009b80 -> #b8871a
    (passes lightness band, chroma floor, CVD separation, normal-vision floor
     and contrast against the dark surface — do not reorder or extend by eye)
"""
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta

import build as B  # palette + drawing primitives; build.py guards its __main__

USER = os.environ.get("GH_USER", "noor202401938-netizen")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

# Validated categorical order — see module docstring. Never cycle or reorder.
SERIES = ["#d94a5f", "#9b6fc4", "#009b80", "#b8871a"]
OTHER = B.ASH

QUERY = """
query($login:String!){
  user(login:$login){
    followers{ totalCount }
    contributionsCollection{
      contributionCalendar{
        totalContributions
        weeks{ contributionDays{ date contributionCount } }
      }
    }
    repositories(first:100, ownerAffiliations:OWNER, isFork:false,
                 orderBy:{field:STARGAZERS, direction:DESC}){
      totalCount
      nodes{
        stargazerCount
        languages(first:8, orderBy:{field:SIZE, direction:DESC}){
          edges{ size node{ name } }
        }
      }
    }
  }
}
"""


def fetch():
    if not TOKEN:
        return None
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}",
                 "Content-Type": "application/json",
                 "User-Agent": "noor-profile-stats"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            payload = json.load(r)
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"fetch failed: {e}", file=sys.stderr)
        return None
    if "errors" in payload:
        print(f"graphql errors: {payload['errors']}", file=sys.stderr)
        return None
    return payload["data"]["user"]


def streaks(days):
    """days: [(date, count)] ascending. Returns (current, longest)."""
    longest = run = 0
    for _, c in days:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    cur = 0
    for i in range(len(days) - 1, -1, -1):
        d, c = days[i]
        if c > 0:
            cur += 1
        elif i == len(days) - 1:
            continue          # today not logged yet — doesn't break the streak
        else:
            break
    return cur, longest


def shape(user):
    cal = user["contributionsCollection"]["contributionCalendar"]
    days = [(datetime.strptime(d["date"], "%Y-%m-%d").date(), d["contributionCount"])
            for w in cal["weeks"] for d in w["contributionDays"]]
    days.sort()
    days = [d for d in days if d[0] <= date.today()]

    langs = {}
    for repo in user["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    ranked = sorted(langs.items(), key=lambda kv: -kv[1])
    total = sum(langs.values()) or 1
    top = [(n, s / total * 100) for n, s in ranked[:4]]
    rest = sum(s for _, s in ranked[4:]) / total * 100
    if rest > 0.5:
        top.append(("Other", rest))

    cur, longest = streaks(days)
    return {
        "contributions": cal["totalContributions"],
        "repos": user["repositories"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in user["repositories"]["nodes"]),
        "followers": user["followers"]["totalCount"],
        "streak": cur,
        "longest": longest,
        "series": days[-91:],
        "langs": top,
    }


# ── drawing ───────────────────────────────────────────────────────────────────
def tile(x, y, w, value, label, accent):
    b = f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="76" rx="11" fill="{B.VOID}" fill-opacity=".45"/>'
    b += (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="76" rx="11" fill="none" '
          f'stroke="{B.MORTAR}" stroke-width="1"/>')
    b += f'<rect x="{x+14:.1f}" y="{y+16}" width="3" height="20" rx="1.5" fill="{accent}" opacity=".9"/>'
    b += B.txt(x + 26, y + 40, value, B.BONE, 27, weight=700)
    b += B.txt(x + 26, y + 60, label, B.ASH, 10, ls=1.8)
    return b


def area_chart(x, y, w, h, series):
    """Single series → no legend; the title names it. Peak is direct-labelled."""
    if not series:
        return ""
    vals = [c for _, c in series]
    hi = max(vals)
    scale = hi or 1          # all-zero series must not break indexing below
    n = len(vals)
    step = w / max(n - 1, 1)

    b = B.txt(x, y - 22, "CONTRIBUTION SIGNAL — LAST 91 DAYS", B.ASH, 10.5, ls=1.8)

    # recessive grid + a single reference label, not a full axis
    for f in (0.5, 1.0):
        gy = y + h - h * f
        b += (f'<line x1="{x}" y1="{gy:.1f}" x2="{x+w}" y2="{gy:.1f}" stroke="{B.MORTAR}" '
              f'stroke-width="1" opacity=".55" stroke-dasharray="3 5"/>')
    b += B.txt(x + w, y - 2, str(hi), B.ASH, 10, anchor="end")

    pts = [(x + i * step, y + h - (v / scale) * h) for i, v in enumerate(vals)]
    d = " ".join(f"{'M' if i == 0 else 'L'}{px:.1f} {py:.1f}" for i, (px, py) in enumerate(pts))
    b += (f'<path d="{d} L{x+w:.1f} {y+h} L{x} {y+h} Z" fill="{SERIES[0]}" fill-opacity=".16"/>')
    b += (f'<path d="{d}" fill="none" stroke="{SERIES[0]}" stroke-width="2" '
          f'stroke-linejoin="round" stroke-linecap="round"/>')
    b += f'<line x1="{x}" y1="{y+h}" x2="{x+w}" y2="{y+h}" stroke="{B.MORTAR}" stroke-width="1"/>'

    if hi:                                        # only label a peak that exists
        pi = vals.index(hi)
        px, py = pts[pi]
        b += (f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{SERIES[0]}" '
              f'stroke="{B.CRYPT}" stroke-width="2"/>')
        lbl = f"peak {hi} · {series[pi][0].strftime('%d %b')}"
        anchor = "end" if px > x + w - 130 else "start"
        # flip below the marker when the peak hugs the plot top, so the label
        # never collides with the chart title
        ly = py + 18 if py - 12 < y else py - 11
        b += B.txt(px + (-9 if anchor == "end" else 9), ly, lbl, B.BONE, 10.5, anchor=anchor)

    b += B.txt(x, y + h + 15, series[0][0].strftime("%d %b"), B.ASH, 10)
    b += B.txt(x + w, y + h + 15, series[-1][0].strftime("%d %b"), B.ASH, 10, anchor="end")
    return b


def lang_bars(x, y, w, langs):
    b = B.txt(x, y, "LANGUAGE MIX — BY BYTES ACROSS PUBLIC REPOS", B.ASH, 10.5, ls=1.8)
    labw, valw = 128, 52
    barw = w - labw - valw
    hi = max((p for _, p in langs), default=1)
    for i, (name, pct) in enumerate(langs):
        ly = y + 26 + i * 26
        col = OTHER if name == "Other" else SERIES[i % len(SERIES)]
        b += B.txt(x, ly + 9, name[:16], B.BONE, 12)          # text token, not series colour
        b += (f'<rect x="{x+labw}" y="{ly}" width="{barw:.1f}" height="12" rx="6" '
              f'fill="{B.MORTAR}" fill-opacity=".45"/>')
        bw = max(barw * (pct / hi), 8)
        b += f'<rect x="{x+labw}" y="{ly}" width="{bw:.1f}" height="12" rx="6" fill="{col}"/>'
        b += B.txt(x + w, ly + 9, f"{pct:.1f}%", B.ASH, 11, anchor="end")
    return b


def render(s, stamp):
    y = 46
    body = B.sec("03", "ACTIVITY", "the receipts", B.VERDIGRIS, y)
    y += 40

    gap, n = 20, 4
    tw_ = (B.CW - gap * (n - 1)) / n
    tiles = [(s["contributions"], "CONTRIBUTIONS · 12 MO", SERIES[0]),
             (s["repos"],         "PUBLIC REPOS",          SERIES[1]),
             (s["stars"],         "STARS EARNED",          SERIES[2]),
             (s["streak"],        "DAY STREAK",            SERIES[3])]
    for i, (v, lab, c) in enumerate(tiles):
        body += tile(B.PAD + i * (tw_ + gap), y, tw_, str(v), lab, c)
    y += 76

    y += 26
    body += B.hairline(y)
    y += 46

    body += area_chart(B.PAD, y, B.CW, 132, s["series"])
    y += 132 + 30

    body += B.hairline(y)
    y += 40

    body += lang_bars(B.PAD, y, B.CW, s["langs"])
    y += 26 + len(s["langs"]) * 26

    y += 14
    body += B.txt(B.PAD, y, f"longest streak {s['longest']} days · {s['followers']} followers",
                  B.ASH, 11)
    body += B.txt(B.W - B.PAD, y, f"self-hosted · regenerated {stamp}", B.ASH, 11, anchor="end")
    y += 26

    B.write("stats.svg", B.svg(y, B.slab_ground(y) + body))


PENDING = {"contributions": "—", "repos": "—", "stars": "—", "streak": "—",
           "longest": "—", "followers": "—", "series": [], "langs": []}


def main():
    user = fetch()
    if user is None:
        print("no data — writing placeholder (the workflow will fill it in)")
        base = date.today()
        s = dict(PENDING)
        s["series"] = [(base - timedelta(days=90 - i), 0) for i in range(91)]
        s["langs"] = [("awaiting first run", 100.0)]
        render(s, "pending")
        return
    render(shape(user), date.today().strftime("%d %b %Y"))


if __name__ == "__main__":
    main()
