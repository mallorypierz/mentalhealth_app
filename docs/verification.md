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
