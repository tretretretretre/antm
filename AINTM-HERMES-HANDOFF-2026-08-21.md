# AINTM Repository Audit, Product Direction, and Hermes Handoff

**Project:** A.I.'s Next Top Models (AINTM)  
**Workspace:** `/home/tre/dev/antm`  
**Snapshot date:** 2026-08-21, America/Toronto  
**Prepared for:** continuation in Hermes Agent  
**Inspection mode:** read-only investigation of existing code and runtime. No production source files were changed during the audit.

## 1. Executive summary

AINTM is a small Python-based social-content automation prototype, not a conventional web application. Its intended flow is:

1. Collect current AI stories from RSS and Hacker News.
2. Ask Claude CLI to select and script the best story.
3. Rotate among three AI presenter characters.
4. Request script approval in Telegram.
5. Generate voice, images, captions, and a vertical video.
6. Request final-video approval in Telegram.
7. Schedule the approved video through Postiz.

The repository contains real working pieces: Python scripts parse, the required local binaries are installed, the host runner is active, n8n responds, and a 31.5-second 1080x1920 test video was rendered on 2026-08-16. However, the end-to-end automation is not active. n8n has zero workflows imported or published; Postiz's backend is down because Temporal is not running; character paths and names are stale; the renderer cannot currently discover the presenter reference images; the configured logo and audio assets are absent; and no analytics feedback loop exists.

The recommended launch path is a **human-approved workflow**: automate research, scoring, scripting, rendering, and packaging; approve the script and final video through Telegram; upload manually during the experimental first week; add platform automation only after the content format is proven.

## 2. Product direction confirmed with the owner

### Business objective

Build an audience interested in AI development, model capabilities, practical tools, prompts, tips, and fast-moving AI news. The long-term business purpose is to sell the owner's completed SaaS applications to this audience.

### Initial platforms

- YouTube Shorts
- TikTok
- Instagram

The default media format is 9:16 portrait. Most production should use inexpensive or already-owned tools. Premium video generation is reserved for occasional special posts and must not be purchased automatically.

### Editorial lanes

1. **Short-form video:** discovery, breaking news, model releases, demonstrations, tips, and useful updates.
2. **Instagram carousels:** tested prompts, practical model-specific recipes, before/after results, and save-worthy reference material.
3. **Later repurposing:** platform-specific captions, threads, blog posts, or other formats after the core loop proves itself.

### Human approval

During experimentation, the owner approves both the script and the final video. Fully automatic publishing is deliberately deferred.

### Week-one rule

Week 1 is an experiment and baseline period. Do not over-optimize or introduce a weekly audit before usable performance data exists.

Starting in Week 2, perform a weekly Instagram audit. Extend the same audit process to other connected platforms when they have sufficient data.

### Benchmark creators

These creators are research inputs and topic signals, not production styles AINTM must imitate:

- Nate Herk — practical AI automation and business outcomes
- Chase AI — content research, automation, repurposing, and human-in-the-loop production
- Leon van Zyl — current AI coding, Claude Code, Codex, Cursor, agents, and SaaS tutorials

Their content may reveal topics, audience questions, useful source links, and high-performing framing. Their scripts must not be copied or minimally rewritten.

## 3. Character and brand decisions

### Canonical presenters

| Presenter | Specialty | Current asset folder | Current state |
|---|---|---|---|
| Siobhan | OpenAI, ChatGPT, and related tools | `assets/characters/girl1 - Siobhan` | 12 images exist; configuration still says Chavonne and points elsewhere |
| Gemma | Google, Gemini, and related tools | `assets/characters/girl2-Gemma` | 31 images exist; configuration still spells the name Jemma |
| Claudia | Anthropic, Claude, and Claude Code | `assets/characters/girl3-Claudia` | 7 images now exist; personality remains blank |

Use `Siobhan` operationally in filenames, configuration, and handles. `Siobhán` may be used selectively in display branding. Ensure TTS pronounces the name approximately “shuh-VAWN.”

### Presenter-assignment rule

Use a hybrid assignment:

- Default: strict Siobhan → Gemma → Claudia rotation.
- Major breaking story: the relevant specialist may override the rotation.
- A skipped presenter moves to the next day so exposure remains balanced.

### Existing brand files

- `assets/brand/brandheader.png` — 1813x1020 RGB
- `assets/brand/roundlogo4profilepic.png` — 1020x1020 RGB

