#!/usr/bin/env python3
"""AINTM poster: upload the day's video to Postiz and schedule per-platform
posts at their peak slots.

Env: POSTIZ_API_KEY (Postiz settings -> API), POSTIZ_URL (default localhost:5000)
Usage: post_postiz.py --episode output/daily/DATE/episode.json --video FILE.mp4
       [--platforms tiktok,instagram,youtube,x] [--now]

Peak slots (America/Toronto): tiktok 19:00, instagram 19:00, youtube 12:00, x 09:00 (+1d if past).
Platform channel IDs are discovered from Postiz /integrations and cached in
config/postiz_channels.json (re-run with --refresh-channels after connecting new accounts).
"""
import argparse
import json
import mimetypes
import os
import sys
import urllib.request
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parent.parent
CHANNELS_CACHE = BASE / "config" / "postiz_channels.json"
TZ = ZoneInfo("America/Toronto")
PEAK = {"tiktok": 19, "instagram": 19, "youtube": 12, "x": 9,
        "facebook": 13, "linkedin": 10}


def api(path, method="GET", body=None, headers=None):
    url = os.environ.get("POSTIZ_URL", "http://127.0.0.1:5000") + "/api/public/v1" + path
    h = {"Authorization": os.environ["POSTIZ_API_KEY"]}
    h.update(headers or {})
    data = None
    if body is not None:
        if isinstance(body, bytes):
            data = body
        else:
            data = json.dumps(body).encode()
            h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def upload_video(path: Path):
    boundary = uuid.uuid4().hex
    mime = mimetypes.guess_type(path.name)[0] or "video/mp4"
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
            f"filename=\"{path.name}\"\r\nContent-Type: {mime}\r\n\r\n").encode() \
        + path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    return api("/upload", "POST", body,
               {"Content-Type": f"multipart/form-data; boundary={boundary}"})


def peak_slot(platform: str, now=None) -> str:
    now = now or datetime.now(TZ)
    hour = PEAK.get(platform, 12)
    slot = now.replace(hour=hour, minute=0, second=0, microsecond=0)
    if slot <= now + timedelta(minutes=10):
        slot += timedelta(days=1)
    return slot.isoformat()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", type=Path, required=True)
    ap.add_argument("--video", type=Path, required=True)
    ap.add_argument("--platforms", default="tiktok,instagram,youtube,x")
    ap.add_argument("--now", action="store_true", help="post immediately")
    ap.add_argument("--refresh-channels", action="store_true")
    args = ap.parse_args()

    if args.refresh_channels or not CHANNELS_CACHE.exists():
        integrations = api("/integrations")
        chans = {i["identifier"]: {"id": i["id"], "name": i.get("name", "")}
                 for i in integrations}
        CHANNELS_CACHE.write_text(json.dumps(chans, indent=1))
        print(f"channels: {list(chans)}")
        if args.refresh_channels:
            return

    chans = json.loads(CHANNELS_CACHE.read_text())
    ep = json.loads(args.episode.read_text())
    media = upload_video(args.video)

    posted, skipped = [], []
    for platform in args.platforms.split(","):
        platform = platform.strip()
        ch = chans.get(platform)
        if not ch:
            skipped.append(platform)
            continue
        if platform == "x":
            content = "\n\n".join(ep["captions"].get("x_thread", [""]))
        else:
            content = ep["captions"].get(platform, ep["captions"].get("tiktok", ""))
        body = {
            "type": "now" if args.now else "schedule",
            "date": datetime.now(TZ).isoformat() if args.now else peak_slot(platform),
            "posts": [{
                "integration": {"id": ch["id"]},
                "value": [{"content": content,
                           "image": [{"id": media["id"], "path": media["path"]}]}],
            }],
        }
        api("/posts", "POST", body)
        posted.append(f"{platform}@{body['date'][:16]}")

    print(f"scheduled: {posted}")
    if skipped:
        print(f"skipped (not connected in Postiz): {skipped}")


if __name__ == "__main__":
    main()
