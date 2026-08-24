# AINTM Week-1 Automation Plan

**Created:** 2026-08-22, America/Toronto  
**Goal:** Within seven days, establish a safe, human-approved content-creation system with specialist Bots, daily research/format experiments, durable assignments, and enough output to choose the first repeatable formats.

## 1. Synopsis of current developments

### Working or completed

- Hermes Desktop and the Telegram gateway are working; scheduled reports can reach Telegram while the owner is away.
- Hermes uses `gpt-5.6-sol` as the default main agent. xAI OAuth is connected and `grok-4.6` is available.
- Tavily is pinned as the web search/extract backend.
- The AINTM repository was audited and documented in `AINTM-HERMES-HANDOFF-2026-08-21.md`.
- A source-linked research-stack recommendation exists at `docs/RESEARCH-AND-TREND-STACK-2026-08-21.md`.
- Two repository-local operating skills exist: `aintm-trend-research` and `aintm-social-account-manager`.
- The existing Python pipeline can ingest RSS/Hacker News, draft scripts, generate TTS/images/captions, render a vertical MP4, and call Postiz.
- One 31.5-second 1080x1920 test MP4 proves the renderer can complete.
- `yt-dlp` can collect recent YouTube metadata and enforce a 48-hour research window.
- The preferred research architecture is token-efficient: deterministic collection, bulk analysis in NotebookLM or a similar notebook, and only a compact synthesis returned to Hermes.
- The Telegram channel `Daily hermes improvements` has been identified as a possible place to document useful Hermes workflows; it is not connected for automatic publishing.

### Not working or not finalized

- No seven-day automated content run has been completed.
- The existing n8n workflow is an export only; n8n has no imported/published workflow.
- Postiz is blocked by Temporal and has no verified connected social accounts or API key.
- Automatic publishing is intentionally deferred during Week 1.
- Character names, reference-image paths, personalities, voices, logo handling, and renderer identity consistency need correction.
- The ingestion ledger marks stories seen too early, before approval or publication.
- Full-source verification, trend velocity, clustering, schema validation, hook variants, carousel generation, technical quality gates, and analytics feedback are incomplete.
- NotebookLM CLI is not installed or authenticated. It remains an experiment, not a production dependency.
- AINTM is inside an incorrectly scoped `/home/tre` Git repository with no commits; do not commit until a project-local repository and ignore rules are established.

## 2. Automation architecture

```text
Operator Bot (06:45)
  readiness + cron health + tools/abilities + ordered status
                    ↓
Researcher Bot (07:30)
  official sources + attention signals + evidence packs
                    ↓
Strategist Bot (09:15)
  format choice + original angles + experiment design
                    ↓
Writer Bot (11:30)
  short-video and/or carousel prototypes
                    ↓
Reviewer Bot (13:30)
  facts + originality + safety + approval gates
                    ↓
Owner Brief (14:15 Telegram)
  concise status, blockers, and decisions
                    ↓
Human approval before rendering, spending, or publishing
```

Shared experimental artifacts live under `automation/daily/`. The scheduled Bots must not modify production code, publish, spend money, connect accounts, or delete files.

## 3. Specialist Bots created

| Bot/profile | Model | Responsibility | Default workspace |
|---|---|---|---|
| `operator` | GPT-5.6 Sol low | Project readiness, cron health, tooling gaps, ordered safe next actions | `/home/tre/dev/antm` |
| `researcher` | Grok 4.6 high | Current AI discovery, primary-source verification, trend evidence packs | `/home/tre/dev/antm` |
| `strategist` | GPT-5.6 Sol medium | Format choices, original angles, hooks, hypotheses, success metrics | `/home/tre/dev/antm` |
| `writer` | Grok 4.6 medium | Short-video scripts and carousel prototype manifests | `/home/tre/dev/antm` |
| `reviewer` | GPT-5.6 Sol high | Fact, originality, safety, quality, and approval-gate review | `/home/tre/dev/antm` |

