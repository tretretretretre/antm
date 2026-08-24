# AINTM Status

**Updated:** 2026-08-24

## Verified working material

- The repository contains reusable Python/FFmpeg ingestion, scripting,
  rendering, approval, and publishing scaffolding.
- Presenter assets exist for Siobhan, Gemma, and Claudia.
- Brand logos, an opening jingle, and four Grok-generated 9:16 reference clips
  exist and are preserved.
- A prior 1080x1920 offline render proves the basic renderer can complete.
- Hermes profiles exist for operator, researcher, strategist, writer, and
  reviewer.

## Corrected in the current cleanup

- The 690-line legacy handoff was replaced by the concise canonical direction.
- `AGENTS.md` now requires every repository agent to follow that direction.
- Claude was removed from the tracked writer and n8n workflow.
- Model, effort, helper, Mixture-of-Agents, and media routing now have one
  machine-readable source at `config/model-routing.yml`.
- Presenter rotation and asset paths are Siobhan -> Gemma -> Claudia.
- The renderer now uses the existing logo and opening jingle paths and defaults
  to `gemini-3.1-flash-image`.
- Dated Week-1/RSS-first plans were replaced by current operating and research
  documents.

## Known gaps

- The current Python ingestion path is still RSS/Hacker News scaffolding; the
  social collector/database does not yet exist.
- Carousel rendering and the weekly long-video workflow do not yet exist.
- The existing renderer still uses edge TTS and still-image FFmpeg assembly.
- The publishing stack is unverified and remains outside the first milestone.
- Hermes runtime profiles, helper models, Mixture-of-Agents preset, and
  scheduled prompts now match the routing direction; the gateway remains
  stopped and the owner brief remains paused.
- A minimal Python dependency manifest and four regression tests now exist;
  broader artifact schemas and integration coverage are incomplete.
- Credential-like literals were present in the initial Git commit. The tracked
  Compose file is clean now, but those old values must be rotated; history
  rewriting is a separate owner-approved operation.

## Next work

1. Define the social observation/research/performance schema and SQLite store.
2. Implement primary X, Instagram, and YouTube collection adapters.
3. Define validated research, strategy, script, carousel, review, and approval
   artifact contracts.
4. Add reusable 9:16 carousel rendering and the weekly long-video path.
5. Produce the first owner-approved offline daily package.
