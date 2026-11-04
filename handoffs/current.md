## Selected recording publication — November 3, 2026

User explicitly requested Git upload of the selected74MiB Screen Recording MOV. Added a narrow ignore exception for that file and included the updated submission report/recording evidence. Larger112MiB original, credentials and runtime databases remain ignored. Relative report link resolves to the selected movie. Newer copy has not been independently reviewed for full content/audio; original inspection limitations remain. Publishing on codex/exercise-quiz, no merge/course upload.

## Local recording link — November 3, 2026

Student added a74MiB Screen Recording MOV under recordings. report.md now links that exact file with a URL-encoded relative path. File existence verified; new copy not re-inspected. Original112MiB inspected recording preserved. Both movies remain Git-ignored and unuploaded; link works only with the accompanying folder, not on GitHub yet. No commit/push.

## Consolidated Part 3.3 submission report — November 3, 2026

Replaced historical Part2 report.md with the current Part3.3 submission report. Earlier report remains linked in Git history. Includes implementation/quiz/personalization, actual class rationale revisions, architecture/SQL RAG, all18 expected/observed scenarios with mode/status/evidence, behavior checks, bounded live variation, exact clean-checkout scope, actual invalid-access failure/retest, generated decide function explanation, Figma limits, AI disclosure and final checklist. Added received5:02 silent frontend video status; no hosted video or completed process recording claimed. Notes desktop recording navigation rail versus selected Figma top-nav intent. Local report links resolve and all18 scenarios are present; diff whitespace check passed. Documentation only; no new runtime tests, provider calls, recording or publication. Published application remains bdf3f84; this report and subsequent evidence edits await publication/student review.

## Frontend recording received — November 3, 2026

User supplied Screen Recording 2026-11-03 at6.58.39PM.mov. Preserved a byte-identical copy at recordings/part3-recording-2026-11-03.mov (117573632 bytes; SHA25627c7ebf4ddb0036e678b8af3eb5385b5d217ac0bbe066a058ccaabf6c7fc6323). Original remains intact. Large local movie excluded from Git; no upload performed. Native AVFoundation inspection reports301.7167seconds and0 audio tracks. Sandboxed frame decoding initially failed; native decoding with approved escalation succeeded. Do not characterize the file as damaged.

Seven sampled frames at6.03,54.31,105.60,156.89,208.18,259.48,292.67seconds show profile chooser, breathing/still cue, typed chat, grounding/checkmarks, STOP, voice controls and profile creation. This is sampled visual review, not complete playback or verification of every action/requirement. No recorded narration/audio present. No process section confirmed by the sampled frames; process recording and full coverage/accessibility review remain pending. Quiz paths, remembering preferences, support opening and history coverage are not established by this sample. Recording must be shared separately with reviewer access checked.

## Process evidence packet — November 3, 2026

Created docs/evidence/part3/recording/error-evidence.md from the actual user error report, published recovery code and retained3-pass mocked test output. Includes a short narration, provenance and original browser-trace/screenshot limitations. No new tests, live calls or recordings; working app unchanged.

## Recording readiness — November 3, 2026

User preparing to record. Both servers were stopped; restarted normal configured backend8000 (session27222) and frontend5173 (session38405). Proxied health confirms provider=openai, voice_enabled=true, selected session14/24 used,10 remaining. No paid readiness call was made; physical microphone/playback and a fresh provider reply are not verified by health. Existing ledger/configuration preserved. Recommend original invalid-access report plus mocked identity-recovery regression test for process evidence; no deliberate disruption of live app. Current readiness supersedes earlier12-remaining observation.

## Recording-outline publication refresh — November 3, 2026

Updated docs/recording-outline.md to identify published implementation bdf3f84c72a9a27c27b10646d4ec2605f5982a81 on codex/exercise-quiz and use a historical diff for process evidence. Prior push verified matching remote hash. Recordings, final-revision clean-checkout and other disclosed gaps remain pending. Documentation-only; no new calls, recordings, server changes or test execution.

