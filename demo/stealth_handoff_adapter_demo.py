#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.stealth_handoff_adapter import adapt_stealth_handoff_evidence


def main() -> int:
    parser = argparse.ArgumentParser(description="Run ReceiptOS-PQ adapter demo for Stealth handoff evidence")
    parser.add_argument(
        "--input",
        default="examples/stealth/session-evidence.v0.sample.json",
        help="Path to Stealth handoff evidence JSON",
    )
    parser.add_argument(
        "--output",
        default="artifacts/stealth_adapter_output.json",
        help="Path to write verifier-style output JSON",
    )
    args = parser.parse_args()

    evidence = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = adapt_stealth_handoff_evidence(evidence)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(out_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
