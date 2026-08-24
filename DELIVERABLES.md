# AINTM — What I need from you (exact spec)

Ordered by what unblocks the machine fastest. Tick them off in any order; #1–#3 are the critical path.

## 1. Telegram (2 minutes) — unblocks approval gates
- Open t.me/AINTM_bot and press **Start**.
- Re-paste the bot token in chat (Telegram → @BotFather → `/mytoken` → @AINTM_bot). It was never saved to `config/.env`.

## 2. The girls (paste in chat + drop files) — unblocks script pipeline test
Paste for **each** of the 3 girls:
- Name
- 2–3 personality lines (tone, what she covers, catchphrase if any)
- Keep or change her assigned voice: girl1 = Aria (energetic US), girl2 = Jenny (warm US), girl3 = Sonia (crisp UK). Preview others: `edge-tts --list-voices`

Drop **3–5 images per girl** into `assets/characters/girl1/`, `girl2/`, `girl3/` (any filenames):
- At least: 1 front-facing head-and-shoulders "selfie" (neutral), 1 smiling, 1 waist-up
- Same face, hair, and style across all of her images (consistency is what Gemini locks onto)
- Portrait orientation, ≥1080px wide, PNG or JPG, HD, no watermarks, no other people, clean/simple background

Logo → `assets/brand/logo.png` — transparent PNG, ≥1024px.

## 3. Postiz (3 minutes) — unblocks posting layer
- Open http://localhost:5000 → register (first account becomes admin)
- Settings → API key → paste it in chat

## 4. Existing accounts inventory (paste in chat) — unblocks platform plan
Since we're reusing accounts under ADUSON: for each account you'll use, paste:
- Platform, current handle, rough follower count
- Whether you can rename/rebrand it now or later
- Which email it's attached to

## 5. Watch the test video (2 minutes)
`output/daily/2026-08-16/aintm_2026-08-16.mp4` — reply with verdict on voice, caption style, pacing, image quality.

## 6. Audio (never blocks launch — deliver when ready)
All files: **WAV, 48 kHz, stereo, 24-bit, peaks ≤ −1 dBTP, loudness ≈ −14 LUFS.**
Deliver at full mix level — the pipeline ducks music under voice automatically.

| File | Spec |
|---|---|
| `assets/audio/intro.wav` | 2–3s brand sting. High energy, ends clean (short tail) so the voice can enter immediately. |
| `assets/audio/outro.wav` | 3–5s jingle. Leave sonic space (thinner mix / bed level) for the spoken tagline "follow for daily AI news" over top. |
| `assets/audio/beds/bed_hype.wav` | 60s **seamless loop**, instrumental, breaking-news energy (girl1's stories) |
| `assets/audio/beds/bed_chill.wav` | 60s seamless loop, instrumental, calm/analytical (girl2) |
| `assets/audio/beds/bed_witty.wav` | 60s seamless loop, instrumental, playful/cheeky (girl3) |

Bed rules: no vocal chops or lead melodies in the speech band (300 Hz–3 kHz kept sparse), loop point inaudible, more beds welcome later (`bed_*.wav`).

---
Already done for you today: runner service installed + enabled (`systemctl --user status aintm-runner`) — survives reboot.
