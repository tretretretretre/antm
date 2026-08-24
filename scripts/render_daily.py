#!/usr/bin/env python3
"""AINTM Tier-1 renderer: episode.json -> finished 1080x1920 vertical video.

Pipeline: edge-tts voice (word-timed) -> Gemini images (or branded fallback
cards) -> ffmpeg assembly with Ken Burns motion, karaoke captions, logo
watermark, intro sting / outro jingle / music bed when those files exist.

Degrades gracefully: missing GEMINI_API_KEY, logo, or audio assets reduce
polish but never block a render.
"""
import argparse
import asyncio
import base64
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

import edge_tts

BASE = Path(__file__).resolve().parent.parent
BRAND_BG = "0x0f0f1a"  # deep navy fallback card color
W, H, FPS = 1080, 1920, 30
GEMINI_MODEL = "gemini-2.5-flash-image"


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.exit(f"cmd failed: {' '.join(map(str, cmd))[:200]}\n{r.stderr[-800:]}")
    return r


def ffprobe_dur(path: Path) -> float:
    r = run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(path)])
    return float(r.stdout.strip())


# ---------- TTS with word boundaries ----------
async def tts(script: str, voice: str, out_mp3: Path):
    words = []
    comm = edge_tts.Communicate(script, voice, rate="+8%", boundary="WordBoundary")
    with open(out_mp3, "wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                words.append((chunk["offset"] / 1e7,
                              (chunk["offset"] + chunk["duration"]) / 1e7,
                              chunk["text"]))
    return words


def ass_time(t: float) -> str:
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def write_captions(words, offset: float, out_ass: Path):
    """Group words into <=3-word chunks, big bold centered captions."""
    header = f"""[Script Info]
PlayResX: {W}
PlayResY: {H}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Outline, Shadow, Alignment, MarginL, MarginR, MarginV
Style: Cap,DejaVu Sans,84,&H00FFFFFF,&H00000000,&H80000000,-1,5,2,2,60,60,420

[Events]
Format: Layer, Start, End, Style, Text
"""
    lines = []
    for i in range(0, len(words), 3):
        chunk = words[i:i + 3]
        start, end = chunk[0][0] + offset, chunk[-1][1] + offset
        txt = " ".join(w[2] for w in chunk).upper().replace("{", "").replace("}", "")
        lines.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Cap,{txt}")
    out_ass.write_text(header + "\n".join(lines))


# ---------- images ----------
def gemini_image(prompt: str, out_png: Path, ref_images: list[Path]) -> bool:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return False
    parts = [{"text": f"{prompt}. Vertical 9:16 composition, 1080x1920."}]
    for ref in ref_images[:3]:
        parts.append({"inline_data": {"mime_type": "image/png" if ref.suffix == ".png"
                                      else "image/jpeg",
                                      "data": base64.b64encode(ref.read_bytes()).decode()}})
    body = json.dumps({"contents": [{"parts": parts}],
                       "generationConfig": {"responseModalities": ["IMAGE"],
                                            "imageConfig": {"aspectRatio": "9:16"}}}).encode()
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent",
        data=body, headers={"Content-Type": "application/json", "x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            resp = json.load(r)
        for part in resp["candidates"][0]["content"]["parts"]:
            if "inlineData" in part:
                out_png.write_bytes(base64.b64decode(part["inlineData"]["data"]))
                return True
    except Exception as e:
        print(f"warn: gemini image failed: {e}", file=sys.stderr)
    return False


def fallback_card(text: str, out_png: Path):
    """Branded solid card with wrapped headline text."""
    wrapped = "\n".join(text[i:i + 22] for i in range(0, min(len(text), 88), 22))
    tf = out_png.with_suffix(".txt")
    tf.write_text(wrapped)
    run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c={BRAND_BG}:s={W}x{H}",
         "-vf", f"drawtext=textfile={tf}:fontcolor=white:fontsize=72:"
                f"x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=20",
         "-frames:v", "1", str(out_png)])
    tf.unlink()


