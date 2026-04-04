# n8n Blueprint — Outreach Monitor v1 (Human-in-the-loop)

## Goal
Automate detection of new replies in multiplayer outreach threads and prepare reply drafts, **without auto-posting**.

## Safety Mode
- `auto_send = false`
- Human approval required before any outbound message/comment.

## Workflow (v1)
1. **Cron Trigger** (every 30 min)
2. **Execute Command**
   - Run:
     - `python tools/outreach_monitor_v1.py --config docs/market_probe/multiplayer_threads.json`
3. **Read JSON**
   - Input: `docs/market_probe/outreach_monitor_report.json`
4. **IF signal_count > 0**
   - For each row with `has_new_signal=true`:
     - format compact alert block:
       - repo
       - thread
       - class
       - quote
       - next_action (draft)
5. **Notify** (Telegram/Discord/email webhook)
   - Send alert to you only
6. **Store snapshot**
   - Save alerts to `docs/market_probe/alerts/alert_<timestamp>.json`

## Optional v1.1 (still safe)
- Add dedupe key: `repo + thread + last_comment_at`
- Skip alerts already sent.

## Data Contract (from outreach_monitor_v1.py)
- `signal_count`
- `rows[]`:
  - `repo`
  - `thread`
  - `title`
  - `has_new_signal`
  - `response_type`
  - `quote`
  - `next_action`
  - `comment_count`
  - `last_comment_at`

## Approval Flow
- n8n sends draft only.
- You reply with explicit approve command (outside workflow).
- Posting remains manual/assistant-triggered.

## Implementation Notes
- Keep n8n runner on same host that has `gh` auth.
- Use absolute paths in Execute Command node to avoid cwd issues.
- Add timeout (30s–60s) and retry (1) on command node.

## Success Criteria
- You receive alert within next schedule window after any new comment.
- Every alert includes class + ready draft.
- Zero unintended outbound posts.
