## Selected Figma design and browser comparison — October 27, 2026

The student selected **Option A: top navigation** and approved a comparison/documentation-only increment. This supersedes earlier bottom-bar selection and static-only Figma status. No application implementation was requested or performed in this increment.

The MCP allowance remained unavailable during creation. With explicit approval, the agent used the signed-in Figma browser editor to create **17 frames** on [Part 2 — Updated app](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-110): seven desktop/phone pairs, flow notes, state/tradeoff notes and Option B. Existing Page 1 baseline frames were preserved. SVG descriptions pasted through the editor produced native Figma text and vector layers; a final library text layer exposed editable Text/Typography/Inter controls. This is browser-created, source-informed design work, not an MCP capture, reusable component library, wired prototype or exact rendering of Vue. Inter differs from the app's Arial/Georgia. The desktop voice frame was replaced after clipping was found; use node37:2 below, not removed node31:558.

| View | Desktop | Phone |
| --- | --- | --- |
| Entry | [1440px](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-148) | [390px](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-115) |
| Practice | [1440px](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-174) | [390px](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-213) |
| Profile | [1440px](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-256) | [390px](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-290) |
| Calendar | [1440px](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-335) | [390px](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-405) |
| Exercise library | [1440px](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-481) | [390px](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-518) |
| Voice chat | [1440px](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=37-2) | [390px](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-600) |
| Crisis support | [1440px](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-649) | [390px](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-679) |

Additional links: [Flow](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-721), [States and tradeoffs](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-773), [Option B — unselected bottom navigation](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3?node-id=31-828). Frame IDs came from the editor after creation; the saved 17-frame inventory was re-read after navigation. Access is verified in the student's signed-in browser, not from an instructor/anonymous account.

Option A exposes destinations without a fixed bar covering controls, at the cost of vertical space (R3/R4 choice; D1/D2 effort). Option B reduces primary choices to Practice/Voice/More but adds an extra step for other destinations and requires keyboard-overlap testing. Selecting A does not authorize changes to timing, ownership, saving, voice or support.

### Comparison with the running app

The agent inspected the existing app in the in-app browser at the available **551 × 688** viewport. Figma references are 390px and 1440px wide, viewed scaled in the editor. This is a qualitative structure/content comparison, **not a matched-viewport or pixel-fidelity pass**. Exact 390px/1440px app comparisons and physical-device checks remain unfinished.

| Area | Observed agreement and remaining difference |
| --- | --- |
| Navigation | App has top, wrapping navigation and the same destinations, plus the active identity switch. Figma uses uniform pills, shortens Session history to History and omits the identity switch from the repeated header. |
| Practice | App idle view shows six cycles, 4/6 instruction, Start, fullscreen and still cue. Figma shows an in-progress reference. No new exercise was started; pacing, completion, Stop and interruption behavior were not retested here. |
| Entry | ProfileGate.vue confirms guest access, optional fields and independent support. The entry chooser was source-inspected only; existing identities were not exited or switched to expose it. Figma shows the create form expanded and simplified empty state. |
| Profile | Browser inspected both guest and an already selected profile. Vue has actual editable fields, Save, Switch, Leave and Delete; Figma combines guest controls with a descriptive profile-selected note. Vue still says Optional chat in one saved-information sentence; copy correction requires separate approval. No profile values were edited. |
| Calendar | Observed loading followed by an empty October calendar, explicit America/New_York timezone, previous/next/month picker/refresh and stopped/interrupted exclusion wording. Vue uses a day/event list; Figma illustrates a month grid. The grid is not implemented or approved for implementation. |
| Library | Available breathing action and all three unavailable Coming later names agree. Figma adds explanatory copy. No unfinished entry has a Start action in the observed app. |
| Voice | Browser currently displays labeled mock preview, microphone off, typed input, playback controls and saved history. Figma shows a simplified ready-state/live-capable reference with shorter notices. Existing saved replies are historical; no new message, audio, microphone permission or model call was submitted. Current UI mode was observed, not reconfigured or diagnosed. |
| Support | Opened/closed the app's independent support panel from Profile without voice or exercise. Vue contains actual resource links and a dated lookup notice; Figma intentionally contains resource-placement notes only. No link was activated and no fresh helpline-content verification is claimed. |

**Boundary:** editable browser-created references, explicit A selection and this limited comparison are complete. A new Figma-to-Vue implementation, exact viewport match, full state coverage and instructor link access are not established. The student reviewed this increment and explicitly approved committing and pushing these four documents. Publication is a documentation follow-up; application source remains unchanged. Historical sections below retain their original dates and should not be read as the latest Figma status.

