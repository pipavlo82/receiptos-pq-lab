# Adapter Interfaces

## Why adapter layer exists
Adapter layer is the integration seam between extension envelopes and future real cryptographic engines.

It lets us lock stable contracts now, while cryptographic backends (ML-DSA / VRF) remain pluggable later.

## Adapter layer vs mock verifier layer
- **Mock verifier layer** (`mock_*`): validates routing and mode-level semantics.
- **Adapter layer** (`*_adapter.py`): defines backend contracts + normalized outputs for future real implementations.

## Frozen integration shape (must not break)
1. Existing unified verification output remains available:
   - `valid`, `mode`, `reason_code`, `checks`, `fail_path`
2. Adapter-contract output for PQ path is stable:
   - `valid`, `adapter_result`, `adapter_reason`, `normalized_reason_code`, `details`
3. Deterministic reason mapping is mandatory.
4. Exceptions are normalized to `ADAPTER_INTERNAL_ERROR` (no raw stack/error-string leakage).
5. Core ReceiptOS schema is not mutated; extension remains additive.

## PQ adapter contract (stable)
Input payload:
- `scheme_id`
- `canonical_payload` or `canonical_digest`
- `public_key`
- `signature`
- `metadata` (optional)

Raw adapter output:
- `ok`
- `raw_reason`
- `details`
- `fail_path`

Normalized/public mapping:
- via `reason_mapping.py`
- surfaced as deterministic `normalized_reason_code`

## ML-DSA stub vs real implementation
### Current stub (`mldsa_adapter_stub.py`)
- deterministic placeholder checks only
- supported scheme ID validation
- required field checks
- placeholder shape checks (`mldsa_pk_`, `mldsa_sig_`)
- deterministic fail trigger (`"fail"` in signature)

### Future real ML-DSA adapter
Must preserve:
- identical input contract
- identical output contract
- deterministic reason mapping via `reason_mapping.py`
- no integration shape breakage for current extension verifier/hybrid composition

May replace only the internal verification mechanics.
