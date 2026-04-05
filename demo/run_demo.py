#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from _demo_lib import make_receipts, read_json, write_json


ART = Path("artifacts/demo_run")


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> int:
    p = argparse.ArgumentParser(description="One-command polished external demo")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--symbol", default="XBTUSD")
    p.add_argument("--with-mirofish", action="store_true")
    args = p.parse_args()

    ART.mkdir(parents=True, exist_ok=True)

    # 1) deterministic match generation
    run([
        "python3",
        "demo/generate_match.py",
        "--seed",
        str(args.seed),
        "--symbol",
        args.symbol,
        "--output",
        str(ART / "match.json"),
    ])

    match = read_json(ART / "match.json")

    # 2) receipt generation
    receipts = make_receipts(match["events"])
    write_json(ART / "receipts.json", receipts)
    write_json(ART / "receipts_chain.json", receipts)

    # 3) dispute scenarios
    dispute_cmd = [
        "python3",
        "demo/simulate_dispute.py",
        "--match",
        str(ART / "match.json"),
        "--receipts",
        str(ART / "receipts_chain.json"),
        "--output",
        str(ART / "disputes.json"),
    ]
    mirofish_status = {
        "requested": bool(args.with_mirofish),
        "enabled": False,
        "reason": "not_requested",
    }
    if args.with_mirofish:
        dispute_cmd.append("--with-mirofish")
        try:
            run(dispute_cmd)
            mirofish_status = {
                "requested": True,
                "enabled": True,
                "reason": "ok",
            }
        except Exception as e:
            # graceful fallback: rerun without optional MiroFish scenarios
            fallback_cmd = [c for c in dispute_cmd if c != "--with-mirofish"]
            run(fallback_cmd)
            mirofish_status = {
                "requested": True,
                "enabled": False,
                "reason": f"optional_step_skipped: {type(e).__name__}",
            }
    else:
        run(dispute_cmd)

    write_json(ART / "mirofish_status.json", mirofish_status)

    # 4) verification + report
    run([
        "python3",
        "demo/verify_demo.py",
        "--disputes",
        str(ART / "disputes.json"),
        "--output",
        str(ART / "verification_output.json"),
        "--report",
        "reports/verification_report.md",
        "--mirofish-status",
        str(ART / "mirofish_status.json"),
    ])

    print("\nDEMO OK")
    print(f"- match: {ART / 'match.json'}")
    print(f"- receipts: {ART / 'receipts.json'}")
    print(f"- chain: {ART / 'receipts_chain.json'}")
    print(f"- disputes: {ART / 'disputes.json'}")
    print(f"- verification: {ART / 'verification_output.json'}")
    print("- report: reports/verification_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
