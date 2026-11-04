# Assignment 3 — Part 3.3: Integration, Evaluation, and Demonstration

**Project:** A little space · **Student:** Mallory Pierz · **Updated:** November 3, 2026

This coursework prototype offers short, reviewed exercises, an optional preference quiz, local profiles and saved activity, and optional typed/voice AI conversation. Vue owns the interface, FastAPI applies business rules, and SQLite stores scoped records. It uses fictional data for evaluation. It is not therapy, diagnosis, safety monitoring or evidence of clinical effectiveness.

## Open the demonstration and error evidence

1. **[Download/play the frontend demonstration video](https://raw.githubusercontent.com/mallorypierz/mentalhealth_app/909f25f32c8b3705a0d5acce82652f4facf6021d/recordings/Screen%20Recording%202026-11-03%20at%206.58.39%E2%80%AFPM.mov)** — download the MOV and open it in a video player if your browser does not play it inline.
2. **[Download/play the combined error/process video](https://raw.githubusercontent.com/mallorypierz/mentalhealth_app/9cbd9a969504913aa766cf7680b3caaa2a66d3ee/recordings/process-demonstration.mov)** — 2:40, silent; recorded tests and app comparison followed by the written failure/fix/code explanation.
3. **[Open the error report, fix and retest evidence](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/recording/error-evidence.md)** — the actual reported local-access failure, code explanation and mocked regression results.
4. **[View the retained passing retest output](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/recording/identity-retest.txt)**.

These are public, commit-pinned links and work independently of the local project folder. The failure and fix are also explained in this report under “Actual failure, decision and retest.” **The combined process recording is supplied with on-screen written explanation; it has no audio track.**

## Submission links and status

| Artifact | Location and status |
|---|---|
| Repository | [mentalhealth_app](https://github.com/mallorypierz/mentalhealth_app) |
| Published implementation | [Commit bdf3f84c72a9a27c27b10646d4ec2605f5982a81](https://github.com/mallorypierz/mentalhealth_app/commit/bdf3f84c72a9a27c27b10646d4ec2605f5982a81), branch `codex/exercise-quiz`; push and remote hash verified. This revised report, selected recording and later evidence are published as a subsequent submission update; the implementation commit remains the source reference. |
| Setup | [README](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/README.md), with credential-free mock setup and documented tests |
| Frontend demonstration | [Watch/download the frontend recording](https://raw.githubusercontent.com/mallorypierz/mentalhealth_app/909f25f32c8b3705a0d5acce82652f4facf6021d/recordings/Screen%20Recording%202026-11-03%20at%206.58.39%E2%80%AFPM.mov). This direct download link works from this report alone; no local project folder is required. The newly added file is 73.6 MiB and has not been independently re-inspected. The separately preserved original is **5:02 with no audio track**; [inspection record](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/recording/received-video.md). The selected submission copy is included in this branch; the larger original remains local. GitHub may offer download rather than inline playback. |
| Process demonstration | [Download/play the process video](https://raw.githubusercontent.com/mallorypierz/mentalhealth_app/9cbd9a969504913aa766cf7680b3caaa2a66d3ee/recordings/process-demonstration.mov) — **2:40, silent**. First clip122.125s; explanation clip38.305s.  [Actual failure/fix evidence](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/recording/error-evidence.md) and [recording outline/narration](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/recording-outline.md) are prepared. The recording shows the retained evidence and code; it is not footage of the original invalid-access error. |
| Evaluation | [18-case matrix](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/scenarios.json), [mock results](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/evaluation.md), [live results](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/live/comparison.md), [verification log](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/verification.md) |
| Disclosure and handoff | [AI-USE.md](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/AI-USE.md), [current handoff](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/handoffs/current.md) |
| Earlier submissions | [Part 3.1/Part 1 rationale](https://github.com/mallorypierz/mentalhealth_app/blob/e958bdcf11e69b5c4451f986742989acd01b497e/report.md); [historical Part 2 report](https://github.com/mallorypierz/mentalhealth_app/blob/bdf3f84c72a9a27c27b10646d4ec2605f5982a81/report.md) |

The report consolidates completed work and evidence; it does not claim that every submission requirement is finished. Outstanding items are listed at the end.

## Finished application and behavior

People may enter as a guest or select a local fictional profile. Profiles have no password and are not secure authentication. Guest activity can be explicitly transferred to a profile or discarded through the existing confirmation flow. Quiz answers for guests are temporary and are not transferred with activity.

| Exercise | Planned sequence and controls |
|---|---|
| Paced breathing | Six 4-second inhale/6-second exhale cycles,60 active seconds; Pause, Resume, Stop and optional still cue |
| 5-4-3-2-1 sensory grounding | Five15-second prompts, up to75 active seconds; optional5/4/3/2/1 checkmarks, Next step and final Finish exercise. Automatic progression remains a fallback. Early advancement saves actual active duration. |
| STOP | Four15-second prompts,60 active seconds; includes a breath-focused step |
| Cognitive reframe | Three20-second prompts,60 active seconds; no required writing or sharing of thoughts |

The student explicitly approved the source-based adaptations before implementation. Grounding and reframe sources were NHS guidance, and STOP came from the VA toolkit; exact source links and contracts are in [design notes](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/design-pipeline.md). Later wording and grounding controls were requested by the student. Reframe's second prompt now reads, “What makes this thought seem true? Could there be another way to explain what happened?” These brief adaptations do not claim the entire underlying skill must be accomplished within a timer.

Application code controls steps, timers, exits and support. Models cannot select arbitrary exercises or change instructions. Stop remains available; old timers are cleared on restart/leaving. Opening support pauses practice, and closing it does not automatically resume. The support route does not require model output, a questionnaire or a classifier. No support service was contacted during checks. The last exercise-implementation support lookup is recorded in verification notes; this report does not claim a new resource lookup today.

Results distinguish stopped, completed and interrupted sessions. Completion records the sequence ending, not improved mood or proof the person performed each activity. Calendar events derive from completed records; stopped/interrupted records remain in history. Grounding checkmarks are temporary UI state and are not stored as wellbeing measurements.

## Quiz, preferences and transparent history

The optional quiz displays one question at a time: preferred activity, then comfort with breath focus. Users can skip a question or the quiz, choose No preference, go back, change answers, retake, reject a suggestion or choose another exercise. Preview and Start remain separate.

| Answer condition | Deterministic output |
|---|---|
| Explicit available activity, no breath conflict | Suggest that exercise and explain the activity answer |
| Breathing or STOP plus Avoid/Not sure | Conflict; no recommendation; invite another choice |
| Skipped/neutral activity plus Yes to breathing | Suggest breathing and explain the Yes answer |
| No clear preference otherwise | No ranked winner; choose manually |
| Unrecognized input or unavailable match | Invalid/unavailable fallback; no arbitrary replacement |

Example1: breathing rhythm + Yes suggests breathing. Example2: surroundings + Avoid suggests grounding. Both examples use actual preferences, not a clinical score or a promise of maximum benefit.

Profiles can explicitly check Remember and Save preferences, choose Use saved answers, update them, or Forget. Background loads never silently replace current choices. Current explicit answers take priority over older saved answers. Previous exercises appear separately and **never influence suggestion ranking**. There is no hidden completion-count inference.

Preferences use owner scope, revisions and stable operation IDs. Forget retains a revision tombstone/receipt so an old retry cannot restore forgotten answers. Delayed responses are ignored after identity/context changes or component departure. Saved/failed/unknown outcomes are shown distinctly and retries reuse operation IDs.

## Architecture, persistence and SQL RAG

| Responsibility | Actual implementation |
|---|---|
| Views and interaction | `frontend/src/App.vue`, `ProfileGate.vue`, `components/ExerciseLibrary.vue`, chat/history/profile components |
| Local exercise and quiz rules | `frontend/src/exercise.js`, `exercises.js`, `recommendation.js` |
| HTTP and persistence coordination | `frontend/src/api.js`, `sessionPersistence.js`; FastAPI routes/controllers and typed `backend/app/schemas.py` |
| Database/model responsibilities | `backend/app/repositories`, `preferences.py`, `db.py`, migrations008/009; SQLite under project-relative `data/app.sqlite3` |
| Retrieval and providers | `backend/app/rag`, provider adapters and application-owned usage ledger |

Vue sends HTTP/JSON to FastAPI; only backend code opens SQLite or reads private provider configuration. Schema changes preserve existing records. Writes are parameterized, scoped and transactional where related rows must succeed together. Conversation/message/request IDs, roles, order, timestamps and actual reply content remain inspectable. Save retries cannot create duplicate records. A failed request does not fabricate an assistant reply.

For history questions, the first model call proposes retrieval SQL from the question/schema. Backend validation treats it as untrusted, restricts grammar/tables/fields, supplies owner scope and bound parameters, and executes only validated reads through a read-only connection with row/time/context bounds. The second model call receives retrieved records with IDs and field meanings plus reviewed context. Stored content is data, not instructions. Returned citations must belong to retrieved records, although citation membership does not prove semantic correctness. Actual accepted answers are saved before being returned with persistence status.

Empty retrieval, rejected SQL, database failure and provider failure remain distinct. Rejected retrieval may permit a general educational answer with unavailable history disclosed, but cannot supply invented personal-history evidence. Voice adds transcription and speech synthesis around the same scoped planning/answer flow. Recognition/audio can fail independently of a saved text answer.

## Changes from the Part 3.1 rationale

These decisions use the class-principle mapping already supplied in the project, rather than inventing new principles.

| Earlier choice | Implementation/testing revision and rationale |
|---|---|
| One60-second breathing exercise | Three reviewed alternatives added at the student's request; breath avoidance excludes both breathing and STOP. R3/R4 support choice and control. |
| Optional introduction | Removed after student review to reduce setup and reading. D3 supports low burden; quiz remains optional. |
| One page containing both questions, preferences, history and library | Student found this overwhelming. One question per step, concise copy and collapsed supporting sections now reduce competing content (D1/D2/D3). Two useful questions retained rather than adding inputs with no meaningful mapping. |
| Automatically timed grounding only | Student requested Next and checkmarks. Actual elapsed time is tracked separately from skipped scheduled time, and grounding-only completion accepts shorter duration. R1 preserves a bounded sequence; R3/R4 preserve agency. |
| Optional remembered choices | Explicit profile-only Save/Use/Forget implemented, with current-answer precedence and no history-based effectiveness inference (D5). |
| Proposed bottom navigation | Student selected Figma OptionA top navigation. The received desktop recording shows a left navigation rail; full breakpoint parity with that reference has not been established. The selection is design intent, not proof of visual equivalence. |
| Voice interruption | Earlier playback cutoff led to explicit Stop speaking and microphone blocking during playback. Speaker echo remained a plausible diagnosis, not a proven historical cause. |
| Reusing stored local access on startup | A real database-switching failure revealed that Retry reused rejected credentials. Bounded401 recovery now returns a fresh chooser while preserving records. |

R2/D4 motivate independent support; D6 motivates restrained motion and neutral language. These are design rationales, not evidence of clinical effectiveness.

## Evaluation method and repeatable checks

Expected results were recorded before execution in the18-case matrix. Fictional temporary databases and mocked responses are the routine default. Automated tests, real-browser interactions and read-only SQLite inspection supply different evidence and are identified below. **17 scenarios passed within their stated scope; S15 remains not-run as a combined browser case.** An automated pass is not relabeled as a browser pass.

The original evaluation ran82 backend tests,33 frontend tests and a production build. Subsequent grounding changes passed83 backend tests; quiz/recovery changes reached37 frontend tests and a successful build. The identity-recovery subset was rerun with3 passes. These are dated runs, not one newly rerun final combined suite. [Verification notes](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/verification.md) retain commands and limitations.

Repeat with existing approved dependencies:

```sh
backend/.venv/bin/python -m unittest discover -s backend/tests -q
npm --prefix frontend test
npm --prefix frontend run build
sh docs/evidence/part3/run_checks.sh
```

The evaluation script uses mocks; the one-off live script is not a routine test command. Original scenario button labels below reflect the evaluated UI before later copy simplification.

### Fictional scenarios: expected and observed

| ID / fictional scenario and setup | Expected | Observed | Mode / status / evidence |
|---|---|---|---|
| S01 — First-time guest skips quiz. New fictional guest; choose Find a suggestion then Skip quiz | Library remains usable; no exercise starts or saves. | Browser: new guest opened quiz, skipped, returned to available library; no Start invoked. | mock · **pass** · [browser-notes.md](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/browser-notes.md) |
| S02 — Quiz suggests breathing. Choose breathing rhythm + Yes | Breathing suggestion explains the chosen activity; preview requires Start. | Browser: breathing + Yes showed breathing and “You chose Follow a breathing rhythm”; separate Continue action. Mapping cross-product passed. | mock · **pass** · [browser-notes.md](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/browser-notes.md) |
| S03 — Quiz suggests alternative. Choose surroundings + Avoid | Grounding suggested; instructions unchanged. | Browser: restored surroundings/Avoid produced grounding and explained non-breath-focus. Mapping test passed. | mock · **pass** · [browser-notes.md](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/browser-notes.md) |
| S04 — Breath activity uncomfortable. Choose STOP + Avoid | No breath-focused suggestion; conflict explained and alternatives available. | Automated decision cross-product: STOP/breathing with Avoid or Not sure returns conflict and no suggestion. Browser conflict screen not separately replayed. | mock · **pass** · [frontend-output.txt](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/frontend-output.txt) |
| S05 — No clear preference. Select No preference for both answers | No ranked winner; choice list remains available. | Automated skips/neutral cases return no exercise; no arbitrary tie-breaker. Browser no-preference case not separately replayed. | mock · **pass** · [frontend-output.txt](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/frontend-output.txt) |
| S06 — Reject suggestion. Reject breathing suggestion; manually open reframe | Reframe preview opens without automatic start. | Browser: rejected breathing recommendation, opened reframe preview; Start still required. | mock · **pass** · [browser-notes.md](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/browser-notes.md) |
| S07 — Load remembered preferences. Fictional profile saves surroundings/Avoid; reload and Use saved answers | Saved values restored only by explicit action. | Browser fresh profile selection and explicit Use saved answers restored surroundings/Avoid. | mock · **pass** · [browser-preferences.txt](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/browser-preferences.txt) |
| S08 — Change or forget preferences. Change saved answers then Forget; replay older save | Answers cleared; old retry cannot resurrect them. | Automated test_preferences_isolation_retry_forget_restart saved then forgot; replay of original save left answers null. | mock · **pass** · [backend-output.txt](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/backend-output.txt) |
| S09 — Profile isolation. Fictional A has records; switch/read as Fictional B | B cannot read A preferences/activity; stale requests rejected. | Automated preferences/identity/calendar/voice tests enforce owner scope and stale context; unrelated profile has no preference answers. | mock · **pass** · [backend-output.txt](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/backend-output.txt) |
| S10 — Completed exercise history. Run a guided sequence to completion | Correct exercise ID, completed status and duration saved once and displayed. | Browser reframe completed and saved; Vue history data-session-id 0ceca131-a343-4098-963c-73c78e1c5777 matches SQLite completed/60000. Start-to-observed completion upper bound 65854ms; setup not timed. | mock · **pass** · [browser-history.txt](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/browser-history.txt) |
| S11 — Stop partway. Start STOP, then Stop | Stopped status and actual active duration saved, not completed. | Browser reframe stopped/36427ms (Vue floors to 36s); new ID f5d08ef6-bab3-4896-a562-c2f7cb38a0ba. Automated alternatives test also covers STOP stop. | mock · **pass** · [database-after.json](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/database-after.json) |
| S12 — Refresh interrupts. Refresh an unfinished practice after a checkpoint | Recovered interrupted record uses last confirmed checkpoint; no duplicates. | Browser reload recovered interrupted/29615ms, ID 47b8c6b8-eadf-4c69-ac19-ea93d6b03f9e; Vue shows 29s. Outbox test confirms last confirmed checkpoint and no duplicate recovery. | mock · **pass** · [browser-history.txt](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/browser-history.txt) |
| S13 — Failed save retry. Inject receipt failure or lose commit response; retry same operation | Honest failed/unknown state; rollback or idempotent replay; one record. | Mocked receipt failure rolled back; retry saved one preference row. Outbox lost-response test replayed same operation without duplication. | mock · **pass** · [backend-output.txt](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/backend-output.txt) |
| S14 — Delayed response. Resolve request after switching identity or leaving screen | Old response ignored; new identity/view unaffected. | Frontend late preference response rejected after identity change; LatestRequest and voice tests ignore cancelled/replaced responses. | mock · **pass** · [frontend-output.txt](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/frontend-output.txt) |
| S15 — Model failure and support. Inject failed provider request; open support | No invented reply; support independently accessible. | Provider-failure automated checks passed, but support access in the same failed-model browser state was not executed in this evaluation. Combined case not-run; do not infer pass from separate checks. | mock · **not-run** · [backend-output.txt](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/backend-output.txt) |
| S16 — Scoped history RAG. Ask fictional latest-practice question with two owners | Only active owner records retrieved; actual answer grounded in IDs. | RAG tests returned owned stopped/23s record with matching source/citation IDs, denied foreign owner, and scoped guest among two profiles. | mock · **pass** · [backend-output.txt](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/backend-output.txt) |
| S17 — Empty retrieval. Ask history question with no saved matches | Empty outcome and insufficient-history reply; no invented records. | test_empty_is_distinct_from_rejection returned empty and no matching saved records reply, with no citations. | mock · **pass** · [backend-output.txt](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/backend-output.txt) |
| S18 — Untrusted write query. Mock planner proposes DELETE FROM exercise_sessions | Rejected before execution; stored rows unchanged; rejection distinguishable. | Parser rejects write structures; pipeline rejected-query test asserts retrieval never called; read-only authorizer denies DELETE; fixture remains readable. | mock · **pass** · [backend-output.txt](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/backend-output.txt) |

### Explicit behavior checks

| Check | Evidence and result |
|---|---|
| B1: A suggestion never starts an exercise; conflicts/invalid/unavailable answers do not produce an arbitrary exercise | Decision cross-product tests plus browser preview/rejection: passed within those scopes |
| B2: Persistence retains truthful status/duration and retry does not duplicate records or resurrect forgotten preferences | Transaction/replay/outbox/recovery tests plus browser saved-history evidence: passed |
| B3: History remains owner-scoped and proposed writes never execute | SQL validation/reader/identity tests, empty/rejected retrieval and fixture checks: passed |
| B4: Support remains usable in the same browser state after a model failure | Combined browser check **not-run**; separate failure tests and independent support observations do not establish this invariant |

### Inspectable saved records

Read-only SQLite queries (`mode=ro`) and Vue DOM history attributes matched reframe session `0ceca131-a343-4098-963c-73c78e1c5777`, completed/60000ms. Stopped and interrupted examples were36427ms and29615ms; the UI floors them to36s and29s. Fictional preference owner `1296fb51-3fb2-44c2-a6a3-b180d183b43e`, revision1, surroundings/avoid matched SQLite, GET `/api/preferences` and Vue `data-preference-id`. API inspection used a separate fictional identity without printing tokens. Later early-grounding completion `191cdf8a-5132-435d-b57e-5479160e7549` saved15859ms and displayed15s. These are different checks with different scopes, not one combined capture.

Evidence: [database snapshot](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/database-after.json), [history UI](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/browser-history.txt), [preference UI](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/browser-preferences.txt), [early-grounding record](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/grounding-next-record.json). Integrity checks passed and foreign-key violations were absent in the inspected evaluation databases.

### Separate live-model variation

The host approved a12-call sample before execution. The existing ledger was inspected without resetting it. Three exact typed cases were repeated twice, with planning+answer counted separately:6 trials,12 calls total. No transcription, speech, retries or failed attempts occurred in this sample. Fictional contexts were isolated from working transcripts; fresh UUIDs prevented repetition contamination. The configured model snapshot was `gpt-5.4-mini-2026-03-17`.

| Case | Exact input and setup | Observed across two repetitions |
|---|---|---|
| L01 grounded history | “What happened in my most recent saved exercise? Give its status and active duration.” Older owned completed breathing, latest owned STOP stopped23000ms, and a later foreign-owner record | Both cited their expected owned STOP record and answered stopped/23s; no improvement claim or foreign-owner evidence |
| L02 insufficient history | Same question, fresh owner with no exercise history | Both acknowledged insufficient history; no invented status, duration or citation |
| L03 education | “What is the difference between a grounding exercise and a breathing exercise? Explain briefly without recommending a treatment.” Fresh owner, approved context | Both distinguished the activities without inventing personal history. One used general benefit wording; another added an unnecessary treatment refusal and simplified grounding to external awareness. |

All6 replies were saved. Wording varied while L01 facts stayed consistent. The general-benefit wording is a quality limitation, not evidence of effectiveness. Two repetitions cannot estimate reliability. No live failure occurred, so timeout/refusal/save-failure variation remains **untested**. Full responses, citations and calls are in [results.json](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/live/results.json) and [comparison](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/live/comparison.md).

This12-call evaluation allowance was consumed. Later user demonstrations used the existing separate24-call session capacity; current remaining capacity must be read from the ledger, not inferred from a dated report. All planning, answer, transcription, speech, retries and failed attempts count. Sessions are host-approved and capped at50; exhausted/unavailable allowance returns new requests to labeled mocks. Peer testing defaults to mocks. Local cost reservations are not invoice guarantees.

### Surprising finding and untested limitation

An evidence-backed surprise was that rejecting unsafe retrieval need not prevent every useful reply. `test_rejected_and_failed_retrieval_can_answer_without_history` verifies a general fallback with unavailable history disclosed, while the rejected SQL never executes. Evaluation therefore checks non-execution, explicit uncertainty and absence of fabricated retrieved evidence, rather than requiring total silence after every rejected query.

Physical mobile sleep and background timer throttling remain untested. Fake-clock tests establish planned60/75-second sequences. One real reframe run reached observed completion within65.854s after Start, including observation overhead. Setup time was not instrumented in that run and is reported separately as unmeasured. Early grounding's15859ms saved active time is not a comprehensive wall-clock performance study. Comprehensive keyboard/narrow-screen checks, all-skill real-time timing, simultaneous browser races, full browser save-outage coverage and live failure variation remain incomplete.

## Clean-checkout reproduction

README commands were followed in `/tmp/mentalhealth-part3-clean`, cloned from a source-only local candidate **b3d8087c3e16e16d880c8a6230e5d43976ac4d6c**. It represented base016d251 plus the then-uncommitted implementation. No credentials, working database, installed Python environment or node_modules were copied. The host approved the exact installations first. Python3.12.5, Node24.20.0 and npm11.19.0 were used; packages installed from declared pins/lockfile. Cached downloaded wheels were reused, so this was not a cold-network-cache test.

Without `.env`, default startup initialized a fresh SQLite database and served mocks. Frontend-to-backend health, guest entry, quiz, separate preview/Start, completed reframe, history, refresh and both service restarts were verified. ID `7a52c388-0797-414b-b75d-d3a9c06a2ba9` remained one completed60000ms row after restart.82 backend tests,33 frontend tests, build and pip check passed. No tracked generated files appeared. [Exact commands, logs and before/after records](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/clean-checkout.md).

This establishes agent reproduction using README, not independent human peer testing. Candidate b3d8087 predates the later quiz presentation, reframe copy, grounding Next/checkmarks and identity recovery. Those changes have their own tests/browser evidence, but the final published bdf3f84 source has **not** received a new full clean-checkout run. The revised report must not imply otherwise.

## Actual failure, decision and retest

The user reported: “why does it say that and wont let me on the pageLocal access is invalid or revoked.” This occurred after the backend changed from the isolated test database to the original live database. The browser retained the earlier local identity. Source inspection found that `ProfileGate.vue`'s startup and Retry reused that token. The expected behavior was a usable chooser after rejected local access, while transient connection failures should preserve valid access.

The fix is `restoreIdentity(request, getAccess, clearAccess)` in [identityRecovery.js](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/frontend/src/identityRecovery.js). A401 response clears only browser access and makes one new bootstrap request. The chooser requires an explicit profile/guest selection. Other failures propagate; records, pending writes and provider ledger are not deleted or replayed.

[Three mocked regression tests](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/frontend/tests/identityRecovery.test.js) verify401 recovery, retained access for network/403/500 failures, valid identity reuse and bounded failed bootstrap. [Retained output](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/recording/identity-retest.txt):3 passed,0 failed. The user later reported the error no longer appeared. No original screenshot/HTTP trace was retained, and automation could not reacquire the original affected tab; this is not a controlled end-to-end browser recovery pass. [Process evidence packet](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/evidence/part3/recording/error-evidence.md) states those limits explicitly. The [combined process screencast](https://raw.githubusercontent.com/mallorypierz/mentalhealth_app/9cbd9a969504913aa766cf7680b3caaa2a66d3ee/recordings/process-demonstration.mov) now shows the test run and retained failure/fix/code evidence. It is silent and retrospective, not a controlled reproduction of the original affected browser state.

## Explanation of generated code

[frontend/src/recommendation.js](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/frontend/src/recommendation.js), function **`decide(activity, breath, available)`**, implements the quiz decision table.

- **Inputs:** a finite activity key (or empty/none), breathing preference (`yes`, `avoid`, `unsure`, empty or none), and the list of available reviewed exercises.
- **Output:** `{ status, reason, exercise }`; `exercise` is an available definition or null. Status distinguishes suggested, invalid, incomplete, unavailable and conflict.
- **Rules:** validate both inputs; use explicit activity first; when activity is absent/neutral, Yes may choose breathing; check availability; reject breath-focused matches for Avoid/Not sure; generate an explanation from the actual answer.
- **Safeguards:** no arbitrary tie-breaker, no model call, no score, no persistence and no timer start. Model output cannot inject an exercise or change reviewed instructions. Preview/Start is handled separately by the application.
- **Limitations:** two preferences do not describe all needs or predict clinical benefit. The classification of STOP as breath-focused follows its reviewed breath step. A person can reject the match and choose manually.

[Mapping tests](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/frontend/tests/recommendation.test.js) cover the activity/comfort cross-product, missing/invalid inputs, unavailable exercises, changed answers and unchanged instructions. Example: `decide('sensory_grounding_5_4_3_2_1', 'avoid')` returns grounding; `decide('stop', 'avoid')` returns conflict with null exercise.

## Demonstration recording

The student supplied a frontend screen recording on November3. A checksum-matched local copy is preserved at `recordings/part3-recording-2026-11-03.mov`:117573632 bytes,301.7167s,**zero audio tracks**. The student subsequently added a second copy, linked as [Watch/download the frontend recording](https://raw.githubusercontent.com/mallorypierz/mentalhealth_app/909f25f32c8b3705a0d5acce82652f4facf6021d/recordings/Screen%20Recording%202026-11-03%20at%206.58.39%E2%80%AFPM.mov). That newer file has not been independently re-inspected. The selected submission copy is included alongside this report for GitHub download; the larger original remains local. The absolute download link works when this Markdown report is submitted by itself.

Seven sample frames showed profile selection/creation, breathing with still cue, typed chat, grounding checkmarks, STOP and voice controls. This was a sampled review, not continuous playback. It does not establish that two quiz paths, rejection, remembered preferences, saved history and opened support are all demonstrated. Those items require full-video review or a short supplementary clip. No narration or AI speech was captured; add narration/captions or a separate explanation if required. That frontend recording contains no confirmed process section. A separate combined process video is now linked above.

The [recording outline](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/recording-outline.md) supplies two marked sections, concise narration and mode labels. Screens showing live controls are not proof of a successful new live reply. The controlled live evaluation above supplies separate evidence. The supplied process video combines122.125seconds of browser comparison/test output with38.305seconds of scrolling through the error evidence, fix code and explanation. Both inputs have no audio. Exported at1920×1080, duration160.433seconds; sampled output frames decode correctly. Full visual-coverage and instructor-access review remain necessary.

## Figma status and AI-use disclosure

The student selected OptionA (top navigation) in [Assignment3 Figma references](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-110). Historical browser-editor work created17 native text/vector frames with sampled editability checks. [Selected practice reference](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-213), [flow](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-721), and [alternativeB](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-828) remain linked for review. Instructor access is unverified.

This was not successful MCP capture, a wired prototype or a verified Figma-to-Vue implementation round trip. The static PNG/SVG fallback predates the editable browser references. Layout/typography/control differences remain, including calendar event list versus grid and the desktop recording's navigation rail. Do not describe them as pixel-matched. Full details are in [design-pipeline.md](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/docs/design-pipeline.md).

Codex assisted with implementation, tests, evidence inspection, documentation and recording planning. The student supplied scope, approved reviewed exercise wording/timings, selected design preferences, tested the app, requested refinements and produced the frontend recording. Agent checks are not attributed to the student. Provider models and important revisions are disclosed in [AI-USE.md](https://github.com/mallorypierz/mentalhealth_app/blob/909f25f32c8b3705a0d5acce82652f4facf6021d/AI-USE.md); no exact coding-agent serving snapshot is asserted. No clinical evaluation was conducted. This report was AI-assisted and needs the student's final review.

## Final submission checklist

- [x] Implementation, preferences, history, SQL RAG, source and tests published in bdf3f84.
- [x] README, architecture/contracts, AI-use disclosure and handoff maintained.
- [x] Eighteen fictional scenarios with expected/observed results and evidence;17 passes and1 not-run honestly identified.
- [x] Three explicit behavior checks, surprising finding and untested limitation reported.
- [x] Bounded live variation sample recorded separately from mocked checks.
- [x] Earlier exact-candidate clean-checkout evidence and later-change limitation recorded.
- [x] Frontend recording received and preserved locally.
- [ ] Review full frontend video coverage; add mode labels/narration or supplementary footage as needed.
- [x] Include the selected frontend video in the repository and link it from this report. Instructor-specific access still requires confirmation.
- [x] Supply a combined process screencast with test output and the written historical failure/fix/code explanation. Silent recording; original error not captured live.
- [ ] Complete S15 combined failure/support browser check, or retain its not-run status.
- [ ] Verify the final source from a clean checkout; retain timing/device/Figma limitations until tested.
- [x] Prepare the revised report, selected recording and later evidence for publication together; use this file’s Git commit history for the documentation/submission revision.
- [ ] Verify instructor access to repository, videos and Figma; submit the coursework. No course upload or merge has been performed.
