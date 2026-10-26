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

Static support is independent of model, classifier, database and budget. Required helpline lookup rechecked the existing region-labeled content October 22; no service was contacted. A small shared phrase rule blocks matching fictional input before new save/call and offers support. It matches five phrases: kill myself, end my life, hurt myself, suicide, suicidal. Case/whitespace handling does not solve meaning: quotations/negations can trigger, indirect wording can be missed, and no match does not establish safety. It is not clinical assessment. At the submitted Part 2 milestone, only fullscreen had sticky support. This later branch also implements a sticky normal-view support/active Stop header; full failure-state visual checks remain open.

## Figma and remaining scope

[Assignment-3 Activity frame](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=1-6) was inspected through MCP; existing Login/Dashboard/Activity frames returned no children and Activity screenshot was blank. Later read-only metadata/whoami confirmed access and Starter/View seat. Editable capture, baseline/alternative creation, frame selection and implementation were not completed. Current Vue is a README-based implementation, not a verified Figma match. No screenshot here is claimed to be editable capture. Access correction or a temporary exported-image/behavior-notes fallback requires a user decision before further work.

Remaining selected work: preference persistence, final navigation/visual verification, Figma round trip. Part 3 clean-checkout reproduction, broader fictional evaluation, varied live checks and recordings remain future work. No questionnaires, behavioral measurements, datasets or extra skills have been introduced.

## Approved post-submission extension — October 25, 2026

This section describes the later milestone on `codex/profiles-calendar`, after submitted Part 2 commit `f133bf99804246fe4fa34f090db37b196abf69c8`. It supersedes the single-demo-owner behavior only on this feature branch. The report/submitted commits are unchanged.

Local fictional profiles use a required trimmed display name (1–60 characters), optional integer age (0–120), and optional gender text (60 characters). No password or real authentication is implemented. Anyone with access to the local chooser can select a profile. The server issues an opaque browser token, stores only its hash, and resolves ownership from that token; the client cannot authorize a request with a profile ID alone. The token and current context version survive refresh in sessionStorage. Activity remains SQLite-backed. Closing a tab is not a reliable deletion mechanism and no automatic guest expiry is promised.

Migration 004 classifies existing owners as `legacy`; original records are not assigned to a new person. New `profile`/`guest` owners use stable UUIDs and existing foreign-key relationships. `browser_sessions` records the active owner/context version; `identity_operations` prevents duplicate identity writes; `deleted_identities` prevents reuse of deleted IDs. A backup precedes runtime migration. Model calls are forced to mock when the profile-enabled application starts, without rewriting backend/.env or resetting provider usage.

`identity.py` resolves the request context; session/conversation repositories enforce it on reads and writes, and the RAG controller supplies the same server-resolved owner to structural read-only retrieval. Request-scoped context rejects stale work after switching. Browser journals are namespaced by owner. Guest transfer updates ownership transactionally while retaining session, conversation, request, and message IDs. Explicit discard/delete removes related activity; historical provider evidence cannot be deleted through this flow. Profile switching is blocked while the owner has an active session or pending reply. Vue offers Continue practice or Stop and switch; failed session saves must be retried first.

### Identity contracts

All write bodies reject unknown fields. UUID operation IDs are required for mutation/retry. Success includes explicit persistence or identity state. Errors use the existing `{error:{code,message,retryable},persistence}` envelope: 401 missing/revoked identity, 404 unknown profile/record, 409 conflicting operation/stale context/revision/in-progress work, 422 invalid input, 503 database failure. Profile and activity reads never accept another owner's ID as authorization.

| Endpoint | Input and result | Persistence |
|---|---|---|
| POST /api/identity/bootstrap | bootstrap UUID → 201 token and chooser identity; duplicate bootstrap → 409 | Hashed token only; raw token returned once |
| GET /api/identity | Bearer token → active owner, mode, context version | None |
| GET /api/profiles | Bearer token → names/IDs/creation dates for shared local chooser | None; demographics/activity excluded |
| POST /api/profiles | Profile UUID, operation UUID, name, optional age/gender → 201 profile; replay 200 | One profile and operation receipt |
| POST /api/identity/guest | Operation UUID and expected context version → guest identity | New guest owner and context; replay safe |
| POST /api/identity/select | Profile UUID, operation UUID, expected version; guest disposition save/discard when needed → selected identity | Atomic transfer/discard and context change |
| POST /api/identity/leave | Operation UUID, expected version; confirm_discard for guest → chooser | Profile retained; guest activity removed only after confirmation |
| GET /api/profile | Token-selected profile → saved fields, creation/update timestamps, revision | None |
| PATCH /api/profile | Operation UUID, expected revision, approved fields → saved profile | Revision-checked update; replay safe |
| POST /api/profile/delete | Operation UUID, expected context/revision, confirm_delete=true → chooser | Delete selected profile/activity, invalidate other active sessions |