The code expects `assets/brand/logo.png`, which does not exist. The existing profile logo is RGB rather than a transparent PNG.

### Missing production assets

- `assets/brand/logo.png`
- `assets/audio/intro.wav`
- `assets/audio/outro.wav`
- Music-bed files inside `assets/audio/beds/`

The audio directories exist, but no audio files were present at audit time.

## 4. Repository map

```text
/home/tre/dev/antm
├── DELIVERABLES.md                 Stale owner checklist
├── AINTM-HERMES-HANDOFF-2026-08-21.md
├── assets/
│   ├── brand/                      Existing header/profile artwork
│   ├── characters/                 Character config and reference images
│   └── audio/beds/                 Empty audio structure
├── compose/
│   ├── docker-compose.yml          n8n, Postiz, Redis, Postgres, Temporal
│   └── dynamicconfig/              Temporal dynamic config
├── config/
│   ├── .env                        Local secrets; mode 600
│   ├── aintm-runner.service        User systemd unit
│   └── sources.yml                 News-source configuration
├── docs/
│   └── TOOL-MENU.md                Earlier tool/cost notes
├── inbox/
│   └── hero-clips/                 Empty manual-ingest area
├── output/
│   ├── candidates_test.json        Test news candidates
│   ├── episode.json                Stale Nova/Aria test episode
│   ├── seen_urls.json              Deduplication ledger
│   ├── runner.log                  Old runner log
│   └── daily/2026-08-16/           One completed test render and intermediates
├── scripts/
│   ├── host_runner.py              HTTP bridge and stage allowlist
│   ├── ingest.py                   RSS/Hacker News ingestion
│   ├── rank_and_script.py          Claude ranking/scripting and rotation
│   ├── render_daily.py             TTS, images, captions, FFmpeg video
│   └── post_postiz.py              Postiz upload/scheduling client
├── workflows/
│   └── aintm_daily.json            n8n workflow export; not imported
└── agent-skills/                    Portable Hermes/Codex skills created with this handoff
```

## 5. File-by-file code behavior

### `scripts/host_runner.py` — 62 lines

Purpose: expose a fixed stage allowlist over HTTP so n8n in Docker can run host-side Python, Claude CLI, FFmpeg, and credentials.

Allowed stages:

- `ingest` → `scripts/ingest.py --out output/candidates.json`
- `script` → `scripts/rank_and_script.py --candidates output/candidates.json --out output/episode.json`
- `render` → `scripts/render_daily.py --episode output/episode.json --out output/today.mp4`
- `post` → `scripts/post_postiz.py --episode output/episode.json --video output/today.mp4`
- `episode` → reads `output/episode.json`

Positive properties:

- Arbitrary commands are not accepted.
- Each stage has a timeout.
- Only the tail of stdout/stderr is returned.
- The user service is enabled and active.

Problems:

- The module text says it listens on localhost, but the actual server binds `0.0.0.0:8484`. Confirm firewall exposure before relying on this bridge.
- Calls are synchronous; a long render occupies the single-threaded HTTP server.
- There is no authentication or request signature.
- There is no persisted job state, resumability, or structured error record.

### `scripts/ingest.py` — 152 lines

Implemented:

- RSS 2.0 and Atom parsing
- Ten configured RSS feeds
- Hacker News top-story lookup with AI keywords and minimum score
- 36-hour freshness filter
- URL-hash deduplication
- `output/seen_urls.json` ledger capped at 5,000 hashes

Configured but not implemented:

- arXiv categories
- YouTube transcript channels

Important defects/risks:

- A URL is written to the seen ledger during ingestion, before selection, approval, rendering, or publishing. A later failure can permanently suppress an unused story.
- The ranker receives only titles and short feed summaries; it does not retrieve and verify the full primary source.
- No source-health telemetry, retry policy, rate limiting, or cache exists.
- No YouTube view velocity, Reddit momentum, Google Trends, TikTok trend signal, creator outlier, or cross-source topic clustering exists.

### `scripts/rank_and_script.py` — 110 lines

Implemented:

- Reads candidate JSON and `CHARACTERS.yml`.
- Rotates `girl1 → girl2 → girl3` and stores the current date/girl in `output/rotation.json`.
- Calls `claude -p --output-format text`.
- Requests a 30–45 second script, platform captions, headline, runner-up story, and image prompts.
- Adds presenter key, name, voice, and date to the episode JSON.

