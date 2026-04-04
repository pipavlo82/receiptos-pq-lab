# NEXT 24H PLAN

1. Re-run monitor every 30–60 min: `python3 tools/outreach_monitor_v1.py --config docs/market_probe/multiplayer_threads.json`.
2. Process only new deduped signals from `outreach_monitor_report.json`.
3. Approve/post replies only for `INTERESTED` and valid `CONFUSED` cases.
4. Avoid any new outbound posts unless high-fit and empty queue.
5. If dismissive/off-topic appears, acknowledge and exit thread once.
6. At +24h, produce signal summary: count by class + notable quotes.
7. At +48h, run resonance gate: continue vs retune messaging.
8. Keep focus strictly on multiplayer authoritative backend threads.