### Calendar contract and view

`GET /api/calendar?month=YYYY-MM&timezone=IANA_ZONE&cursor=0&limit=100` requires Bearer token and matching `X-Context-Version`. Years 1900–2100, months 1–12, valid IANA zone, nonnegative cursor, limit 1–100. The backend computes local-month boundaries in UTC and reads only that owner's completed `paced_breathing_4_6` sessions. Stopped/interrupted/in-progress rows are excluded but retained in session history. There is no event table and no calendar write operation.

200 returns `month`, `timezone`, `placement: completion`, `events`, `next_cursor`. Each event contains the saved `session_id`, exercise name `Paced breathing (4–6)`, UTC `completed_at`, timezone-derived local date/time with offset, active duration, and fixture flag. Stable ordering is completion instant then ID. SQLite queries bind all user values. Invalid ranges/zones return 422; database failures return 503; empty history returns an empty list rather than a failure.

`CalendarView.vue` displays date headings and a semantic event list with `<time>` elements, month navigation, explicit timezone, loading/empty/failure states, and refresh. Device timezone is read on mount/refresh and rechecked on window focus. Completion time determines placement even if a practice starts the previous day. Repeated DST hours include timezone abbreviations. There are no wellbeing scores or inferred benefits. Lists and wrapping controls support the approved 390px reference without requiring a dense calendar grid.

`ProfileGate.vue` provides guest/chooser access; `ProfileView.vue` reads approved profile fields from FastAPI and links conceptually to history/calendar/chat. `SupportContent.vue` reuses the existing independent support content in the chooser and practice app. At the profile/calendar increment no library was present; the following increment adds names-only placeholders. Figma extension frames remain a draft reference: final screenshots/editability comparison and pixel-level fidelity are not claimed by this increment.

## Exercise library and responsive web increment — October 26, 2026

Approved library is implemented in `components/ExerciseLibrary.vue` and reached by Exercises in App.vue. Its only action opens the existing practice view; it does not automatically start or save a session. Paced breathing remains six4/6 cycles. Sensory grounding (5-4-3-2-1), STOP and One-minute cognitive reframe are static names marked Coming later / Unavailable, with no actions, instructions or completion state. No new skills or backend contracts were implemented.

Shared responsive styles cover the chooser, practice, profile, calendar, library, chat and support. Navigation remains in normal document flow and wraps; it is not a fixed overlay. The support header is sticky, including an additional Stop action during active practice, and the chooser support header stays reachable. Identity notices now occupy document flow instead of covering controls. Mobile forms use bounded widths and readable input sizes; long text wraps; short landscape uses a two-column practice layout. Visible focus includes textarea/summary, navigation targets the destination heading, and primary controls have a minimum44px height. Still-cue and system reduced-motion rules are retained. This is a responsive website, not a PWA or native app. These layout changes require visual verification; browser access was policy-blocked during this increment, as recorded in verification.md.

## Later milestone review — October 26, 2026

The approved chooser label is now “Create a profile”; the nearby fictional-data and local-authentication explanation remains. This is a copy-only change in ProfileGate.vue. No fields, ownership rules, persistence or API contracts changed.

The submitted Part 2 report is historical; this branch's optional expansion is summarized separately in [later milestone report](later-milestone-report.md). Current navigation wraps in normal flow rather than implementing the selected draft's mobile bottom bar. This difference and visual fidelity require review; do not claim a completed Figma-to-Vue comparison. The latest metadata request for calendar node22:249 returned the Figma Starter-plan tool limit, so its current contents and editability were not verified. Earlier frame references are historical, not newly verified links.
