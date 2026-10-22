# Assignment 3.2 — Part 2: Working prototype

**Project:** A little space · **Prepared:** October 22,2026 · **Status:** ready for student review, not yet committed/submitted.

| Submission field | Value |
| --- | --- |
| Repository | [mallorypierz/mentalhealth_app](https://github.com/mallorypierz/mentalhealth_app) |
| Working branch | `codex/part2` |
| Submitted Part 2 commit | **PENDING separate commit approval.** Current HEAD e958bdcf11e69b5c4451f986742989acd01b497e is Part 1 and must not be used as the Part 2 version. |
| Evidence access | Local relative links below work within this repository. Before uploading this report alone, replace them with verified commit-specific hosted links after approved push. Instructor access is not yet verified for Part 2. |
| Preserved Part 1 | [Part 1 report](https://github.com/mallorypierz/mentalhealth_app/blob/e958bdcf11e69b5c4451f986742989acd01b497e/report.md) and [submission branch](https://github.com/mallorypierz/mentalhealth_app/tree/part1-submission) remain intact. |

## Purpose and scope

A fictional college student can practice one short skill before an assignment without explaining how they feel. Six cycles preserve the supplied paced-breathing sequence: four seconds in, six seconds out. The interface offers direct Start, Pause, explicit Resume, Stop, still cue, fullscreen/minimize and neutral results. Optional chat and saved history are outside timed practice.

This is a localhost coursework prototype, not therapy, diagnosis, monitoring or a service to rely on during distress. All tests use fictional scenarios. No clinical outcomes are inferred from duration, stopping or clicks. No questionnaires, emotional-state measurements, extra skills or conversational datasets were added.

## Requirement audit

| Part 2 requirement from supplied assignment | Evidence and completion status |
| --- | --- |
| Complete at least one chosen skill in running interface | Implemented: six 4/6cycles; [current completion](docs/evidence/part2-final-completed.png) and fresh measured run |
| Demonstrate model contribution with relevant context | Implemented two-call SQL RAG; [historical live answer](docs/evidence/part2-live-saved.jpg) plus [current mock answer](docs/evidence/part2-final-chat.png), clearly distinguished |
| Conversation/session persistence in SQLite | Browser/API/read-onlySQLite comparison, exact replay, refresh/restart; [record extract](docs/evidence/part2-final-records.json) |
| Measure intended exercise ≤90 seconds including delays | Fresh conservative observed bound 72.336 seconds; setup 5.036 seconds separate; no pauses excluded |
| Independent crisis-support route | Static route works without model/classifier/budget; [fullscreen support](docs/evidence/part2-final-support.png), historical outage checks; normal-view viewport visibility limitation disclosed |
| Show request failure and leaving practice | [Provider failure](docs/evidence/part2-live-auth-failure.jpg), [save failure](docs/evidence/part2-smoketest-save-failure.jpg), stopped/interrupted records and explicit recovery |
| Coherent scope and honest unfinished work | Core skill/persistence/RAG implemented; preferences/Figma/normal-view safety refinements remain unfinished |
| Research-grounded decisions and AI-use/evidence trail | [Design notes](docs/design-pipeline.md), [AI-USE](AI-USE.md), [curated evidence](docs/evidence/README.md) |
| Report with submitted commit and accessible links | **Pending** commit/push approval and final hosted-link update/check before upload |

The working evidence supports the core Part 2 milestone, not completion of every originally proposed feature. Part 3's broader 15 fictional scenarios, 3 behavior checks, varied live evaluation, clean-checkout reproduction and finished-app process recordings are not claimed completed here. No recording is provided for this milestone.

## Research rationale and tradeoffs

The supplied R1–R4/D1–D6 findings describe 15 patients, 13 clinicians and 15 prototype evaluations. Mention counts identify study concerns, not clinical effect sizes. The fictional student scenario is a design application of those findings, not a validated clinical population.

R1 supports the fixed short sequence; a duration picker was deferred to reduce setup. R3/R4 support explicit control and stopping without penalties. D1/D2 support a single cue and atomic skill, while optional chat avoids disrupting pacing. D3 motivates no mandatory questionnaire or disclosure. D6 motivates restrained motion, a still alternative and neutral language. R2/D4 motivate support independent of model success; normal-view scrolling remains a gap against persistent visibility. D5 motivates explicit optional preference remembering, but current display choice remains temporary. The gain is low setup effort; the loss is repeated choice after refresh. Full alternatives and limits appear in the design notes.

## Model contribution and architecture

Vue sends HTTP/JSON to FastAPI; only the backend opens project-relative SQLite or contacts OpenAI. Application code owns timing, exits, support, validation and saving. The model's bounded job is to explain reviewed app/skill context and describe permitted saved history without claiming improvement.

The first RAG call proposes retrieval from the question and reviewed schema. Backend code structurally parses a narrow SQL grammar, restricts tables/columns, reconstructs SQL with bound values and backend-owned scope, and uses a read-only connection with row/time/context limits. It does not execute raw model SQL or trust a SELECT-prefix check. The second call receives permitted records and reviewed skill context; stored text is data, not instructions. The actual reply is saved through ordinary application transactions. Empty results, rejected queries, database failures and provider failures stay distinct.

Current runtime uses a labeled deterministic mock provider. Historical live evidence used OpenAI `gpt-5.4-mini-2026-03-17`: request 8cfe378a-6795-4a94-ab2c-016a33aeafe7 returned a saved answer citing an interrupted20430ms session. Configuration/key presence alone was never counted as success. Both stages and failed attempts consume a durable six-attempt budget; all six are used. Final checks made no paid calls. Mock tests establish repeatable software behavior, not live-model quality or robustness.

## Saved data and inspection

One fictional demo profile owns sessions and conversations. Messages retain stable IDs, roles, actual content, sequence, timestamps and linked request status. Sessions retain active/paused durations, stopped/completed/interrupted status, checkpoints and revisions. Operation IDs/input hashes and uniqueness constraints prevent duplicate writes. No preference records currently exist.

The final completed session 60c50e57-77b8-4b6e-8666-6b22e43268f0 contains 60000ms active/0paused. The stopped session 8097f4b9-ff32-4d1e-bce5-b4317a0e0ba3 contains 8580ms active/11149 ms paused. Conversationb95bcf01-ca77-4e3d-9233-e3617f8e5a3c contains one question and one actual mock reply describing stopped 8.58 seconds. The same IDs/content/status were compared in SQLite/API and the rendered Vue record. Exact replay left two messages, and backend restart plus browser refresh preserved them.

The table displays floored whole seconds; raw/API values retain milliseconds. Approved UI formatting hides technical message/session IDs and the mock `Record [UUID].` sentence. The [curated extract](docs/evidence/part2-final-records.json) retains actual raw reply/citations for inspection. This is a display transformation, not a change to stored model output. No generated answer becomes a clinical interpretation.

## Timing, failure and interruptions

Fresh final run: setup 5.036 seconds measured separately. Pre-Start-click to observed completed UI was 72.336 seconds, a conservative bound including click/observation overhead and application delays. First instruction was observed 1.091 seconds after the click, so the bound covers the entire instructed sequence. No voluntary pause, support or hidden interval was excluded. Stored start/end span was 60.001 seconds with 60000ms active; the capped counter alone is not the timing proof. No typing or breathing confirmations are required; actual breathing adherence is not measured. Results do not force an exit.

The second run verified fullscreen, still cue, opening support pauses practice, Resume is disabled while support is open, and closing requires explicit Resume. Stop then produced a distinct saved stopped record. Historical Chrome background-tab testing verified automatic pause and explicit Resume; refresh recovery uses only the last confirmed checkpoint and labels interrupted. Cleared storage/different browsers and device sleep are limitations.

Failed model requests retain the user message without fabricating an assistant reply. Failed saves display uncertainty/failure with retry, while practice/Stop/support continue. Historical outage/retry evidence and automated temporary-database failures establish these cases. New final verification passed 35 backend tests, 10 frontend tests and production build; [verification](docs/verification.md) separates fresh, historical, mocked, live and untested claims.

## Independent support and crisis-related text

Support information is static and independent of model, phrase rule, database and call budget. Resource content was rechecked through the required helpline lookup October 22; no service was contacted during tests. A limited application-owned phrase rule offers the approved notice and prevents matching new input from being saved/sent. It can flag quotations/negations and miss indirect wording; no-match is not evidence of safety. The app does not assess safety or imply monitoring. Fullscreen provides a sticky support header; normal-view support can scroll away, and the selected persistent bottom-bar refinement remains unfinished.

## A revised approach and generated-code explanation

An early live planning request failed; a scoped diagnostic change distinguished connection errors from HTTP status failures without exposing bodies or secrets. The retry returned 401. The student corrected the key locally, after which an actual two-call answer was saved. Failed attempts remained in the budget. This illustrates why configured status is distinct from working provider evidence and why failure must not fabricate success.

Relevant generated code: [rag/validator.py](backend/app/rag/validator.py) converts a proposed SQL string into a small `Query` structure. Its tokenizer rejects unsupported tokens; parsing requires allowed columns (including ID), one allowlisted table, bound comparisons, permitted ordering and a final limit with no trailing SQL. The [reader](backend/app/rag/reader.py) reconstructs SQL from that structure and adds ownership itself. Values are bound rather than interpolated. A separate read-only connection/authorizer prevents retrieval writes. This deliberately limited parser rejects many legitimate SQL forms in exchange for a smaller reviewable surface. It is not a general SQL sanitizer, and valid citations do not guarantee the model's claims are semantically correct. Parameterized application repositories save messages separately.

A design revision also replaced independent animation with a clock-derived cue, avoiding drift when motion is toggled mid-cycle. The later smoothing request changed visuals without adding the proposed half-second holds. The student verified that UI cleanup; agent-run test results are not represented as personal student test execution.

## Unfinished work and submission checklist

Saved preferences/change/forget, editable Figma capture/alternative/selected-frame round trip, normal-view persistent support/Stop bar and navigation refinements remain unfinished. Figma inspection found a blank Activity frame; current Vue is README-based, not a verified Figma implementation. No clinical testing, multi-user authentication, full accessibility audit, physical-mobile fullscreen proof, >100 message UI pagination check or clean-checkout reproduction is claimed.

Before upload:

- [ ] Student reviews report, AI disclosure and evidence for accuracy.
- [ ] Approve a Part 2 source/evidence commit separately; record its actual hash.
- [ ] Approve push separately; verify branch/commit reached the supplied remote.
- [ ] Replace local report links with commit-specific hosted links and verify access; separately commit that report update if needed.
- [ ] Confirm Part 1 remains accessible and upload the finalized `report.md` for Part 2.

Nothing has been merged, deployed or submitted to the course site. [README/run instructions](README.md) and [handoff](handoffs/current.md) document the current local state.