## Saved project checkpoint — November 3, 2026

User requested saving all work. Checkpoint includes Part3 implementation, tests, evaluation evidence, README/design/verification updates, AI-use disclosure and recording outline on codex/exercise-quiz. Credentials, runtime SQLite, installed dependencies and temporary environments remain local/ignored. No remote push requested. Latest checks:83 backend tests,37 frontend tests,production build; identity-recovery targeted retest3 passed. Recordings and other documented limitations remain pending. Use git log for this checkpoint hash; older uncommitted statements below describe earlier stages.

## Recording outline — November 3, 2026

Prepared docs/recording-outline.md with two marked sections, exact fictional mock recording setup, UI steps/narration, actual invalid-access failure evidence, generated decide function explanation, and submission checklist. Recordings remain pending; no screen capture was made. Re-ran identityRecovery.test.js:3 passed, retained docs/evidence/part3/recording/identity-retest.txt. No paid calls or running-server changes. Current live backend remains live; recording instructions require deliberate isolated mock setup. Earlier original affected-tab browser recovery remains unverified. Final clean-checkout/source publication and S15 remain pending.

## Invalid local access recovery — November 3, 2026

After switching from isolated mock data to the original live database, the user's browser retained an identity token unknown to that database. Boot previously retried the same rejected token indefinitely. Added bounded recovery on HTTP401 during identity restore: clear only browser access, request a fresh chooser identity, and let the user explicitly select a profile/guest. No saved database records, outbox entries, or usage ledger are deleted; no pending mutation is replayed. Network/403/500 failures retain credentials and report failure. A failed bootstrap does not loop.

Verification:37 frontend tests/build passed, including401 recovery, valid identity, other failures and bounded failed bootstrap. Existing browser handles could not be reacquired (browser-control error); recovery in the user's existing tab is not claimed browser-verified. User should refresh. No paid calls, backend restart or credential/configuration change.

## Live chat restored — November 3, 2026

At the user's request, replaced isolated mock backend with normal project startup on8000 (session91043), using existing ignored configuration and original data/app.sqlite3. Frontend5173 proxy health verified provider=openai and voice_enabled=true. Selected existing session has12 used of24,12 remaining; no ledger reset/cap increase/.env edit or provider call made. The user requested restoration of live voice/text; remaining existing allowance is available for their interactions. Legacy health live_calls fields (6/6) refer to a separate old ledger, not the selected profile/voice session. Configuration success is not a new end-to-end provider/audio test. Existing recent live text evidence remains separate; microphone/playback not reverified. Isolated mock database remains preserved in /tmp/mentalhealth-part3-clean/data/app.sqlite3; its profiles are not merged into the original database. Refresh and choose an original profile/guest after switching databases. No source change or commit/push.

## Grounding Next step and tracking — November 3, 2026

Student requested manual advancement and checkmarks. Grounding now has optional numbered checkboxes (5/4/3/2/1), Next step and Finish exercise. The existing automatic 15-second steps remain as fallback; Pause/Stop/support remain available. Checkmarks are local, reset on restart, never required and never saved or interpreted as wellbeing. Reviewed instruction text unchanged. Setup separate; active guided sequence remains at most75s, excluding voluntary pauses. Explicit Next may shorten it.

Contract change: grounding completed duration may be 0–75000ms; other exercises still require their full planned duration. Repository validates against the stored skill; request schema cannot do that without the saved record. No database migration required. Frontend tracks skipped scheduled time separately from actual elapsed time; saves actual active duration and last confirmed interruption checkpoint. Manual advancement is disabled while paused/support open; late boundary clicks cannot skip an extra step.

Checks: 83 backend tests,34 frontend tests,build passed. New tests cover early completion/replay, timing/pauses/restart/automatic boundary and non-grounding exclusion. Browser: two checkmarks, Next through4/3/2/1, Finish → saved completed15s. Read-only SQLite actual ID/duration in docs/evidence/part3/grounding-next-record.json; screenshot grounding-checkmarks.png. No paid calls/dependencies. Updated project backend serves explicit mocks using the preserved isolated database on8000 (session46475); frontend5173. Clean candidate b3d8087 is historical and does not include this change. No commit/push.

