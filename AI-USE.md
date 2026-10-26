# AI-use disclosure — Assignment 3 Part 2

Updated October 26, 2026. Earlier sections describe the submitted Part 2 work; the later-milestone section below supersedes current-state statements for the feature branch. This is an AI-assisted coursework prototype. The student selected the skill, flow, scope and interface revisions, approved implementation increments, and reviewed reported results. This disclosure does not claim the student personally ran the agent's tests or authored every generated line. Final submission review remains necessary.

## Tools, models and roles

| Tool/model | Known identifier | Role |
| --- | --- | --- |
| Codex desktop coding agent | GPT-6-based agent; exact serving snapshot not exposed in this task | Proposed architecture, generated/refined Vue/Python/tests/docs, inspected files and ran authorized checks |
| OpenAI application provider | `gpt-5.4-mini-2026-03-17`, Responses API | Historical live retrieval planning and grounded reply generation; bounded six-attempt ledger |
| Mock provider | Repository `backend/app/providers/mock.py` | Deterministic SQL proposals/replies/failures; current application mode; not live AI |
| Browser/computer tools | Codex in-app browser and native Chrome UI; tool build identifiers unavailable | Operated fictional scenarios, inspected rendered state and captured evidence; Chrome used for real hidden-tab event |
| Terminal/Python/Node | Python 3.12.5, SQLite 3.45.3, Node 24.20.0/npm 11.19.0 | Tests, API/SQLite inspection, build and document preparation |
| Figma MCP | Tool/plugin version not captured for historical calls | Read-only metadata/design screenshot/account access inspection; no completed editable capture or round trip |
| Required helpline lookup | Version not exposed | Checked existing resource content October 15 andOctober 22; no service contacted |

Dependencies include Vue 3.5.44, Vite 7.3.7, FastAPI 0.158.1, Uvicorn 0.54.0 and HTTPX 0.28.1; manifests/lockfiles declare the environment. No external therapy dataset or research-participant data was used. Research rationale came from the user-supplied assignment study table, not an invented clinical study. Existing Part 1 application code and course Vue/FastAPI/SQLite/RAG patterns were extended; no specific travel-app source was copied in this work.

## Human choices and generated work

The student chose one six-cycle 4/6breathing skill, direct Start, optional chat, still cue, one fictional demo profile, interruption/pause rules, mock-first testing and a finite live budget. They approved crisis wording and later requested simpler UI, fullscreen arrows, unchanged timing with smoother visuals, and hidden technical metadata. They explicitly returned chat to mock mode. Preference remembering/forgetting and Figma work were planned but not completed.

The agent generated and revised backend schemas/routes/repositories, restricted SQL retrieval, provider code, persistence coordination, frontend components and tests, plus report/document drafts. Application code—not a model response—owns timers, exits, support and writes. The student explicitly verified the earlier SmokeTest report and latest UI cleanup. Final documentation and fresh verification are offered for review; no personal student test execution is inferred.

## Selected prompt → change → evidence → decision trail

| Selected instruction (paraphrased) | Work/evidence | Decision or limit |
| --- | --- | --- |
| Preserve Part 1 and inspect environment before installation | Local environment/declarations inspected; minimal FastAPI save/read and duplicate replay checked before expansion | Project-local dependencies; existing data/config preserved |
| Save completed/stopped practice and show honest failures | Session journal, revision/operation IDs, asynchronous saves; browser outage/retry and SQLite comparison | Cues never await network; recovery uses last confirmed checkpoint |
| Mock chat first; no fabricated replies | User/pending transaction then actual reply/success transaction; failure/retry tests and saved history screenshots | Failed generation retains user input, no assistant fabrication |
| Structurally validate two-call SQL RAG | Restricted parser/reconstructed SQL/read-only scoped reader; write/scope/empty/instruction-like tests | Raw model SQL never executed; citation membership is not semantic truth verification |
| Approve bounded live example | Initial call failed; diagnostic retry returned 401; student corrected key locally; later actual live answer saved | Generic errors revised into safe diagnostic codes; failed attempts still counted; credentials never pasted |
| Check real hidden-tab behavior | IAB did not yield the necessary event; separately approved native Chrome did | Report genuine Chrome observation separately from IAB limitations |
| Use existing Assignment-3 Figma design | Activity frame was blank; later read-only access inspection | README-based implementation, no invented Figma match or editable capture |
| Smoother visuals, same timing | Clock-derived cue smoothing instead of adding a breath hold | Six4/6cycles unchanged; final measured run below 90 seconds |
| Remove technical IDs/citations from UI | Display-only metadata removals and mock-assistant citation filter | Stored/API reply and traceable IDs preserved for evidence |
| Prepare Part 2 submission | Fresh35/10 tests/build; browser/API/SQLite/replay/restart checks and curated evidence | No paid calls/source edits; final commit/push needs separate approval |

Another revised approach: independent CSS pacing could drift when motion was re-enabled mid-cycle; clock-derived cue scaling replaced it. Final API/SQLite timestamp comparison initially compared strings, then correctly normalized equivalent UTC instants (`Z`/`+00:00`). This was a verification correction, not an app failure.

## Disclosure and limits

[Verification](docs/verification.md) separates newly observed, historical, mock and live evidence. [Evidence index](docs/evidence/README.md) contains selected prompts/decisions and screenshots rather than a full private chat export. Fictional record IDs are deliberate traceability data; keys, runtime database and environment are excluded from submission. No recordings, clinical evaluation, full accessibility assurance, completed personalization, Figma round trip or deployment is claimed. Preserve this disclosure with the submitted source; review the generated code explanation in [report](report.md).

## Later milestone — profiles/calendar/library

User approved the local chooser model, required display name with optional age/gender, guest refresh retention, explicit transfer/discard, pause-before-switch rules, completed-only calendar using device timezone and completion time, library placeholders and responsive web changes. The agent generated the migration, identity/API/repository code, Vue views and automated tests, then documented actual evidence and gaps. No real authentication, new therapeutic instructions, paid calls or physical-device verification were added. The user approved commit and push of this later milestone; this is not evidence that they personally executed every check.

49 backend and 10 frontend tests passed. Browser observations include guest entry, completion/saved state within a conservative 72.082-second bound, and library navigation without auto-start. Remaining visual/failure coverage and Figma comparison are disclosed in the [later milestone report](docs/later-milestone-report.md). Existing Figma draft references could not be freshly checked because MCP returned its Starter-plan limit. The submitted report.md remains unchanged.
