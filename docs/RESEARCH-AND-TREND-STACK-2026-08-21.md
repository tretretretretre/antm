# AINTM Research, Trend Detection, and Knowledge Stack

**Research date:** 2026-08-21 (America/Toronto)  
**Purpose:** Keep AINTM ahead of mainstream AI coverage with source-grounded, measurable topic discovery at low cost.  
**Current Hermes web backend:** Tavily, explicitly pinned on 2026-08-21. The API key remains in Hermes' credential store and must never be copied into this repository or chat.

## 1. Executive recommendation

Do not buy a large “all-in-one social listening” subscription yet. AINTM can build a stronger Week-1 research loop from tools already available or free:

1. **Tavily** for broad web discovery and selective extraction.
2. **Primary-source monitors** for OpenAI, Anthropic, Google/DeepMind, GitHub releases, papers, and product changelogs.
3. **Free platform signals** from Hacker News, Reddit, TikTok Creative Center, YouTube Data API, GitHub/OSS Insight, Product Hunt, Google Trends, GDELT, and Bluesky Jetstream.
4. **Local storage first:** SQLite + FTS5 for the research database; add DuckDB/Parquet for analytics and local embeddings only when semantic clustering proves necessary.
5. **Open-source extraction:** Trafilatura for ordinary pages and Crawl4AI/Playwright only for JavaScript-heavy pages. Use RSSHub and changedetection.io for recurring monitoring.
6. **Cheap LLM routing:** use a low-cost model only to classify, cluster, summarize, or validate structured output. The evidence and trend scores—not the model—must select the story.

The first paid research upgrade should be driven by a measured gap:

- extraction failures → Firecrawl;
- a platform-specific scraper → one Apify Actor;
- semantic discovery/recurring web monitors → Exa;
- high-volume cheap search → Parallel or Brave;
- human-facing cited answer engine → Perplexity, only if Tavily plus a model is insufficient.

## 2. Search and extraction API comparison

Pricing and capabilities below were checked against official vendor documentation on the research date. Re-check before purchase.

| Tool | Best AINTM role | Current price signal | Strength | Limitation | Recommendation |
|---|---|---:|---|---|---|
| **Tavily** | Default discovery, extraction, crawl | Basic search 1 credit; advanced 2; basic extract 1 credit per 5 successful URLs; crawl = map + extract | Agent-ready results, search/extract/crawl in Hermes, usage reporting | Credits can disappear quickly in broad multi-agent loops | **Use now.** Basic search by default; advanced only for ambiguous/high-value stories. Cap results and request usage metadata. |
| **Parallel Search** | Cheap high-volume URL discovery | $1/1K turbo/fast; $5/1K basic/advanced; $1/1K extra results | Very low cost, compressed excerpts, high free allowance advertised | Less proven for difficult extraction than dedicated crawlers | Best cost fallback if Tavily search volume grows. Test on an AINTM benchmark before switching. |
| **Brave Search API** | Independent-index search/news/images | $5/1K searches with $5 monthly credits | Independent web index, news/image results, predictable price | Search-first; extraction requires another tool | Strong second-index check and inexpensive alternative. |
| **Exa** | Semantic discovery, similar-page search, scheduled monitors | Search $7/1K; contents $1/1K pages; monitors $15/1K | Neural retrieval, coding/docs search, semantic similarity, deduplicated monitors/webhooks | More expensive than Parallel/Brave for routine discovery | Add only when semantic retrieval or recurring monitor quality clearly beats our free monitors. |
| **Firecrawl** | Reliable LLM-ready extraction/crawl | Free 1,000 pages; Hobby $16/mo annual for 5,000 credits; scrape/crawl/map/monitor 1 credit/page; search 2 credits/10 results | Strong extraction, JS handling, map/crawl/monitor, clean Markdown | Recurring cost and per-page burn; self-hosting adds operational/licensing concerns | Best first paid extraction upgrade if Crawl4AI/Trafilatura fail too often. |
| **Perplexity Sonar** | Cited answers and deep human research | Sonar $1/M input and output plus $5/$8/$12 per 1K requests by context; Pro costs more | Fast cited synthesis, OpenAI-compatible API | Duplicates Tavily + LLM; request and token billing stack | Do not add to production yet. Consider a human Pro subscription only if it saves substantial research time. |
| **Apify** | Surgical site/platform-specific scraping | Actor-specific pay-per-event plus compute/storage/proxy usage | Large Actor marketplace; useful for difficult social/platform sources | Quality, legality, maintenance, and pricing vary by Actor | Use one reviewed Actor for a proven data gap—never as the default crawler. |
| **SearXNG** | Free self-hosted search fallback | Software free; pay only hosting | Private, multi-engine, JSON API, no per-query bill | Search only; engine blocking/maintenance; no extraction | Useful later as a resilience/volume fallback, not our highest-quality first source. |