Important defects/risks:

- The approved hybrid rotation/specialist override is not implemented.
- It performs no full-source retrieval or independent fact verification.
- It has no JSON schema validation; malformed but parseable output can reach rendering.
- It creates only one final hook/script rather than variants for approval/testing.
- It has no content-type selection for carousel versus Reel/Short.
- It does not record why a topic won, what metrics supported it, or which hypothesis is being tested.
- It relies on a single Claude call and exits on failure.
- The current character configuration still uses old names and paths.

### `scripts/render_daily.py` — 238 lines

Implemented:

- edge-TTS speech with word boundaries at `+8%` rate
- ASS captions in three-word uppercase chunks
- Gemini image requests using `gemini-2.5-flash-image`
- Optional reference images for the anchor image
- Solid-color FFmpeg fallback cards
- Ken Burns-style motion, vertical 1080x1920 output, H.264/AAC
- Optional logo, intro, outro, and background-bed mixing

Important defects/risks:

- It looks for references at `assets/characters/<episode.girl>` such as `girl1`, but the actual directories are descriptive names. It ignores the configured `images` field. Therefore it currently loads zero presenter references.
- It hardcodes `assets/brand/logo.png`; the available brand files have different names.
- It uses only reference images for the first generated anchor shot, not for later shots.
- The generated test video showed a generic futuristic brunette presenter rather than Siobhan, Gemma, or Claudia.
- The test audio is 24 kHz mono; no voice-quality comparison has been run.
- There are no safe-zone checks for platform UI overlays.
- No content or technical quality gate checks legibility, black frames, silence, caption timing, clipping, or output duration.
- Bed selection uses Python's process-randomized `hash()`, so the same date can select a different bed in another process.

### `scripts/post_postiz.py` — 117 lines

Implemented:

- Postiz API requests
- Video upload
- Integration discovery and cache
- Platform captions
- Toronto-time scheduling for TikTok, Instagram, YouTube, X, Facebook, and LinkedIn

Current blockers:

- `POSTIZ_API_KEY` is not in `config/.env`.
- `config/postiz_channels.json` does not exist.
- No platforms are verified as connected.
- Postiz's backend is not running.
- Peak times are hardcoded guesses rather than learned from account insights.
- There is no retrieval of published URLs, status reconciliation, retry idempotency, or analytics feedback.

### `workflows/aintm_daily.json` — 182 lines

Designed nodes:

1. Daily 06:00 trigger
2. Ingest
3. Rank and script
4. Load episode
5. Telegram script approval
6. Conditional render
7. Read MP4
8. Send video preview
9. Telegram final approval
10. Conditional Postiz scheduling
11. Confirmation

Current state:

- Valid JSON.
- Exists only as an export file.
- n8n reports zero draft workflows and zero published workflows.
- Telegram nodes do not contain exported credential bindings.
- The workflow does not offer topic choices, hook choices, revisions, rejection reasons, retries, or resume semantics.

### `compose/docker-compose.yml` — 137 lines

Services:

- n8n
- Postiz
- Postiz PostgreSQL
- Redis
- Temporal
- Temporal PostgreSQL

Current state:

- n8n: running and reachable on `127.0.0.1:5678`; version 2.34.6 in logs.
- Postiz container: running on `127.0.0.1:5000`, but its backend failed to start.
- Postiz PostgreSQL: healthy.
- Redis: healthy.
- Temporal PostgreSQL: healthy.
- Temporal: container state `Created`, never started.
- Postiz backend error: cannot resolve/connect to `temporal:7233`.

Additional concerns:

- Postiz JWT/database secrets are hardcoded in a mode-664 Compose file.
- The Compose comment itself says newer Postiz expects Elasticsearch visibility and signup remains broken without a lighter path.
- Images use mutable `latest` tags for n8n and Postiz, preventing reproducible deployments.

### `assets/characters/CHARACTERS.yml` — 30 lines

Current parsed values:

- `girl1.name = Chavonne`
- `girl1.images = assets/characters/girl1-Siobhan` — nonexistent
- `girl2.name = Jemma`
- `girl2.images = assets/characters/girl2-Gemma` — exists
- `girl3.name = Claudia`
- `girl3.personality = ""`
- `girl3.images = assets/characters/girl3-Claudia` — exists
- `brand.logo = assets/brand/logo.png` — nonexistent

The final inline comment contains stray prose (`TheseThat when you come across T` in the music-bed comment). YAML still parses, but the file needs cleanup.

