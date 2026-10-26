# Verification — Part 2 final preparation, October 22, 2026

Current evidence below supersedes older current-state claims. Older sections are retained as dated historical observations, not proof of today's UI. All checks were agent-run with fictional data. The student verified the earlier SmokeTest report and recent UI cleanup; the student subsequently confirmed review and approved commit/push.

## Fresh final checks

| Check | Observed result |
| --- | --- |
| `backend/.venv/bin/python -m unittest discover -s backend/tests -q` |35 passed; mocked/temporary-database tests, no paid calls. Starlette TestClient deprecation warning remains. |
| `npm --prefix frontend test` |10 passed |
| `npm --prefix frontend run build` |Production build passed |
| `git diff --check` |Passed before final documentation edits; repeated after preparation |
| Secret/database boundaries |backend/.env and runtime SQLite ignored and not tracked; no credential values printed |
| Browser completed practice |New six-cycle run; setup 5036ms separately. Pre-Start-click to observed completed state72336ms, a conservative bound including tool/observation delay. First cue observed1091ms after click. No pause/support/hidden interval excluded. |
| Stored completed session |ID 60c50e57-77b8-4b6e-8666-6b22e43268f0; active 60000ms, paused 0; timestamp span 60001ms. Capped active duration alone is not the timing proof. |
| Support/pause/stop/fullscreen |Second run in fullscreen/still mode; support paused practice and disabled Resume while open; closing required explicit Resume. Stop saved 8580ms active,11149 ms paused. Escape restored normal view. No crisis link activated. |
| Mock RAG answer |New question about most recent practice retrieved stopped session 8097f4b9-ff32-4d1e-bce5-b4317a0e0ba3. Actual scripted reply says stopped/8.58 seconds; records outcome, two mock calls, one attempt. |
| Exact replay |Reposting identical request 0480ce29-6b39-493e-8759-bad86d9c03d2 retained exactly2 messages and attempt_count 1, with no duplicate assistant. |
| Restart and refresh |Backend terminated/restarted; browser reloaded. Completed/stopped sessions and same two-message conversation persisted. API values unchanged; SQLite one row per session. Live ledger unchanged 6/6. |

Inspection used Python sqlite3 URI `mode=ro`, parameterized SELECTs and HTTPX GETs against localhost, not a separate viewer installation. The saved [fictional record extract](evidence/part2-final-records.json) contains IDs, exact durations, actual reply and status. API/SQLite messages matched IDs/content/role/sequence. Session comparisons normalized UTC timestamps (`Z` versus `+00:00`); an initial string-only equality assertion was revised to compare instants, not an application fix. Vue shows floored whole seconds in the session table (8s for8580ms), and8.58 seconds in the generated answer. UI hides the mock citation sentence while raw stored/API text retains it.

Screenshots: [completed](evidence/part2-final-completed.png), [support in fullscreen](evidence/part2-final-support.png), [mock conversation](evidence/part2-final-chat.png), [history after restart](evidence/part2-final-history.png). These show current appearance; they do not independently prove timing or persistence.

## Evidence boundaries and repeatable review

Fresh tests cover deterministic failure paths; historical browser evidence below covers backend/save outage, retry, missing configuration, provider failure, empty retrieval, rejected writes, scoped access and instruction-like stored text. These are mock/temporary-database checks, not new live-model trials. Historical Chrome hidden-tab pause/explicit Resume and refresh interruption were observed separately; they were not repeated in this final run.

Historical live request 8cfe378a-6795-4a94-ab2c-016a33aeafe7 in conversationdc043c5e-b2ed-4ed3-bf24-a9c450e01a57 produced an actual saved OpenAI answer from interrupted sessionbca4b56e-e2b6-484a-a609-089474646545 (20430 ms). Initial provider/authentication failures saved user input without invented replies. Historical successful live evidence does not make today's mock reply live. Local live ledger is now6/6; earlier4/6 entries below are historical.

To repeat without live calls: verify mock in `/api/health`; run the commands above; complete one practice and stop another; ask a fictional latest-practice question; inspect the IDs returned by API against SQLite; replay the same request ID/body; restart backend/reload browser and inspect again. Use temporary databases and mock providers for destructive/failure injections as the test suite does, never inject failures into the working database. New runtime records and any configuration change need the user's scoped authorization.

Untested/incomplete: editable Figma round trip, saved preferences, normal-view persistent support bar, comprehensive keyboard/contrast/zoom audit, physical mobile fullscreen, device sleep, cleared/disabled browser storage, cross-browser recovery, >100-message UI pagination, clean-checkout reproduction and Part 3 recordings/evaluation. No clinical efficacy or production security claim.

## Historical verification log

The following dated records preserve the development trail. Their implementation-status statements and process IDs describe those earlier moments only.

# Verification — October 15, 2026

## Environment and commands observed
- `node --version`: v24.20.0; `npm --version`: 11.19.0; `python3 --version`: 3.12.5.
- User approved local installation in `frontend/`: `npm install vue@3` and `npm install --save-dev vite@7 @vitejs/plugin-vue@6`.
- `npm ls --depth=0`: Vue 3.5.44, Vite 7.3.7, plugin-vue 6.0.10. npm reported zero vulnerabilities. npm warned about esbuild install-script approval; the actual Vite build worked without additional changes.
- From `frontend/`, `npm test`: 4/4 tests passed. Tests use a fake monotonic clock for every 4/6 boundary across six cycles, pause exclusion, stop/restart, stale-response cancellation/replacement, and failures with no invented reply.
- From `frontend/`, `npm run build`: passed, 11 modules transformed. Repeated after the clock-synchronized cue refinement; passed again.
- `npm run dev -- --port 5173`: sandbox initially rejected binding with EPERM; approved elevated run succeeded. Server was stopped with Ctrl+C and restarted; real browser reload showed the entry screen again.
- One test invocation from the project root failed because package.json lives in frontend/. Corrected working directory; the actual passing commands above ran in frontend/.

