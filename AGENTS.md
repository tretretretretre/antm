# AINTM Agent Operating Contract

This file is the mandatory starting point for every agent working in this
repository. Repository history, old generated artifacts, and reusable code do
not override this direction.

## Canonical sources

Read these in order before making changes:

1. `AINTM-HERMES-HANDOFF-2026-08-21.md` — product mission and operating model.
2. `config/model-routing.yml` — approved model, effort, and generation routing.
3. `STATUS.md` — verified current state and immediate work.

When another document conflicts with these files, update or remove the stale
document. Do not blend incompatible directions.

## Mission

AINTM is a social-growth intelligence and AI-content system. It studies what
is winning on X, Instagram, and YouTube; identifies topics and presentation
patterns associated with attention and follower growth; produces original
AINTM-branded media; measures results; and improves from evidence.

It is not an RSS/Hacker News summarizer, a generic AI-news bot, or a vehicle
for copying creator content. Supporting sources may help verify or discover a
story, but social growth evidence drives selection.

## Required output model

- One 9:16 lead video each day.
- Presenter rotation: Siobhan, then Gemma, then Claudia.
- A quick existing brand jingle at the start.
- Multiple branded, template-structured 9:16 carousels around strong topics.
- One longer video each week based on accumulated research.
- Existing approved presenters, logos, audio, backgrounds, and video assets
  should be reused and varied before replacement assets are generated.
- Human approval is required before publication while the system is being
  proven.

## Required operating chain

`Researcher -> Strategist -> Writer -> Reviewer -> Owner approval -> Production`

- Operator maintains readiness and reports blockers; it does not select topics
  or produce content.
- Researcher gathers social evidence, tracks accounts/posts, and verifies
  consequential claims.
- Strategist selects the opportunity, format, hook, schedule, and experiment.
- Writer creates original scripts and carousel manifests from approved inputs.
- Reviewer checks facts, originality, brand consistency, quality, and safety.
- Production renders only approved work. Publishing requires separate owner
  approval.

## Model and tool rules

- Claude is not part of the AINTM runtime, automation, or agent architecture.
- Use `config/model-routing.yml`; do not silently substitute another model.
- Use the least expensive capable model and the lowest sufficient reasoning
  effort. Escalate for complexity or risk, not habit.
- Mixture of Agents is disabled by default. Use its critical-decision preset
  only when one model's judgment is insufficient.
- Use specialized generation tools for images, video, and voice. GPT-5.6 Sol
  orchestrates or reviews those tools; it is not itself the media generator.
- Record intentional job-level overrides. Unexplained differences between a
  profile default and a scheduled job are configuration drift.

## Research and evidence rules

- X, Instagram, and YouTube are primary discovery and measurement surfaces.
- Record post/account baseline, velocity, format, hook, CTA, timing, and visible
  engagement or follower-growth signals when available.
- Store unavailable metrics as `unknown`; never infer fake precision.
- Verify consequential claims against direct announcements, documentation,
  repositories, papers, or other primary sources before publication.
- Competitor work is evidence about demand and technique, never source copy.
- RSS, Hacker News, Reddit, GitHub, Google Trends, and similar feeds are
  supporting signals only.

## Engineering rules

- Preserve useful working code and approved assets unless replacement is
  clearly necessary.
- Add tests before behavior changes and keep the offline render path usable.
- Generated artifacts belong under ignored runtime directories, not in source
  control.
- Keep secrets, tokens, account identifiers, and credentials out of tracked
  files. Use environment variables and `.env.example` placeholders.
- Do not publish, connect accounts, spend money, or delete owner media without
  explicit approval.
- Update `STATUS.md` when verified repository state materially changes.

## First operating milestone

The first milestone is an owner-approved offline package containing a sourced
daily opportunity, one branded lead video, multiple branded 9:16 carousels,
correct presenter rotation, and stored research/performance records. Automatic
publishing comes later.