## Reframe wording — November 3, 2026

At the student’s annotated request, simplified step 2 to “What makes this thought seem true? Could there be another way to explain what happened?” This preserves considering evidence and alternative explanations, the 20-second step and 60-second sequence. No other exercise instructions or behavior changed. Frontend exercise tests passed; no new live calls. This wording is newer than the clean-checkout candidate.

## Quiz presentation refinement — November 3, 2026

User requested less overwhelming UI and shorter wording. Two existing preference questions now appear one at a time with progress, Back, Skip question and Skip quiz. Kept two because additional questions do not yet have an approved meaningful mapping to the four exercises. Activity labels and fallback copy shortened; deterministic mapping and stored activity/breath values unchanged. Saved preferences and history are collapsed; history/library are hidden while answering. Result offers preview/another choice/edit/retake, never automatic Start. Step changes focus the heading. Reviewed steps, backend/data contracts, voice/chat and top navigation unchanged by this increment.

Verification: 33 frontend tests and production build passed; browser guest surroundings/avoid produced grounding, Change preserved answers, Skip cleared each answer, both skipped gave no match, retake reset selections. Support remained visible. Screenshot: docs/evidence/part3/quiz-simplified.png. Full saved-profile browser and physical-device checks not repeated. No new dependencies or paid calls. Serving project frontend on5173 (session56918), still connected to isolated mock backend8000; earlier clean checkout is preserved. This UI revision is newer than clean candidate b3d8087 and is not covered by that historical byte-equality result. No commit/push.

## Current Part 3.3 status — November 3, 2026

This section supersedes older current-state claims below; those entries are historical. Branch `codex/exercise-quiz`, root base `016d251a957870f9196de4a9b96e705801c644d5`; unfinished changes preserved, no root commit/push.

Approved live sample completed: six typed trials, exactly 12 planning/answer calls, no speech/transcription/retries/failures. Existing selected 24-call ledger preserved and charged 12 reservations; earlier “working database untouched” claims apply only to earlier mock increments. No production transcripts were used: fixtures/replies remained in fresh temporary databases. Run allowance exhausted; underlying session still has unused capacity, which is not authorization for more calls. See `docs/evidence/part3/live/comparison.md`. Live failure behavior untested.

Approved isolated dependencies installed and README followed in `/tmp/mentalhealth-part3-clean`, exact local candidate `b3d8087c3e16e16d880c8a6230e5d43976ac4d6c`. No .env/private data/installed folders copied. 82 backend tests, 33 frontend tests, build and pip check passed. Real browser quiz → explicit preview → completed reframe → saved history survived both service restarts and reload, same ID `7a52c388-0797-414b-b75d-d3a9c06a2ba9`, completed/60000, one database row. Read-only integrity/FK checks passed. Final documentation/evidence is newer than that candidate; application files match. This is agent verification, not independent peer testing or a published remote checkout.

README, Part 3 evaluation, disclosure and evidence now distinguish actual results from remaining work. Figma status: selected top-nav A; historical browser-created editable text/vector frames, not successful MCP capture or a verified implementation round trip. No new Figma operation.

Remaining: S15 combined failed-model/support browser check; full physical-device/keyboard/timing and live-failure evidence; demonstration/process recordings and student review. Do not label these passed. Next: complete a controlled mock S15 and recordings, then review/checkpoint the source when requested. Current isolated mock servers started for verification on 8000/5173; recheck availability before use. Private configuration was not changed, so normal root startup must not be assumed mocked.

---

## Live variation proposal — November 2, 2026

