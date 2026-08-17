#!/usr/bin/env python3
"""
Collects live GitHub data into stats.json. It does NOT draw anything —
build.py is the renderer and reads this file.

Run by .github/workflows/stats.yml on a schedule, using the workflow's built-in
GITHUB_TOKEN (no personal access token required) to read PUBLIC data via the
GraphQL API. Nothing here depends on a third-party widget service.

  python3 stats.py     writes stats.json   (needs GITHUB_TOKEN)
  python3 build.py     redraws profile.svg from it

Without a token this exits without touching stats.json, so a failed fetch can
never blank out numbers that are already published.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date, datetime

USER = os.environ.get("GH_USER", "noor202401938-netizen")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
HERE = os.path.dirname(os.path.abspath(__file__))

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
        print("no GITHUB_TOKEN — leaving stats.json untouched", file=sys.stderr)
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
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"fetch failed: {e}", file=sys.stderr)
        return None
    if payload.get("errors"):
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
        c = days[i][1]
        if c > 0:
            cur += 1
        elif i == len(days) - 1:
            continue          # today not logged yet — doesn't break the streak
        else:
            break
    return cur, longest


def shape(user):
    cal = user["contributionsCollection"]["contributionCalendar"]
    days = sorted((datetime.strptime(d["date"], "%Y-%m-%d").date(), d["contributionCount"])
                  for w in cal["weeks"] for d in w["contributionDays"])
    days = [d for d in days if d[0] <= date.today()]

    langs = {}
    for repo in user["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    ranked = sorted(langs.items(), key=lambda kv: -kv[1])
    total = sum(langs.values()) or 1
    top = [[n, round(s / total * 100, 1)] for n, s in ranked[:4]]
    rest = sum(s for _, s in ranked[4:]) / total * 100
    if rest > 0.5:
        top.append(["Other", round(rest, 1)])
    if not top:
        top = [["no public code yet", 100.0]]

    cur, longest = streaks(days)
    return {
        "contributions": cal["totalContributions"],
        "repos": user["repositories"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in user["repositories"]["nodes"]),
        "followers": user["followers"]["totalCount"],
        "streak": cur,
        "longest": longest,
        "series": [[d.strftime("%d %b"), c] for d, c in days[-91:]],
        "langs": top,
        "stamp": date.today().strftime("%d %b %Y"),
    }


def main():
    user = fetch()
    if user is None:
        sys.exit(0)          # soft-fail: never clobber good data with a bad run
    with open(os.path.join(HERE, "stats.json"), "w") as f:
        json.dump(shape(user), f, indent=1)
    print("wrote stats.json")


if __name__ == "__main__":
    main()
