# ATP agent-loop → ReceiptOS-PQ Adapter Plan

## 1) Source facts

- agent-loop HEAD: `bd708ab` (`Update README.md`)
- generated run path: `../agent-loop/runs/atp_photo_001`
- artifacts found:
  - `receipt.json`
  - `leases.json`
  - `public-keys.json`
  - `transcript.jsonl`
  - `envelopes.jsonl`
  - `lease-access-log.jsonl`
  - `verification.json`
  - `artifacts/manifest.json`
  - `artifacts/duplicate-candidates.csv`
  - `artifacts/album-plan.json`
  - `capability-card.json`
  - `contract.json`

## 2) Core observation

ReceiptOS-PQ should treat ATP output as a **receipt bundle**, not only a single `receipt.json` file.

## 3) Bundle inputs

- `receipt.json` = terminal Proof of Cognition receipt
- `leases.json` = structured lease boundary source
- `public-keys.json` = signer trust set source
- `transcript.jsonl` = event chain source
- `envelopes.jsonl` = signed protocol envelope provenance
- `lease-access-log.jsonl` = allowed/denied resource access audit trail
- `verification.json` = ATP baseline verification result

## 4) Mapping table

| ATP artifact/field | ReceiptOS-PQ verifier role |
|---|---|
| `receipt.json.receiptHash` | canonical receipt hash input |
| `receipt.json.eventRoot` | eventRoot / chain anchor |
| `receipt.json.signatures[]` | receipt-level signature proof |
| `receipt.json.transactionId` | correlation/idempotency candidate |
| `receipt.json.requested` | requested/action intent block |
| `receipt.json.accessed` | accessed resources/leases |
| `receipt.json.changed` | changed artifacts/external state |
| `receipt.json.approved` | approval block |
| `receipt.json.paid` | settlement block, optional for ReceiptOS-PQ MVP |
| `leases.json[]` | `context.leased_resources` normalization |
| `public-keys.json` | trust set **L** |
| `transcript.jsonl` | chain continuity / prev-hash validation |
| `envelopes.jsonl[].proofs[]` | envelope signature provenance |
| `lease-access-log.jsonl` | lease-boundary evidence / `LEASE_VIOLATION` checks |
| `verification.json` booleans | baseline ATP self-checks mapped to deterministic reason codes |

## 5) Reason-code mapping

- missing or invalid schema → `INVALID_SCHEMA`
- receiptHash mismatch → `TAMPER`
- receipt signature invalid → `BAD_SIGNATURE`
- signer not in public-keys/trust set → `UNTRUSTED_SIGNER`
- event chain mismatch → `CHAIN_PREV_HASH_MISMATCH`
- missing explicit sequence → adapter should synthesize sequence from transcript order or mark strict chain verification as unsupported
- repeated nonce/transactionId under policy → `REPLAY`
- timestamp outside policy → `CLOCK_SKEW`
- lease-access-log `allowed=false` or access not covered by lease → `LEASE_VIOLATION`
- all checks pass → `OK`

## 6) Gaps / normalization needed

- explicit integer sequence not observed
- explicit `lane_id` not observed
- nonce exists, but uniqueness policy must be defined
- reason-code output is not native; verification.json uses booleans
- leases are rich enough but need canonical ReceiptOS-PQ schema normalization
- changed.externalState exists, but may need stricter delta model
- ReceiptOS-PQ should verify ATP as a bundle, not only receipt.json

## 7) Proposed adapter CLI

```bash
python3 tools/atp_agent_loop_adapter.py \
 --run ../agent-loop/runs/atp_photo_001 \
 --lane classic_ed25519_v1 \
 --out artifacts/atp_adapter_verdict.json
```

Expected output:

```json
{
 "outcome": "OK",
 "source": "ATP_AGENT_LOOP",
 "transactionId": "...",
 "receiptHash": "...",
 "eventRoot": "...",
 "reason_code": "OK",
 "lane": "classic_ed25519_v1"
}
```

## 8) Scope

This is an adapter plan, not a completed implementation.
