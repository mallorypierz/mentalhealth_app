# Assignment 3.1 — Part 1: Design proposal

**Project:** A little space — mental health skills coursework prototype

**Milestone:** Part 1 design proposal with an optional frontend experiment

**Prepared:** October 15, 2026

**Submission status:** Draft; repository identity and hosted access remain unverified.

| Required submission field | Status |
| --- | --- |
| Repository URL | **PENDING — no repository URL supplied or verified.** |
| Submitted milestone commit | **PENDING — Part 1 milestone commit will be recorded in a separate report-update commit.** |
| Instructor access to linked materials | **PENDING — local file links checked; hosted access not verified.** |

Links below are repository-relative. They work when these files are kept together, but an isolated report.md uploaded to Canvas may not resolve them. Before submission, replace or supplement them with verified hosted links to the submitted version. No local machine path or localhost address is presented as remotely accessible evidence.

## Purpose, scenario, and chosen skill

The application is intended to let someone practice one short skill with little reading, typing, or setup, while retaining control over starting, pausing, stopping, and accessing support. The fictional scenario is a college student choosing a brief breathing practice before starting an assignment. The app does not assume the student is distressed or infer their emotional state from interaction.

The chosen skill is **paced breathing: inhale for four seconds, exhale for six seconds, repeated for six cycles**. Its planned guided duration is 60 seconds. The design preserves the skill sequence rather than having a language model invent or modify instructions. This is a coursework prototype tested only through fictional scenarios, not therapy, diagnosis, a monitored service, or evidence of clinical effectiveness. It must not be offered to someone as a support tool to rely on during distress.

## Main experience and timing

**Entry → optional introduction or direct Start → breathing practice → stopped/completed result → optional history.** Practice presents one current instruction with a count and an optional moving cue. Pause and Stop remain available. Opening crisis support pauses running practice; closing support leaves it paused until an explicit Resume. Mock introduction failure permits retry without blocking Start or support, and starting practice invalidates pending introduction responses.

[Initial flow diagram (SVG)](docs/diagrams/part1-flow.svg) · [PNG preview](docs/diagrams/part1-flow.png) · [Editable flow and behavior notes](docs/diagrams/part1-flow.md)

The diagram is **initial design, not a completed Figma capture**. It labels selected future revisions separately from the current prototype.

Timing is measured from the first actionable exercise cue through the final planned exhale, including application delays within the sequence. Six cycles × ten seconds gives 60 seconds at the intended pace, below the assignment's 90-second limit. Entry reading, optional introduction, and display setup are reported separately; voluntary pauses and support time are excluded without double-counting. No typing or breath confirmations are required. The timer cues intended pacing, not actual breathing adherence. Completion leaves a result rather than forcing an exit. External timing under rendering delays, background tabs, and device sleep remains to be checked; a capped display counter is not sufficient proof of experienced duration.

## Research-grounded decisions and tradeoffs

Source: the supplied Assignment 3 study table, **R1–R4 and D1–D6**. The overview describes 15 patients, 13 clinicians, and 15 prototype evaluation sessions. Mention counts identify concerns in the study; they are not effect sizes or evidence that this app improves mental health. Applying these findings to the fictional college-student scenario is a design hypothesis.

