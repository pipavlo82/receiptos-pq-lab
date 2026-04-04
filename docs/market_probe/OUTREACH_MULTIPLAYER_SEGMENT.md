# Outreach Pivot — Multiplayer / Authoritative Backend Segment

## Positioning (locked)
- **Core phrase:** `interactive match execution integrity`
- **Framing line:** `This is for stateful / real-time systems where results can't be recomputed from public inputs.`

## Why this segment
- Deterministic/public-input systems can often recompute outcomes directly.
- Real-time authoritative systems cannot always reconstruct full truth from public inputs.
- Disputes in these systems need verifiable execution trails, not just "trust server logs".

## 1) Short opener (primary)
Quick technical question:

I’m testing **interactive match execution integrity** for real-time authoritative servers.

- valid event chain -> PASS
- tampered event -> FAIL
- replay/duplicate event -> FAIL
- continuity break -> FAIL

This is for stateful / real-time systems where results can’t be recomputed from public inputs.

Would this be useful in your backend flow for dispute resolution or anti-fraud escalation?

## 2) Technical follow-up (if interested)
Context:
- receipt schema: `{event_id, prev_hash, payload, hash}`
- chain rule: `hash = H(event_id + prev_hash + payload)`
- verifier checks:
  1. hash consistency
  2. continuity (`prev_hash` linkage)
  3. replay/duplicate detection

Not replacing anti-cheat; this is post-match integrity evidence for support/audit decisions.

## 3) "Who are you?" response template
Fair question.

I’m an independent engineer prototyping an integrity check for multiplayer event logs.
I’m validating whether this solves a real backend dispute pain before expanding scope.

If useful, I can share a minimal demo with 3 fixtures (valid/tamper/replay).

## 4) Target profile (strict)
Keep only targets working on:
- multiplayer authoritative servers
- real-time game state sync / replay handling
- anti-fraud or dispute tooling
- backend observability for match events

Avoid targets focused only on:
- deterministic provably-fair casino logic
- pure RNG marketing claims without backend dispute flow

## 5) Outreach rules
- one message per person/repo
- no repo links in first touch (unless asked)
- no broad blast
- no arguing in dismissive threads
- if called off-topic: acknowledge and exit thread

## 6) Success metric
- >= 2 technical replies OR >= 1 concrete request to review demo details

## Operator Run Order
1. **Demo integrity pass**
   - Ensure demo outputs still reproduce:
   - valid -> PASS, tamper -> FAIL, replay -> FAIL.
2. **Monitor responses**
   - Run: `python3 tools/outreach_monitor_v1.py --config docs/market_probe/multiplayer_threads.json`
   - Read `outreach_monitor_report.json`.
3. **Human reply loop**
   - Reply only after manual approval.
   - One concise technical response per signal thread.
