#!/usr/bin/env python3
"""AINTM host runner: tiny localhost HTTP bridge so the n8n container can run
pipeline stages on the host (where Python dependencies, FFmpeg, model CLIs,
and generation credentials live).

Listens on 127.0.0.1:8484 (reachable from containers via host-gateway).
POST /run/<stage>  -> runs the stage synchronously, returns {ok, stdout, stderr}.
Stages are a fixed allowlist — nothing arbitrary is executable.
"""
import json
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PY = "python3"
STAGES = {
    "ingest": [PY, "scripts/ingest.py", "--out", "output/candidates.json"],
    "script": [PY, "scripts/rank_and_script.py",
               "--candidates", "output/candidates.json",
               "--out", "output/episode.json"],
    "render": [PY, "scripts/render_daily.py",
               "--episode", "output/episode.json",
               "--out", "output/today.mp4"],
    "post": [PY, "scripts/post_postiz.py",
             "--episode", "output/episode.json",
             "--video", "output/today.mp4"],
    "episode": ["cat", "output/episode.json"],
}
TIMEOUT = {"ingest": 300, "script": 700, "render": 900, "post": 300, "episode": 10}


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        stage = self.path.strip("/").removeprefix("run/")
        if stage not in STAGES:
            self._reply(404, {"ok": False, "error": f"unknown stage {stage!r}"})
            return
        try:
            r = subprocess.run(STAGES[stage], cwd=BASE, capture_output=True,
                               text=True, timeout=TIMEOUT[stage])
            self._reply(200 if r.returncode == 0 else 500,
                        {"ok": r.returncode == 0, "stage": stage,
                         "stdout": r.stdout[-4000:], "stderr": r.stderr[-2000:]})
        except subprocess.TimeoutExpired:
            self._reply(500, {"ok": False, "stage": stage, "error": "timeout"})

    def _reply(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} {fmt % args}", flush=True)


if __name__ == "__main__":
    print("AINTM runner on 127.0.0.1:8484", flush=True)
    HTTPServer(("0.0.0.0", 8484), Handler).serve_forever()
