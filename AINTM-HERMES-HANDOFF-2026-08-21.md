# AINTM Hermes Handoff

**Project:** A.I.'s Next Top Models (AINTM)  
**Workspace:** `/home/tre/dev/antm`  
**Status:** Canonical product direction

## Mission

AINTM is a social-growth intelligence and AI-content system built to gain
followers quickly through evidence, original media, and continuous learning.

The system studies what is winning across AI-related social media, identifies
the topics and presentation patterns associated with attention and follower
growth, turns those opportunities into original AINTM-branded content,
measures results, and improves.

It is not simply an AI-news summarizer. Existing code is reusable
implementation material, not the product definition.

## Content model

- Produce one short 9:16 lead video each day.
- Rotate presenters: Siobhan, then Gemma, then Claudia.
- Open with the existing short branded jingle, then immediately address the
  strongest current opportunity supported by social evidence.
- Produce multiple template-structured branded 9:16 carousels around strong
  AI topics.
- Cycle existing approved presenter images, logos, backgrounds, video clips,
  and other brand assets so the feed is consistent without being identical.
- Produce one longer video per week from accumulated research.
- Use 9:16 by default and adapt only when a platform specifically requires it.
- Keep human approval during development and early operation. Automate only
  after the owner trusts repeated results.

## Growth intelligence

Daily research focuses primarily on X, Instagram, and YouTube. Track:

- fast-growing AI accounts and reliable early trend leaders;
- breakout posts, Reels, Shorts, videos, and carousels;
- the precise topic and event date;
- hook, wording, information sequence, slide count, duration, visual format,
  CTA, posting frequency, and posting time;
- visible views, likes, comments, shares, saves, retention, profile actions,
  and follower-growth signals when available;
- performance relative to the account's own baseline; and
- new formats or patterns outperforming prior winners.

Persist observations locally. Unavailable metrics remain `unknown`.

## Research tools

Use the best tool for each job:

- Grok and X Search for X-native discovery and current creator/post signals.
- YouTube search, YouTube Data, and `yt-dlp` for channel/video discovery,
  metadata, uploads, captions, and visible performance.
- NotebookLM optionally for bulk comparison of selected videos, transcripts,
  webpages, and primary sources.
- Tavily for broad web discovery, extraction, and locating primary evidence.
- Apify only for a reviewed, narrowly scoped social collection gap.
- Direct announcements, documentation, repositories, papers, and release notes
  for consequential factual verification.

RSS, Hacker News, Reddit, GitHub, Google Trends, and similar sources are
supporting inputs, not the core strategy.

## Originality

Competitor content can reveal topic demand, timing, hook style, structure,
format, cadence, retention methods, and calls to action. Verify the facts and
create a new AINTM thesis, script, wording, sequence, design, and presentation.
Do not copy or lightly paraphrase creator content.

## Hermes team

- Operator: readiness, blockers, cron/tool health, and ordered next actions.
- Researcher: social discovery, account tracking, evidence, and verification.
- Strategist: topic, format, hook, schedule, and measurable experiment.
- Writer: original short-video scripts and 9:16 carousel manifests.
- Reviewer: facts, originality, brand consistency, safety, and quality.

Required flow:

`Researcher -> Strategist -> Writer -> Reviewer -> Owner approval -> Production`

Operator oversees readiness; it does not write or produce content.

## Model routing

Claude is removed from the runtime and architecture. The machine-readable
authority is `config/model-routing.yml`.

- GPT-5.6 Sol: owner orchestration, strategy, and final review.
- Grok 4.6: X-native research and social writing.
- Google Flash/Lite: high-volume multimodal helper work.
- GPT-Image-2, Nano Banana, Grok Imagine, Gemini Omni, and Veo: specialized
  image/video generation according to the routing configuration.
- Mixture of Agents: disabled by default; critical decisions only, with Sol
  aggregating independent Grok and Gemini references.

Use the least expensive capable model and lowest sufficient effort. Routine
jobs use Low or Medium. High is for research judgment, final review, and major
strategy. xHigh/Max is manual only.

## Repository direction

- Preserve working Python/FFmpeg pieces, presenter assets, brand files, and
  useful orchestration experiments.
- Do not let the old RSS/Hacker News-first pipeline select the product's topics.
- Keep n8n, Postiz, or other infrastructure only when it helps the current
  workflow.
- Keep credentials and personal identifiers out of tracked files.
- Treat publication as a separate owner-approved step.

## Learning loop

For every published item, store the topic, source/trend origin, presenter,
hook, format, wording/structure, posting time, production style, visible
performance, profile actions, and follower conversion when available. Use
results to improve research, ranking, hooks, formats, timing, and production.

## Build priorities

1. Keep repository direction and model routing canonical and contradiction-free.
2. Build the social trend collector and persistent observation database.
3. Finish presenter/brand production and reusable 9:16 media templates.
4. Connect the full research-to-owner-approval artifact chain.
5. Build the performance-learning loop before publishing automation.

## First success milestone

AINTM is ready for its first operating phase when it can reliably identify a
strong current opportunity from social evidence, create one branded daily lead
video plus multiple branded carousels, rotate presenters correctly, reuse the
existing brand assets, prepare one longer weekly video, keep claims sourced,
present everything for owner approval, and store enough performance data to
learn what actually grows the account.
