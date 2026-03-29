# PQ Demo Narrative (ReceiptOS PQ Lab)

## Goal
Present a clear, credible PQ story without overclaiming cryptographic finality.

## Two fixture roles

### 1) `vector_001.json` (technical fixture)
- Purpose: deterministic, engineering-oriented verification path
- Shape: already normalized (`msg_hash`, `public_key_raw`, `signature_raw`)
- Best for:
  - adapter/backend contract testing
  - stable CI/regression checks
  - boundary correctness (input shape, reason mapping)

### 2) `vector_raw.json` (historical payload)
- Purpose: provenance-rich, narrative-oriented payload
- Shape: richer context + base64 fields (`sig_pq_b64`, `pq_pubkey_b64`) + metadata
- Best for:
  - demo storytelling
  - hybrid provenance framing
  - showing real-world context, not just bare verifier input

## Technical fixture vs historical payload
- **technical fixture** = clean deterministic engineering input
- **historical payload** = contextual evidence object with signing metadata and provenance signals

Together they support both:
1. "Does the pipeline work deterministically?" (vector_001)
2. "Does this look like real operational provenance?" (vector_raw)

## Current ReceiptOS PQ story this enables
1. **Off-chain first** verification semantics remain primary.
2. PQ lane is integrated via frozen adapter/backend boundaries.
3. Real path exists in transitional form (fixture-backed, digest-based).
4. Demo can show both hard-engineering credibility and trust/provenance narrative.

## Suggested live sequence (short)
1. Run vector_001 flow (technical confidence).
2. Run vector_raw normalization + adapter pass (provenance confidence).
3. Explain where real backend becomes full verifier next.

## Positioning discipline
Do not claim full production PQ verifier yet.
Claim what is true now:
- stable contracts
- deterministic semantics
- real integration boundary with fixture-backed backend path
- richer provenance demo payload support