---

# Current contract summary — October27,2026

The student approved inclusion of the complete profile/calendar/library/voice expansion in updated Part2 and explicitly verified the chatbot. The dated sections below retain the decision history; later entries supersede earlier mock-only, disabled-voice and automatic barge-in descriptions.

Current behavior: one Voice chat tab with typed alternative; explicit microphone Start; automatic silence-based submission; actual saved transcript/reply; playback with frames ignored during speaking and explicit Stop speaking; no silent capture restart. General educational wellbeing answers are permitted while personal-history claims require scoped records. Retrieval rejection/database error/timeout can yield general answers with unavailable context disclosed; invalid SQL never executes and outcomes remain distinguishable. Provider/budget failures still fail. Identity controls, calendar, library placeholders and six-cycle practice remain as documented.

Current source has no completed verified Figma round trip. Normal-view support/Stop now use a sticky header, superseding older statements that no sticky normal-view control exists; comprehensive viewport/failure testing remains incomplete. Navigation still wraps instead of the drafted bottom bar. The65-call cumulative live allowance is for the separately approved local demo, not compliant per-session peer-test enforcement. Peer tests should remain mocked. See [updated report](../report.md) and [current verification](verification.md).

---

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


## Voice preview — first mock increment, October 26, 2026

The existing ChatView.vue now owns a single Voice chat page, typed input, transcript preview, test-tone controls and history. voiceSession.js owns epoch-guarded WebSocket events and explicit stop; support opening, visibility loss, unmount and profile switching stop the session. This first increment deliberately does not call getUserMedia: a fixed fictional transcript and a 300ms generated WAV tone exercise the pipeline without personal recording. The tone is visibly labeled non-speech. Automatic submission is implemented for the mock finalized transcript, not verified real speech.

New API/controller/repository/provider voice.py modules separate transport, coordination, application writes and offline fixtures. HTTP uses existing token/context-version middleware. WebSocket /api/voice/stream authenticates in its first message (never in URL), checks Origin, binds the browser context and validates ownership again through repository operations. A 5-second authentication timeout and 30-second event inactivity timeout end the socket. There is no live-provider selection in the voice adapter; profile runtime still forces mock. Approved $1/20-attempt future live voice allowance is NOT implemented or activated by this preview; live voice budget tables/adapters are deferred, and no live voice call is possible through these routes.

Migration005 adds voice_sessions, voice_turns and voice_operations transactionally; existing requests/messages remain the canonical ordered transcript/reply store. Session->conversation->owner relationships preserve guest transfer. Deleting owned activity cascades voice metadata before ordinary request deletion. Active voice sessions block identity switching until stopped. Startup marks unfinished sessions/turns interrupted; it never resumes audio or spends a call. Runtime migration was preceded by an ignored SQLite backup; existing table snapshots matched afterward.

Contracts implemented: POST /api/voice/sessions (session_id, conversation_id, operation_id; 201 or replay200), GET /api/voice/sessions/{id} (ordered turn status), POST /api/voice/sessions/{id}/stop (operation_id, expected_revision), POST /api/voice/turns/{id}/actions (operation_id, expected_revision, cancel/retry_speech/retry_reply_save), GET /api/voice/turns/{id}/audio (WAV or410 expired). HTTP errors use existing identity/not-found/conflict/validation/database handling. WebSocket accepts strict MockTurn JSON with stable turn/request/operation UUIDs; success/failure fixtures are API test inputs, not a UI dropdown. It emits ready/accepted/transcript/submitted/status/error/stopped events. Raw audio input is not supported yet.

Transcription success precedes ordinary atomic user-message/request insertion. Generation uses the existing structural validator and read-only owner-scoped SQL RAG without modifications. Only a saved actual mock reply can produce audio. Speech failure leaves the successful text request intact. Duplicate operation bodies replay; conflicting bodies reject. Cancellation prevents later assistant insertion. An unsaved generated reply can be held in bounded process memory for up to five minutes (or session stop/restart) and explicitly retried as a save-only transaction without additional model calls. Audio and retained replies are not written to temporary files or SQLite; in-memory audio expires and is cleared when the session ends. Browser playback status is local, not a claim the user heard the reply.

Remaining approved architecture: real microphone capture/PCM validation and limits, continuous silence-based turn segmentation and barge-in, live transcription/speech adapters, durable cost ledger/reservations, live output/transcript fidelity checks, complete response schemas and production-level stream bounds. Historical conversation text persists on refresh/restart, but voice playback controls are presently associated only with the current mock turn; restoring these controls for historical turns is unfinished. No Figma changes or baseline replacements occurred.


