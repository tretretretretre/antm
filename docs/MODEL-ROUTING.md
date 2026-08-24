# AINTM Model Routing

The machine-readable authority is `config/model-routing.yml`. This document
explains the policy.

## Principle

Delegate by task, risk, and modality. Use the least expensive capable model
and the lowest sufficient reasoning effort. Scheduled jobs should normally
inherit their profile assignment; an override must be intentional and written
down so the UI and actual execution do not disagree.

## Role routing

| Role | Default | Effort | Why |
|---|---|---:|---|
| Owner/default | GPT-5.6 Sol | Low | Reliable orchestration; escalate for decisions |
| Operator | GPT-5.6 Sol | Low | Deterministic readiness and blocker reporting |
| Researcher | Grok 4.6 | High | X-native discovery and current social evidence |
| Strategist | GPT-5.6 Sol | Medium | Cross-source judgment and experiment design |
| Writer | Grok 4.6 | Medium | Native short-form social drafting |
| Reviewer | GPT-5.6 Sol | High | Final factual, originality, and quality gate |

Google Flash/Lite models handle repetitive multimodal helper work such as
vision, extraction, compression, and titles. Terra handles inexpensive tool
routing and curation. Sol is reserved for decisions and final judgment.

## Effort routing

- Low: routing, extraction, formatting, scheduling, and simple status work.
- Medium: synthesis, drafting, ordinary strategy, and curation.
- High: research judgment, final review, and major campaign decisions.
- xHigh/Max: manual exception only; never a routine cron default.

## Mixture of Agents

Mixture of Agents is off by default. Claude must not appear as an aggregator,
reference model, fallback, or hidden preset. The critical-decision preset uses
Sol to aggregate independent Grok and Gemini views. Routine daily content does
not warrant this latency and cost.

## Media routing

- Nano Banana 2 is the everyday carousel/image route.
- Nano Banana Pro is for text-heavy or complex layouts.
- GPT-Image-2 is the premium alternative for creation or editing.
- Grok Imagine Image is useful for fast, reference-driven social imagery.
- Gemini Omni Flash is the default iterative video route.
- Veo Lite is the efficient production route; Veo is reserved for hero shots.
- Grok Imagine Video is useful for short reference-to-video social clips.
- Edge TTS is acceptable for drafts; final voice should use the selected xAI
  voice route after a presenter bake-off.

Generation never bypasses owner approval or the asset-preservation rule.
