#!/usr/bin/env python3
"""receiptos_outreach_monitor_v1

Checks configured GitHub threads for new comments and prepares simple classifications
+ reply drafts for multiplayer/backend outreach.

Usage:
  python tools/outreach_monitor_v1.py --config docs/market_probe/multiplayer_threads.json
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


CLASSES = ["CONFUSED", "INTERESTED", "DISMISSIVE", "REDIRECT"]


def gh_issue_view(repo: str, number: int) -> dict:
    cmd = [
        "gh",
        "issue",
        "view",
        str(number),
        "-R",
        repo,
        "--json",
        "url,title,comments",
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or f"gh failed for {repo}#{number}")
    return json.loads(p.stdout)


def classify(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["who are you", "what exactly", "not sure", "don’t understand", "dont understand"]):
        return "CONFUSED"
    if any(k in t for k in ["useful", "how integrate", "show demo", "interesting", "can you share"]):
        return "INTERESTED"
    if any(k in t for k in ["off-topic", "spam", "not relevant", "stop", "no thanks"]):
        return "DISMISSIVE"
    if any(k in t for k in ["better in", "post in", "ask in", "use-case is"]):
        return "REDIRECT"
    return "INTERESTED"


def draft_reply(cls: str) -> str:
    if cls == "CONFUSED":
        return (
            "Fair question. I’m testing a minimal integrity check for real-time event histories: "
            "valid sequence -> PASS, tamper/replay -> FAIL. Not anti-cheat replacement, "
            "just post-match evidence for dispute handling."
        )
    if cls == "INTERESTED":
        return (
            "Great — I can share the tiny verifier + 3 fixtures (valid/tamper/replay) and how it fits "
            "into authoritative server logs without changing core gameplay logic."
        )
    if cls == "DISMISSIVE":
        return "Thanks for the direct feedback — understood. I’ll stop here in this thread."
    return (
        "Makes sense. If you point me to the better-fit workflow/thread, I’ll adapt the message "
        "to that context."
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", default="docs/market_probe/outreach_monitor_report.json")
    args = ap.parse_args()

    config_path = Path(args.config)
    out_path = Path(args.out)
    cfg = json.loads(config_path.read_text(encoding="utf-8"))

    me = cfg.get("self_login", "pipavlo82").lower()
    rows = []

    for item in cfg.get("threads", []):
        repo = item["repo"]
        number = int(item["number"])
        try:
            data = gh_issue_view(repo, number)
            comments = data.get("comments", [])
            inbound = []
            for c in comments:
                author = (c.get("author") or {}).get("login", "").lower()
                if author and author != me:
                    inbound.append(c)

            if inbound:
                last = inbound[-1]
                body = (last.get("body") or "").strip()
                cls = classify(body)
                row = {
                    "repo": repo,
                    "thread": data.get("url"),
                    "title": data.get("title"),
                    "has_new_signal": True,
                    "response_type": cls,
                    "quote": body[:240],
                    "next_action": draft_reply(cls),
                    "comment_count": len(comments),
                    "last_comment_at": last.get("createdAt"),
                }
            else:
                row = {
                    "repo": repo,
                    "thread": data.get("url"),
                    "title": data.get("title"),
                    "has_new_signal": False,
                    "response_type": None,
                    "quote": None,
                    "next_action": "wait",
                    "comment_count": len(comments),
                    "last_comment_at": None,
                }
        except Exception as e:
            row = {
                "repo": repo,
                "thread": None,
                "title": None,
                "has_new_signal": False,
                "response_type": None,
                "quote": None,
                "next_action": "check_auth_or_permissions",
                "error": str(e),
            }
        rows.append(row)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "signal_count": sum(1 for r in rows if r.get("has_new_signal")),
        "threads_total": len(rows),
        "rows": rows,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    md = [
        "# Outreach Monitor Report v1",
        "",
        f"- generated_at: {summary['generated_at']}",
        f"- threads_total: {summary['threads_total']}",
        f"- signal_count: {summary['signal_count']}",
        "",
        "| repo | signal | class | next_action |",
        "|---|---:|---|---|",
    ]
    for r in rows:
        md.append(
            f"| {r['repo']} | {'yes' if r.get('has_new_signal') else 'no'} | {r.get('response_type') or '-'} | {r.get('next_action','-')} |"
        )
    Path("docs/market_probe/outreach_monitor_report.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "out_json": str(out_path), "signals": summary["signal_count"]}))


if __name__ == "__main__":
    main()
