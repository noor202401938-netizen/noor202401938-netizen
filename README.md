<!--
═══════════════════════════════════════════════════════════════════════════════
  NOOR FATIMA — GITHUB PROFILE README

  SINGLE IMAGE. The whole profile is one SVG. Not a stack of cards, not three
  slabs with page background showing between them — one continuous surface, so
  there are no seams and nothing to misalign.

    assets/profile.svg   hero · 01 SYSTEMS · 02 ARSENAL · 03 ACTIVITY
                         04 BUILT · 05 PRINCIPLES · 06 NOW · profile.json
    assets/link-*.svg    footer buttons, separate ONLY so the links are clickable

  REGENERATING
    python3 stats.py     fetches live GitHub data -> stats.json  (needs a token)
    python3 build.py     redraws assets/profile.svg from stats.json

  build.py is the renderer; stats.py is the data collector. Never hand-edit an
  SVG — the next build overwrites it.

  STATS ARE SELF-HOSTED. .github/workflows/stats.yml runs daily, pulls real
  numbers from the GitHub GraphQL API with the workflow's built-in GITHUB_TOKEN,
  and commits stats.json + profile.svg. No third-party widget service is
  involved, so nothing external can break this page. Until the first run, the
  03 ACTIVITY section shows a short "awaiting first workflow run" note instead
  of empty tiles. A failed fetch leaves the previous numbers in place.

  CRYPT palette (gothic — blood & bone)
    void #0b0b0e · sepulchre #0e0e13 · crypt #14141a · mortar #332a35
    bone #e8e3d9 · ash #7f7480
    blood #d94a5f · blood-deep #9b1b30 · candle #c9a227 · tallow #d9b64a
    nightshade #a487bd · verdigris #6faa96 · moss #93ae72

  Chart series use a SEPARATE, colour-vision-validated order — see build.py.

  The ?v=N query is a cache-buster. GitHub's image proxy caches by URL, so BUMP
  N whenever the stale image keeps showing.
═══════════════════════════════════════════════════════════════════════════════
-->

<p><img src="assets/profile.svg?v=8" width="100%" alt="Noor Fatima — Software Engineer, Founder, Builder. Building AI-first systems for Pakistani SMEs. 01 SYSTEMS: SixtyHours, an 8-week build-it-yourself engineering program; Autometiq, AI operations for Pakistani SMEs. 02 ARSENAL: Python, TypeScript, JavaScript, SQL; Claude, n8n, Twilio, Deepgram, ElevenLabs; FastAPI, Fastify, Supabase, PostgreSQL, Redis; Next.js, React, Tailwind, shadcn/ui; Docker, Vercel, Railway, GitHub Actions. 03 ACTIVITY: contributions, public repos, stars, day streak, a 91-day contribution chart and language mix. 04 BUILT: voice-agent-core, n8n-sme-workflows, sixtyhours-platform, retrieval-lab. 05 PRINCIPLES: Systems beat shortcuts, always. 06 NOW: Autometiq, SixtyHours, Pakistan-focused AI infrastructure, content. Faisalabad, Pakistan — open to collaborations, consulting and speaking."><a href="https://autometiq.com"><img src="assets/link-autometiq.svg?v=8" width="25%" alt="Autometiq"></a><a href="https://sixtyhours.tech"><img src="assets/link-sixtyhours.svg?v=8" width="25%" alt="SixtyHours"></a><a href="mailto:autometiq@gmail.com"><img src="assets/link-email.svg?v=8" width="25%" alt="Email"></a><a href="https://www.linkedin.com/in/YOUR-HANDLE"><img src="assets/link-linkedin.svg?v=8" width="25%" alt="LinkedIn"></a></p>
