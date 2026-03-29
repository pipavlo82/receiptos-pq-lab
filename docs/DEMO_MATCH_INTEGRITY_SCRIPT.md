# Demo Script: Match Integrity (3–5 min)

## Goal
Show that off-chain game match events can be verified with deterministic failure semantics.

## Setup
- Demo payloads: `examples/gaming/demo_match_integrity/`
- CLI helper: `scripts/demo_match_integrity.py`

Run:
```bash
python3 scripts/demo_match_integrity.py
```

---

## Step-by-step flow

### 1) Show valid receipt
Use `valid_match_result_receipt.json`.

What to say:
- This is a canonical match result event.
- It includes extension mode `hybrid` (signature + entropy context).
- Verification should return `valid=true` and `reason_code=OK`.

### 2) Explain chain continuity
Point to `chain.prev_hash` + `chain.seq`.

What to say:
- Event continuity is tracked to detect missing/reordered events.
- Continuity is part of integrity semantics, not just payload integrity.

### 3) Show tampered receipt -> fail
Use `tampered_match_result_receipt.json`.

What to say:
- Winner/score/signature path is altered.
- Verification returns deterministic fail (`reason_code` expected fail-class, often `HYBRID_PARTIAL_FAILURE` / `VERIFY_FAILED`).

### 4) Show continuity/replay failure
Use `invalid_continuity_match_result_receipt.json`.

What to say:
- `prev_hash` is intentionally mismatched.
- Continuity check flags failure (`CONTINUITY_MISMATCH` in demo helper continuity layer).

### 5) Show richer historical payload (`vector_raw`)
Use `fixtures/mldsa/vector_raw.json` through historical loader.

What to say:
- Contains digest + PQ signature + PQ pubkey + metadata/signer context.
- Useful for provenance/hybrid narrative beyond minimal test vector.

### 6) Optional: Hardhat anchor demo
- `anchorReceipt(bytes32)`
- duplicate anchor rejection

What to say:
- On-chain is minimal anchoring/integrity harness.
- Full verification remains off-chain first.

---

## What this proves
- Deterministic verification outcomes
- Tamper and continuity failures are explicit
- Hybrid provenance payloads can be normalized into the same verification pipeline
- Optional on-chain anchor path complements off-chain verification