Prepared docs/evidence/part3/live-plan.md: three exact typed cases, two repetitions each, up to12 calls total (planning+answer only; no transcription/speech/retries). All live results UNTESTED pending explicit host approval. Read-only ledger: selected active24-call session4078a5d0-8b28-4dc4-8aac-324d5dc16cc9 has0 attempts;49 unassigned historical voice attempts and6 legacy text attempts preserved. Proposed12-call run consumes at most$0.60 local reservations, not guaranteed actual invoice cost. No ledger reset, new session, configuration change or paid call. Next: obtain explicit host approval, then verify model availability and execute only the approved sample with fictional fixed contexts.

---

## Part 3.3 evaluation — November 2, 2026

Created docs/evidence/part3/scenarios.json with all 18 expected cases before running checks; readable results are in docs/evidence/part3/evaluation.md. This run records 17 passes within explicitly stated automated/browser scopes and S15 not-run as a combined failed-model-plus-support browser case. Separate provider-failure tests are not treated as proof of that combined invariant. Reproducible command: sh docs/evidence/part3/run_checks.sh. Logs retain 82 backend passing tests (16.667s), 33 frontend passing tests, successful production build. No application source corrections were made during this evaluation.

Real browser: guest skip; breathing recommendation/explanation; rejection and manual reframe preview; reframe completed/saved/history within65854ms of pre-Start timestamp; stopped36427ms; reload recovered interrupted29615ms; returning profile explicitly restored saved surroundings/Avoid answers; grounding suggestion explained actual choice. Vue history ID0ceca131-a343-4098-963c-73c78e1c5777 matches read-only SQLite completed60000ms. Database snapshots: integrity ok, no FK violations, zero voice provider attempts. Screenshots and AX text retained. Setup time was not instrumented; do not present the Start-to-observation bound as setup timing.

B1 choice/no-auto-start: mapping tests + manual preview passed. B2 idempotent saves/status: temporary-DB/outbox checks passed. B3 scoped history/read-only SQL: RAG/identity checks passed. B4 independent support after a model failure: combined browser verification still not-run. Surprising result: rejected SQL may lead to general fallback answer with unavailable history disclosed; no query execution or invented retrieved evidence. Untested limitation: physical mobile sleep/throttling. No live variation, paid calls, clean checkout or recordings.

Branch codex/exercise-quiz, base016d251, existing uncommitted work retained. New evaluation files only plus documentation. Next: execute S15 in a controlled mock failure browser session; obtain explicit live-call budget for a small variation sample when requested, then clean-checkout/recording tasks. No commit/push or working-database changes.

---

## Saved quiz preferences — November 2, 2026

Implemented profile-scoped GET/PUT /api/preferences, additive migration 009, explicit Remember+Save, Use saved answers, Forget, reload and same-operation retry. Guests cannot persist quiz answers; those answers are not transferred with activity. Current answers drive suggestions and are never silently overwritten by a background fetch. Late responses are rejected by existing identity-context guards and component lifetime/read-generation checks. Previous exercise choices show saved status/duration/time/ID separately; history never influences suggestions. RAG allowlist/reader/providers unchanged; preferences are not model-readable.

Verification: backend unittest discovery 82 passed (16.742s), frontend 33 passed, production build passed, git diff --check passed. New tests cover two-profile isolation, injected receipt-insert failure with transactional rollback, same-operation retry, revision conflict, stale context, restart, forget followed by an old-save replay (cannot resurrect answers), and frontend stale-response rejection. Initial full-suite discovery failed on a test helper relative import; corrected to package import and reran successfully. Existing deprecation warning remains.

Browser/API/SQLite comparison: in isolated mock app, created Fictional Preference Alex, chose surroundings + avoid breath focus, explicitly remembered and saved. Vue showed Preferences saved. Fresh browser load and reselecting the profile showed Use saved answers; clicking it restored the two choices. Vue DOM data-preference-id, HTTP GET /api/preferences, and read-only SQLite preferences.owner_id matched 1296fb51-3fb2-44c2-a6a3-b180d183b43e, revision 1, sensory_grounding_5_4_3_2_1 / avoid. API check used a separate fictional browser identity and compared parsed answers and revision, without printing access tokens. This is preference-record evidence, not a new exercise or model response. Restart persistence and failed-save retries were tested in temporary-database TestClient runs, not browser outage injection.

