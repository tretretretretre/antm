# AINTM Tool Menu — everything on the table, you decide

Rule of this document: **nothing is filtered out for costing money.** Every relevant option is listed with its cost and a value score (1–10 = impact on follower growth per dollar+effort). Prices marked ~ are estimates to verify at signup time.

## Already owned / already running ($0 marginal)

| Tool | What it does for AINTM | Value | Notes |
|---|---|---|---|
| Claude Max (`claude -p`) | Script writing, ranking, prompts | 9 | Already wired into pipeline |
| Codex CLI (`codex`) | Second writer/reviewer via ChatGPT Plus | 7 | Installed, not wired yet |
| Gemini CLI (`gemini`, `agy`) | Research, summarization via Google AI Pro | 7 | Installed, not wired yet |
| Grok CLI (`grok`) | X-native trend research via SuperGrok | 7 | Installed, not wired yet |
| Grok Imagine **in-app** | Image→video 720p clips of the girls from your prompts/refs | 9 | $0 with SuperGrok; manual generate + drop in inbox/ |
| Postiz self-hosted | Posting/scheduling layer | — | **Free.** $29 was only the cloud version |
| n8n + Telegram + host bridge | Orchestration + approval gates | — | Built, verified |
| edge-tts | Free TTS voices | 5 | Works but robotic — the weak link |
| Adobe Express | Manual template graphics | 4 | No API; manual fallback |

## Credits you already hold (spend-down, no new subscription)

| Tool | Credit | Best use | Value |
|---|---|---|---|
| Google AI API | **$20** | Gemini TTS (big voice upgrade), Imagen images; Veo API is ~$0.35+/sec — reserve for special shots | 8 |
| RunPod serverless | **$60** | ComfyUI: train a **Chavonne LoRA** from her 12 refs → unlimited consistent renders; open video models (WAN) | 8 | 

## Pay-per-use APIs (metered, no subscription)

| Tool | Cost | What it buys | Value |
|---|---|---|---|
| Grok Imagine API | $0.02–0.07/image; $0.08/sec video | Automated girl clips in-pipeline (8s ≈ $0.64; daily 8s hook ≈ ~$14/mo) | 8 |
| Google Veo (API) | ~$0.35+/sec | Highest-end video; ~$10+ per 30s — special occasions only | 6 |

## Subscriptions worth considering (recurring)

| Tool | Cost | What it buys | Value |
|---|---|---|---|
| ElevenLabs | ~$5/mo starter | Best-in-class TTS; one distinct, human voice per girl | 9 |
| Kits.ai | Free (1 slot, 15 min/mo) → $9.99+ | Voice-to-voice conversion; music-leaning; free trial on Chavonne first | 6 |
| HeyGen / Hedra / D-ID | ~$24–30/mo | Talking-head avatars — lips actually sync to the script | 7 |
| Postiz Cloud / Blotato | $29/mo | Hosted posting with pre-approved platform APIs — escape hatch if dev-app approvals drag | 5 (situational) |
| Creatomate / JSON2Video | ~$40/mo | Template video rendering API | 2 — redundant; ffmpeg + your templates already do this |

## Current recommendation stack (your call)

1. **Voice** is the biggest quality-per-dollar jump: trial Gemini TTS (uses $20 credit) vs ElevenLabs ($5) vs tuned edge-tts in a bake-off; pick per girl.
2. **Visuals**: your templates + Grok Imagine in-app clips ($0) now; Chavonne LoRA on RunPod ($60 credit) for unlimited consistent stills; Grok API (~$14/mo) once the format is proven and you want the manual step gone.
3. **Avatars (HeyGen etc.)**: revisit after the template format verdict — may be unnecessary if Grok clips land.

## Research and trend stack update — 2026-08-21

The detailed, source-linked recommendation now lives in [`RESEARCH-AND-TREND-STACK-2026-08-21.md`](RESEARCH-AND-TREND-STACK-2026-08-21.md).

Current decision:

1. Use the existing **Tavily** key for broad discovery and selective primary-source extraction; Hermes is pinned to the Tavily backend.
2. Spend **$0 additional** until usage telemetry proves a gap. Add free official APIs, RSSHub, changedetection.io, Crawl4AI/Trafilatura, SQLite/FTS5, GitHub/HN/Product Hunt/GDELT/Bluesky, Google Trends, YouTube, Reddit, and TikTok Creative Center signals first.
3. First likely paid extraction upgrade: **Firecrawl Hobby (~$16/month annual)** only if local extraction reliability blocks daily production.
4. Use **Apify** surgically for one reviewed site/platform Actor, **Exa** for semantic monitors, and **Parallel/Brave** when measured search volume makes them cheaper than Tavily.
5. Treat **Perplexity, OpenCode, Freebuff, and OpenRouter models** as research/processing aids—not primary evidence sources or autonomous publishing systems.
