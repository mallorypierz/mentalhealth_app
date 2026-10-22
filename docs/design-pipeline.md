# Design pipeline — current Part 2 implementation

Updated October 22, 2026. This document supersedes earlier implementation-status notes. The preserved [Part 1 proposal](https://github.com/mallorypierz/mentalhealth_app/blob/e958bdcf11e69b5c4451f986742989acd01b497e/report.md) and [initial flow](diagrams/part1-flow.md) remain historical design evidence.

## Chosen experience and rationale

Entry → six 4/6 breathing cycles → completed/stopped result → optional saved history. Chat is outside timed practice. Six cycles remain 60 planned seconds; smoothing the moving cue adds no breath hold or delay. Fullscreen/minimize arrows, Pause, Stop, explicit Resume and still cue are application-owned controls. Optional scripted introduction and developer testing dropdown were removed following student review.

Source: the supplied assignment research table (15 patients, 13 clinicians, 15 evaluation sessions, 150 participant–task combinations). Counts below are mentions, not effect sizes, unique-person counts or proof of clinical benefit. Applying them to a fictional college student is a design hypothesis.

| Finding | Design choice, alternative and tradeoff |
| --- | --- |
| R1: short duration (38 mentions) | Fixed 60-second skill avoids duration setup; less flexible than a picker. Measured observed completion remains below 90 seconds. |
| R2/D4: frictionless safety (30/31) | Independent support is available without chat or saving. Fullscreen header stays visible; normal-view scrolling is an unresolved limitation. Selected persistent bottom bar remains unimplemented. |
| R3/R4: stop and choose (39/68) | Pause, explicit Resume, Stop, optional chat/history. Easy stopping permits accidental exits but avoids coercive completion. |
| D1/D2: simplification and atomic skill (54/100) | One cue, optional fullscreen, one skill. No distress inference. General navigation refinement outside fullscreen is still pending. |
| D3: low emotional cost (148) | No required typing/questionnaires before Start. This sacrifices personal context rather than inventing it. |
| D5: low-burden personalization (49) | Current still-cue choice is temporary. Approved future opt-in remembering/change/forget behavior remains unfinished; no preference table/API exists. |
| D6: restrained language (97) | Neutral results and restrained motion with still alternative. Less expressive; full accessibility and universal comfort are not established. |

## MVC and ownership

Vue owns presentation/input and local pacing. `App.vue` coordinates views, support and exercise; `exercise.js` uses a monotonic clock; `sessionPersistence.js` serializes asynchronous saves and recovery; `api.js` owns HTTP errors/timeouts; `components/ChatView.vue` owns conversation view state. `style.css` supplies shared styles.

FastAPI `main.py` and `api/conversations.py` expose routes. `schemas.py` and `chat_schemas.py` validate typed contracts. `controllers/conversations.py` coordinates generation outside database write transactions. Repositories implement business checks and parameterized writes; `db.py` resolves the database from the project location. The backend alone opens SQLite and calls providers. The single fictional demo profile is resolved by backend code, not selected by model SQL. This is not authentication for a multi-user service.

Current SQLite tables: `demo_users`; `exercise_sessions` (owner, fixed skill, status, timestamps, active/paused duration, checkpoint, revision, fixture flag and owner token); `operations` (session operation ID/input hash/result); `conversations`; `requests` (status, attempts/calls, provider/model, retrieval/citation/failure metadata); `messages` (conversation/request foreign keys, role, actual content, sequence, timestamp); `conversation_operations`; `provider_attempts`. Schema migrations and idempotent initialization preserve existing records. There is no preference table, separate retrieval-record table or session-to-conversation relationship; session retrieval uses the shared demo-user ownership.

Stable UUIDs and foreign keys preserve identity. Unique `(conversation_id, sequence)` and `(request_id, role)` prevent duplicate messages. One pending request per conversation prevents overlapping generation. Operation ID replay with identical input returns the recorded result; conflicting reuse returns 409. Session revisions and owner tokens reject stale or unauthorized mutation. Owner tokens are local recovery protection, not production account security.

## Actual HTTP contracts

All paths use `/api`. Unknown input fields are rejected. UUIDs and timezone-aware times are validated. Common immediate errors: 422 `invalid_input`, 404 missing/out-of-scope, 409 `operation_conflict`, 503 `database_unavailable` with persistence `unknown`. Error bodies contain `error.code`, `message`, `retryable` and persistence. Empty lists are successful empty results. Generation errors are normally persisted request outcomes returned by status polling, not invented synchronous 502/504 responses.

| Method/path | Input | Success and persistence | Errors/special behavior |
| --- | --- | --- | --- |
| GET /health | None | 200 provider/model/configured and call counters; no provider call | Database errors 503; configured does not prove a live call |
| POST /sessions | session_id, operation_id, fixed skill_key, started_at, optional owner_token | 201 saved in-progress record; replay 200 with replayed=true | Validation/conflict/database errors; no duplicate row |
| PUT /sessions/{id} | operation_id, owner_token, expected_revision, status, active_duration_ms 0–60000, nonnegative paused_duration_ms, ended_at | 200 committed checkpoint/final record and replay flag | Completed requires 60000 ms; terminal states require end time; stale revision/ownership/terminal conflicts rejected |
| GET /sessions/{id} | UUID | 200 saved record | 404 absent; no writes |
| GET /sessions | cursor ≥0, limit 1–100 (default 20) | 200 sessions/next_cursor | Read-only; invalid pagination 422 |
| POST /conversations | conversation_id, operation_id | 201 committed conversation; replay 200 | ID/input conflicts409 |
| GET /conversations | cursor ≥0, limit 1–100 (default 20) | 200 owned conversations/next_cursor | Read-only |
| GET /conversations/{id}/messages | UUID, cursor ≥0, limit 1–100 (default 100) | 200 sequence-ordered messages/request status/next_cursor/latest_request_id | 404 absent/out-of-scope; read-only |
| POST /conversations/{id}/messages | request_id, nonblank content ≤2000 characters, mock_mode success/failure/delayed (default success) | 202 request status after atomic user-message/pending-request save; background generation | Same input/request replay does not schedule again; pending conflict 409; crisis phrase 422 support_notice before writes/calls |
| GET /requests/{id} | UUID | 200 status, attempts/calls, IDs, actual reply, retrieval/citations/failure and persistence flags | Read-only; failures remain visible with no fabricated assistant |
| POST /requests/{id}/retry | operation_id, mock_mode | 202 original request with explicit retry operation | Invalid state/conflict 409; original user message retained; duplicate retry operation does not start another attempt |

There are no preference endpoints. The mock testing modes remain available to deterministic API tests, not as a user dropdown. `RequestStatus` distinguishes pending/succeeded/failed and user/assistant persistence. Connection loss is not proof of saving: the UI reconciles by stable ID or offers retry.

## Worked records and interruption contracts

Completed: session `60c50e57-77b8-4b6e-8666-6b22e43268f0` saved completed/60000 ms, retained after restart. Stopped: `8097f4b9-ff32-4d1e-bce5-b4317a0e0ba3` saved stopped/8580 ms active and11149ms paused after opening support and explicitly resuming. Practice cues and Stop never wait for a save.

Successful conversation: request `0480ce29-6b39-493e-8759-bad86d9c03d2` retrieves that stopped session. Two mock stages produce an actual scripted answer describing 8.58 seconds; the assistant message and success status commit together. Repeating the exact submission retains one user and one assistant message. [Curated records](evidence/part2-final-records.json) retain IDs for inspection.

Failed provider request: the submitted user message stays saved, request becomes failed with an error code/stage, and no assistant row is invented. Explicit retry reuses the user message. If assistant persistence fails, reply is not reported saved; if failure-status persistence also fails, the UI must treat state as uncertain and reconcile. Startup marks abandoned pending work interrupted without automatically spending another call.

Five-second and pause/resume checkpoints are serialized with final writes. A localStorage journal and Web Locks prevent recovery from interrupting a live owner tab. Returning after refresh/closure reconciles browser-owned unfinished sessions as interrupted at the last confirmed database checkpoint. Cleared storage, different origins/browsers and legacy ownerless records remain limitations. Hidden tabs pause and require explicit Resume; real Chrome backgrounding was historically verified. Device sleep remains untested. Opening support pauses and closing it does not resume.

## Two-call SQL RAG and model limits

1. The provider receives the question and reviewed schema to propose SQL plus bound parameters. Schema is not the data.
2. `rag/validator.py` tokenizes and parses a deliberately narrow complete grammar: one allowed table/projection, optional bounded comparisons/order, required limit, no trailing tokens. It rejects unsupported joins/subqueries/functions/writes/fields. `reader.py` reconstructs SQL rather than executing the original string, adds backend-owned user/conversation/prior-message scope and binds values. Read-only connection, SQLite authorizer and query-only mode provide additional boundaries; maximum 20 rows, 100 ms query time and 8000 characters context.
3. The answer call receives only permitted records with IDs/field meanings and reviewed `context/skill.md`. Stored instruction-like text is data. Grounding/citation membership is checked, but semantic correctness is not guaranteed by that check.
4. Normal application repository code saves the actual reply in a transaction. Retrieval cannot write. Empty retrieval, query rejection, database failure and provider failure have distinguishable outcomes.

Mock is deterministic and limited, not open-ended conversational intelligence. Historical live implementation uses OpenAI Responses with `gpt-5.4-mini-2026-03-17`, finite 15 s / 5 s connect timeouts, checked responses, bounded input/output and no automatic retries. `config.py` explicitly reads ignored `backend/.env` at startup. Both stages and failed attempts reserve durable budget before a live call; local ceiling 6 is exhausted. No further live call is part of final preparation.

## Display, personalization and safety boundaries

Newest request groups appear first with question before reply. Message timestamps/order and save/request status remain visible. Technical IDs are omitted from session rows and message metadata; conversation selector IDs remain. Only mock-assistant display text removes the `Record [UUID].` sentence. API/SQLite actual content and citation metadata remain intact, so evidence compares raw records separately from the approved display transformation.

Still cue is temporary. Proposed opt-in remembering at entry would save an explicit display choice; turning Remember off would delete the saved preference only after backend confirmation, retain this visit's choice, and honestly report deletion failures. System reduced motion should override a future saved animated preference. This proposal is not an implemented persistence feature.

Static support is independent of model, classifier, database and budget. Required helpline lookup rechecked the existing region-labeled content October 22; no service was contacted. A small shared phrase rule blocks matching fictional input before new save/call and offers support. It matches five phrases: kill myself, end my life, hurt myself, suicide, suicidal. Case/whitespace handling does not solve meaning: quotations/negations can trigger, indirect wording can be missed, and no match does not establish safety. It is not clinical assessment. Fullscreen keeps support in a sticky header; normal view can scroll it offscreen. Proposed bottom-bar work remains open.

## Figma and remaining scope

[Assignment-3 Activity frame](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=1-6) was inspected through MCP; existing Login/Dashboard/Activity frames returned no children and Activity screenshot was blank. Later read-only metadata/whoami confirmed access and Starter/View seat. Editable capture, baseline/alternative creation, frame selection and implementation were not completed. Current Vue is a README-based implementation, not a verified Figma match. No screenshot here is claimed to be editable capture. Access correction or a temporary exported-image/behavior-notes fallback requires a user decision before further work.

Remaining selected work: preference persistence, normal-view safety/navigation revisions, Figma round trip. Part 3 clean-checkout reproduction, broader fictional evaluation, varied live checks and recordings remain future work. No questionnaires, behavioral measurements, datasets or extra skills have been introduced.
