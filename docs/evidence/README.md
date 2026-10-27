# Curated evidence — Part 2

Original evidence dated October22,2026. See [October27 updated evidence](voice-update.md) for live voice, user verification and current checks. Older images are historical rather than current voice screenshots. All demonstrated records are fictional. Screenshots are supporting views, not standalone proof of timing, persistence or live generation. Agent-run results and student verification are distinguished in [verification](../verification.md). The [AI disclosure](../../AI-USE.md) links selected prompts, changes, checks and decisions, including failed/revised approaches.

## Historical October22 final preparation

| Artifact | What it demonstrates | Limits |
| --- | --- | --- |
| [Completed practice](part2-final-completed.png) | Current UI, six-cycle result, saved state | Timing comes from observation log plus records |
| [Fullscreen support](part2-final-support.png) | Support panel and paused controls during practice | No service contacted; not a clinical assessment |
| [Mock conversation](part2-final-chat.png) | Question and actual saved mock answer, order/time/status | Clearly mock; displayed citation sentence hidden by approved formatting |
| [History after restart](part2-final-history.png) | Current completed/stopped records retained after restart/refresh | Table floors milliseconds to whole seconds |
| [API/SQLite record extract](part2-final-records.json) | Exact session/message/request IDs, raw actual reply, duration/status, replay and restart comparison | Selected fictional records only; not a database dump or independent live call |

Observed full run bound 72.336 seconds; setup 5.036 seconds separate, no pauses excluded. Stopped run8580 ms active / 11149 ms paused. Exact request replay retained 2 messages / 1 attempt. See verification for commands/method and report for requirement mapping.

## Historical Part 2 evidence

| Artifact | Evidence category |
| --- | --- |
| [Live reply](part2-live-saved.jpg) | Historical actual OpenAI reply; older UI, not today's mock mode |
| [Authentication failure](part2-live-auth-failure.jpg) | Historical failed live attempt, user saved without invented assistant |
| [Save outage](part2-smoketest-save-failure.jpg) | Historical backend-unavailable save; Stop/support usable and explicit retry |
| [SmokeTest history](part2-smoketest-history.jpg) | Historical completed/stopped records after retry/restart |
| [Crisis notice](part2-crisis-notice.jpg) | Fictional phrase-rule input, application-owned notice; not clinical detection |
| [Earlier mock success](part2-chat-saved.jpg), [failure](part2-chat-failure.jpg), [saved sessions](part2-saved-history.jpg) | Earlier integration milestones, not final appearance |

Historical live request 8cfe378a-6795-4a94-ab2c-016a33aeafe7 used modelgpt-5.4-mini-2026-03-17 and cited interrupted20430ms recordbca4b56e-e2b6-484a-a609-089474646545. Initial failure/401 diagnostic led to local credential correction, then success. All six approved live attempts are now consumed. Final verification made no paid calls.

## Preserved Part 1 and unfinished artifacts

[Part 1 submitted report](https://github.com/mallorypierz/mentalhealth_app/blob/e958bdcf11e69b5c4451f986742989acd01b497e/report.md) preserves its design/evidence links. Local [entry](desktop-entry.jpg), [paused practice](narrow-practice.jpg), [history](narrow-history.jpg) and [initial flow notes](../diagrams/part1-flow.md) are historical, not current screenshots.

No editable Figma capture, selected-frame comparison or recording is included. Existing blank Figma frames were preserved. Screenshots do not substitute for editable design layers. No full chat export, private credentials, research-participant content or runtime database is submitted. Hosted Part 2 links must be checked after a separately approved commit and push.