No working database, .env, provider ledger or dependencies changed; zero paid calls. Mock verification backend 8001 session 25107; test frontend 5173 proxies to it via temporary config. Existing uncommitted changes preserved on codex/exercise-quiz (base 016d251); no commit/push. Still unverified: full browser preference failure/retry/forget and simultaneous profile-switch races, physical-device/keyboard checks, complete timing/evaluation/recordings. Next: review these paths in the browser and then final Part 3 evaluation.

---

## Quiz decision-table refinement — November 2, 2026

Implemented pure decide(activity, breath, available) with explicit suggested/conflict/incomplete/invalid/unavailable outcomes and answer-specific reasons. Activity wording now describes the desired action. Skip and no preference are distinct values; Change preserves answers; Retake resets both; rejecting returns to the library. Only explicit acceptance emits an available exercise key to preview; Start remains separate. No provider, database, voice/chat, exercise-instruction or support code changed in this increment. Existing uncommitted work preserved on codex/exercise-quiz, base 016d251.

Checks: targeted backend exercise suite 3 passed (temporary databases, save/replay/restart/migration); frontend 32 passed including full activity/comfort cross-product, incomplete inputs, invalid inputs, unavailable choices, answer changes and unchanged instructions; production build and git diff --check passed. Existing previous-turn browser STOP → saved → SQLite stopped/13990ms evidence establishes the frontend/backend path; not a new browser quiz interaction run. Browser quiz, keyboard/mobile and real-time completion checks remain pending. No paid calls, credentials, working-data mutation, dependency installation, commit or push. Next: browser verification of quiz acceptance/override/retake/support and confirmation that preview creates no session.

---

## Part 3 exercise implementation — November 2, 2026

Branch codex/exercise-quiz, base 016d251; uncommitted. Existing October 29 notes preserved. Added three student-approved exercises (grounding 75s, STOP 60s, reframe 60s), two-question optional quiz with deterministic suggestions/override, distinct saved identifiers, calendar names, migration 008, and tests. Breathing remains six 4/6 cycles. New instructions are still text with Pause/Stop; no model-generated steps. Quiz answers are transient, not saved preferences. Third display question omitted to keep quiz short; new exercises have no motion.

Checks run: backend unittest discovery 80 passed (16.567s); frontend node tests 28 passed; Vite production build passed; git diff --check passed. Mock/temporary SQLite tests verify per-exercise durations, completion rejection, stopped/interrupted records, calendar exclusion, replay, restart, old-row/receipt preservation and migration idempotence. Frontend fake-clock checks verify every new step boundary, completion, pause/stop and recommendation exclusions. Existing Starlette/httpx deprecation warning remains; no dependencies installed.

Browser: isolated mock backend on 8001, temporary fictional database /tmp/mentalhealth-part3-check/fictional.sqlite3; frontend on 5173. Initial 5174 origin rejected correctly; moved test frontend to existing allowed origin without changing protection. Browser handle failed once; fresh tab recovered. Guest entry, all four library entries, STOP preview, first live step, Stop, and Session saved were observed. SQLite read-only inspection confirmed the STOP stopped record. No paid calls, private environment changes or working-database migration. Support resource lookup rechecked; links not contacted.

Remaining: full real-browser completion timing for all new exercises (setup separately), quiz interaction/keyboard/mobile checks, browser API/SQLite comparison by record ID, outage/support/refresh/restart regression. Automated clock checks are not wall-clock evidence. No claim of full Part 3 evaluation, clean checkout, saved personalization, recordings or Figma implementation. Next: finish those browser checks, then review the diff before a requested commit. Test servers use isolated mock data; normal startup still uses existing local configuration.

---

## Current handoff — selected Option A, October 27, 2026