## Observed real-browser checks
Tested at http://localhost:5173/ through the in-app browser, using fictional data only. This was an implementation-and-correction pass, not a source-unchanged SmokeTest across the entire session.

| Check | Expected | Observed |
|---|---|---|
| Entry | Direct Start, support, visible mock/persistence disclosures | Present |
| Failed mock | Honest failure and retry action | Simulated failure text, Retry introduction, Start still available |
| Retry success | Scripted instruction shown | Success after choosing Success and requesting again |
| Delayed mock then Start | No response disrupts practice | Pending mock cleared; exercise continued; no reply appeared after delay or on stopped result |
| Support during exercise | Pause, Stop accessible, Resume disabled while open | Paused at 5 active seconds; Resume disabled; two Stop controls present |
| Close support | Remain paused and restore focus | Paused remained; focus returned to Crisis support |
| Resume / Stop keyboard | Enter activates controls | Resumed, then stopped at 10 active seconds |
| Stopped history | One record with exact displayed status/duration and ID | 90f6bcde-9dbc-4f3c-8542-8b738d765b3f, stopped, 10s; fixture separate |
| Refresh | Reset records and preferences honestly | History contained only fixture-001; still cue unchecked and mode Success |
| Full exercise | Complete at 60 active seconds | Observed Cycle 1, Cycle 5 with 15 seconds left, then Completed and 60-second result |
| Completed history | One completed record, fixture separate | 7120f8e9-ed9e-4d0b-b668-48d743b19294, completed, 60s; only one new record |
| Narrow layout | No page horizontal overflow, readable controls/history | 390px viewport and 390px document width; practice and history screenshots inspected |
| Still cue | Static cue with text/count preserved | Checkbox checked and static label observed; final refinement verified scale 0.859994 → 1 → 0.859994 while paused |
| Stop from support | End paused practice without requiring close | Stopped result shown; 0 seconds after immediate pause rounded down, Restart disabled while support remained open |
| Keyboard focus | Visible focus and reachable checkbox | Tab from Start focused still-cue checkbox; computed 3px solid brown outline |
| Browser warnings/errors | None from app | Empty captured warning/error log |
| Restart | Entry loads | Reload after server restart showed complete entry view |

The full 60-second browser run occurred before the final visual-only cue synchronization change. The final timing unit tests/build passed again, and the affected pause/still-toggle behavior was rechecked in the browser. No accelerated browser timers were used.

## Visual evidence
- `evidence/desktop-entry.jpg`: 1280 × 900 viewport, full-page entry screenshot.
- `evidence/narrow-practice.jpg`: 390 × 844 viewport, paused practice, full page.
- `evidence/narrow-history.jpg`: completed session and fictional fixture at 390px.
Temporary viewport overrides were reset. The app tab was retained as a deliverable.

## Limits / not tested
No FastAPI, SQLite, RAG, paid/live model requests, actual conversation persistence, or database/API comparison exists in this increment. No clinical efficacy claim is made. Helpline details were checked through the mandated lookup tool, but calls/text/chat were not initiated. System-level reduced-motion preference changes, screen-reader speech, background-tab throttling/sleep, multi-browser testing, and exhaustive accessibility auditing remain unverified. Figma frame 1:6 was blank, so there is no populated visual reference to match. No capture, editable-layer validation, design-change experiment, or Figma round trip has occurred.

## Part 1 documentation review

Reviewed the developer-supplied R1–R4/D1–D6 table against the current Vue/CSS source. The support button is in normal document flow rather than a sticky/fixed container; it can scroll offscreen. General navigation remains rendered during practice (History is disabled). Motion preferences are an in-memory Vue ref initialized from the system setting; they do not persist. These are static-inspection findings, not new browser observations.

Updated the design mapping with ten findings and explicit observed/proposed/unverified distinctions. The developer chose a persistent bottom bar, hidden general navigation during practice, and optional remembered display choice; none was implemented. No runtime tests were rerun for this documentation-only change.

## Part 1 flow artifact review

Created `diagrams/part1-flow.svg`, `diagrams/part1-flow.png`, and the Markdown/Mermaid companion. Parsed SVG XML successfully and visually inspected the rendered final 1600px square preview: all three sections, labels, arrows, and design-status footer are visible. An initial Quick Look thumbnail cropped the bottom of the portrait canvas; the square canvas corrected that export issue. Mermaid source is provided as editable text; it was not separately rendered or parser-tested in this task.

Reviewed transitions against the documented baseline: direct Start, optional failure/retry, six-cycle completion, stopped/completed result and history, support opening from all named states, pause on support opening, no auto-resume on close, and Stop within support. The artifact is explicitly labeled initial design, not Figma capture. System reduced-motion precedence is now a developer-confirmed proposal. SHA-256 checks confirmed frontend source and package manifests/lockfile unchanged. No application tests were rerun for this documentation-only task.

## Part 1 architecture documentation review

