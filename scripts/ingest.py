#!/usr/bin/env python3
"""AINTM ingest: pull candidate AI stories from RSS + HackerNews.

Outputs JSON list of candidates to stdout (or --out file), deduped against
a seen-URLs ledger so the same story is never offered twice.
Run daily at 06:00 by n8n. No API keys required.
"""
import argparse
import hashlib
import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from defusedxml import ElementTree

import yaml

BASE = Path(__file__).resolve().parent.parent
LEDGER = BASE / "output" / "seen_urls.json"
UA = {"User-Agent": "Mozilla/5.0 (AINTM news bot; contact via site)"}
MAX_AGE_HOURS = 36


def fetch(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def text_of(el, *names):
    for n in names:
        found = el.find(n)
        if found is not None and found.text:
            return found.text.strip()
    return ""


def parse_rss(name: str, raw: bytes):
    """Handle both RSS 2.0 and Atom."""
    out = []
    try:
        root = ElementTree.fromstring(raw)
    except ElementTree.ParseError:
        return out
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    items = root.findall(".//item") or root.findall(".//atom:entry", ns)
    for it in items[:15]:
        title = text_of(it, "title", "{http://www.w3.org/2005/Atom}title")
        link = text_of(it, "link")
        if not link:  # Atom link is an attribute
            le = it.find("{http://www.w3.org/2005/Atom}link")
            link = le.get("href", "") if le is not None else ""
        desc = text_of(it, "description",
                       "{http://www.w3.org/2005/Atom}summary",
                       "{http://www.w3.org/2005/Atom}content")
        desc = re.sub(r"<[^>]+>", " ", desc)[:600].strip()
        pub = text_of(it, "pubDate", "{http://www.w3.org/2005/Atom}published",
                      "{http://www.w3.org/2005/Atom}updated")
        if title and link:
            out.append({"source": name, "title": title, "url": link,
                        "summary": desc, "published": pub})
    return out


def recent_enough(published: str) -> bool:
    if not published:
        return True  # keep undated items; ranker can judge
    for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z",
                "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            dt = datetime.strptime(published.replace("GMT", "+0000"), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return datetime.now(timezone.utc) - dt < timedelta(hours=MAX_AGE_HOURS)
        except ValueError:
            continue
    return True


def fetch_hackernews(cfg):
    out = []
    try:
        ids = json.loads(fetch("https://hacker-news.firebaseio.com/v0/topstories.json"))[:60]
    except Exception:
        return out
    kws = [k.lower() for k in cfg.get("keywords", [])]
    for sid in ids:
        try:
            item = json.loads(fetch(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", 10))
        except Exception:
            continue
        if not item or item.get("score", 0) < cfg.get("min_score", 80):
            continue
        title = item.get("title", "")
        if not any(k in title.lower() for k in kws):
            continue
        out.append({"source": f"HackerNews ({item.get('score')} pts)",
                    "title": title,
                    "url": item.get("url") or f"https://news.ycombinator.com/item?id={sid}",
                    "summary": f"HN discussion: https://news.ycombinator.com/item?id={sid}",
                    "published": ""})
        if len(out) >= 10:
            break
        time.sleep(0.1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--config", type=Path, default=BASE / "config" / "sources.yml")
    args = ap.parse_args()

    cfg = yaml.safe_load(args.config.read_text())
    seen = set(json.loads(LEDGER.read_text())) if LEDGER.exists() else set()

    candidates = []
    for feed in cfg.get("rss", []):
        try:
            candidates += parse_rss(feed["name"], fetch(feed["url"]))
        except Exception as e:
            print(f"warn: {feed['name']}: {e}", file=sys.stderr)
    candidates += fetch_hackernews(cfg.get("hackernews", {}))

    fresh, new_hashes = [], []
    for c in candidates:
        h = hashlib.sha256(c["url"].encode()).hexdigest()[:16]
        if h in seen or not recent_enough(c["published"]):
            continue
        seen.add(h)
        new_hashes.append(h)
        c["id"] = h
        fresh.append(c)

    # persist ledger (cap size)
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(sorted(seen)[-5000:]))

    payload = json.dumps({"generated": datetime.now(timezone.utc).isoformat(),
                          "count": len(fresh), "stories": fresh}, indent=1)
    if args.out:
        args.out.write_text(payload)
        print(f"{len(fresh)} fresh stories -> {args.out}")
    else:
        print(payload)


if __name__ == "__main__":
    main()