### Cost-control rules

- Discover broadly, extract narrowly.
- Cache by normalized URL and content hash.
- Never re-extract unchanged pages.
- Use basic/fast search first; escalate only when confidence is low.
- Store vendor, endpoint, credits/cost, latency, result count, and failure reason for every call.
- Benchmark providers on the same 50–100 AINTM research questions before changing the default.

## 3. Free and open-source collection stack

### Recommended now

| Tool/source | Cost | Use |
|---|---:|---|
| RSS/Atom + `feedparser`/current parser | Free | Official labs, blogs, release notes, creator uploads, newsletters with feeds |
| Hacker News Firebase API | Free/no key | Near-real-time top/new/best AI developer stories and velocity |
| Algolia HN Search | Free/public | Historical HN search and faster comment/topic lookup |
| GitHub REST Events/Search | Free within quota | Release velocity, stars/forks/activity, repository events, changelogs |
| OSS Insight trending endpoint | Free/public | API-friendly trending repository signal where GitHub has no official Trending API |
| Product Hunt GraphQL API | Read-only public access | Daily launches, votes, comments, makers, AI product discovery |
| GDELT DOC/GKG | Free | Global news volume, cross-language confirmation, timeline acceleration |
| Bluesky Jetstream | Free/no auth | Real-time public post stream in JSON; keyword and mention acceleration |
| TikTok Creative Center | Free/public UI | Trending hashtags, songs, creators, videos, keywords by region |
| Google Trends API Alpha/manual UI | Free/limited access | Search-interest acceleration and regional interest |
| YouTube Data API | Free quota | Upload discovery, channel/topic searches, view/comment/like velocity |
| Reddit official/public feeds and approved API access | Usually free within terms | Community questions, repeated pain points, topic acceleration |
| RSSHub | Free/self-hosted | Convert supported sites/channels into feeds; one normalized ingestion path |
| changedetection.io | Free/self-hosted | Watch official docs, pricing, release, model, and changelog pages for meaningful changes |
| Trafilatura | Free/open source | Fast clean extraction from ordinary HTML pages |
| Crawl4AI + Playwright | Free/open source | JavaScript-heavy pages and LLM-ready Markdown when simple extraction fails |
| `yt-dlp` | Free/open source | Metadata and available captions/transcripts; obey platform terms and creator rights |

### Do not overbuild yet

Scrapy is excellent for large, stable crawls, but AINTM does not yet have enough volume to justify a large crawler framework. Qdrant, Elasticsearch, and a dedicated vector database are also unnecessary at current scale.

## 4. Social-trend signal design

A “trend” is not a single popular post. AINTM should detect **acceleration plus cross-source confirmation**.

### Source layers

1. **Primary event layer:** official announcement, documentation, repository, paper, release notes.
2. **Developer attention:** GitHub events/stars, Hacker News rank/score/comment velocity, Reddit post/comment velocity, Product Hunt votes/comments.
3. **Search attention:** Google Trends and search-query frequency.
4. **Video/social attention:** YouTube view/comment/like velocity; TikTok Creative Center hashtags/songs/videos; Bluesky and X mention acceleration.
5. **Creator signal:** Nate Herk, Chase AI, Leon van Zyl and other benchmark creators as topic/question signals—not sources to copy.
6. **Owned-account response:** AINTM's 1h/24h/72h reach, retention, saves, shares, profile visits, follows, and clicks.

### Measurements to store

For each observation, store:

- source, source type, URL/post/repository ID;
- observed time and original event/publication time;
- title/text excerpt and language;
- author/account/channel;
- views, likes/upvotes, comments, shares/reposts, stars/forks when available;
- prior observation and elapsed time;
- calculated velocity and acceleration;
- region/platform/topic/entity tags;
- primary-source status and verification confidence.

### Scoring model

Score 0–5 for:

- recency;
- attention velocity;
- acceleration relative to the source's normal baseline;
- independent cross-source confirmation;
- primary-source evidence quality;
- AI-builder usefulness;
- novelty;
- demonstration/visual potential.

Subtract 0–5 for:

- weak sourcing/speculation;
- content saturation;
- unavailable product/access mismatch;
- legal, safety, or reputational risk;
- inability to explain the topic accurately in short form.

Use log/smoothed velocity rather than raw percentage when the prior count is near zero. Record `unknown` rather than inventing inaccessible metrics.

### Timing

- Fast sources: 15–60 minute observations during a breaking event.
- Routine daily sources: 2–4 checks per day.
- Creator and release sources: change-triggered or hourly/daily.
- Owned post metrics: 1h, 24h, 72h, then 7d.

The useful lead is often: official release/GitHub/HN/Reddit acceleration first, followed by YouTube/TikTok saturation later. A Reddit creator report described a similar cross-platform mention-velocity system gaining a 6–12 hour lead; treat that as an anecdote to test, not proof.

## 5. Local research database

Start with one local SQLite database using WAL mode and FTS5. Keep it separate from Postiz's databases.

### Minimum tables

- `sources` — source identity, type, URL/API, cadence, terms, health.
- `items` — canonical URL/ID, title, author, timestamps, raw metadata, content hash.
- `observations` — metric snapshots over time.
- `topics` — normalized topic/entity.
- `topic_items` — item/topic links and clustering confidence.
- `evidence` — claim, source URL, quote/excerpt, verified/inferred/unknown.
- `candidates` — daily scores, reasons, risks, rejection reasons.
- `content_runs` — presenter, format, hooks, script, source IDs, approvals, package path.
- `published_posts` — platform, URL, publish time, cost, experiment ID.
- `post_metrics` — 1h/24h/72h/7d observations.
- `tool_usage` — provider, endpoint, credits/cost, latency, success/failure.

Use content hashes and canonical IDs to deduplicate. Keep fetched excerpts and citations; do not retain unnecessary full copyrighted pages indefinitely.

### Semantic clustering

Begin with keyword/entity normalization and FTS5. If duplicate-topic clustering is insufficient, add a small local embedding model plus `sqlite-vec` or FAISS. Move analytics snapshots to Parquet/DuckDB only when time-series queries outgrow SQLite.

## 6. LLM and agent economics

### OpenRouter

OpenRouter is valuable for routing cheap classification/summarization work, not as a trend source. Model availability changes quickly, so maintain an AINTM fixture benchmark and pin exact model IDs.

One current high-value example is `deepseek/deepseek-v4-flash-0731`, listed at $0.07/M input and $0.14/M output on 2026-08-21. It is cheap enough for topic classification, entity extraction, schema repair, and first-pass summaries. Do not let a cheap model independently verify facts or select a winner without evidence scores.

### OpenCode

OpenCode can enable hosted Exa web search without a key using `OPENCODE_ENABLE_EXA=1` when supported. This is useful as a free secondary research/checking harness, but it is not a durable data API and should not be the production collector.

### Freebuff

Freebuff is an ad-funded free coding/research agent with specialized agents and included models. It may be valuable for disposable experiments and public-code tasks. Do not give it secrets, private account data, or sole control of the production pipeline; free capacity/model availability can change.

### Hermes

Hermes already supports Tavily, Exa, Parallel, Firecrawl, Brave, SearXNG, DDGS, and xAI search backends. A strong future split is:

- `web_search` → Tavily or Parallel/Brave;
- `web_extract` → Tavily initially, Firecrawl or local Crawl4AI at volume;
- `x_search` → X-native topic confirmation when authorized;
- cron/monitor scripts → source collection and change detection;
- AINTM trend-research skill → scoring, evidence packs, originality gates;
- a cheap model → classification/normalization;
- a frontier model → final high-value reasoning/script review only.

## 7. Subscription and spending recommendation

### Spend now: $0 additional