## Approved voice/chat wording increment — October 26, 2026

The user approved the proposed concern notice, explicit limitations and educational boundaries. Frontend and backend normalize a small phrase list, including three indirect forms; matching draft/recognized words hold automatic submission and stop the mock voice session/playback. Users can open independent support, review/edit recognized words, discard the draft or end the conversation. Restart is explicit. Partial recognition has uncertain submission status unless the backend confirms a hold; the UI must not promise unsaved content when evidence is missing. Mock holds explicitly say no audio was recorded or sent.

The backend checks recognized input before conversation writes/RAG. Held voice metadata is retained but recognized words are not persisted. Application input checks remain separate from generated-output checks. The latter run after RAG answer validation and before assistant persistence, and before cached audio/retry delivery. A withheld generated answer is a failed request, not a fabricated assistant message; an already saved user message remains saved. Selected lexical patterns cover diagnosis, treatment, medication instructions, unsupported reassurance and monitoring claims. Reviewed refusal wording lives in backend/app/context/skill.md. These are limited checks, not reliable distress detection or clinical assessment; quotes/negations can trigger false positives, misrecognition and indirect language can be missed.

Support is static and available without backend, microphone, classifier or provider budget. Required helpline lookup was repeated October 26, 2026; US/territories resource links retained exactly. No service was contacted. Current voice is still a fixed mock transcript/test tone; this increment does not enable live transcription, AI speech or continuous capture.


## Real-voice capability, disabled pending activation — October 26

Approved implementation extends the existing tab. `frontend/src/microphone.js` and `frontend/public/pcm-worklet.js` request microphone permission only after Start, keep audio in memory, resample to mono16kHz PCM WAV, segment after900ms silence and cap each utterance at30s. Silence alone is not sent. This is continuous hands-free turn-taking with processing gaps, not a direct duplex realtime model session. While processing, microphone frames are discarded; while a reply plays, detected speech stops playback and starts another utterance. Echo cancellation is requested, not guaranteed. Opening support, hiding/unmounting the page, switching identity or End conversation stops tracks. Late permission grants are immediately closed after cancellation. This still needs actual-device verification.

`voiceSession.js` sends strict `audio_turn` messages over the existing authenticated WebSocket: stable turn/request/operation UUIDs plus base64 WAV. Backend limits JSON length and validates mono16kHz16-bit PCM, actual frame count and0.2–30s duration before provider processing. Provider calls use `gpt-4o-mini-transcribe`, existing `gpt-5.4-mini-2026-03-17` SQL planning/answer, and `gpt-4o-mini-tts`/marin speech. WAV only; no new packages or temporary audio files. Audio HTTP responses are bounded; connect timeout5s, audio total30s, RAG15s, no automatic provider retries. Saved replies longer than600 characters remain readable but speech fails honestly; the prompt requests concise replies.

Migration006 adds independent `voice_provider_attempts` with unique operation_key, stage, reservation, outcome and timestamp. Atomic reservations count failed/cancelled calls, both RAG stages, transcription, speech and speech retries. Each attempt reserves50000 microdollars ($0.05);20 attempts reserve$1. Reservations are never refunded after uncertain failure. This is a conservative local allowance, not a provider invoice guarantee: speech billing depends on generated audio tokens and there is no provider-side dollar cap here. Existing six-attempt ledger is unchanged. Budget entries intentionally survive deletion of activity, preventing budget reset via profile deletion. No content or credentials are stored in this ledger.

`VOICE_ENABLED=false` and `VOICE_PRICES_VERIFIED=false` are documented in .env.example; the existing ignored .env was not modified. Both flags plus valid key/config are required. Health exposes only voice_enabled, never secrets. Current runtime remains mock. Typed chat switches to the same live RAG/ledger only after activation. Retries preserve stable operation IDs; speech failure leaves the saved text reply intact. Exact retry replays cannot purchase the same speech operation twice. Audio expires after5minutes/end/restart; stored text remains.

Official documentation inspected October26 marks gpt-4o-mini-tts deprecated with January6,2027 shutdown: https://developers.openai.com/api/docs/deprecations . No replacement was silently chosen. Resolve model lifecycle and billing/pricing bounds with the user before setting live flags or making paid calls. Provider retention is outside this app's local audio-discard guarantee. Baseline Figma and submitted report.md remain unchanged.


October27 activation update: user retained the speech model for the short demo and approved four live calls. The running backend has a temporary4-attempt ceiling (generic startup still20). Transcription/RAG/saving succeeded with empty history; speech returned HTTPsuccess but failed local validation. This is partial live evidence, not working spoken playback. See verification; audio correction/retry and restored historical voice controls require approval.