### `config/.env`

Present keys, values deliberately omitted:

- `GEMINI_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `AINTM_TG_CHAT_ID`

File mode is 600. Do not paste these secrets into agent chats or the handoff report.

### Existing output

`output/daily/2026-08-16/aintm_2026-08-16.mp4`:

- Duration: 31.533 seconds
- Resolution: 1080x1920
- Video: H.264, 30 fps
- Audio: AAC, 24 kHz, mono
- Size: 9,682,374 bytes
- Content: stale test script with presenter `Nova`, voice `en-US-AriaNeural`, and generic visuals

This proves the renderer can complete a vertical MP4, not that the current branded workflow works.

## 6. Runtime and development-state assessment

### Working

- Python 3.12.3
- FFmpeg/FFprobe 6.1.1
- Claude CLI at `/home/tre/.local/bin/claude`
- edge-TTS CLI at `/home/tre/.local/bin/edge-tts`
- Required Python modules observed: PyYAML, defusedxml, edge_tts
- All five Python source files parse successfully
- Core YAML and JSON files parse successfully
- `aintm-runner.service` is enabled and active
- `/run/episode` successfully returns the stale episode JSON

### Not working or not proven

- Scheduled daily n8n automation
- Telegram workflow credentials and approval loop
- Current character identity consistency
- Branded renderer output
- Postiz backend
- Any connected social platform
- Automatic publishing
- Carousel generation
- Trend scoring using engagement velocity
- Account analytics collection
- Weekly social-account audit
- Learning loop from performance to future content
- Seven consecutive daily runs

### Version-control problem

`git rev-parse --show-toplevel` returns `/home/tre`, not `/home/tre/dev/antm`. The enclosing home-directory repository has no commits and shows the user's entire home directory as untracked. AINTM has no usable project history. Do not stage or commit from the current Git root. Establish a correctly scoped repository before implementation commits.

### Testing/dependency problem

There is no test suite, `requirements.txt`, `pyproject.toml`, lockfile, schema directory, CI configuration, or documented bootstrap command.

## 7. Current research and content-strategy findings

**Current automation plan:** [`docs/AUTOMATION-WEEK-1-PLAN-2026-08-22.md`](docs/AUTOMATION-WEEK-1-PLAN-2026-08-22.md). It records the four specialist Bots, five active cron jobs, the seven-day implementation sequence, safe unattended-operation boundaries, and the ordered completion backlog.

**Current research-stack reference:** [`docs/RESEARCH-AND-TREND-STACK-2026-08-21.md`](docs/RESEARCH-AND-TREND-STACK-2026-08-21.md). It compares Tavily, Exa, Perplexity, Apify, Firecrawl, Parallel, Brave, open-source collectors, social-trend signals, database architecture, and current cost recommendations. Hermes was explicitly pinned to the existing Tavily backend on 2026-08-21. Re-check vendor pricing before purchase.

### Originality requirement

Competitor videos and transcripts may be used to discover topics, questions, and primary-source leads. Do not take an entire transcript and merely reword it. YouTube treats minimally transformed or mass-produced content as reused/inauthentic content, and TikTok can make unoriginal content ineligible for its recommendation feed.

Required editorial transformation:

1. Extract the underlying topic or question.
2. Locate and read primary sources.
3. Verify factual claims.
4. Choose an original angle relevant to AI builders.
5. Add AINTM-specific explanation, judgment, examples, or testing.
6. Create original visuals and wording.

References:

- YouTube channel monetization policies: https://support.google.com/youtube/answer/1311392?hl=en
- TikTok integrity/authenticity guidelines: https://www.tiktok.com/community-guidelines/en/integrity-authenticity/

### Instagram carousel opportunity

Metricool's June 2026 Instagram study analyzed 24.3 million posts across 375,000 accounts. It reported:

- Reels remain stronger for discovery.
- Carousels generated nine times more saves than single-image posts.
- Question-based posts generated more comments.
- Natural-language captions/Instagram SEO are increasingly important.

Conclusion: use Reels/Shorts for reach and prompt carousels for saves, shares, authority, and profile conversion. AINTM should test both instead of treating them as substitutes.

Source: https://metricool.com/press-release-instagram-study-2026/

### Prompt-carousel quality standard

Avoid generic “magic prompt” dumps. A useful AINTM prompt carousel should:

- Be tied to a current model or capability.
- State which model/version was tested.
- Show the prompt, expected use case, and a real output/result.
- Explain why the prompt works and where it fails.
- Use a strong first-slide outcome hook.
- Keep slide text readable and focused on one idea.
- End with a legitimate save/share reason and optional discussion question.
- Be assigned to the relevant presenter persona.

### Recommended research/analytics tool path

Start free during Week 1:

- Instagram Professional Insights
- Meta Instagram API for owned account/media insights after connection
- YouTube Data and Analytics APIs
- TikTok Creative Center
- Google Trends
- RSS and official OpenAI/Anthropic/Google sources
- Hacker News and selected relevant Reddit communities
- Manual review of benchmark creators and visible outliers

After baseline data exists, trial Metricool for affordable cross-platform reporting/scheduling. Consider Socialinsider only if deeper competitor benchmarking becomes worth its higher monthly cost.

Meta notes that some account metrics are unavailable below 100 followers and some account-level insight data is retained for only 90 days. Archive first-party metrics locally.

Meta reference: https://www.postman.com/meta/instagram/folder/23987686-f659d7d1-d74c-44e4-9192-9b1e8694c511

## 8. Recommended launch workflow

```text
Current sources + official lab sources + platform/creator signals
                              ↓
          Topic clustering, evidence, and velocity scoring
                              ↓
                Five ranked candidate evidence packs
                              ↓
         Rotation + specialist-override presenter assignment
                              ↓
          Original angles, hook variants, and script draft
                              ↓
                   Telegram topic/script approval
                              ↓
       Character voice + presenter visuals + captions + b-roll
                              ↓
                    Telegram final-video approval
                              ↓
       Platform-ready package for manual Week-1 publication
                              ↓
       1h/24h/72h metrics + weekly audit + learned adjustments
