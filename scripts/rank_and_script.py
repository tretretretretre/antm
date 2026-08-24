#!/usr/bin/env python3
"""AINTM rank + scriptwrite: feed candidate stories to headless Claude (Max sub,
$0 API cost) to pick the top stories and write the day's video script in the
rotating character's voice.

Usage: rank_and_script.py --candidates output/candidates.json --out output/episode.json
Rotation state lives in output/rotation.json (girl1 -> girl2 -> girl3 -> ...).
"""
import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parent.parent
CHARS = BASE / "assets" / "characters" / "CHARACTERS.yml"
ROTATION = BASE / "output" / "rotation.json"

PROMPT = """You are the head writer for "A.I.'s Next Top Models", a short-form
daily AI-news show fronted by AI anchor characters. Today's anchor:

Name: {name}
Personality: {personality}

Below are today's candidate stories (JSON). Do all of the following:

1. RANK: pick the {n_stories} stories with the highest viral potential for a
   general TikTok/Reels/Shorts audience (novelty, stakes, "wait, what?" factor,
   visual potential). Ignore incremental/enterprise news unless huge.
2. VERIFY TONE: only claims supported by the provided title/summary — never
   invent numbers, quotes, or details not present in the source material.
3. SCRIPT: write one 30-45 second spoken script (75-110 words) covering the top
   story (mention story 2 in one closing line if strong). Structure:
   HOOK (first line, <=8 words, no greeting) -> WHAT HAPPENED -> WHY IT MATTERS
   -> sign-off in character. Write it in {name}'s voice throughout.
   It must sound natural READ ALOUD by TTS: short sentences, no headers, no
   emojis, no URLs, spell out numbers/acronyms the natural spoken way.
4. CAPTIONS: per-platform caption + hashtags (tiktok, instagram, youtube, x).
   X gets a 2-3 tweet thread text instead of a caption.
5. VISUALS: 4-6 image prompts for b-roll stills matching script beats. Each
   prompt must be self-contained, photorealistic-editorial style, 9:16.
6. HEADLINE: <=8 word on-screen headline for the video's title card.

Return ONLY valid JSON, no markdown fence, with keys:
  chosen_story: {{id, title, url, source}}
  runner_up: {{id, title}} or null
  headline: str
  script: str
  captions: {{tiktok: str, instagram: str, youtube: str, x_thread: [str]}}
  image_prompts: [str]

CANDIDATE STORIES:
{stories}
"""


def next_girl(chars: dict) -> str:
    state = json.loads(ROTATION.read_text()) if ROTATION.exists() else {}
    if state.get("date") == date.today().isoformat():
        return state["girl"]  # idempotent within a day
    order = ["girl1", "girl2", "girl3"]
    girl = order[(order.index(state.get("girl", "girl3")) + 1) % 3]
    ROTATION.write_text(json.dumps({"date": date.today().isoformat(), "girl": girl}))
    return girl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--n-stories", type=int, default=3)
    args = ap.parse_args()

    chars = yaml.safe_load(CHARS.read_text())
    girl_key = next_girl(chars)
    girl = chars[girl_key]
    if not girl.get("name"):
        sys.exit(f"error: {girl_key} has no name in CHARACTERS.yml — fill it in first")

    stories = json.loads(args.candidates.read_text())["stories"]
    if not stories:
        sys.exit("error: no fresh stories today")

    prompt = PROMPT.format(name=girl["name"], personality=girl["personality"],
                           n_stories=args.n_stories,
                           stories=json.dumps(stories, indent=1))

    r = subprocess.run(["claude", "-p", "--output-format", "text"],
                       input=prompt, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        sys.exit(f"claude failed: {r.stderr[:500]}")

    raw = r.stdout.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1].removeprefix("json").strip()
    episode = json.loads(raw)  # hard-fail loudly if Claude returned non-JSON

    episode["girl"] = girl_key
    episode["girl_name"] = girl["name"]
    episode["voice"] = girl["voice"]
    episode["date"] = date.today().isoformat()
    args.out.write_text(json.dumps(episode, indent=1))
    print(f"episode ({girl['name']}) -> {args.out}")


if __name__ == "__main__":
    main()
