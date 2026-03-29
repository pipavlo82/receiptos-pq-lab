# ML-DSA Vector Alignment Debug (vector_001)

## Scope
Debug/alignment for real ML-DSA backend path in `receiptos-pq-lab` without changing architecture, adapter contract, or normalized output shape.

## What was checked

1. **Fixture identity (copy integrity)**
- `fixtures/mldsa/vector_001.json` in `receiptos-pq-lab`
- vendor source: `vendors/ml-dsa-65-ethereum-verification/test_vectors/vector_001.json`
- SHA-256 both files: identical.

2. **Input format / lengths**
- `public_key_raw`: 1952 bytes (expected)
- `signature_raw`: 3309 bytes (expected)
- `msg_hash`: 32 bytes (expected)
- All are `0x` hex strings, no wrapper-level hex transformation detected.

3. **Verify surface expectation**
- Vendor harness path executed: `test_verify_fips_kat_vector0` (Foundry)
- It calls `verify(pk, sig, msgDigest)` directly (digest path, not raw message path).

4. **Wrapper-level transformations**
- Transitional backend passes digest/pk/sig bytes through as-is (no packing/unpacking rewrite).

5. **Verifier code-path semantics**
- In `MLDSA65_Verifier_v2.verify(...)`, final check is:
  - `poly_challenge(dsig.c)` vs `poly_challenge(messageDigest)`
- This is a placeholder/challenge-binding shortcut, not full FIPS verification reconstruction.

## Mismatch found
- `msg_hash` in vector_001 is **not equal** to trailing `c` extracted from `signature_raw`.
- Since verifier compares challenge of `dsig.c` with challenge of `messageDigest`, this path deterministically returns `ok_flag=0` for current vector alignment.

## Root cause
**Verifier/harness-level semantic mismatch** (not fixture format mismatch, not wrapper transformation issue):
- Current vendor verify implementation is transitional and not full final FIPS verification logic.
- It uses challenge(messageDigest) comparison that does not match vector_001’s current digest/signature relationship.

## Minimal fix needed next
- Minimal meaningful fix is in verifier logic (vendor side), not in `receiptos-pq-lab` adapter boundary:
  - replace placeholder challenge-binding step with full expected challenge reconstruction path for provided vector format,
  - or provide fixture where `messageDigest` matches verifier’s current challenge-binding expectation.

## Status after debug
- Alignment checks passed for bytes/format/wiring.
- `vector_001` still returns `VERIFY_FAILED` via real backend path due to verifier semantic mismatch described above.