Checked the architecture proposal against README, AGENTS instructions, current design/handoff, and the timing controller. Confirmed backend/ and data/ are empty. Reviewed planned records against endpoint coverage, message-save transaction order, idempotent retry semantics, scoped read-only SQL validation, independent support, explicit preferences, and timing exclusions. Frontend source and package hashes were compared before/after and are unchanged. No backend/runtime tests, installations, database creation, or live model calls occurred; proposed checks remain unexecuted.

## Part 1 evidence curation review

Re-read prior verification/prompt/handoff notes and visually inspected desktop-entry.jpg, narrow-practice.jpg, and narrow-history.jpg. Created the curated index in evidence/README.md and AI-USE.md with limitations and confirmed-versus-unverified review claims. No new browser/unit/build tests or paid/live provider calls ran. The original screenshots were retained; the paused screenshot does not show the still-cue checkbox enabled. Pattern checks across repository-owned text (excluding node_modules, dist and Git internals) found no common private-key/provider-token/literal-credential patterns, personal email addresses, or absolute user-home paths. No .env files were found. This is not an exhaustive security certification.

## Part 1 report audit

Drafted report.md against the supplied Part 1 requirements and verified project notes. Checked local linked-file targets and Markdown section anchors; report distinguishes design proposals, optional prior prototype evidence, and unfinished backend/persistence/live AI/Figma work. Repository URL, milestone commit, and hosted/instructor access remain explicitly unverified. Source/package SHA-256 checks confirmed no changes during drafting. No runtime checks or paid calls were run.

## Part 1 repository checkpoint preparation

Remote inspection found main at a0ae23ea4a57b4dde7f2171582429f340db18a05 with only a README heading. Preserved that repository name above the full local README content. Initialized local part1-submission using the remote initial commit as parent; main is not being replaced. A sandbox blocked the first Git initialization; the authorized elevated attempt succeeded. Extended ignores for local environment variants/logs while retaining example environment files. Credential-pattern scan found no matches in intended files, and no environment or SQLite files were present.

Reran npm --prefix frontend test: four tests passed. Reran npm --prefix frontend run build: passed, 11 modules. No browser checks or live provider calls were rerun. Dependencies and dist output are excluded from the submission. Remote push verification will follow the milestone and separate report update.

Milestone pushed: `2475ce0e59aa627d05725b4bdd9d9c8805abdf26` on `part1-submission`. `git ls-remote` matched the local milestone; remote main remained `a0ae23ea4a57b4dde7f2171582429f340db18a05`. GitHub CLI confirmed the supplied repository URL and PUBLIC visibility. The separate report-update commit pins links to this milestone. Instructor-specific access is not tested. Git used its automatically derived local author/committer identity; no identity was fabricated or rewritten.


## Part 2 inspection — October 21, 2026

Read-only audit of source/notes confirmed mock introduction, in-memory history, unchanged six-cycle timing, and empty backend/data. No new browser/build/unit checks performed. `python3 --version`, `python3 -m pip --version`, `node --version`, `npm --version`, `npm --prefix frontend ls --depth=0`, and Python SQLite/package metadata inspection returned Python 3.12.5, pip 24.2, Node 24.20.0, npm 11.19.0, SQLite 3.45.3, Vue 3.5.44, Vite 7.3.7, plugin-vue 6.0.10. Backend packages are absent from system Python; no backend environment exists.

`git check-ignore -v backend/.env data/app.sqlite3 data/app.sqlite3-wal data/app.sqlite3-shm` confirmed all four paths ignored. No credentials or database created. Approved branch creation initially failed due to sandbox Git write restriction; elevated retry succeeded. Planned backend checks (not run): validated session save/read, persistence across connections/restart, project-relative path from another working directory, identical replay/no duplicate, conflicting replay rejection, invalid inputs/no writes, and transactional rollback. Full browser/API/database verification follows a separately approved frontend integration.


## Minimal backend verification — October 21, 2026

Approved project-local venv creation and `pip install fastapi uvicorn httpx` completed. First install failed because sandbox networking could not resolve the package host; authorized elevated retry succeeded. `pip freeze > backend/requirements.txt` records installed dependencies. `pip check` returned No broken requirements found. Actual versions: FastAPI 0.158.1, Uvicorn 0.54.0, HTTPX 0.28.1, Pydantic 2.14.1, Starlette 1.9.0; Python 3.12.5 / SQLite 3.45.3. Starlette emits a deprecation warning for HTTPX TestClient support; checks still pass. No replacement package installed.

`backend/.venv/bin/python -m unittest discover -s backend/tests -v`: 6/6 passed. Cases: create/read/replay and new-app startup over the same database; conflicting operation or session ID; malformed inputs/extra owner field/SQL-like skill rejected with zero writes; missing record; forced operation-insert failure rolls back the session; absolute database path remains unchanged after chdir. Tests use temporary SQLite files. App-lifespan restart was tested; a separate process restart was not tested in this increment.

Real localhost Uvicorn smoke check (after sandbox port/network restrictions required elevated execution): POST fictional session 11111111-1111-4111-8111-111111111111 using operation 22222222-2222-4222-8222-222222222222 returned 201; identical POST returned 200/replayed=true; GET returned in_progress, active_duration_ms=0, revision=1. Read-only SQLite URI inspection matched ID/status/duration and COUNT=1. Working DB contains this single submitted fictional session. Server stopped cleanly after checks. No actual breathing duration is claimed for this API-only record.

No browser round trip, frontend changes, completed/stopped persistence, full process restart, hidden-tab recovery, live provider, or Figma work was performed. These remain next-increment checks. No credentials or environment file created.