Latest task completed: approved qualitative Vue/Figma comparison and edits to docs/design-pipeline.md, docs/verification.md, handoffs/current.md and report.md only. Branch codex/profiles-calendar; unchanged HEAD175fc28ecadb5d0a50bf48a39208d44e10ef6014; published application source aaa6fce619ec3e1a4baaedcf6bc4fa64f0f354a8. The student subsequently reviewed this increment and explicitly approved its commit and push. This publication is documentation-only; use Git history for its resulting commit.

Student selected A (top navigation). Browser-created Figma page31:110 now has14 desktop/phone view frames, flow31:721, states31:773 and unselected B31:828. Desktop voice was corrected to37:2. Native text/vector layers were inspected, existing Page 1 preserved and inventory re-read. See the new leading section of design-pipeline.md for all links, research tradeoffs and comparison. No successful MCP capture or new Figma-to-Vue implementation is claimed.

Read-only running-app inspection used available551×688 viewport, not exact390/1440. App top navigation agrees in structure; calendar is an event list (Figma grid), profile and voice have more actual controls/notices, fonts differ, and profile still mentions Optional chat. Entry source-inspected only. Current browser voice UI said mock; no configuration change or call-budget diagnosis was attempted. Do not assume earlier live-activation notes describe the current UI. No new exercise, message, save, microphone or paid call was initiated.

The student approved the documentation and differences and authorized this commit/push. Next: retain the disclosed limitations for submission. Obtain specific approval before any source correction, grid/layout implementation or additional evidence files. Exact viewport/device checks, implementation round trip and instructor Figma access remain incomplete. Original submitted commits and data preserved. README and AI-USE were outside this four-document approval; their older static-only summaries have not been updated in this increment and should be reconciled in a separately approved publication update.

All older handoff entries below are historical, with this section authoritative for the latest comparison/documentation task.

---

## Latest publication — October27,2026

