# Final submission audit — November 3, 2026

Expectations were recorded in plan.md before execution. Tested revision: c6d8377ce4782abd5e3467e78e03eddf25e74d6b, branch codex/exercise-quiz. This audit changes evidence/documentation only; application source is unchanged. All new runtime tests used fictional data and mock providers. Zero new paid calls.

## Clean checkout

Preserved the previous isolated checkout by renaming it to /tmp/mentalhealth-part3-clean-prior-audit. Ran `git clone --no-hardlinks /Users/mallorypierz/mentalhealth_app /tmp/mentalhealth-part3-clean`; no credentials, working database or installed folders copied. Followed README commands with the host's explicit installation approval:

```sh
python3 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements.txt
npm --prefix frontend ci
backend/.venv/bin/python -m pip check
backend/.venv/bin/python -m unittest discover -s backend/tests -v
npm --prefix frontend test
npm --prefix frontend run build
backend/.venv/bin/python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
npm --prefix frontend run dev -- --port 5173 --strictPort
```

Expected: install and run without private configuration; tests/build pass. Observed: pip check passed, 83 backend tests passed, 37 frontend tests passed, production build passed. Logs retained in this folder. Browser served frontend and mock API; fresh database initialized. Dependencies came from declared requirements and npm lockfile, with package caches permitted. This is agent reproduction, not independent human peer testing.

## Additional executed browser checks

| Case | Expected | Observed and evidence | Result |
|---|---|---|---|
| S15 combined failure/support | Saved user message, no fabricated reply; support opens in same failure state | Audit-only failure-harness.py patched mock planning to raise MockFailure while /tmp/mentalhealth-final-failure existed. UI showed planning failure, saved message, one attempted mocked call; support opened and focus moved to its heading. model-failed.png, support-after-failure.png, failure-db.json (one message, one failed request). No human service contacted. | PASS, mock |
| Retry after provider recovery | Reuse request without duplicating submitted message | Removed test switch, clicked Retry reply. UI showed scripted insufficient-history reply, order2, succeeded, three cumulative mocked attempts. retry-db.json: two messages total, one request, empty retrieval. | PASS, mock |
| Invalid local access | Refresh recovers to chooser without deleting records | Revoked only isolated fictional browser_sessions rows through test fixture SQL; reload displayed chooser, guest button and profile creation. recovered-access.png. This reproduces the failure condition against fixed code, not the original incident footage. | PASS, mock |
| Quiz and remembered answers | Explicit opt-in; current answers override older saved ones; no automatic start | Created Fictional Final Audit. Surroundings + avoid suggested grounding; opted in and saved. Refresh retained profile and Use saved answers restored surroundings/avoid. Changed to breathing/yes and got breathing. Preview required a separate Start. | PASS, deterministic |
| Grounding and history | Next advances steps; actual elapsed completion recorded once | Marked first item and used Next/Finish. Completed8789ms; Vue displayed8s. ID0a9d7220-b2f0-4147-90b3-fdff0612b5e3 matched Vue DOM data-session-id, API and read-only SQLite. vue-history.json and record-api-db.json. | PASS, mock |
| Save outage/retry/restart | Honest unconfirmed state and retry without duplication | Stopped isolated backend, saved changed preferences. UI showed “Preference change not confirmed” and Retry same preference change. Restarted using README command, retried, saw Preferences saved. restart-db.json: one current preference row revision2, two successful operations for the two intentional saves; sessions2/messages2/requests1 unchanged. history-after-restart.png confirms completed row persists. | PASS, mock |
| Narrow-screen keyboard | Quiz fits390px, visible focus | 390×844: document scrollWidth390; Tab reached activity radio, computed outline solid3px. quiz-390.png. At1440×1100 history scrollWidth1440. Temporary viewport reset. | PASS within these two views; not a full accessibility audit |

Read-only database inspection used Python sqlite3 URI mode=ro. The separate token-revocation test fixture was the only direct test mutation, confined to the fresh isolated database. No root working database was changed by these tests. Access tokens and owner tokens are omitted from evidence.

Breathing session880670b5-d883-4bb0-9dfb-11ed225e37a1 completed60000ms, with recorded start/end separation60.003s; retry-db.json. Setup was not instrumented and remains separately unmeasured. Grounding manual completion was8.791s wall-clock from stored start/end; this is sequence advancement, not a claim the user performed every activity. Comprehensive real-device/background timing is untested.

## Recording coverage

The actual published frontend MOV was decoded at two-second intervals (151 frames), then six relevant frames visually inspected (video-coverage.png). Duration301.7167s, no audio track. This is dense sampled inspection, not continuous playback or verification of audible speech.

- 0:00–0:10: guest option and profile chooser; subsequent profile use. Guest entry itself is not established by these frames.
- 0:42–0:44 and1:12–1:14: saved history;1:10 stopped breathing12s.
- 1:16–1:18: independent crisis support opened.
- 2:10–2:24: quiz answers and grounding suggestion.
- 2:30–2:42: grounding checkmarks, Next and completion.
- 2:50: breathing suggestion;2:54–3:04: choose another, STOP preview/start/stop.
- 3:06 and3:34: saved exercise outcomes.
- 3:50–3:54: grounding suggestion, Remember answers and Preferences saved.
- 4:10–4:58: profile switching, existing chat, fictional Avery creation.

Section1 is the frontend demonstration. Its UI labels saved OpenAI replies/live controls; no new audio success is inferred from a silent movie. Quiz/exercises/preferences/history are deterministic app behavior, not model-generated. Section2 is the separate160.433s process-demonstration.mov: historical browser comparison/test evidence then appended failure/fix/code explanation after approximately2:02. It remains a silent retrospective, not original-error footage. These section descriptions provide written context alongside the videos.

## Figma and access

MCP metadata and screenshot reads succeeded for Assignment3 page31:110 and desktop practice31:174. Native text/vector frame structure is present; figma-reference-desktop.png retained. Browser sharing initially restricted the file to the team. With explicit host approval, changed to Anyone / View and saved; UI confirmed Anyone can view (figma-sharing.png). No design edits, capture or implementation round trip occurred. Public GitHub/video link checks are recorded in public-links.json. Instructor-specific device/login access has not been personally witnessed; Figma's sharing setting is verified, not an anonymous-session rendering claim.

Remaining limitations: physical-device sleep/background behavior, exhaustive accessibility and concurrency, live failure variation, and Figma-to-Vue round-trip/pixel parity. These are disclosed rather than marked passed. Course upload remains the student's action.

## Runtime restoration

Restored original root backend/frontend after tests. Proxied health reports OpenAI configured and voice enabled; selected testing session16/24 used,8 remaining. Separate health live-call counter6/6 has0 remaining. No counters were reset or extended and no new paid check was made. Configuration is not proof of a new successful live reply. Existing database/.env preserved. Python3.12.5, Node24.20.0, npm11.19.0. Clean checkout has no tracked changes; only the explicitly added untracked test harness.