```

## 9. The next five coding tasks

### Task 1 — Stabilize the repository and identity/configuration layer

Work:

- Establish correctly scoped version control and ignore secrets/generated output.
- Add a Python project/dependency definition and test framework.
- Correct Siobhan, Gemma, and Claudia names, personalities, voices, and paths.
- Make `CHARACTERS.yml` the single source of truth for renderer asset discovery.
- Implement strict rotation plus specialist override and skipped-presenter carry-forward.
- Define and validate schemas for candidate, evidence pack, episode, render manifest, publishing package, and metrics.
- Prevent ingestion failures from prematurely consuming stories.

Acceptance:

- Tests fail before each behavior is implemented, then pass.
- All three presenters resolve real reference assets.
- A deterministic test proves rotation, specialist override, and balance behavior.
- No source/config validation errors remain.

### Task 2 — Build daily trend intelligence and evidence packs

Work:

- Add official OpenAI, Anthropic, Google/Gemini, and relevant product sources.
- Implement configured arXiv and YouTube inputs.
- Monitor Nate Herk, Chase AI, and Leon van Zyl as topic signals.
- Add YouTube view/engagement velocity and safe public trend signals.
- Cluster different URLs discussing the same event.
- Score recency, cross-source confirmation, velocity, builder relevance, novelty, practical value, visual potential, and evidence quality.
- Retrieve primary sources and record citations before scripting.
- Produce five ranked evidence packs, with uncertainty and rejection reasons.

Acceptance:

- A fixture-based test run produces deterministic rankings.
- Every selected factual claim maps to a source.
- Competitor transcripts alone cannot qualify a story as verified.
- Failed/slow sources degrade gracefully and are reported.

### Task 3 — Build the editorial and carousel engine

Work:

- Generate multiple hooks/angles for approval.
- Produce original presenter-specific short scripts.
- Add content-type selection: Reel/Short, prompt carousel, or defer.
- Generate platform-specific titles, captions, SEO language, and CTAs.
- Create carousel slide manifests with tested prompt, model, use case, result, limitations, and visual hierarchy.
- Record topic, hook, presenter, format, CTA, and hypothesis for later analysis.
- Add originality, unsupported-claim, length, and schema checks.

Acceptance:

- Telegram-ready approval payload contains sources, score reasons, hook choices, and draft.
- Carousel manifests are complete and machine-validated.
- Scripts cannot cite unsupported numbers/claims.
- Output is not a paraphrase of a source transcript.

### Task 4 — Finish low-cost production and approval orchestration

Work:

- Repair presenter reference loading and logo discovery.
- Test inexpensive voices for distinctness and Siobhan pronunciation.
- Generate branded 9:16 video and 4:5 Instagram carousel assets.
- Add caption-safe zones, legibility checks, audio checks, duration checks, and technical validation.
- Import/activate the n8n workflow.
- Configure Telegram credentials without storing secrets in workflow JSON.
- Add topic approval, hook/script revision, final-video approval, rejection reasons, retries, and resumable state.
- Produce a platform-ready package: MP4, carousel images if applicable, captions, title, source record, and manifest.

Acceptance:

- Approving a test script generates a branded preview using the intended presenter.
- Rejection/revision does not corrupt rotation or consume the story.
- One command/test fixture validates a complete offline package without paid calls.
- Paid generation cannot occur without explicit approval/configuration.

### Task 5 — Add manual launch tracking, weekly audits, then publishing automation

Work:

- Build manual-upload packages for YouTube, TikTok, and Instagram during Week 1.
- Record published URLs and 1h/24h/72h metrics.
- Add Instagram owned-data ingestion through Professional Insights/Meta API when connected.
- Create weekly scorecards covering profile, content, hooks, visuals, captions, cadence, engagement, conversion, presenter, topic, and format.
- Produce three specific fixes plus one or two controlled experiments each week.
- Feed proven performance signals into future ranking.
- Only after content proof, repair Postiz or choose a lighter publisher and implement idempotent publishing/status reconciliation.

Acceptance:

- Week 1 completes with usable baseline data.
- Starting Week 2, the audit explains bottlenecks with evidence and proposes measurable tests.
- The system distinguishes views from follower conversion.
- Publishing automation is not a prerequisite for content experimentation.

## 10. Owner-only to-do list

These require the owner's identity, account access, creative judgment, or spending authority. An agent should not decide or perform them independently.

### Before the first branded test

- [ ] Confirm Gemma's final personality, tone boundaries, and voice preference.
- [ ] Complete Claudia's personality, tone boundaries, and voice preference.
- [ ] Approve Siobhan's personality and final canonical reference-image subset.
- [ ] Select 3–5 canonical reference images per presenter. More images can remain archived, but the production set should be deliberate.
- [ ] Approve the final logo treatment or provide a transparent `logo.png`.
- [ ] Decide whether the existing show name and likeness/assets are cleared for commercial use.
- [ ] Watch the existing test MP4 and describe what should be kept or rejected: pacing, captions, voice, imagery, and overall polish.

### Accounts and access

- [ ] Provide the exact Instagram handle for the first audit.
- [ ] Convert/confirm it as an Instagram Professional Creator or Business account if first-party analytics/API access is desired.
- [ ] Provide the YouTube, TikTok, and Instagram account inventory: handle, follower count, current niche, and whether rebranding is allowed.
- [ ] Connect accounts through official OAuth/UI flows when the integration stage begins.
- [ ] Never paste passwords, tokens, recovery codes, or session cookies into an agent chat.
- [ ] Start/confirm the Telegram bot conversation and approve storing its credential in n8n's credential manager.

### Business and content judgment

- [ ] Provide examples of the SaaS applications/products that will eventually be sold, so calls to action attract the correct buyer.
- [ ] Define prohibited or sensitive topics, claims, and brand-safety boundaries.
- [ ] Approve scripts and final assets during Week 1.
- [ ] Manually upload Week-1 packages and provide published URLs if APIs are not yet connected.
- [ ] Approve any recurring or per-use expenditure before it is incurred.

### After Week 1

- [ ] Review the first weekly audit and choose which one or two experiments to run next.
- [ ] Decide whether Metricool is worth trialing based on actual reporting friction.
- [ ] Decide whether publishing automation is now worth repairing/replacing.

## 11. Agent to-do list for Hermes

1. Read this handoff completely.
2. Re-run the snapshot checks before trusting runtime status; assets may change.
3. Do not use the enclosing `/home/tre` Git repository for AINTM commits.
4. Read the portable skills under `agent-skills/` before trend research or account audits.
5. Present a file-level implementation plan for Task 1 before changing production code.
6. Use test-first development for every behavior or bug fix.
7. Preserve owner-created assets and unrelated changes.
8. Do not call paid generation APIs or publish externally without explicit permission.
9. Keep script and final-video approval human-controlled during the experiment.
10. Prefer primary sources and record evidence for factual claims.

## 12. Weekly account-audit specification

Start after the experimental first week. For Instagram, inspect:

- Profile photo, handle, name field, category, bio, link, and immediate promise
- Grid coherence and brand recognition
- Content pillars and format mix
- First-slide and first-second hooks
- Text readability, safe zones, visual hierarchy, and consistency
- Caption opening, natural-language keywords, CTA, and question quality
- Posting consistency and timing relative to account-specific insights
- Reach, plays/views, non-follower reach, watch time, retention, and completion
- Saves, shares, comments, profile visits, follows, and link clicks
- Follows per 1,000 views/reached accounts
- Performance by topic, presenter, hook, format, CTA, and production cost
- Best and worst outliers and what changed

Each weekly report must contain:

1. One-sentence diagnosis of the primary growth constraint.
2. Evidence table with current metric, previous metric, and interpretation.
3. What to keep, stop, and change.
4. Three concrete fixes, prioritized by expected impact and effort.
5. One or two controlled experiments for the next week.
6. Exact success/failure thresholds for those experiments.
7. Missing data that prevents confident conclusions.

Do not confuse views with business progress. Track follower conversion, returning audience, saves/shares, profile actions, and eventual SaaS interest.

## 13. Snapshot hashes

Use these SHA-256 hashes to identify the audited source snapshot:

```text
c47f80b24c70a962d3118a803d4f09e455f24f823e6d7ed47ec2994350e6142a  scripts/host_runner.py
5af86839949474f57fe467890b34a9cd139c570f172448e13ee0dbe478f26bcb  scripts/ingest.py
79e1d1e76b2a3368a6c5e8cab8d3e5213328b20a8671d17d0e651772b780aea1  scripts/post_postiz.py
946fa4a03c4ee6f97d89b32273dbcf95ce38c3d9fc4f79a215d40d0e03ea8f7c  scripts/rank_and_script.py
c49012933c4bccf2cbc48dfa8080a0e3ab0518117ab775176d7cd61975639147  scripts/render_daily.py
d4c99dfc78281a0afb118f901ed3d0fca0215963d4920801f94c04df78a2c3be  workflows/aintm_daily.json
ae7afd1f69a8a643ffc30ab2f9f6995e91330f2b3866bfb13c2fa3e5a054d501  compose/docker-compose.yml
c6b4a813405dd4a72203156dd3410a8443086288c9cddd854a348f6f4d41042b  config/sources.yml
f38d2fb36fe7927780ae60b4990b9327e1ea508990d72fea2ae0303ee182999a  assets/characters/CHARACTERS.yml
d908f460ccfadad431dc624c26af46a6413cc028c7e2b31caa09eec275f6e392  DELIVERABLES.md
cc41e636b100640dc6421eaa079d30944e05a60719044fe3f2ac8a2e718c3eb2  docs/TOOL-MENU.md
```

## 14. Definition of the first launch milestone

The first milestone is complete when AINTM produces one approved, original, source-grounded post package per day for seven consecutive days; uses the intended presenter and branding; never spends money or publishes without permission; and records enough performance data to identify which topic, hook, presenter, format, and CTA are driving followers.

Automatic publishing is not part of this milestone. Reliable learning is.

## 15. Portable operating skills for Hermes

Two repository-local skills accompany this handoff:

1. `agent-skills/aintm-trend-research/SKILL.md`
   - Use for daily AI topic discovery, ranking, verification, evidence packs, original angles, hooks, and source-grounded scripts.
   - It forbids unmeasured “viral/hottest” claims, minimal transcript rewrites, invented engagement data, and scripting before primary-source verification.
2. `agent-skills/aintm-social-account-manager/SKILL.md`
   - Use for Week-2-and-later account audits, funnel diagnosis, prioritized fixes, controlled experiments, and tested prompt carousels.
   - It separates facts from inference, avoids generic external benchmarks, and requires model/version/date, real inputs/outputs, and limitations in prompt carousels.

Both skills passed the local skill validator and were exercised against realistic before/after scenarios. They are intentionally portable and contain no account credentials or machine-specific logic.

For Hermes, copy each complete skill directory into the Hermes-compatible skill folder, normally `~/.agents/skills/`, and preserve the directory names. If the Hermes installation uses a different skill root, keep each `SKILL.md` at the top of its named directory. Restart/reload the agent session if required, then ask it to read this handoff and the relevant skill before working.

The skills guide agent behavior; they do not replace the application code described in the five tasks above.
