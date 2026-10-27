# Assignment 3.2 — Part 2: Updated working prototype

Prepared October 27, 2026. The student explicitly confirmed “the chatbot is all finished and verified” and approved inclusion of all completed additions. This report describes the current local implementation, not just the earlier submission. **Published source:** updated source/evidence commit is pushed and its linked files verified publicly readable. This finalized report is a subsequent documentation-only update. Figma remains blocked as disclosed below.

| Submission field | Value |
| --- | --- |
| Repository | [mallorypierz/mentalhealth_app](https://github.com/mallorypierz/mentalhealth_app) |
| Current branch | `codex/profiles-calendar` |
| Updated submitted source commit | [`aaa6fce619ec3e1a4baaedcf6bc4fa64f0f354a8`](https://github.com/mallorypierz/mentalhealth_app/commit/aaa6fce619ec3e1a4baaedcf6bc4fa64f0f354a8) — verified on remote `codex/profiles-calendar`. |
| Prior published expansion | [e593a522b7a1b0718e1a19987ac133e66cfbc36b](https://github.com/mallorypierz/mentalhealth_app/commit/e593a522b7a1b0718e1a19987ac133e66cfbc36b) — profiles/calendar/library |
| Original Part 2 | [Source080ad639](https://github.com/mallorypierz/mentalhealth_app/commit/080ad6393a2ade204f6f2b417b422a5778a8ed4c), [reportf133bf99](https://github.com/mallorypierz/mentalhealth_app/blob/f133bf99804246fe4fa34f090db37b196abf69c8/report.md) preserved |
| Part 1 | [Reporte958bdcf](https://github.com/mallorypierz/mentalhealth_app/blob/e958bdcf11e69b5c4451f986742989acd01b497e/report.md) preserved |
| Evidence access | All10 linked source/document/evidence files below were verified publicly readable without authentication at the new commit on October27. This is not a check from the instructor’s device. |

## Experience and completed scope

A person can choose a local profile or continue directly as guest, practice paced breathing, review saved activity and calendar events, or use optional voice/typed chat. Display name is required only when creating a profile; age and gender are optional. Profiles have no passwords and are not secure authentication. Guest history survives refresh/navigation; explicit Exit guest or confirmed discard clears it, while explicit transfer can attach it to a selected profile. Switching during practice offers continuation or Stop and switch. Profile deletion requires confirmation. Legacy records remain under their original owner.

Paced breathing (4–6) is the only completed skill: six cycles with Pause, explicit Resume, Stop, still cue, fullscreen and neutral results. The exercise library opens this existing exercise without auto-start. 5-4-3-2-1 sensory grounding, STOP and One-minute cognitive reframe are names-only, unavailable Coming later entries. No generated instructions or fabricated completions are provided for them.

The calendar derives events from the active identity's completed SQLite sessions, placed at completion time in the device's timezone. Stopped/interrupted sessions remain visible in history but are excluded from the calendar. Activity counts do not indicate wellbeing or improvement. This is a responsive website, not a native application or PWA.

## Assignment audit

| Part 2 requirement | Evidence and status |
| --- | --- |
| Complete at least one chosen skill | Six-cycle paced breathing implemented; [completion evidence](https://github.com/mallorypierz/mentalhealth_app/blob/aaa6fce619ec3e1a4baaedcf6bc4fa64f0f354a8/docs/evidence/part2-final-completed.png), timing and tests |
| Model contribution with relevant context | Two-call SQL RAG plus actual live transcription, answer generation and speech; [evidence categories](https://github.com/mallorypierz/mentalhealth_app/blob/aaa6fce619ec3e1a4baaedcf6bc4fa64f0f354a8/docs/evidence/voice-update.md) distinguish agent observations, mocks and student verification |
| Conversation/session persistence and history | Stable IDs/order/timestamps, parameterized transactions, actual saved replies, session table, calendar; [original browser/API/SQLite extract](https://github.com/mallorypierz/mentalhealth_app/blob/aaa6fce619ec3e1a4baaedcf6bc4fa64f0f354a8/docs/evidence/part2-final-records.json) and [verification](https://github.com/mallorypierz/mentalhealth_app/blob/aaa6fce619ec3e1a4baaedcf6bc4fa64f0f354a8/docs/verification.md) |
| Guided exercise no longer than90 seconds | Historical measured bounds below90 seconds; sequence remains unchanged; timing detail below |
| Independent crisis-support route | Application-controlled support accessible without microphone/model/classifier/database/budget; historical backend-outage checks; no service contacted |
| Request failure and leaving exercise | Saved/failed/unknown states, retry idempotency, stopped/interrupted records, pause/recovery; voice audio failure separate from text persistence |
| Research rationale and control | R1–R4/D1–D6 tradeoffs below and [design contracts](https://github.com/mallorypierz/mentalhealth_app/blob/aaa6fce619ec3e1a4baaedcf6bc4fa64f0f354a8/docs/design-pipeline.md) |
| Report, accessible evidence, source commit, disclosure | Source committed/pushed, hash recorded and10 hosted evidence links verified; [AI disclosure](https://github.com/mallorypierz/mentalhealth_app/blob/aaa6fce619ec3e1a4baaedcf6bc4fa64f0f354a8/AI-USE.md) |
| Class Figma workflow in AGENTS.md | Not fully verified; draft access/tool-limit evidence does not prove editable capture, alternative selection and Vue round-trip fidelity |

Profiles, calendar, exercise placeholders and speech are optional additions to the assignment. Implementing all four skills is not required. The supplied assignment permits honest unfinished work in Part2. Part3's fifteen fictional scenarios, three explicit behavior checks, varied live evaluation, clean-checkout reproduction and final demonstration/process recordings are not claimed complete here. No recording is attached.

## Research rationale

The supplied study reports15 patients,13 clinicians and15 prototype evaluations. Mention counts are design concerns, not clinical effect sizes. R1 and D1/D2 motivate one short, fixed, atomic exercise with minimal setup. R3/R4 motivate direct guest access, explicit Start/Stop, pause-before-switch and reversible optional choices. D3 motivates optional age/gender and a typed alternative to speech. D5 motivates saved profile activity and explicit guest transfer instead of silently assigning data; the tradeoff is a chooser and visible profile-selection privacy limits. Still-cue preference itself remains temporary, not persisted. R2/D4 motivate independent support even when chat fails. D6 motivates neutral language, restrained motion and no clinical claims.

Voice lowers typing effort but introduces recognition errors, latency, privacy and cost. We chose automatic silence-based turns only after explicit Start. Playback no longer supports automatic spoken interruption because the microphone could mistake speaker output for user speech; explicit Stop speaking remains. Saved text and typed input preserve access when audio fails. Navigation wraps rather than implementing the drafted mobile bottom bar; comprehensive phone/zoom/keyboard verification remains incomplete.

## Model contribution and data flow

Vue talks to FastAPI; only backend code accesses project-relative SQLite or provider credentials. Application code owns skill timing, exits, support and writes. The model may discuss general educational wellbeing topics such as stress, emotions, coping, relationships and seeking professional help. It must not diagnose, prescribe treatment or medication changes, promise improvement, invent therapeutic exercises, or imply monitoring. This is a fictional-scenario coursework demonstration, not a support service.

The voice pipeline is speech-to-text → SQL planning → answer generation → speech synthesis, using `gpt-4o-mini-transcribe`, `gpt-5.4-mini-2026-03-17` for both RAG calls, and `gpt-4o-mini-tts`/`marin`. It is continuous turn-taking with processing gaps, not duplex realtime audio. Typed input uses the same scoped RAG and persistence flow.

The first model proposes SQL using reviewed schema. Backend structural validation restricts fields/tables/grammar, reconstructs parameterized SQL and adds ownership itself. A read-only connection, authorizer and row/time/context limits bound retrieval. Raw model SQL is never executed. The second model receives only permitted records plus reviewed instructions. Stored text remains data, not instructions. Citations must belong to retrieved IDs, although membership alone cannot prove semantic correctness.

Rejected SQL never runs. Rejected queries, database errors and timeouts can now reach answer generation with explicitly empty context and an unavailable-history status. General educational discussion may continue, while personal-history claims must be withheld and the limitation disclosed. This correction preserves retrieval outcomes rather than pretending retrieval succeeded. Configuration, provider or exhausted-budget failures remain failures. Actual accepted replies use normal application persistence before audio generation; an audio failure cannot erase a saved reply.

SQLite keeps identities, sessions, conversations, ordered user/assistant messages, requests, voice turns/operations and durable attempt reservations. Ownership is checked using browser context tokens, not a client-supplied profile ID alone; the local chooser still is not secure authentication. Operation receipts and unique IDs prevent duplicate writes. Audio is transient in memory and expires; transcripts/replies follow profile/guest retention rules. Provider-side retention is outside this application's local discard guarantee.

## Verification and timing

[Verification notes](https://github.com/mallorypierz/mentalhealth_app/blob/aaa6fce619ec3e1a4baaedcf6bc4fa64f0f354a8/docs/verification.md) provide dated commands and separate mock, live, historical and untested evidence. The October27 preparation checks are recorded there. No new paid call was made for document preparation. The student's current message explicitly verifies the chatbot; it does not establish every physical-device/browser combination or clinical quality.

Historical final Part2 measurement: setup5.036s separately; pre-Start-click to completed UI72.336s, conservatively including observation overhead and application delays. First instruction was observed1.091s after click, so that bound covers the full guided sequence. No voluntary pauses/support were excluded. SQLite stored60000ms active with60.001s wall span; the capped timer alone is not the measurement. Later profile-enabled measurement was bounded by72.082s from guest entry through completed/saved state, with entry/setup observation bound3.770s. These are historical runs, not a new voice-era timing measurement; six-cycle timer tests still pass and voice remains outside timed practice.

Historical evidence covers stopped practice, support-induced pause, explicit Resume, Chrome hidden-tab pause, refresh recovery and backend restart. Failed provider requests retain submitted messages without fabricated replies. Failed saves expose uncertainty/retry. Voice errors distinguish transcription, submission and speech; budget failure can occur mid-turn after the question was saved.

Required helpline lookup was last recorded October26; no service contacted. That dated lookup is not a claim of a new lookup today. Limited wording/transcript/output checks can miss indirect distress or flag quotations/negation and are not reliable detection or clinical assessment. The static support route is independent of them.

## Revised approaches and generated code

First, the mock audio was intentionally a tone, not speech; the student requested real voice. The first live speech response then failed local WAV validation despite HTTP success. The correction requests PCM and constructs a valid WAV header locally; a speech-only retry reused the saved answer without repeating transcription/RAG. Browser playback reached completion. The student later reported a two-word cutoff; inspection found automatic sound-onset interruption could react to speaker echo. Ignoring microphone frames during playback replaced it, and the student now confirms the chatbot is verified. Echo was a plausible cause, not independently proven for the earlier event.

A second revision addressed overly restrictive app-only answers and rejected retrieval. The approved educational prompt now permits general discussion; a failed lookup supplies empty context rather than preventing all answers. Mock tests verify rejected writes do not execute, no foreign citations pass, actual fallback replies are saved and failure statuses remain distinct.

Generated code example: [reader.py](https://github.com/mallorypierz/mentalhealth_app/blob/aaa6fce619ec3e1a4baaedcf6bc4fa64f0f354a8/backend/app/rag/reader.py) takes a validated `Query`, maps approved fields to physical columns, adds owner/conversation scope with bound parameters, and opens SQLite read-only with an authorizer. The model cannot provide ownership predicates or write data. [pipeline.py](https://github.com/mallorypierz/mentalhealth_app/blob/aaa6fce619ec3e1a4baaedcf6bc4fa64f0f354a8/backend/app/rag/pipeline.py) preserves retrieval status when context is unavailable, checks returned citations and response boundaries, then returns actual content for the repository to save. [microphone.js](https://github.com/mallorypierz/mentalhealth_app/blob/aaa6fce619ec3e1a4baaedcf6bc4fa64f0f354a8/frontend/src/microphone.js) rejects frames during playback/processing/hidden states so speaker audio does not become a new turn. These checks are software boundaries, not guarantees of medical safety or perfect recognition.

## Remaining work and submission checklist

Unfinished: saved still-cue preferences; fully verified editable Figma round trip and viewport comparison; comprehensive phone/landscape/zoom/keyboard/accessibility and failure-state coverage; clean-checkout reproduction; broader live quality testing and final recordings. [Assignment-3 Figma file](https://www.figma.com/design/3fMOXNlHnM4ebWaFKI0CXi/Assignment-3) is a historical reference, not newly verified evidence. Prior MCP quota prevented current node verification. No missing result is treated as passed.

October27 compliance follow-up: live testing now uses explicit host-created sessions capped at50 calls/$2.50 reservations each. All49 prior voice attempts remain historical/unassigned and are not charged to a new session counter. Refresh/restart/profile changes never reset the selected session. New sessions and live activation require explicit host approval. The template and peer-test default remain mocked. After offline verification, the student separately approved a24-call/$1.20 live demo session; activation used0 paid calls. Historical65-call authorization is superseded. Subsequent live sessions still require explicit approval. Speech model migration remains a separate decision.

The approved [manual Figma fallback](https://github.com/mallorypierz/mentalhealth_app/blob/aaa6fce619ec3e1a4baaedcf6bc4fa64f0f354a8/docs/figma-fallback/README.md) provides14 static desktop/390px PNG boards, matching SVG sources and flow notes. These are simplified source-informed references, not exact captures or editable Figma components; the MCP quota still blocks direct updates. This follow-up is committed and pushed; the source hash above includes testing-session budgets and the static reference pack. Prior reportf93bc0d remains preserved.

- [x] Student explicitly verified chatbot completion and approved documentation inclusion.
- [x] Current implementation, optional features and remaining limitations documented.
- [x] Original Part1 and Part2 commit references preserved.
- [ ] Student reviews this revised report and disclosures.
- [x] Student separately approved committing all updated source/evidence.
- [x] Created approved source/evidence commit; actual hash recorded above.
- [x] Student separately approved pushing all updated changes.
- [x] Verified exact source/evidence hash on remote after push.
- [x] Replaced local evidence links with verified commit-specific hosted links. Finalized report is published as a documentation follow-up.
- [x] Use mocked peer testing and enforce an explicit50-call maximum per approved testing session.
- [x] Prepare approved static Figma fallback; disclose that editable workflow remains incomplete.
- [x] Committed/pushed this follow-up and pinned its fallback evidence link.
- [ ] Student uploads the finalized report.md. No course upload, merge or deployment has been performed.