## Session integration checks — October 21, 2026

Commands: `backend/.venv/bin/python -m unittest discover -s backend/tests -v` (9/9 passed), `npm --prefix frontend test` (8/8 passed), `npm --prefix frontend run build` (passed), `git diff --check` (passed before final docs update). Backend additions cover terminal update/replay/list, ownership/revision rejection, last-confirmed interrupted duration and invalid completion. Frontend additions cover pause accounting, offline final retry, lost response after commit reusing operation, and recovery skipping live owners/preserving database duration. Provider behavior is still scripted; no live calls.

Real browser through cua_repl at http://127.0.0.1:5173/: full six-cycle run showed saved completed 60s; observed cycle 1, cycle 4, then completion about 65.9 seconds after first instruction (observation upper bound, not a precise rendering timestamp). Stored start/end delta was 60.003 seconds. Setup excluded; no accelerated timer. Session fca29a4f-6a7d-47f4-9f8a-838bfc5501a9: completed, active 60000ms, paused 0. Still-cue run ca2f5134-1aaa-46ef-9243-dd1bfb2c3037: support paused practice, Resume disabled while support open, closing retained pause, explicit Resume worked; stopped at 14424ms active/3674ms paused (UI floors to 14s). Backend deliberately stopped before final save: UI reported unconfirmed save with Retry and preserved Stop/support. New backend process started; Retry succeeded. Read-only SQLite URI query and HTTP GET matched both records' IDs/status/durations and COUNT=1 each. Browser history matched and retained both after refresh. Full completion preceded final recovery-only refinement; affected recovery and all automated tests/build rechecked afterward.

Second-tab history kept live session e39b067a-3d7e-4cdc-a12a-cc33da5bb5ba in_progress; refreshing owner later recovered it as interrupted with 15s displayed. Earlier hot-reload during initial timing check interrupted a94e0736-6469-4870-8622-0ed66e98846d at 15s; test restarted on final pacing code rather than claiming that run completed. Initial API-only 11111111-1111-4111-8111-111111111111 remains in_progress/0s, explicitly legacy test data without browser ownership. A final visibility experiment produced another stopped fictional record; all records preserved.

Hidden-page limitation: creating another in-app tab and hiding/showing browser panel did not trigger document.hidden/automatic pause. This does not verify real background-tab behavior. Device sleep, another browser/origin, disabled storage, large histories/pagination under concurrent writes, screen readers and a new narrow-width audit remain untested. Support content was preserved, not reverified or contacted. Saved screenshot docs/evidence/part2-saved-history.jpg shows actual records; it is not Figma capture. Screenshot visually inspected. Local backend/frontend remain running for user review; process/session IDs are ephemeral.


## Mock chat verification — October 21, 2026

Commands: backend/.venv/bin/python -m unittest discover -s backend/tests -v: 16/16 passed (seven chat cases plus nine session cases). npm --prefix frontend test: existing eight checks passed. npm --prefix frontend run build passed; git diff --check passed. Existing Starlette HTTPX deprecation warning remains. Chat tests cover success/replay/provider call count, failure/retry with one user row, initial-save rollback, assistant-save rollback then retry, invalid/conflicting/concurrent-pending submissions, interrupted app restart without regeneration, ownership denial and message pagination. Save failures were injected with SQLite triggers only in temporary test databases. Those tests are mock/deterministic evidence, not live API calls.

Browser via cua_repl: empty conversation list and empty selected conversation observed; submitted fictional text, saw saved user/pending response with Send disabled, then actual saved mock reply. Conversation 6278e5b0-e6ee-4972-b340-bae197e1263a contains initial successful request a613f489-0109-436d-84bb-a2c58699c6a0 (user 8d0fcc3a-ddce-4f13-8eb7-9a7d84b72a40, assistant 8f87c26d-06a8-4939-95a5-31c80d9593a7). Failed request 9ac16518-cccf-41d3-bb6e-e9986a6a1cd8 retained user ddc0784c-6307-43d5-bc5a-3080654a0f37 and had zero assistant rows, verified by read-only SQLite. Retry success added assistant 8c046b4d-1246-4c1a-9ffb-75a5f8d46979, preserving user ID; one row per role. Refresh retained all four ordered messages.

Second conversation a6eea6bc-cd99-4928-85c8-f9e19b235279: delayed request completed in its own conversation after switching back to the first; first view stayed unchanged. Actual backend process stop/restart preserved messages. An intended mid-request interruption completed before the shutdown reached it, so that browser run proves restart persistence, NOT mid-request cancellation; interrupted-pending recovery is covered by automated tests. Backend offline submission displayed failed/unconfirmed state and preserved original text/request for retry across refresh. Retry after server restoration produced one user/assistant pair for 6145057a-7c6a-49c1-bb66-697a3fb43d67. Final exact API/read-only SQLite comparison matched four first-conversation and six second-conversation messages by IDs, role, content, sequence, request ID and timestamp instant. Initial raw timestamp-string assertion failed because API uses Z and SQLite +00:00; comparison corrected to UTC instants, not data changed.

Browser check found previous-request success text beside a new uncertain save; fixed by clearing current request on submission and suppressing old success/failure controls while an uncertain submission exists, including reload recovery. Rechecked corrected UI and successful original-ID retry. Screenshots part2-chat-failure.jpg and part2-chat-saved.jpg capture actual fictional records; saved screenshot visually inspected. No resources contacted. No new full-duration breathing run, exhaustive accessibility audit, large-history stress test, real provider, or RAG checks in this increment.

