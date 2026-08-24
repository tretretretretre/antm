# A.I.'s Next Top Models

AINTM is a social-growth intelligence and AI-content system for X, Instagram,
and YouTube. It finds evidence-backed AI attention opportunities, turns them
into original branded media, and learns from performance.

Start with [`AGENTS.md`](AGENTS.md), then read the concise
[`AINTM Hermes handoff`](AINTM-HERMES-HANDOFF-2026-08-21.md) and
[`STATUS.md`](STATUS.md).

## Daily operating flow

```text
Researcher -> Strategist -> Writer -> Reviewer -> Owner approval -> Production
```

The target package is one 9:16 lead video per day, multiple 9:16 carousels,
and one longer video per week. Existing presenter and brand assets are primary
production inputs. Publication remains human-approved.

## Repository map

- `assets/` — approved presenters, branding, audio, and reference video.
- `agent-skills/` — AINTM research and account-management standards.
- `automation/daily/` — ignored daily research/draft/review artifacts.
- `config/` — sources, model routing, and service configuration.
- `docs/` — current operating, research, and tooling guidance.
- `scripts/` — reusable ingestion, writing, rendering, and publishing pieces.
- `workflows/` — orchestration exports; these are implementation material, not
  the product definition.

## Safety

Do not place credentials in tracked files. Do not publish, spend, connect
accounts, or remove owner assets without explicit approval.

## Local validation

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/*.py
```
