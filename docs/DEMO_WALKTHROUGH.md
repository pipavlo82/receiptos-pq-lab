# Demo Walkthrough (2 minutes)

## 1) One command

```bash
cd /mnt/d/receiptos-pq-lab
python3 demo/run_demo.py
```

Optional:
```bash
python3 demo/run_demo.py --with-mirofish
```

---

## 2) What happens

1. `demo/generate_match.py` creates deterministic match events.
2. `demo/run_demo.py` generates receipts + receipt chain.
3. `demo/simulate_dispute.py` creates dispute cases (tamper/replay/altered/etc).
4. `demo/verify_demo.py` verifies all cases and writes reason-coded output + report.

---

## 3) Expected output files

- `artifacts/demo_run/match.json`
- `artifacts/demo_run/receipts.json`
- `artifacts/demo_run/receipts_chain.json`
- `artifacts/demo_run/disputes.json`
- `artifacts/demo_run/verification_output.json`
- `reports/verification_report.md`

---

## 4) Example reason codes

- `OK` → valid baseline match integrity
- `TAMPER` → event payload/result changed after signing
- `REPLAY` → duplicate event/receipt detected
- `BAD_SIGNATURE` → signature mismatch/forged receipt
- `CHAIN_MISMATCH` → broken `prev_hash` continuity

---

## 5) How to read the report

Open `reports/verification_report.md` and check:

1. **Summary**: total/passed/failed.
2. **Reason code distribution**: counts per code.
3. **Case table**: expected vs actual per dispute scenario.

If valid case is `OK` and all attack cases map to expected reason codes, demo is successful.