## Mock RAG verification — October 21, 2026

Actual commands: `backend/.venv/bin/python -m unittest discover -s backend/tests -v` passed 26 tests; `npm --prefix frontend test` passed eight; `npm --prefix frontend run build` passed. Existing TestClient deprecation warning remains. Ten new RAG tests cover relevant scoped records/two calls, empty results, complete unsafe-query rejection, bound injection strings, owner/conversation isolation, read-only authorizer, missing database without creation, deadline exhaustion, row/context truncation, stored instruction-like text as data, planning/answer failure counts, invalid citations, and actual generated reply persisted through the normal operation. Temporary fictional databases only. Mock prompt-injection evidence does not establish live-model behavior.

Browser RAG verification is NOT complete. Existing backend process 78013 stopped normally. Restart required port-binding approval; automatic approval review failed because its usage limit was reached, so the restart was not executed. No bypass attempted. Backend is stopped; prior chat screenshots/API comparisons are historical, not RAG browser evidence. No live calls, live configuration tests or live-provider failures were tested. Git ignore check again confirmed backend/.env and data/app.sqlite3 ignored. No credentials created or printed.


## Live provider and exercise verification — October 21, 2026

Commands: backend/.venv/bin/python -m unittest discover -s backend/tests -q: 32 passed. npm --prefix frontend test: eight passed; npm --prefix frontend run build passed; git diff --check passed. No packages installed. Existing HTTPX TestClient deprecation warning unchanged. New provider tests use httpx.MockTransport and temporary fictional databases, covering strict configuration, missing key/no network/no budget consumption, checked Responses payload, repeated-stage prevention, durable ledger, HTTP failure, timeout, refusal, incomplete/malformed output, six-call exhaustion without seventh network call, actual two-stage reply persistence and failure with no assistant. These tests are NOT live model evidence.

Live run: conversation dc043c5e-b2ed-4ed3-bf24-a9c450e01a57; request 8cfe378a-6795-4a94-ab2c-016a33aeafe7; user message 9ddbc7e7-253f-4b7b-aa62-623796876df3. First planning attempt failed with generic provider_failure (original implementation did not retain safe HTTP status). User approved one diagnostic retry after safe HTTP/connection error distinction; second planning attempt returned provider_http_401. Read-only SQLite confirmed exactly one user and zero assistant rows. User corrected local key and explicitly authorized another retry. Planning and answer succeeded: actual assistant 98924f0c-5d62-40c8-83a0-d2632bbf8f85 stated latest session bca4b56e-e2b6-484a-a609-089474646545 was interrupted with 20430ms active. Exact API/SQLite message IDs/content/order/time match; citation/status/duration match source row and visible Vue text. One user and one assistant after retries. Refresh/backend restart preserved reply and four ledger attempts; no regeneration. Successful calls reported 364/38 and 398/82 input/output tokens respectively; failed attempts have unknown token usage, not assumed zero billing. Four of six approved attempts consumed. Screenshots part2-live-auth-failure.jpg and part2-live-saved.jpg; saved screenshot visually inspected. No secrets displayed/captured. Live evidence does not establish general groundedness or injection robustness.

Actual full-duration exercise d6e9094b-071e-4a4b-a671-36c6eaee1cdc: setup observation-to-Start interval 3326ms; first cue observed 407ms after pre-click timestamp; final completion observed 67503ms after pre-click timestamp (67096ms after first observed cue). This is a conservative observation upper bound including application delays, not an exact rendering timestamp. SQLite start/end span 60002ms; active 60000ms, paused 0. No voluntary pause, support visit or hidden interval was subtracted from this timed run. Backend restarted during practice: checkpoint save became unconfirmed but cues continued and completion occurred under 90 seconds. Explicit Retry saved the original completed record once. A selector wait timed out before completion; subsequent timed observations captured cycle 6 and completion, rather than treating that timeout as a failed exercise.

Stopped test 14626005-9c08-4da7-99af-62cd3eb24488: still cue, voluntary Pause/Resume, support-induced pause, Resume disabled while support open, closing support did not resume, Stop while paused succeeded. Stored active6389ms/paused10904ms; Vue floors to6s. Refresh-interruption test bca4b56e-e2b6-484a-a609-089474646545 saved interrupted at last checkpoint20430ms. HTTP/read-only SQLite compared IDs/status/active/paused durations exactly against all three records; Vue shows60s completed,6s stopped,20s interrupted.

Hidden-tab gap resolved using user-authorized native Google Chrome: browser connector unavailable, so used native UI without installing anything. Started session49c91d2f-f545-409d-8e11-46e111f66a13, opened a temporary blank tab, returned and observed explicit hidden-tab pause notice with Resume/Stop. No automatic resume; explicit Resume restored pacing, then Stop saved active7016ms/paused14256ms. Temporary tabs closed; original user tabs preserved. This separate interruption trial is not the uninterrupted timing measurement.

Support panel opened while backend was stopped, after live authentication failure. Static resource links remained available; no call/text/chat service contacted. Required helpline lookup on October21 confirmed existing US/territories 988 service and exact phone/SMS/chat links. No new crisis-input handling applied. Device sleep, exhaustive accessibility testing, and clinical validity are not verified.


## Crisis-chat increment — October 22, 2026

