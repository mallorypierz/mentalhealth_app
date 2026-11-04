# Part 3.3 recording outline

**Frontend recording received; process recording pending.** Updated November 3, 2026. Received a5:02 silent frontend recording; see evidence/part3/recording/received-video.md for storage and sampled review. Full requirement coverage remains unverified. Use one recording with the two title cards below, or two files. Suggested total: 7–9 minutes. Rehearse first; pause recording while navigating files. All demonstrations use fictional data. No new paid calls are needed.

## Before recording

1. Save unfinished work. Published implementation is branch `codex/exercise-quiz`, commit `bdf3f84c72a9a27c27b10646d4ec2605f5982a81` (remote verified). Show `git status --short` and `git rev-parse HEAD`; disclose any later changes. This outline publication-status refresh is newer than that commit.
2. The last verified running backend was restored to LIVE; recheck its current health. Do **not** assume it is mocked or submit a test message there. For the recording, stop the existing backend using Ctrl+C in its terminal, then run the explicit mock command below from the project root. It uses a fresh temporary database and existing dependencies; do not copy `.env`, databases or dependency folders. Keep the frontend on5173. Stop any previous process occupying8000 before starting; do not run both backends on that port.
3. Open a fresh browser tab at `http://127.0.0.1:5173/`. Check `/api/health`: require `provider: mock`, `voice_enabled: false`, zero live usage for this temporary database. If not, stop and correct the server. The quiz and exercise controls are deterministic application code even when chat is live.
4. Close private tabs/notifications and terminals displaying credentials. Do not show `.env`, request Authorization headers, browser storage, or raw identity bootstrap responses. Show only fictional record fields. Keep microphone off in the app. Enable your recorder's narration microphone only.
5. On macOS press Shift–Command–5, choose Record Selected Portion, frame only the app/editor area, choose your narration microphone under Options, then Record. Stop with the menu-bar stop control or Command–Control–Escape. Rename outputs `part3-demo.mov` and `part3-process.mov` (or one `part3-demo-and-process.mov` with marked chapters). Review audio, readable text, secrets and start/end frames before sharing.

Explicit mock recording backend (run manually when ready; not executed by this preparation):

```sh
cd /Users/mallorypierz/mentalhealth_app
backend/.venv/bin/python -c 'from pathlib import Path; import tempfile; import uvicorn; from backend.app.main import create_app; from backend.app.config import Settings; folder = Path(tempfile.mkdtemp(prefix="mentalhealth-recording-")); print("Fictional recording database:", folder / "app.sqlite3"); uvicorn.run(create_app(folder / "app.sqlite3", Settings(), enable_profiles=True), host="127.0.0.1", port=8000)'
```

Leave that terminal open; note its printed database path privately for inspection. Frontend command if needed: `npm --prefix frontend run dev -- --port 5173 --strictPort`. After recording, stop the mock server. Restoring live is a separate deliberate startup with the existing allowance, never a ledger reset. This guide does not authorize extra provider calls.

## SECTION 1 — Finished-app demonstration (about 4–5 minutes)

Title card: **Finished-app demonstration — fictional data; mock provider; deterministic quiz and exercises**.

