# Historical `vector_raw.json` Support

## What this payload is
`vector_raw.json` is a historical/generated payload containing richer context than basic test vectors:
- `msg_hash`
- `sig_pq_b64` (ML-DSA signature, base64)
- `pq_pubkey_b64` (ML-DSA public key, base64)
- additional metadata (timestamp, mode, signer context, ECDSA fields, etc.)

## How it differs from `vector_001.json`
- `vector_001.json`: already normalized hex fields for verifier tests (`signature_raw`, `public_key_raw`, `msg_hash`).
- `vector_raw.json`: richer provenance payload, but signature/public key are base64 and need decoding before adapter use.

## Why it is useful
- better for provenance/demo narrative (historical generation context included)
- supports hybrid storytelling (ECDSA + ML-DSA metadata context)
- still can feed the same adapter/backend contract after normalization

## Current integration
Added loader/helper in `src/mldsa_historical_loader.py`:
- load fixture
- decode base64 fields
- preserve metadata
- convert to current adapter payload shape (verify-by-digest)

No changes to existing `vector_001` path, adapter contract, or normalized output shape.