35 backend tests and10 frontend tests pass; build and git diff --check pass. Three backend tests cover phrase limits, direct422 before repository write even without configuration/budget, and legacy saved-input handling with zero calls/no invented reply. Two frontend tests cover phrase variants and known misses/false positives. Initial backend run exposed an indentation error from a duplicated insertion; removed the duplicate guard and reran successfully. No dependencies changed.

Browser: entered “Fictional test quotation: I am not suicidal.” and pressed Send. Fixed notice appeared, draft remained editable, no new message/reply displayed. Read-only SQLite before/after counts unchanged:12 messages,6 requests,4 provider attempts; exact fictional input count0. Stopped backend and repeated Send/opened support successfully, then fully reloaded with backend offline: configuration/history failures remained honest and standing notice/support still rendered. No service links activated. Source support URL/region checked against required helpline lookup on October 22, review date updated. Screenshot part2-crisis-notice.jpg shows the actual notice and independent panel, visually inspected. Old-success text was suppressed beside blocked new input; final build rechecked. Full60s run/Chrome hidden-tab checks from October21 were not repeated because timers/recovery were unchanged. No paid calls.

Figma inspection only: metadata node1:6 and page0:1 plus whoami succeeded. No Figma writes, capture, frame selection or implementation occurred. Read access confirmed; edit access remains unverified with reported Starter/View seat. Available capture tool is not evidence of successful editable capture.


## SmokeTest — October 22, 2026 (user-confirmed results)

Agent-run checks; the user subsequently stated “I verify and approve.” This confirms review of the reported results, not a claim that the user personally performed these tests. No application source was edited. SHA-256 over sorted paths and contents in frontend/src and backend/app (excluding __pycache__) matched before/after: 2465a38b8685f1e494776c825b449b00e0c77988e5d9d14d95a01dee03d252a6.

Commands actually run: `backend/.venv/bin/python -m unittest discover -s backend/tests -v` (35 passed), `npm --prefix frontend test` (10 passed), `npm --prefix frontend run build` (passed), and `git diff --check` (passed). Existing Starlette HTTPX TestClient deprecation warning remains; no dependency change. No unexpected defect found; AutoLoop corrections: zero.

### Newly observed browser/API/SQLite evidence

Unaccelerated six-cycle completion: setup observation 3,812 ms, first cue observed 437 ms after pre-click timestamp, completion observed 61,529 ms after that timestamp (61,092 ms after first observed cue). The conservative Start-to-completion bound includes application and observation delays and is below 90 seconds; it is not an exact render timestamp. No voluntary pause or support time was excluded. Stored active duration is 60,000 ms, not independent evidence of wall-clock performance or breathing adherence.

| Session ID | SQLite/API status | Active ms | Paused ms | Revision | Row count |
| --- | --- | ---: | ---: | ---: | ---: |
| 23824a84-6e8b-4c54-84b3-85a5d6683446 | completed | 60000 | 0 | 13 | 1 |
| 0324f43b-72a6-4c42-84ab-f59bec4fd3dc | stopped | 7923 | 3690 | 3 | 1 |

During the second practice, the backend was stopped. Support opened, paused practice, and allowed Stop with still cue enabled. The UI honestly showed Save not confirmed. Restarting Uvicorn and selecting Retry save saved the same ID. Browser refresh showed both records (60s completed and 7s stopped; whole-second display). Python sqlite3 with mode=ro and GET /api/sessions/{id} agreed exactly on ID/status/active/paused duration/revision; each ID had one row. No service links were activated.

Evidence: [offline save failure and independent support](evidence/part2-smoketest-save-failure.jpg), [history after retry, restart and refresh](evidence/part2-smoketest-history.jpg). Screenshots show UI state; the recorded API/SQLite checks establish the underlying comparisons.

### Newly run simulated evidence

Temporary SQLite databases and FastAPI TestClient additionally checked: empty retrieval with an honest mock reply; provider failure retaining one user and no assistant; retry operation submitted twice leaving one user/one actual mock reply; an assistant-insert failure induced by a temporary database trigger yielding reply_save_failed without an assistant; DELETE proposal rejected before answer generation; and missing live key yielding configuration_unavailable with no provider ledger rows while session GET remained available. No external requests were made. The trigger existed only in a disposable test database. The automated suite separately covers ownership, stored instruction-like text, query limits, and initial-save rollback.

### Historical live evidence, freshly rechecked

October 21 live conversation dc043c5e-b2ed-4ed3-bf24-a9c450e01a57 and request 8cfe378a-6795-4a94-ab2c-016a33aeafe7 were compared again across SQLite, API and refreshed Vue after backend restart. User message 9ddbc7e7-253f-4b7b-aa62-623796876df3 and actual assistant 98924f0c-5d62-40c8-83a0-d2632bbf8f85 matched content, roles, order, IDs and timestamp instants. The reply cites bca4b56e-e2b6-484a-a609-089474646545 as interrupted with 20430 ms, matching its saved row. Exactly one message per role exists for the request. This is reinspection of an earlier live answer, not newly generated live evidence.

Health and SQLite usage remained four of six live attempts consumed. No new paid calls. Historical native Chrome hidden-tab pause/explicit resume was not rerun. Missing-key, injected provider/database failures and rejected SQL were not individually replayed in the browser this run; actual browser backend-outage support and save recovery were checked. Device sleep, exhaustive accessibility, live-model variation and clean-checkout reproducibility remain unverified.


## Chat layout cleanup — October 22, 2026