| Shot | Exact actions | Concise narration |
|---|---|---|
| 1. Mode and guest | Briefly show health mock/voice disabled. Return to app; Continue as guest. | “This is a fictional coursework demo. Chat uses scripted mocks here; no paid AI calls are made. Quiz decisions and exercise timing are application code.” |
| 2. First answer path | Exercises → Help me choose → Follow a breathing rhythm → Next → Yes → See suggestion. | “These choices suggest breathing. The explanation uses my answers, and nothing starts automatically.” |
| 3. Reject | Click Choose another. Show the exercise library. | “I can reject the suggestion and choose any available exercise.” |
| 4. Second path | Help me choose → Notice my surroundings → Next → I’d rather avoid it → See suggestion. | “Different answers suggest grounding, which does not focus on breathing. This is a preference match, not a clinical score or a claim that it will help most.” |
| 5. Practice and support | Preview exercise → Start practice. Mark two boxes. Click Next step. Open Crisis support while the exercise is active. Close it; show paused state, then Resume. Do not call/text a listed service. | “The checkmarks are optional. I can advance, pause or stop. Support opens directly without sending a message or completing the quiz; opening it pauses practice.” |
| 6. Finish or stop | Continue through the prompts with Next step and Finish exercise, or choose Stop practice. Wait for Session saved. | “This fictional run records the actual active duration and whether I finished or stopped. It does not measure how I feel.” |
| 7. History | View history. Show exercise, duration and status. For ID evidence inspect only the row's `data-session-id` in Elements, not network headers/storage. | “The saved row identifies this exercise and its outcome. Interrupted sessions retain their last confirmed checkpoint.” |
| 8. Profile | Guest · switch → Create a profile → display name `Fictional Recording Alex`; leave age/gender empty → Save profile. Select Save this guest activity to my profile, then select the new profile. | “Profiles are local fictional identities, not secure accounts. I explicitly choose to keep this guest activity.” |
| 9. Remember | Exercises → Help me choose → surroundings/avoid → See suggestion. Expand Saved preferences → check Remember these answers → Save preferences. Wait for Preferences saved. | “Remembering answers is opt-in. Current answers always control the suggestion; history counts never rank exercises.” |
| 10. Return/change | Refresh; return to Exercises. Expand Saved preferences → Use saved answers; show restored choices. Use Next/See suggestion. Optionally Forget saved answers and show confirmation. Reopen history. | “Saved answers are reused only when I choose. I can change or forget them. My exercise history is separate.” |

If an action fails, retain the failure, fix it and record a labeled retest rather than narrating success over an error. Do not mark this outline's planned steps as observed passes.

Optional live-evidence insert, no new requests: show `docs/evidence/part3/live/comparison.md` and one fictional result from `live/results.json`. Label **Previously recorded live text-model evidence; not a live call in this video**. Say: “The separate approved sample used six typed trials and twelve provider calls. Both RAG calls counted. Live voice was not retested in this recording.” A mock test tone is not spoken AI; do not present it as live speech. If a new live demonstration is requested, inspect the current ledger and obtain a specific allowance first; never assume the earlier remaining count is current.

## SECTION 2 — Process evidence (about 3–4 minutes)

Title card: **Process evidence — actual invalid-session failure; mocked automated retest**.

### Failure → evidence → decision → retest

1. **Actual failure:** display the recorded user report “Local access is invalid or revoked.” from the conversation, cropped to that report, or the dated Invalid local access recovery entry in `docs/verification.md`. Narration: “After I switched from the isolated mock database to the original live database, the browser still held the previous local identity. The user reported being unable to enter.” There is no retained original failure screenshot or HTTP trace; do not invent one or portray a reconstruction as original footage.
2. **Expected:** “The app should offer a usable profile chooser when its saved local credential is rejected. A temporary network failure should not discard valid access.”
3. **Evidence:** show the ProfileGate change with `git diff bdf3f84^ bdf3f84 -- frontend/src/ProfileGate.vue`, then `frontend/src/identityRecovery.js`. The previous boot path retried `/identity` with the same stored credential; the new helper handles401 explicitly. The database switch and browser report support the diagnosis; there was no record-by-record database trace proving the rejected token. Do not open or display credentials to manufacture that proof.
4. **Decision/fix:** “On401 only, clear the browser access reference and bootstrap once. Return to the chooser without deleting records, resetting the usage ledger, replaying a pending save or choosing a profile automatically. Network,403 and500 failures remain errors.” Show `restoreIdentity(request, getAccess, clearAccess)` and the call in ProfileGate's `boot()`.
5. **Retest:** run `node --test frontend/tests/identityRecovery.test.js` in a clean terminal. Point to the three passing tests: rejected identity becomes chooser; other failures retain access; valid identity and bounded bootstrap. Retained output: `docs/evidence/part3/recording/identity-retest.txt` (3 passed during outline preparation). Say: “This is a mocked regression test, not a paid request. The original affected browser tab could not be reacquired by automation, so that exact browser recovery remains unverified.” Do not equate a new guest tab with reproducing that stale-token case.

### Explain generated code: actual `decide` function

