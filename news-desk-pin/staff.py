#!/usr/bin/env python3
"""Lite staff router for GHA. Same denies. aired stays false."""
from __future__ import annotations

import json
import os
import uuid
from pathlib import Path

PIN = Path(__file__).resolve().parent
WINDOWS = {0, 6, 12, 18}


def _roster() -> dict:
    return json.loads((PIN / "STAFF.json").read_text())


def assign(work: str, *, lane: str = "official", hour: int | None = None, extra_roles=None) -> dict:
    if os.environ.get("MAC_BOX") == "1":
        return {"ok": False, "refuse": "mac-box", "aired": False}
    if hour is not None and hour not in WINDOWS:
        return {"ok": False, "refuse": "fifth-window", "aired": False}
    roster = _roster()
    needed = list(roster["work_kinds"][work])
    for extra in extra_roles or []:
        if extra not in needed:
            needed.append(extra)
    if work == "social_queue" and "skeptic" not in needed:
        needed.append("skeptic")
    aid = "asg-" + uuid.uuid4().hex[:12]
    return {
        "kind": "pulse-staff-assignment",
        "ok": True,
        "assignment_id": aid,
        "work": work,
        "lane": lane,
        "hour": hour,
        "assigned_to": {"desk": "pulse", "roles": needed, "chief": "chief"},
        "jobs": [{"role": r, "disjoint": True} for r in needed],
        "aired": False,
        "sold_now": False,
        "not_truth": lane == "social",
    }


def attach_window_packet(packet: dict, *, lane: str, hour: int) -> dict:
    out = dict(packet or {})
    lane = (lane or "official").lower()
    if lane == "social":
        asg = assign("social_queue", lane="social", hour=hour, extra_roles=["producer"])
    else:
        asg = assign("window_packet", lane="official" if lane != "country" else "country", hour=hour)
    out["lane"] = lane
    out["assignment"] = asg
    out["assignment_id"] = asg.get("assignment_id")
    out["assigned_to"] = asg.get("assigned_to")
    out["aired"] = False
    out["sold_now"] = False
    if lane == "social":
        out["not_truth"] = True
    return out
