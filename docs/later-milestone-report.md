# Later milestone: profiles, calendar and exercise library

Status: implemented expansion with incomplete browser verification; committed and pushed on `codex/profiles-calendar` with user approval. This is separate from the submitted Assignment3 Part2 milestone.

Repository: https://github.com/mallorypierz/mentalhealth_app

The submitted Part2 report commit f133bf99804246fe4fa34f090db37b196abf69c8 and source/evidence commit080ad6393a2ade204f6f2b417b422a5778a8ed4c remain unchanged. Part1 remains at e958bdcf11e69b5c4451f986742989acd01b497e. Later-milestone source/tests/documentation commit: [e593a522b7a1b0718e1a19987ac133e66cfbc36b](https://github.com/mallorypierz/mentalhealth_app/commit/e593a522b7a1b0718e1a19987ac133e66cfbc36b). Remote branch verification matched this hash. This documentation-only follow-up records publication; no course-site submission is claimed.

Implemented: local profile chooser with required display name and optional age/gender, direct guest entry, identity-scoped saved activity, explicit guest transfer/discard, profile editing/deletion, completed-session calendar, exercise-library navigation, and responsive web styles. Local profile selection is not secure authentication. Guest refresh/navigation retention does not guarantee deletion on tab close. Legacy activity remains under its original owner.

Available exercise: existing six-cycle four-second-in/six-second-out paced breathing. 5-4-3-2-1 sensory grounding, STOP and One-minute cognitive reframe are unavailable Coming later placeholders, with no instructions or completion records. Chat is mock-only in the profile-enabled app. No paid calls were made for this milestone.

[Behavior contracts](design-pipeline.md) describe identity ownership, API contracts, calendar completion-time/device-timezone rules and read-only RAG separation. [Verification](verification.md) separates automated mock tests, actual browser/SQLite observations, historical evidence and untested work. A fresh browser run completed and showed saved within a conservative72.082s of guest entry, including setup and observation delays. Entry-to-instruction observation was bounded by3.770s. No pauses/support time were excluded; exact rendering instants were not instrumented. See verification for timestamps. Support content remains application-controlled and independent of chat; fresh failure-state reachability and resource currency are not established by automated tests alone.

AI contribution: generated implementation and tests under user-approved increments, performed read-only audits, and drafted these notes. Profile context is resolved on the backend from a browser token and checked again during repository operations; a client-supplied profile ID alone does not authorize activity reads. Idempotent operation receipts let exact retries reuse results instead of duplicating records.

Revised approach: the earlier single-demo-owner model was retained for legacy records while new profile/guest identities were introduced, avoiding silent reassignment of submitted evidence to a new person. Responsive navigation currently wraps in document flow, differing from the selected draft's bottom-bar idea. This deviation needs review.

Unfinished: complete fresh phone/landscape/zoom/keyboard/failure browser checks, final Figma editability and viewport comparison, preference remembering/forgetting, physical-device and comprehensive accessibility testing. Figma MCP quota prevented current frame verification; no current verified frame links are asserted here. No native app or PWA is claimed.

Review checklist:
- [ ] Complete remaining browser checks and record results.
- [ ] Resolve or approve documented design differences.
- [ ] Verify Figma references when tool access permits.
- [ ] User verifies label and documentation accuracy.
- [x] User explicitly approved milestone commit and push.

Nothing in this milestone has been merged, deployed or submitted by the agent.