Open `frontend/src/recommendation.js`, function `decide`, lines9–26.

Narration: “This generated function takes an activity choice, a breathing preference and the available exercise list. It returns a status, a reason and either an approved exercise or null. First it validates both inputs. An explicit activity takes priority; if activity is skipped, Yes to breathing can select breathing. It checks that the exercise exists and rejects breathing or STOP when breath focus is avoided or uncertain. Invalid, incomplete, conflicting and unavailable choices produce a clear fallback instead of an arbitrary winner. The reason quotes the actual activity choice. The function cannot start an exercise, save answers, call a model or rewrite instructions.”

Show two calls and one safeguard using the existing mocked tests: `node --test frontend/tests/recommendation.test.js`. Explain: “Surroundings plus avoid maps to grounding; breathing plus Yes maps to breathing; STOP plus avoid returns no suggestion. This is a small preference table, not an assessment of effectiveness. Two answers cannot capture every need, and users can always choose another exercise.”

## Evidence checklist

- [ ] Both sections have visible title cards and mode labels.
- [ ] Guest and fictional profile shown; no real personal details.
- [ ] Both answer paths and their distinct explanations shown.
- [ ] Rejection, separate preview/Start, and Stop or Finish shown.
- [ ] Optional grounding marks and accurate outcome/duration shown.
- [ ] Explicit remember, refresh/reuse and change/forget shown.
- [ ] History shown; row ID matched to evidence if claiming cross-layer verification.
- [ ] Independent support opened; no emergency resource contacted.
- [ ] Actual failure is identified as user-reported; historical evidence distinguished from a reconstruction.
- [ ] Expected behavior, source fix and three-test retest visible; browser retest limitation stated.
- [ ] `decide` inputs/outputs, validation, availability/conflict safeguards and limitations explained.
- [ ] Recordings reviewed for readable text, narration, secrets, and honest mock/live labels.

Optional read-only ID verification: use the printed recording database path with Python `sqlite3.connect('file:/absolute/path/app.sqlite3?mode=ro', uri=True)`; select only `id, skill_key, status, active_duration_ms` from `exercise_sessions` for the exact displayed ID using `WHERE id=?`. Do not select all identity/token columns. The retained earlier grounding example is `docs/evidence/part3/grounding-next-record.json`; it is historical evidence, not the new recording's record.

## Submission checklist

Completed artifacts (implementation and original evidence published in bdf3f84):

- [x] Implemented quiz, reviewed exercises, explicit preferences, session history and scoped read-only RAG.
- [x] README, architecture/contracts, verification notes, AI-USE and current handoff.
- [x] Part3 evaluation: `docs/part3-evaluation.md`; 18-scenario matrix and expected/observed evidence.17 pass within stated scope; S15 not-run.
- [x] Three explicit behavior checks, evidence-backed surprising finding and untested limitations documented.
- [x] Separate approved live variation sample/results (12 calls), preserved ledger.
- [x] Clean-checkout evidence for exact local candidate b3d8087; later quiz/grounding/recovery changes explicitly excluded from that claim.
- [x] This outline, narration and retained mocked identity-retest output.
- [x] Source committed and pushed to codex/exercise-quiz; remote hash verified as bdf3f84.

Still missing or needing final review:

- [ ] Finished-app video and process screencast (or one clearly divided video), links and access permissions.
- [ ] Retest/review the exact final source from a clean checkout; prior candidate predates latest changes.
- [ ] S15 combined model-failure/support browser evidence; do not infer from separate checks.
- [ ] Original affected-tab identity recovery browser retest, if claiming end-to-end recovery.
- [ ] Full physical-device/keyboard/timing evidence; setup-time measurement separate from exercise active time. Keep untested limits explicit.
- [ ] Figma workflow limitations remain: no verified MCP capture/implementation round trip, exact viewport parity or instructor-access check. Do not describe browser-created references as completed MCP workflow.
- [ ] Student review of narration/code explanation and final Part3 report reflecting later grounding/identity changes.
- [ ] Review any changes after bdf3f84, record the exact submission revision, and verify reviewer access to source/video links. Course submission remains pending.