| Findings | Design response | Alternative and tradeoff |
| --- | --- | --- |
| **R1:** attention declined beyond 90–100 seconds (38 mentions) | Use six 4/6 cycles for a fixed 60-second practice. | A duration picker offers flexibility but adds setup; the fixed duration simplifies entry. |
| **R2 / D4:** frictionless, persistently visible safety (30 / 31 mentions) | Keep support independent of model results. The student selected a persistent bottom bar with support and active-practice Stop. | The current in-flow button occupies less fixed space but can scroll offscreen. A bottom bar needs reserved space to avoid covering controls. **The bar is not implemented.** |
| **R3 / R4:** permission to stop and control the journey (39 / 68 mentions) | Pause, explicit Resume, consequence-free Stop, optional introduction/history, and neutral results. | Mandatory completion or automatic routing reduces choice. Easy stopping allows accidental exits but avoids coercive confirmation or penalties. |
| **D1 / D2:** less interface and one atomic skill (54 / 100 mentions) | One breathing cue at a time. The student selected hiding general navigation during active practice, then restoring it. | Keeping navigation visible aids discovery but competes with the cue. The proposed simplification follows explicit Start, not detected distress. **General navigation is still visible today.** |
| **D3:** minimize emotional cost (148 mentions) | No required questionnaire, disclosure, or typing before Start. | Required check-ins provide more context but demand more effort; this app does not claim to know how the person feels. |
| **D5:** personalization without configuration burden (49 mentions) | Proposed optional “Remember my display choice,” with visible saved status and change/forget controls. | Silent automatic saving reduces one decision but weakens transparency. Opt-in adds a small choice; persistence is not implemented. |
| **D6:** low-stimulus, non-judgmental presentation (97 mentions) | Restrained colors, neutral wording, and a still text/count cue. System reduced motion takes precedence over a future saved animated preference. | Less motion is less expressive; visual calm must not compromise contrast or discoverability. Universal comfort and full accessibility are not established. |

