#!/usr/bin/env python3
"""GHA helper: attach chief assignment to a window packet. Host only."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

PIN = Path(__file__).resolve().parent


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", action="store_true")
    ap.add_argument("--hour", type=int, default=18)
    ap.add_argument("--lane", default="official")
    args = ap.parse_args()
    if not args.host:
        print("FAIL gha_packet refused-without --host")
        return 2
    if os.environ.get("MAC_BOX") == "1":
        print("FAIL gha_packet mac-box")
        return 2
    if args.hour not in {0, 6, 12, 18}:
        print("FAIL gha_packet fifth-window")
        return 2
    dest = PIN / "windows" / f"window-{args.hour:02d}.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_file():
        packet = json.loads(dest.read_text())
    else:
        packet = {
            "kind": "pulse-window-packet",
            "window_hour_utc": args.hour,
            "shortlist": [],
            "aired": False,
            "sold_now": False,
        }
    packet["aired"] = False
    packet["lane"] = args.lane
    staff_path = PIN / "staff.py"
    if staff_path.is_file():
        import importlib.util

        spec = importlib.util.spec_from_file_location("pulse_staff", staff_path)
        staff = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(staff)
        packet = staff.attach_window_packet(packet, lane=args.lane, hour=args.hour)
        packet["aired"] = False
    dest.write_text(json.dumps(packet, indent=2) + "\n")
    print("PASS gha_packet", dest, "aired", False, "assignment", packet.get("assignment_id"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