# ---------- assembly ----------
def build_video(images, voice_mp3, ass_file, ep, workdir: Path, out_mp4: Path):
    brand = BASE / "assets" / "brand" / "logo.png"
    intro = BASE / "assets" / "audio" / "intro.wav"
    outro = BASE / "assets" / "audio" / "outro.wav"
    beds = sorted((BASE / "assets" / "audio" / "beds").glob("*")) if \
        (BASE / "assets" / "audio" / "beds").exists() else []

    intro_d = ffprobe_dur(intro) if intro.exists() else 0.0
    outro_d = ffprobe_dur(outro) if outro.exists() else 0.0
    voice_d = ffprobe_dur(voice_mp3)
    main_d = voice_d + 0.6
    total_d = intro_d + main_d + outro_d
    per_img = main_d / len(images)

    inputs, fparts = [], []
    for i, img in enumerate(images):
        inputs += ["-loop", "1", "-t", f"{per_img + (intro_d if i == 0 else 0) + (outro_d if i == len(images)-1 else 0):.3f}", "-i", str(img)]
        frames = int((per_img + (intro_d if i == 0 else 0) + (outro_d if i == len(images)-1 else 0)) * FPS)
        fparts.append(
            f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,"
            f"crop={W}:{H},zoompan=z='min(zoom+0.0006,1.10)':d={frames}"
            f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
            f"setsar=1[v{i}];")
    concat = "".join(f"[v{i}]" for i in range(len(images)))
    fparts.append(f"{concat}concat=n={len(images)}:v=1:a=0[vseq];")

    vlabel = "vseq"
    n_img = len(images)
    if brand.exists():
        inputs += ["-i", str(brand)]
        fparts.append(f"[{n_img}:v]scale=180:-1[logo];"
                      f"[{vlabel}][logo]overlay=W-w-40:60[vlogo];")
        vlabel = "vlogo"
    ass_esc = str(ass_file).replace(":", r"\:")
    fparts.append(f"[{vlabel}]ass='{ass_esc}'[vfinal]")

    # audio graph: voice delayed past intro; bed under voice; sting/jingle at ends
    a_inputs_start = n_img + (1 if brand.exists() else 0)
    ain, amix = [], []
    def add_audio(path, filt):
        nonlocal a_inputs_start
        ain.append(("-i", str(path)))
        amix.append(f"[{a_inputs_start}:a]{filt}[a{len(amix)}];")
        a_inputs_start += 1

    add_audio(voice_mp3, f"adelay={int(intro_d*1000)}|{int(intro_d*1000)},volume=1.0")
    if intro.exists():
        add_audio(intro, "volume=0.9")
    if outro.exists():
        add_audio(outro, f"adelay={int((intro_d+main_d)*1000)}|{int((intro_d+main_d)*1000)},volume=0.9")
    if beds:
        add_audio(beds[hash(ep['date']) % len(beds)],
                  f"aloop=loop=-1:size=2e9,atrim=0:{total_d:.2f},"
                  f"adelay={int(intro_d*1000)}|{int(intro_d*1000)},volume=0.12")
    labels = "".join(f"[a{i}]" for i in range(len(amix)))
    amix.append(f"{labels}amix=inputs={len(amix)}:normalize=0[afinal]")

    flat_ain = [x for pair in ain for x in pair]
    fgraph = "".join(fparts) + ";" + "".join(amix)
    run(["ffmpeg", "-y", *inputs, *flat_ain,
         "-filter_complex", fgraph,
         "-map", "[vfinal]", "-map", "[afinal]",
         "-t", f"{total_d:.2f}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "21",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", str(out_mp4)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    ep = json.loads(args.episode.read_text())
    workdir = BASE / "output" / "daily" / ep["date"]
    workdir.mkdir(parents=True, exist_ok=True)
    out_mp4 = args.out or workdir / f"aintm_{ep['date']}.mp4"

    # 1. voice
    voice_mp3 = workdir / "voice.mp3"
    words = asyncio.run(tts(ep["script"], ep["voice"], voice_mp3))
    print(f"voice: {ffprobe_dur(voice_mp3):.1f}s, {len(words)} words")

    # 2. images (first = anchor shot with the girl's reference images)
    girl_dir = BASE / "assets" / "characters" / ep["girl"]
    refs = sorted([p for p in girl_dir.glob("*") if p.suffix.lower() in
                   (".png", ".jpg", ".jpeg")])
    images = []
    prompts = ep["image_prompts"][:6]
    anchor_prompt = (f"News anchor {ep['girl_name']} (match the reference person "
                     f"exactly) in a sleek futuristic newsroom, presenting to "
                     f"camera. On-screen headline: {ep['headline']}")
    for i, prompt in enumerate([anchor_prompt] + prompts):
        img = workdir / f"img{i}.png"
        ok = gemini_image(prompt, img, refs if i == 0 else [])
        if not ok:
            fallback_card(ep["headline"] if i == 0 else prompt[:80], img)
        images.append(img)

    # 3. captions
    intro = BASE / "assets" / "audio" / "intro.wav"
    intro_d = ffprobe_dur(intro) if intro.exists() else 0.0
    ass_file = workdir / "captions.ass"
    write_captions(words, intro_d, ass_file)

    # 4. assemble
    build_video(images, voice_mp3, ass_file, ep, workdir, out_mp4)
    print(f"DONE: {out_mp4} ({ffprobe_dur(out_mp4):.1f}s)")


if __name__ == "__main__":
    main()