Approved chat layout check: 10 frontend tests passed, production build passed, and git diff --check passed. Actual existing desktop (1280px) and narrow browser tabs showed removed copy and composer before both history sections; existing saved conversation remained visible. Keyboard Tab from empty textarea skipped disabled Send to New conversation; with a temporary unsent fictional draft, Tab focused Send. Draft was cleared without submission. No model calls or new database records were initiated. Review screenshots are temporary /tmp/chat-layout-desktop.jpg and /tmp/chat-layout-narrow.jpg, not curated submission evidence. No full exercise/backend regression rerun for this template-only change.


## Newest question and reply layout — October 22, 2026

Chat pair ordering check: 10 frontend tests/build/diff check passed. Focused in-memory check of the actual grouping code passed newest-group order, question/reply order, failed single-question group, empty input and nonmutation of stored-order input. Existing desktop and narrow browser conversations show newest question first, previous successful question immediately followed by its actual reply, and conversation history below. Latest existing request 2bf7b7cb-d24c-4cfb-aeb9-0e6f363352bd displays budget_exhausted beside its question; read-only SQLite confirms failed/budget_exhausted/zero provider calls for this request and six ledger attempts overall. This is newly observed existing data, not a call made by this layout check. No messages submitted or budget changed. Screenshot /tmp/chat-newest-pairs.jpg is temporary review evidence. Multi-page loading is implemented but not browser-tested with a >100-message conversation; no new pending request was generated.


## Practice fullscreen — October 22, 2026

Fullscreen increment: 10 frontend tests, build and diff check passed. Actual browser verified native fullscreen, Minimize, Escape and keyboard Enter activation; same session retained paused progress at3s and still-cue choice across transitions. Resume/support induced pause worked, closing support did not resume, and Stop saved session3c0ae768-509a-4404-a0cc-f81db5301515. Read-only SQLite status/duration: ('stopped', 3768). Desktop fullscreen and narrow normal layout inspected; introduction absent. No paid calls/service contacts. Browser-denied fullscreen fallback and physical mobile fullscreen remain untested. No new full60s timing run; engine unchanged. Temporary review screenshot /tmp/practice-fullscreen.png.

## Submission publication verification — October 22, 2026

Student explicitly confirmed review and authorized commit/push plus final report update. Source/evidence milestone `080ad6393a2ade204f6f2b417b422a5778a8ed4c` pushed on `codex/part2`. All15 unique source/document/evidence paths linked by report were fetched from the public commit-specific raw GitHub URLs without authentication: HTTP200 for every file. Part1 pinned report also returned200; remote Part1 branch remained e958bdcf11e69b5c4451f986742989acd01b497e. No new application code or live model calls in this publication step. Final report replaces approval placeholders with actual review/commit/link status; course upload remains unperformed by the agent.

## Profile/calendar extension — newly observed October 25, 2026

Branch `codex/profiles-calendar`, uncommitted; Part 2 submission and report unchanged. New work uses fictional local profiles and mock providers only. No paid call, dependency installation, commit, push, merge, deployment, or course submission performed.

Commands: `backend/.venv/bin/python -m unittest discover -s backend/tests -q` → 49 passing; `npm --prefix frontend test` → 10 passing; `npm --prefix frontend run build` → passed. An initial attempted pytest command found pytest absent; used the project's existing unittest runner without installing anything. Existing Starlette/httpx deprecation warning remains. Python 3.12.5 and Node 24.20.0 were inspected during the foundation increment.

Isolated temporary SQLite fixtures in `test_calendar.py` verify empty history; two same-day completions; exclusion of stopped/interrupted records; completion across a local midnight/month boundary; UTC versus America/New_York placement; repeated DST 01:30 with distinct -04:00/-05:00 offsets; pagination; invalid ranges/zones; missing/stale identity rejection; duplicate session writes; refresh and recreated application persistence; two-profile/guest isolation. Guest-transfer/delete tests preserve IDs on transfer, reject cross-profile conversation/request reads, scope mock RAG to the guest's own session, reject switching during active practice, preserve guest through restart, and verify confirmed discard removes its records. Delete/discard tests use isolated fictional fixtures, not the user's original records. These automated fixture checks are not live-model evidence.

Fresh actual browser checks on localhost:

- Created `Fictional Calendar Alex` with name only; calendar initially empty. Created `Fictional Calendar Bailey`; its calendar remained empty despite Alex's completed sessions. Guest also saw no Alex events.
- Ran two full practices through the existing Vue timer. SQLite stored 60,000ms active duration for each. First record `85c5a3ff-e367-457b-8391-cab0abd9bdc0` started `2026-10-26T02:03:56.439+00:00`, ended `2026-10-26T02:04:56.440+00:00` (60.001s between persisted start/end). This interval is not a fresh setup-to-final-step measurement; the earlier full-sequence evidence above remains historical.
- First event matched the same session ID in SQLite, the HTTP calendar response, and the Vue rendered `data-session-id`. API completion `2026-10-26T02:04:56.440Z` became browser **Sunday October 25, 10:04:56 PM EDT**. Second rendered record `94c369ee-a6a3-4b7a-a4bc-526d632025dc` showed **10:07:05 PM EDT** under the same day.
- Next month showed empty November; Previous returned October. Page refresh retained Alex selection; opening Calendar returned saved entries. Backend process was stopped/restarted and Refresh calendar returned both identical entries.
- At 390×844 CSS pixels, date headings, event times, labeled month input and wrapping controls were observed. Temporary viewport override was reset. Screenshot `/tmp/calendar-phone.png` is local review evidence, not a committed evidence artifact. Native phone hardware and screen-reader operation were not tested.
- Guest practice → Switch paused and displayed Continue practice / Stop and switch. Stop and switch saved a stopped record. Continue as guest, browser refresh, and Session history showed that stopped record. Explicit Save this guest activity to my profile and Alex selection transferred it; Calendar still showed only the two completions.

