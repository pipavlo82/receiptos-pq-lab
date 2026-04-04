# EXECUTION BOARD — ReceiptOS Multiplayer Pivot

## Step 1 — Lock positioning + operator flow
- **Owner:** Kimi
- **Objective:** Freeze messaging and link demo -> monitor -> human reply loop.
- **Files:** `docs/market_probe/OUTREACH_MULTIPLAYER_SEGMENT.md`
- **Status:** DONE
- **Done criteria:** core phrase + framing present; Operator Run Order present.
- **Blocker:** none
- **Rollback:** revert doc commit only.

## Step 2 — Run monitor and produce reply queue
- **Owner:** Qwen
- **Objective:** Execute outreach monitor and produce actionable signal report.
- **Command:** `python3 tools/outreach_monitor_v1.py --config docs/market_probe/multiplayer_threads.json`
- **Artifacts:** `docs/market_probe/outreach_monitor_report.json`, `docs/market_probe/outreach_monitor_report.md`
- **Status:** DONE
- **Done criteria:** command succeeds; `signal_count` available; rows include class + next_action.
- **Blocker:** `gh` auth required.
- **Rollback:** none (read-only monitor).

## Step 3 — Human-reviewed replies to active signals
- **Owner:** Dir
- **Objective:** Post only approved replies for current signal threads.
- **Status:** READY
- **Prereq:** Step 2 done + approved drafts.
- **Done criteria:** 1 reply max per active signal thread; no off-topic escalation.
- **Rollback:** acknowledge+exit if thread rejects context.

## Step 4 — 48h signal evaluation gate
- **Owner:** Lightning
- **Objective:** Decide resonance from real responses (not impressions).
- **Status:** READY
- **Prereq:** Step 3 replies posted.
- **Done criteria:** classify outcomes and decide continue/retune/stop.
- **Blocker:** waiting period (24–48h).

## Step 5 — Message tuning v2 (if needed)
- **Owner:** NVIDIA
- **Objective:** Tighten wording if low response quality.
- **Status:** BLOCKED
- **Prereq:** Step 4 evidence.
- **Done criteria:** one updated opener + one tight-thread variant only.
- **Rollback:** revert to v1 message pack.

## Step 6 — Demo handoff packet (on demand)
- **Owner:** Kimi + Qwen
- **Objective:** Send minimal demo packet only when someone asks.
- **Status:** READY
- **Prereq:** explicit request from target.
- **Done criteria:** send 3 fixtures + verify command + one-paragraph integration note.
- **Rollback:** stop if request quality is low/no intent.