Each is an isolated Hermes profile with its own memory, sessions, skills, config, and canonical Bot Chat. They appear in Desktop's **Bots** tab.

## 4. Cron jobs created

| Time | Profile | Job ID | Output |
|---|---|---|---|
| 06:45 daily | `operator` | `0174583c53dc` | Readiness/tool report + Telegram morning status |
| 07:30 daily | `researcher` | `c2dd2ad7a92a` | Dated research report + `latest-research.md` |
| 09:15 daily | `strategist` | `bbfc33e8c3e4` | Dated format lab + `latest-format-lab.md` |
| 11:30 daily | `writer` | `b2ace2e8bd14` | Dated prototypes + `latest-prototypes.md` |
| 13:30 daily | `reviewer` | `0bd88599ff49` | Dated verdict + `latest-review.md` |
| 14:15 daily | `default` | `9f7165ae6099` | Concise owner status delivered to Telegram |

The first four jobs write experimental files and deliver their result into each specialist's Bot Chat. The final job reads the shared files and sends one concise daily status to Telegram.

## 5. Possible future cron jobs

Do not activate these until their prerequisites pass manual tests.

1. **16:30 YouTube/NotebookLM experiment**
   - Prerequisites: working deterministic YouTube collector; NotebookLM CLI installed; owner completes browser authentication; one manual 7–20 source run succeeds; source dedup verified.
   - Output: notebook ID, source list, themes, citations, compact synthesis, and optional carousel/PPTX brief.

2. **Official release change monitor every 30–60 minutes**
   - Prerequisites: stable monitor script or URLs with timestamp-free output.
   - Use `monitor_script`/`monitor_url` so unchanged pages trigger no LLM call.

3. **Daily media-render candidate**
   - Prerequisites: reviewer PASS; corrected character paths; approved reference subsets, logo, voices; safe-zone/audio/duration tests; explicit owner approval.
   - Must never call paid generation automatically.

4. **Week-1 publication-package reminder**
   - Prerequisites: approved draft and rendered media.
   - Creates/upload checklist only; no automatic posting.

5. **1h/24h/72h metrics collector**
   - Prerequisites: owner supplies published URLs and official analytics access/export.

6. **Week-2 weekly account audit**
   - Prerequisites: at least one week of comparable post/account data.
   - Attach `aintm-social-account-manager`; recommend no more than three fixes and one or two controlled experiments.

7. **Publishing automation**
   - Prerequisites: proven content format, connected accounts, Postiz/alternative repaired, idempotency/status reconciliation, owner authorization.
   - Keep a human approval gate before every external post until explicitly changed.

## 6. Ordered seven-day implementation plan

### Day 1 — Prove research-to-format handoff

- Run and inspect all five new jobs.
- Confirm research contains primary-source links and no invented trend claims.
- Compare short-video, carousel, both, and defer decisions.
- Keep output experimental; publish nothing.

### Day 2 — Tune research quality

- Adjust source roster, recency window, scoring weights, and result count.
- Add official OpenAI, Anthropic, Google/Gemini, GitHub/release, HN, Product Hunt, and selected community signals.
- Define what qualifies as verified versus editorial pick.

### Day 3 — Choose initial content-format tests

- Select one short-video template and one carousel template.
- Require original angle, tested prompt/result where relevant, model/version/date, limitations, and source citations.
- Choose the initial success metrics and guardrails.

### Day 4 — Repair the production-critical identity layer

- Establish project-local Git and ignore secrets/output.
- Add dependency/test configuration.
- Correct Siobhan, Gemma, Claudia names, personalities, voices, paths, and canonical reference subsets.
- Make `CHARACTERS.yml` the single asset source of truth.
- Fix early story-consumption behavior with tests.

### Day 5 — Produce one branded offline package

- Correct logo/reference loading.
- Run the voice comparison and choose one voice per presenter.
- Add technical gates for duration, audio, captions, safe zones, and output validity.
- Produce one complete package without publishing.

### Day 6 — Human review and iteration