Before runtime migration, SQLite backup was made at ignored `data/before-profiles-20261026T020236Z.sqlite3`. A read-only row-by-row comparison confirmed the original 25 sessions, 5 conversations, 23 messages, 13 requests, 474 session operation receipts, 9 conversation receipts, and 6 provider attempts were identical after migration. Legacy records remain under their existing owner. No synthetic calendar events were inserted into the working database; runtime completions came from the browser timer.

Corrections during verification: an interrupted fixture initially tried to advance duration and correctly received409; corrected fixture to use its last saved checkpoint. Recovery test originally used the old unscoped journal key; updated it for the approved identity namespace. No timer duration change was made. Full Figma comparison, physical phone testing, browser UI deletion/destructive failure injection, and a complete screen-reader audit remain unverified. Local profiles remain an explicitly shared chooser, not real authentication. User verification of this calendar increment is pending.

## Library and responsive layout — October 26, 2026

User approved preceding profile/calendar increment and requested library plus responsive web layouts. Saved profile names now John and Bailey: John had already been changed before inspection and was preserved; Fictional Calendar Bailey was renamed through the existing revision-checked profile API, retaining its ID and activity.

Before browser access was interrupted, the library was observed in the running browser with one Open breathing practice button and three Coming later / Unavailable names. Clicking each unfinished entry left the accessibility tree unchanged. Source review confirms those entries are plain headings/text with no handlers or links. The available button emits `practice` to the existing navigation function; final click-through browser verification remains outstanding. Read-only SQLite comparison afterward confirmed all28 session rows exactly unchanged from the pre-check snapshot: no fabricated sessions or completions.

After responsive changes: `npm --prefix frontend test`10 passed; production build passed; backend unittest49 passed; `git diff --check` clean. No exercise timer/model/database code changed for the library or layout. Existing tests cover unchanged60-second six-cycle timing, pause/stop and failure/retry persistence. Source review confirms viewport permits zoom, form/long-text wrapping, focus outlines,44px minimum primary control heights, in-flow navigation, sticky support and Stop, and retained reduced-motion/still-cue rules. Source inspection is not visual evidence.

Browser verification was blocked by a browser security-policy rejection when acquiring localhost access. No alternate browser/control surface was used to circumvent it. Therefore new320/390px portrait, landscape, text zoom, keyboard traversal, touch-target geometry, long-content/forms, desktop regression, and support/Stop during failure checks remain unverified in the browser. Previous390px calendar observations above predate these CSS changes. No physical-device/native-app/PWA verification is claimed. User visual verification pending; do not treat automated build/tests as a substitute for these checks.

## Later milestone SmokeTest checkpoint — October 26, 2026

Source-unchanged SmokeTest reran backend unittest (49 passing), frontend tests (10 passing), production build (passing), and git diff --check (clean). Tests use isolated fictional SQLite data and mocks; no live-model calls occurred. These cover ownership isolation, guest transfer/discard, calendar timezone/midnight/DST boundaries, duplicate prevention, persistence, RAG scope and failure/recovery behavior. Automated checks do not substitute for complete browser coverage.

Read-only runtime SQLite PRAGMA integrity_check returned ok; foreign_key_check returned zero violations. At that checkpoint there were28 sessions:10 completed,2 in_progress,5 interrupted,11 stopped. Previously observed calendar session IDs85c5a3ff-e367-457b-8391-cab0abd9bdc0 and94c369ee-a6a3-4b7a-a4bc-526d632025dc retained their completion timestamps and60000ms active durations. This is persisted-record evidence, not a new duration measurement.

Browser inspection initially failed because the connection-error page used a policy-blocked data: URL. After the user manually reopened the app, inspection succeeded. The user confirmed only that the app was visible, not that all flows passed. Separately approved copy change: Create a fictional profile → Create a profile. Browser accessibility output confirmed the new label; production build passed after the change. Direct Continue as guest opened practice successfully. Remaining fresh visual/failure checks must be recorded individually; earlier profile/calendar observations remain historical.

Figma metadata request for22:249 returned Starter-plan tool-limit error. No newly verified design comparison, editable capture, or frame contents are claimed. Physical-device checks remain untested.

Fresh browser follow-up: guest entry click timestamp1793044354438; next-call instruction observation1793044358208 (setup/entry upper bound3.770s); Start click returned1793044358565; completion and Session saved observed1793044426520. Conservative entry-to-final-observation upper bound72.082s includes setup, application and tool-observation delays; no voluntary pauses/support time were excluded. The first instruction appeared during entry, so this also bounds first-instruction-through-final-step below90s for this run. Exact rendering timestamps were not instrumented. A premature completion wait timed out while Cycle2 was visibly running; subsequent observation confirmed normal completion.

Exercises navigation showed one available breathing action and three noninteractive unavailable headings. Open breathing practice returned to the existing completed-practice view without starting another session. Guest switch returned to the chooser with explicit save/discard choices; neither was selected. The new guest completion remains retained. Chooser screenshot: /tmp/profile-label-review.png (temporary local review artifact). No physical-device verification or complete refreshed SmokeTest is claimed.
