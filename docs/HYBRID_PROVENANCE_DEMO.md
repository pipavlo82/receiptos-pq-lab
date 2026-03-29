# Hybrid Provenance Demo

## Narrative intent
Show how a metadata-rich historical payload can strengthen trust/provenance communication beyond a bare technical vector.

## Dual-signature / metadata-rich framing
`vector_raw.json` includes context that supports a hybrid narrative:
- ML-DSA payload material (`sig_pq_b64`, `pq_pubkey_b64`)
- digest (`msg_hash`)
- additional context (timestamp/mode/legacy ECDSA fields and signer metadata)

This lets you tell a realistic story:
"not only can we verify data shape, we can preserve execution provenance context around signatures."

## What `vector_raw` proves now
- historical payload ingestion
- deterministic decode/normalization to current adapter contract
- metadata retention (provenance context preserved)
- compatibility with current digest-based path

## What `vector_raw` does NOT prove yet
- full final cryptographic production guarantees by itself
- universal arbitrary-vector real verification in all modes

## How to demo it next to `vector_001`
1. **Start with `vector_001`**
   - technical path
   - stable verifier input shape
2. **Then show `vector_raw`**
   - decode base64 -> normalized hex
   - same adapter contract output shape
   - richer metadata retained
3. **Conclude**
   - vector_001 = engineering baseline
   - vector_raw = provenance/hybrid narrative layer

## Trust/provenance story fit
This pair demonstrates:
- integrity pipeline discipline (technical fixture)
- context-aware provenance retention (historical payload)

That combination is strong for outreach with security/compliance/game-integrity audiences.