October 27 approved correction supersedes the partial activation note: speech now requests provider PCM and wraps mono 24kHz, 16-bit little-endian samples into an exact-length WAV in memory. Empty, odd-length and oversized output is rejected. No dependency or schema change. GET /api/voice/conversations/{conversation_id}/latest-turn restores an ownership-scoped latest turn (or null), returning 404 for inaccessible conversations. Restoring history opens neither microphone nor WebSocket and never autoplays. Explicit Retry reply audio reuses the saved answer with an idempotent operation ID; it does not repeat transcription or RAG. One approved live speech retry succeeded.


### Approved additional voice allowance — October 27

User approved20 additional paid attempts and corrected unsaved-message wording. Running backend uses absolute voice_call_limit=25 and voice_budget_microdollars=1250000, preserving5 previous attempts/$0.25 reservations and leaving20/$1 additional reservations. This is not an invoice guarantee. No paid verification call was made. Settings validation permits this explicit ceiling; defaults remain20/$1. Restart must use the approved25/1250000 overrides to retain this allowance (not add another20). Budget ledger is never reset. Current backend session13139.

Voice errors now distinguish “Your message was not saved,” saved messages, and unknown save status. Checked8 backend live-adapter/budget tests,25 frontend tests and build: passed. Read-only runtime ledger remains5 attempts. No profile deletion or recreation performed; user deleted the demo profile. Submitted milestones unchanged; no commit/push. User microphone verification pending.


Approved broader chat behavior, October27: reviewed context permits general education about stress, emotions, coping, relationships and seeking professional help; diagnosis, individualized treatment/medication instructions and monitoring claims remain excluded. Planning instructions include strict SQL examples and recent-message context for general questions. Parser/reader and ownership enforcement are unchanged. Rejected queries are never executed. Rejection/database_error/query_timeout now reach answer generation with no records, explicit retrieval_status and history_available=false. Answer instructions require disclosure of unavailable history and prohibit invented personal history; citations remain restricted to retrieved IDs. Actual replies use normal persistence, while retrieval_outcome retains the failure code. Provider/configuration/budget failures still fail; no automatic retry or extra unbudgeted call. Fixed parser rejection categories go to backend logs, never raw SQL, bound values or transcript. No schema/API shape/dependency change. Prompt rationale: https://developers.openai.com/api/docs/guides/prompting .


October27 approved playback fix: microphone frames are discarded/reset while reply audio is loading or playing. Removed automatic sound-onset interruption, which could mistake speaker echo for user speech. Stop speaking remains explicit; once playback finishes or is manually stopped, frames are accepted only within the still-active visible conversation. Hidden/support/stopped states remain blocked. This supersedes the earlier barge-in behavior; microphone permission/tracks are not silently restarted.


October27 budget extension: user explicitly approved40 further attempts. Absolute running ceilings increased25→65 and1250000→3250000 microdollars. Settings validation allows these ceilings, but defaults remain unchanged. Ledger is preserved; no reset/refund or per-conversation replenishment. No provider/model/schema change.


October27 publication follow-up: user explicitly approved committing/pushing all completed changes and updating the existing Assignment-3 Figma file. Figma create_session succeeded, but get_metadata returned the Starter-plan MCP tool-call limit. No design read/edit or frame verification succeeded; no Figma changes were made. This remains an external-access blocker, not completed design work.


Approved October27 follow-up: Figma fallback is docs/figma-fallback/README.md with14 static PNG/SVG reference boards and flow notes; no editable Figma verification. Live hard ceiling is now50 attempts/$2.50 cumulative reservations, stricter than a session cap with no automatic resets. Existing49 voice attempts preserved; ignored .env VOICE_ENABLED=false, other settings/key preserved. Peer demo now mock. No live reactivation authorized.


Approved testing-session increment: migration007 creates live_test_sessions (UUID,label,call limit1–50,reservation cap,state,created time) and nullable voice_provider_attempts.test_session_id. Old rows remain NULL; no guess of who initiated them. Host-only CLI creates/closes sessions; no web budget-creation endpoint. Settings selects an explicit VOICE_TEST_SESSION_ID; flags/key alone no longer enable live. Atomic reservations count only selected-session rows, checking both settings and immutable recorded caps. One active session, idempotent same-ID create, explicit close before next. Health/new requests choose mock if unavailable/exhausted; new voice handshake is labeled accordingly. Mid-turn budget failure stays honest, with no automatic retry or fabricated reply. Transient audio remains cached by controller; stopped/old replies are not repurchased automatically.