- Owner reviews topic, script, carousel/video, pacing, captions, visuals, voice, CTA, and brand fit.
- Record specific revisions and run one controlled iteration.
- Optionally test one manual YouTube→NotebookLM batch if authentication is complete.

### Day 7 — Baseline launch readiness

- Confirm seven-day research/format logs are durable.
- Freeze the first repeatable daily checklist.
- Manually publish only approved Week-1 packages.
- Record URLs and measurement times.
- Decide whether to activate rendering, metrics, and Week-2 audit jobs.

## 7. Ordered backlog and completion conditions

### P0 — Required immediately

- [x] Create specialist Bots.
- [x] Create safe research/format/writing/review cron chain.
- [x] Deliver a daily owner brief to Telegram.
- [ ] Verify the first full scheduled chain writes all four rolling artifacts.
- [ ] Review first-day quality and tune prompts/sources.

### P1 — Required for a branded offline content package

- [x] Create correctly scoped AINTM Git repository and ignore secrets/generated media.
- [ ] Add Python dependencies, schemas, and test framework.
- [ ] Fix character names, personalities, voices, paths, and logo.
- [ ] Fix renderer reference discovery.
- [ ] Fix ingestion ledger semantics.
- [ ] Add full-source verification and schema gates.
- [ ] Add hook variants and carousel manifests.
- [ ] Add media technical-quality checks.

### P2 — Owner decisions/access

- [ ] Confirm presenter personalities and 3–5 canonical images each.
- [ ] Approve transparent logo treatment.
- [ ] Review the existing test MP4 and give pacing/voice/caption/visual feedback.
- [ ] Provide initial platform handles and rebranding status.
- [ ] Define prohibited topics and brand-safety boundaries.
- [ ] Approve each Week-1 script and final asset.

### P3 — Experiments after manual proof

- [ ] Install/authenticate NotebookLM only if the experiment remains worthwhile.
- [ ] Run one 7–20 source NotebookLM batch and compare output to direct Hermes research.
- [ ] Import and repair n8n only if it improves resumable human approvals.
- [ ] Repair Postiz or select a lighter publisher only after format proof.
- [ ] Add account analytics and weekly audit after baseline data exists.

## 8. How to operate Bots and cron

### Bots

- Desktop → **Bots** → click a specialist to open its persistent Bot Chat.
- Type `@researcher investigate this topic` from another Bot chat to hand off work.
- Use group chat when multiple specialists must deliberate; direct assignment is cheaper and clearer for routine work.
- Edit a Bot's model, SOUL, skills, tools, or MCP servers from **Edit Profile**.

CLI equivalents:

```bash
researcher chat
strategist chat
writer chat
reviewer chat
hermes profile list
```

### Cron

```bash
hermes -p researcher cron list
hermes -p researcher cron run c2dd2ad7a92a
hermes -p researcher cron runs c2dd2ad7a92a --limit 10
hermes -p researcher cron pause c2dd2ad7a92a
hermes -p researcher cron resume c2dd2ad7a92a
```

Cron jobs run in fresh sessions and therefore need self-contained prompts, explicit paths, safe delivery targets, and verification through execution history. Use `continuity` for deduplicating scouts, `monitor_script`/`monitor_url` for change-only jobs, and script-only mode for deterministic checks that need no LLM.

## 9. Safety policy for unattended operation

- Research, analysis, drafting, local experimental files, and status reports may run unattended.
- Publishing, paid generation, account connection, credential changes, file deletion, production-code changes, and approval decisions remain human-controlled.
- Cron outputs are drafts, not approval.
- Never copy creator scripts or claim trend leadership without measured evidence.
- Every consequential factual claim in publishable content must map to a primary source.

## 10. Week-1 success definition

Week 1 succeeds when the system reliably produces a daily source-grounded research pack, format experiment, content prototype, and review verdict; the owner receives a concise Telegram brief; one branded offline package passes human review; and enough observations exist to choose the first repeatable video and carousel formats. Automatic publishing is not required.