The [full decision table](docs/design-pipeline.md#decisions-alternatives-and-checks) includes each finding's supporting evidence, implementation status, alternative, tradeoff, and proposed check.

## Planned architecture, model role, and data

The proposed stack is Vue/JavaScript → FastAPI/Python over HTTP/JSON → SQLite. Vue owns interface state, local exercise timing and controls; backend controllers validate scope and requests, coordinate provider calls, and save through parameterized transactions. Only backend code opens the project-relative database or holds provider credentials. None of that backend/persistence flow exists yet.

The model's planned role is limited to reviewed app/skill explanations and grounded descriptions of saved history. It cannot alter steps, timers, exits, support access, preferences, or saving rules. Proposed SQL RAG uses a first call to suggest retrieval from a reviewed schema; the backend structurally validates a single restricted read-only query, independently enforces ownership scope, binds values, and limits time/rows/context. A second call receives only permitted relevant records with IDs and reviewed context. Stored text is data, not governing instructions. The actual reply is saved through the normal transaction. Empty retrieval, rejected SQL, database failure and provider failure remain distinct. Neither call is implemented.

Proposed records are conversations, ordered user/assistant messages, exercise sessions, explicit opted-in motion preferences, and request bookkeeping. Stable IDs and ownership relationships support retry protection and traceable history. Users would review actual messages with roles/times/status, sessions with active duration and stopped/completed status, and the current/saved display choice. A failed save must not be displayed as saved; summaries cannot turn activity into a diagnosis or improvement claim.

The student selected optional preference remembering and confirmed system reduced-motion precedence. Users may skip remembering, change the effective display, or forget a saved choice. This saves repeated configuration without treating clicks or stopped sessions as emotional evidence. Current choices and records reset on refresh.

[Architecture, record relationships, request contracts, and behavior proposal](docs/design-pipeline.md#planned-architecture-and-behavior-part-1-proposal)

## Crisis boundaries and user control

Support must remain available without a questionnaire, classifier result, model response, or successful save. The current independent panel contains region-labeled US/territories resource information checked through the helpline lookup; no service was contacted for testing. Its button is present in each view but scrolls with the page, so persistent viewport visibility is an identified limitation.

For future free-text chat, the proposal considers a reviewed application-owned cue check that offers support and explains the unmonitored coursework role. It would not diagnose, promise safety, contact anyone, or force a skill. Exact wording and coverage remain unresolved. Such a check can miss indirect or unfamiliar wording and falsely flag quotations; no-match cannot establish safety. A model may also fail or misinterpret a message. These limitations are why support access cannot depend on detection. The current prototype has no free-text crisis detector or real chatbot.

## Optional prototype experiment and evidence

A working application is not required for Part 1. The optional Vue experiment makes the initial flow concrete; it does not complete Parts 2 or 3.

| Evidence | What it shows | Limit |
| --- | --- | --- |
| [Desktop entry](docs/evidence/desktop-entry.jpg) | Direct Start, optional scripted introduction, still-cue control, and demo/reset labels. | Screenshot only; not measured emotional effort or usability for a clinical population. |
| [Narrow paused practice](docs/evidence/narrow-practice.jpg) | Paused state with Resume/Stop at 390px width; general navigation still visible. | Full-page image cannot prove viewport-persistent support or timer behavior. |
| [Narrow history](docs/evidence/narrow-history.jpg) | A completed 60-second temporary session with a stable ID, separate from a labeled fixture. | No SQLite persistence, API/database comparison, or clinical outcome. |
| [Recorded checks](docs/verification.md) | Agent observed mock failure/retry, delayed response cancellation, support pause/explicit Resume, stopped/completed history, refresh reset, and keyboard activation/focus. Four unit tests and production build previously passed. | Not a new test run or full accessibility audit. The 60-second browser run preceded the final cue refinement; only affected behavior plus unit tests/build were rechecked afterward. |

[Curated evidence and prompt/change/decision trail](docs/evidence/README.md) explains these limits and the revised approaches. In particular, the supplied Figma Activity frame was blank, so the student requested a README-based prototype instead of claiming a design-to-code match. The agent also replaced an independent CSS animation with a clock-derived cue to avoid a potential mismatch when re-enabling motion mid-cycle. These are documented observations and decisions, not invented user-test findings.

## Completion status, open questions, and next steps

**Prepared for Part 1:** design rationale and research mapping; initial flow diagram; model/data/personalization and behavior proposal; optional frontend experiment; curated evidence; AI-use disclosure.

**Unfinished:** FastAPI backend, SQLite persistence, SQL RAG, live conversational AI, persistent preferences, selected bottom-bar/navigation revisions, and Figma capture/editable-layer verification/design round trip. No Parts 2 or 3 completion is claimed. No recording is provided for this design milestone; the supplied overview places finished-app demonstrations/process screencasts in the later milestone.

Open questions include preference-control placement and forgetting semantics, crisis-text wording/coverage and resource updates, retention/deletion and demo identity, recovery from interrupted saves/sessions, hidden-tab/sleep handling, and provider/parser choices and call budgets. These are explicitly unresolved design details, not completed features.

Next: review the proposal and disclosure, finalize submission links and commit, then plan a small backend save/read and one frontend/backend round trip. Later work will implement and verify persistence/RAG, the selected UI revisions, and any requested Figma comparison. Paid calls require an agreed limit; routine checks use mocks and fictional data.

[README and run instructions](README.md) · [Project instructions](AGENTS.md) · [Current handoff](handoffs/current.md) · [AI-USE.md](AI-USE.md)

The disclosure identifies documented tools and roles, known versions and unknown model identifiers, generated/reused material, student-confirmed choices, and review limits. Agent-run checks are not represented as personal student testing. A scoped privacy review found no common credential patterns or unnecessary private content in selected screenshots; it was not an exhaustive security audit.

## Part 1 audit and remaining submission gaps

| Supplied Part 1 requirement | Audit result |
| --- | --- |
| Explain purpose, skill, and fictional use | Covered in this report. |
| Show the main experience with a sketch or flow | Linked initial SVG/PNG and editable flow notes exist locally. |
| Connect important choices to R/D findings and alternatives/tradeoffs | Covered here and individually in the detailed decision table. |
| Describe model role, expected stored data, personalization, and user control | Covered as proposed capabilities, distinct from the baseline. |
| Explain timing, independent crisis access, and testing boundaries | Covered, including present visibility/timing limits and unresolved crisis-text design. |
| Maintain project context and disclose AI use with curated evidence | Local documents and disclosure exist; student review is still required. |
| Include repository URL and submitted-version commit | **Missing/unverified; placeholders intentionally retained above.** |
| Provide accessible design/evidence links | Local targets exist; **hosted links and instructor access still unverified.** |

Before uploading: supply and verify the repository URL; commit the intended milestone and verify its hash; add hosted version-specific links; confirm instructor access; and personally review the report and AI-use disclosure for accuracy. A future commit cannot be inferred from these local files. The current draft is not yet a verified submission package.
