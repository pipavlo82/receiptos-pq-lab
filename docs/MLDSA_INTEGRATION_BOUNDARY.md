# ML-DSA Integration Boundary

## Adapter vs Backend
- **Adapter (`mldsa_adapter.py`)**
  - Owns external contract stability
  - Validates payload shape and scheme gate
  - Calls backend through narrow interface
  - Normalizes raw outcomes into deterministic adapter result
- **Backend (`mldsa_backend_interface.py`)**
  - Owns verification mechanics (mock now, real later)
  - Returns narrow backend-local result: `ok/raw_reason/details`

## What is already stable
1. PQ adapter contract input shape
2. Adapter-level normalized output:
   - `valid`, `adapter_result`, `adapter_reason`, `normalized_reason_code`, `details`
3. Compatibility unified output remains available:
   - `valid`, `mode`, `reason_code`, `checks`, `fail_path`
4. Deterministic reason mapping (`reason_mapping.py`)

## What can be replaced later
- `MockMLDSABackend` can be swapped with a real ML-DSA backend.
- Replacement point: implement `MLDSABackend.verify(...)` only.
- Adapter and public integration shape stay unchanged.

## Invariants that must not break
- No schema-direction breakage (extension remains additive).
- No raw exception-string leakage to public outputs.
- Unknown/internal failures map deterministically to `ADAPTER_INTERNAL_ERROR`.
- Existing mode routing and hybrid composition continue to work.
