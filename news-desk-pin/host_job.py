#!/usr/bin/env python3
"""Host-only deadline job. Prefers full dry_runner; falls back to gha_packet."""
from __future__ import annotations
import argparse, json, os, subprocess, sys
from pathlib import Path
PIN = Path(__file__).resolve().parent
WINDOWS = {0, 6, 12, 18}

def die(msg, code=2):
    print("FAIL host_job", msg); raise SystemExit(code)

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", action="store_true")
    ap.add_argument("--hour", type=int, default=18)
    ap.add_argument("--country", default="NG")
    ap.add_argument("--lane", default="official")
    ap.add_argument("--wrap-only", action="store_true", default=True)
    ap.add_argument("--live", action="store_true")
    args = ap.parse_args(argv)
    if not args.host: die("refused-without --host")
    if os.environ.get("MAC_BOX") == "1": die("refused-MAC_BOX", 2)
    if args.hour not in WINDOWS: die("fifth-window")
    dry = PIN / "dry_runner.py"
    env = os.environ.copy(); env["MAC_BOX"] = "0"
    if dry.is_file():
        r = subprocess.run([sys.executable, str(dry), "--hour", str(args.hour), "--country", args.country], cwd=str(PIN.parent), env=env)
        if r.returncode != 0:
            print("HOLD dry-runner-missing-or-fail; using gha_packet")
    helper = PIN / "gha_packet.py"
    r = subprocess.run([sys.executable, str(helper), "--host", "--hour", str(args.hour), "--lane", args.lane], cwd=str(PIN.parent), env=env)
    if r.returncode != 0:
        die(f"gha-packet-exit-{r.returncode}")
    out = PIN / "windows" / f"window-{args.hour:02d}.json"
    if not out.is_file():
        die("missing-packet")
    packet = json.loads(out.read_text())
    packet["aired"] = False
    out.write_text(json.dumps(packet, indent=2) + "\n")
    print("PASS host_job", "window", args.hour, "aired", False, "out", out)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
