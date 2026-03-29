# ML-DSA Real Backend Path (Fixture-Backed, Digest Flow)

## What is already real
- The backend now executes a **real local verifier path** through vendor Foundry test infrastructure:
  - `vendors/ml-dsa-65-ethereum-verification`
  - `test_verify_fips_kat_vector0`
- Input is wired through the existing backend contract boundary.

## What is transitional
- Current real path is **fixture-backed** (`vector_001.json`) and digest-based.
- It validates integration against local verifier execution, but does not yet provide arbitrary-vector runtime verification.

## What is not implemented yet
- General-purpose real ML-DSA verify backend for arbitrary payloads
- direct in-process cryptographic verify implementation in this repo

## Invariants preserved
- Adapter contract unchanged
- Normalized output shape unchanged:
  - `valid`, `adapter_result`, `adapter_reason`, `normalized_reason_code`, `details`
- Reason taxonomy unchanged
- Existing schema direction unchanged

## Verify-by-digest path
Uses fields from fixture loader:
- `msg_hash` -> `canonical_digest`
- `public_key_raw` -> `public_key`
- `signature_raw` -> `signature`

This is the first real PQ verification integration path through frozen boundaries.