Use the existing Tavily key, official/free APIs, RSSHub, changedetection.io, Crawl4AI/Trafilatura, SQLite, and existing Claude/Codex/Gemini/Grok access. Build usage telemetry before subscribing to another research vendor.

### Best likely first research spend

1. **Firecrawl Hobby (~$16/month annual)** only if extraction reliability/maintenance is blocking daily output.
2. **One Apify Actor** only for a specific platform/source we cannot legally and reliably access otherwise.
3. **Exa pay-as-you-go monitors** only if free page/release monitors miss important semantic developments.

### Good value, but not required yet

- **Parallel:** likely best raw search cost at scale.
- **Brave:** strong independent second index and predictable $5/1K pricing.
- **Perplexity Pro/API:** useful for a human researcher who values its UX; redundant for the automated pipeline until measured otherwise.
- **Metricool:** reconsider after Week 1 when cross-platform reporting friction is known.

## 8. Implementation sequence

1. Add source/tool schemas and SQLite research database.
2. Fix the existing ingestion ledger so observation does not consume a story.
3. Add official release/RSS/GitHub/HN/Product Hunt sources.
4. Add YouTube/Reddit/TikTok Creative Center/Google Trends observations within platform terms.
5. Calculate source-specific velocity and cross-source topic clusters.
6. Use Tavily to discover and extract primary evidence for the highest-ranked clusters.
7. Produce five evidence packs with citations, uncertainties, and rejection reasons.
8. Generate hooks/scripts only after verification.
9. Record tool costs and owned-post performance to improve routing.

## 9. Safety, originality, and platform rules

- Use official APIs, feeds, and public data whenever possible.
- Respect robots.txt, platform terms, rate limits, copyright, privacy, and account-access boundaries.
- Do not bypass authentication, CAPTCHAs, paywalls, or anti-bot controls.
- Do not request passwords, cookies, session tokens, or recovery codes.
- Do not copy or lightly paraphrase creator scripts.
- Do not describe a topic as viral/hottest without comparable measured data.
- No paid call, account connection, publishing action, file deletion, or external modification without explicit owner approval.

## 10. Primary references

- Tavily credits: https://docs.tavily.com/documentation/api-credits
- Exa pricing: https://exa.ai/docs/reference/pricing
- Exa monitors: https://exa.ai/docs/reference/monitors-api-guide
- Parallel pricing: https://docs.parallel.ai/getting-started/pricing
- Brave Search API: https://brave.com/search/api
- Firecrawl pricing: https://www.firecrawl.dev/pricing
- Perplexity pricing: https://docs.perplexity.ai/docs/getting-started/pricing
- Apify pricing: https://apify.com/pricing
- Hermes integrations: https://hermes-agent.nousresearch.com/docs/integrations
- OpenCode tools: https://opencode.ai/docs/tools
- Freebuff repository: https://github.com/CodebuffAI/freebuff
- Crawl4AI: https://github.com/unclecode/crawl4ai
- RSSHub: https://github.com/DIYgod/RSSHub
- changedetection.io: https://github.com/dgtlmoon/changedetection.io
- Hacker News API: https://github.com/HackerNews/API
- GitHub REST events/rates: https://docs.github.com/en/rest/activity/events and https://docs.github.com/rest/using-the-rest-api/rate-limits-for-the-rest-api
- OSS Insight trending repos: https://ossinsight.io/docs/api/list-trending-repos
- YouTube Data API: https://developers.google.com/youtube/v3/getting-started
- Google Trends API Alpha: https://developers.google.com/search/apis/trends
- TikTok Creative Center: https://ads.tiktok.com/business/creativecenter
- Product Hunt rate limits: https://api.producthunt.com/v2/docs/rate_limits/headers
- GDELT: https://www.gdeltproject.org/data.html
- Bluesky firehose: https://bsky.network/docs/consuming-the-firehose
- Reddit practitioner search-API discussion: https://www.reddit.com/r/LocalLLaMA/comments/1p0c1yw/what_is_the_most_accurate_web_search_api_for_llm
- Reddit cross-platform velocity anecdote: https://www.reddit.com/r/ContentCreators/comments/1ry27r8/built_trending_topic_detector_for_instagram_and
