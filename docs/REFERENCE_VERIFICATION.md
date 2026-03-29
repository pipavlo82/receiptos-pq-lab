# Reference Verification Layer (Mock)

## What this is
A **deterministic mock verification layer** for extension envelopes.

It validates integration shape, mode routing, and failure semantics for:
- `signature_extension`
- `entropy_proof`
- `hybrid`

## What it proves
- Additive extension model can be validated without breaking core ReceiptOS
- Mode auto-detection and path routing are deterministic
- Failure outputs are structured and stable (`reason_code`, `fail_path`, `checks`)
- Hybrid path can express partial failures explicitly

## What it does NOT prove
- Real post-quantum cryptographic soundness
- Real VRF proof verification
- Production security/performance characteristics
- Distributed trust guarantees

## Unified output format
All verifiers return:
- `valid`
- `mode`
- `reason_code`
- `checks`
- `fail_path`

## Why this phase matters
Before implementing heavy crypto, we lock:
1. contracts
2. routing behavior
3. failure semantics

This reduces integration risk and avoids premature cryptographic complexity.