The student approved committing/pushing all updates. Published source/evidence: [aaa6fce](https://github.com/mallorypierz/mentalhealth_app/commit/aaa6fce619ec3e1a4baaedcf6bc4fa64f0f354a8) on `codex/profiles-calendar`, including explicit testing-session budgets and14 desktop/phone static reference PNGs plus SVGs. All10 report-linked files and14 reference PNGs verified publicly readable without authentication. The report now pins this source version. Previous uncommitted/pending-publication statements below are historical and superseded here. Tests for this source:77 backend,26 frontend and production build passed; no paid publication checks. Figma is still a static manual-import fallback, not an editable MCP update. No merge, deployment or course upload.

# Current handoff — October27,2026

Working directory: /Users/mallorypierz/mentalhealth_app. Branch codex/profiles-calendar; HEAD6f995d4ff1c7e60de72ce42ac62f1ab301d25e3e. Approved voice source/tests and evidence are now published at1b7b834978c78051655bb25e273ff58101e3e4a7; publication details below supersede the earlier HEAD. User has now explicitly approved commit and push for this updated milestone. Publication verification follows below.

The student explicitly verified the chatbot and approved all completed additions for the updated Part2 documents. report.md now consolidates profile/guest access, calendar, library placeholders, responsive styles and real voice/typed chat. Original Part2 source080ad63/reportf133bf99 and Part1e958bdcf remain preserved. docs/later-milestone-report.md points to the consolidated report.

Current checks:74 backend tests,26 frontend tests and production build passed; whitespace checks clean. Provider tests mocked; no paid calls during final audit. Runtime read-only ledger49 attempts/$2.45 reservations at inspection. Exact counters may change. Backend last started in tool session74073 PID81198 with absolute ceilings65 calls/3250000 microdollars. Generic startup defaults20/$1. Do not reset budget or add allowance again. Live peer testing must stay mocked pending compliance with assignment's maximum50 calls per session; current cumulative limit is not session enforcement.

Voice is hands-free turn-taking with gaps, not duplex realtime. Capture starts explicitly, stops on support/hide/profile switch, ignores frames during reply playback, and resumes listening only within an active visible session. Typed input remains. Actual text is saved before speech; retries and state guards prevent duplicate/stale results. General wellbeing discussion is allowed under educational boundaries; personal-history claims require records. Rejected SQL remains blocked, but an explicitly empty context permits general answers. No raw SQL/private values in rejection diagnostics.

Submission steps: source commit/push/hash and hosted evidence checks completed; final report review and student upload remain. No new hash or remote access claimed yet. Figma editable round trip remains unverified; comprehensive phone/accessibility checks, saved still-cue preference and clean-checkout reproduction remain incomplete. Part3 evaluation/recordings are not claimed complete. See report.md and docs/evidence/voice-update.md.

No application source, runtime configuration, Figma or Git state changed during this final document-preparation task. No merge/deployment/course upload. Next action: complete authorized commit/push and pin report evidence links. Figma get_metadata is blocked by Starter-plan MCP quota; do not claim an update. Do not spend calls to verify chat again.


## Publication result — October27

User explicitly approved commit/push of all completed changes. Source/evidence commit1b7b834978c78051655bb25e273ff58101e3e4a7 was pushed to codex/profiles-calendar and git ls-remote matched exactly. Original codex/part2f133bf99 and part1-submissione958bdcf remote hashes remained unchanged. All9 report-linked files were verified publicly readable at the new source commit using certificate-verified system curl (Python’s separate local certificate store failed). Report links now pin that source snapshot. Earlier pending/uncommitted wording is historical and superseded here. This documentation follow-up finalizes publication evidence. No merge, deployment or course upload. Figma metadata was blocked by Starter-plan MCP quota; no Figma edit occurred.


Latest follow-up supersedes65-call configuration: hard/default cap50 and2500000 microdollars; .env live voice flag disabled, backend session81914 PID82391 using normal uvicorn startup in mock mode.49 historical voice attempts retained, no reset. Static Figma pack in docs/figma-fallback (14 PNGs plus SVG sources and notes) needs manual import; no native editable-frame claim. Changes are not yet committed/pushed under a new approval; report relative fallback link must be pinned after publication.


New approved increment supersedes cumulative cap: explicit host-created testing sessions, each max50, with immutable prior unassigned ledger. Live requires VOICE_TEST_SESSION_ID as well as flags/key; no session auto-created. Default runtime remains mock. No new paid allowance activated. Tests/migration verification below; changes still await separate commit/push approval.

Testing-session increment verified:77 backend/26 frontend/build passed. Backend session71807 PID83039; mock mode and no selected/new testing session. Migration007 preserved all49 historical rows against backup. User review and separate live session/budget approval remain next; do not create/activate a paid session automatically.


October27 approved live activation: student explicitly approved24 new calls/$1.20 local reservations for3–5 spoken exchanges plus retry margin. Created testing session4078a5d0-8b28-4dc4-8aac-324d5dc16cc9 with immutable24/1200000 caps, selected it in ignored backend/.env and enabled voice. Other settings/key preserved.49 historical attempts remain unassigned and do not count toward this session. Backend restarted in session54339 PID83363. No paid verification call made; this is configuration/ledger evidence, not a new successful model reply. Actual provider charges may differ from reservations. Earlier mock-only current-runtime notes are superseded for this explicitly approved session; peer testing should still use mocks by default.


## Local server startup — October 29, 2026

Requested frontend/backend startup on `codex/profiles-calendar`, HEAD `016d251`. Used existing dependencies: Python 3.12.5 and Node 24.20.0. Started `backend/.venv/bin/python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000` (tool session 87294) and `npm --prefix frontend run dev -- --port 5173 --strictPort` (session 74917). Sandbox initially blocked listening; approved elevated execution succeeded. `curl` verified frontend `/` HTTP 200 and proxied `/api/health` success on http://127.0.0.1:5173. Existing configuration reports voice enabled and active testing session with 24 remaining calls; no provider call made. No source, dependency, configuration or budget changes. Full browser/functional testing was not run for this startup request. Next: user accesses the running app; recheck server availability in future sessions.
