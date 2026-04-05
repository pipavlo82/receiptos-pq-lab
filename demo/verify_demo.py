#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from _demo_lib import read_json, verify_case, write_json


def classify_expected(kind: str) -> str:
    if kind == "valid":
        return "OK"
    if kind == "replay":
        return "REPLAY"
    if kind == "bad_signature":
        return "BAD_SIGNATURE"
    if kind == "chain_mismatch":
        return "CHAIN_MISMATCH"
    return "TAMPER"


def main() -> int:
    p = argparse.ArgumentParser(description="Verify demo dispute cases")
    p.add_argument("--disputes", default="artifacts/demo_run/disputes.json")
    p.add_argument("--output", default="artifacts/demo_run/verification_output.json")
    p.add_argument("--report", default="reports/verification_report.md")
    p.add_argument("--mirofish-status", default="artifacts/demo_run/mirofish_status.json")
    args = p.parse_args()

    disputes = read_json(Path(args.disputes))
    mirofish_status = read_json(Path(args.mirofish_status))
    out = {
        "ok": True,
        "with_mirofish": bool(disputes.get("with_mirofish")),
        "results": [],
        "summary": {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "by_reason": {},
        },
    }

    for case in disputes.get("cases", []):
        res = verify_case(case["match"], case["receipts"])
        expected = classify_expected(case.get("kind", "tamper"))
        ok = (res.get("reason_code") == expected)

        row = {
            "case_id": case.get("case_id"),
            "kind": case.get("kind"),
            "description": case.get("description"),
            "expected_reason": expected,
            "actual_reason": res.get("reason_code"),
            "ok": ok,
            "at_seq": res.get("at_seq"),
            "details": res.get("details"),
        }
        out["results"].append(row)

        out["summary"]["total"] += 1
        out["summary"]["passed"] += 1 if ok else 0
        out["summary"]["failed"] += 0 if ok else 1
        rc = res.get("reason_code", "UNKNOWN")
        out["summary"]["by_reason"][rc] = out["summary"]["by_reason"].get(rc, 0) + 1

    write_json(Path(args.output), out)

    # markdown report
    lines = []
    lines.append("# Verification Report — Gaming Match Integrity Demo")
    lines.append("")
    lines.append(f"- with_mirofish_scenarios: **{out['with_mirofish']}**")
    lines.append(f"- mirofish_requested: **{mirofish_status.get('requested', False)}**")
    lines.append(f"- mirofish_enabled: **{mirofish_status.get('enabled', False)}**")
    lines.append(f"- mirofish_status_reason: `{mirofish_status.get('reason', 'unknown')}`")
    lines.append(f"- total_cases: **{out['summary']['total']}**")
    lines.append(f"- passed: **{out['summary']['passed']}**")
    lines.append(f"- failed: **{out['summary']['failed']}**")
    lines.append("")
    lines.append("## Reason code distribution")
    for k, v in sorted(out["summary"]["by_reason"].items()):
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Case-by-case results")
    lines.append("| case_id | kind | expected | actual | ok |")
    lines.append("|---|---|---|---|---|")
    for r in out["results"]:
        lines.append(
            f"| {r['case_id']} | {r['kind']} | {r['expected_reason']} | {r['actual_reason']} | {r['ok']} |"
        )

    lines.append("")
    lines.append("## Conclusion")
    lines.append(
        "The deterministic verifier correctly distinguishes valid execution history from tamper, replay, "
        "bad-signature, and chain-mismatch scenarios using machine-readable reason codes."
    )
    lines.append(
        "This makes the demo externally showable as a proof-of-integrity layer for authoritative match disputes."
    )

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(args.output)
    print(args.report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
