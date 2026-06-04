# Stealth Handoff Adapter v0

## Purpose

This demo adapter is the smallest bridge from **Stealth handoff evidence** to a **ReceiptOS-PQ verifier-style result**.

It does **not** add real PQ signatures yet.
It only proves the adapter seam:

`stealth.session.evidence.v0` -> normalized ReceiptOS-PQ-style receipt bundle -> verifier-style output

## Input

Sample input:
- `examples/stealth/session-evidence.v0.sample.json`

Expected source shape:
- `schema`
- `session_id`
- `directory`
- `task`
- `agent`
- `scope`
- `commands`
- `changes`
- `metadata`

## Output

Stable verifier-style output fields:
- `valid`
- `reason_code`
- `checks`
- `fail_path`
- `details`
- `receipt`
- `receiptHash`
- `eventRoot`

The adapter emits a normalized receipt bundle in `receipt` and a deterministic sequence-aware event chain in `details.transcript`.

Transcript/event chain rules:
- command records preserve original array order
- each event gets explicit `seq`
- each event gets `prev_hash` and `event_hash`
- genesis uses `GENESIS`
- a deterministic `change` event is appended after all command events
- `eventRoot` is the final event hash in the chain

Schema freeze file:
- `schemas/stealth_adapter_output.v0.schema.json`

## Initial reason codes

- `OK`
- `MISSING_REQUIRED_FIELD`
- `BAD_SCHEMA`
- `EMPTY_TRANSCRIPT`
- `DIFF_MISMATCH`
- `TAMPER`
- `CHAIN_MISMATCH`
- `ADAPTER_INTERNAL_ERROR`

### Mapping rules
- missing top-level required fields -> `MISSING_REQUIRED_FIELD`
- invalid source/schema shape -> `BAD_SCHEMA`
- empty commands plus no change event material -> `EMPTY_TRANSCRIPT`
- malformed or missing diff commitment for changed files -> `DIFF_MISMATCH`
- malformed command payload / content corruption -> `TAMPER`
- explicit sequence mismatch / chain continuity violation -> `CHAIN_MISMATCH`
- unexpected adapter exception -> `ADAPTER_INTERNAL_ERROR`

## Deterministic chain semantics

For the current v0 adapter:
- each Stealth command becomes one `type: "command"` event
- the Stealth change metadata becomes one trailing `type: "change"` event
- `seq` starts at `1` and increments without gaps
- `prev_hash` must equal the previous event's `event_hash`
- `eventRoot` is derived from the final event hash

## Demo command

```bash
python3 demo/stealth_handoff_adapter_demo.py \
  --input examples/stealth/session-evidence.v0.sample.json \
  --output artifacts/stealth_adapter_output.json
```

## Sample verifier output

See frozen OK fixture:
- `examples/stealth/adapter-output.ok.v0.json`

Key shape:

```json
{
  "valid": true,
  "reason_code": "OK",
  "checks": {
    "schema": true,
    "receipt_hash": true,
    "event_root": true,
    "scope": true,
    "commands": true,
    "diff_commitment": true
  },
  "fail_path": null,
  "details": {
    "source": "STEALTH_HANDOFF",
    "transcript": []
  },
  "receipt": {},
  "receiptHash": "sha256:...",
  "eventRoot": "sha256:..."
}
```

## Notes

- No Stealth source code is modified by this adapter.
- No real PQ signatures are introduced yet.
- This is a demo/adapter seam PR only.
