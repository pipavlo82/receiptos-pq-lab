# VRF / Entropy Integration Boundary

## Adapter vs Backend (entropy track)
- **Entropy adapter (`entropy_adapter.py`)**
  - validates extension envelope shape for entropy path
  - keeps public output contracts stable
  - delegates proof verification mechanics to backend
- **VRF backend (`vrf_backend_interface.py`)**
  - narrow backend contract only:
    - `verify(entropy_proof_payload, metadata) -> {ok, raw_reason, details}`
  - no public normalization responsibility

## What is stable now
1. Adapter-contract output shape:
   - `valid`, `adapter_result`, `adapter_reason`, `normalized_reason_code`, `details`
2. Compatibility/unified output shape:
   - `valid`, `mode`, `reason_code`, `checks`, `fail_path`
3. Deterministic reason mapping via `reason_mapping.py`
4. No raw exception string leakage to public layer

## What can be swapped later
- `MockVRFBackend` can be replaced by real VRF/entropy verifier backend.
- Integration seam remains the same (`VRFBackend.verify(...)`).
- No schema-direction or output-shape changes required.

## Invariants (must not break)
- extension schema remains additive/optional
- normalized reason mapping remains deterministic
- unknown/internal failures map to `ADAPTER_INTERNAL_ERROR`
- hybrid and entropy mode routing remain compatible with existing verifier layer
