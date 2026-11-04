> Historical evaluation summary: see [report.md](../report.md) for the consolidated current submission, including later grounding controls, identity recovery and received frontend video. The dated results below retain their original scope.

# Part 3.3 integration and evaluation

Updated November 3, 2026. This is an agent-executed evaluation using fictional data, not a clinical study or evidence of emotional improvement. The student approved the exercise adaptations, quiz scope, top navigation and the bounded live sample. Recordings and final student submission review remain unfinished.

## Changes from the actual Part 3.1 choices

The initial rationale is retained in `report.md` at commit `e958bdcf` (Part 1 submission). It proposed one 60-second breathing skill, optional introduction, direct Start, practice, result and history. Its supplied principles were R1 short sequences; R2/D4 independent safety access; R3/R4 agency and stopping; D1/D2 simple, atomic steps; D3 low emotional burden; D5 optional remembered choices; D6 restraint. No additional class principles were invented.

| Initial choice | Final implementation and reason |
|---|---|
| One breathing exercise | Breathing is preserved; three explicitly reviewed alternatives fill the existing library placeholders. Grounding is 75 seconds, STOP and reframe 60. Avoiding breath focus excludes breathing and STOP from suggestions. This supports choice without claiming a best treatment. |
| Optional introductory screen | Removed after student review to reduce setup demands. Quiz and preview remain optional/separate from Start. |
| Future bottom navigation | Student selected Option A top navigation after comparing alternatives. Existing top navigation was preserved. |
| Optional personalization | Two multiple-choice questions; deterministic available-exercise mapping, no score/model selection. Explicit profile-only Remember/Save and Forget implement D5; current answers take priority. History does not influence ranking. |
| Simple completion history | Accurate completed/stopped/interrupted records, stable IDs and checkpoint recovery. Completion means the sequence elapsed, not participation or improvement. |
| Conversational assistance | Scoped SQL RAG remains read-only. Testing showed rejected retrieval can still support a general answer when unavailable history is disclosed; validation must prevent query execution and fabricated evidence. |
| Voice interruption | Earlier reported playback cutoff led to explicit Stop speaking instead of automatic barge-in. Echo was a hypothesis, not a confirmed cause. Physical microphone reliability remains outside this evaluation. |

## Repeatable evaluation

Expected results were recorded before execution in [the 18-case matrix](evidence/part3/scenarios.json). [Scenario results](evidence/part3/evaluation.md) list fictional inputs, setup, expected/observed outcomes, mode, status and evidence locations. Seventeen pass within their stated automated/browser scope. S15, combined model failure plus independently usable support in that same browser state, is **not-run**. Separate failure tests do not establish that combined invariant.

Routine command: `sh docs/evidence/part3/run_checks.sh`. Mock checks passed 82 backend tests, 33 frontend tests and production build. [Clean-checkout verification](evidence/part3/clean-checkout.md) repeats the README commands using newly installed isolated dependencies. Automated tests do not stand in for every browser interaction.

Three explicit cross-case behavior checks:

1. **Choice controls the exercise:** invalid/incomplete/conflicting/unavailable answers never produce an arbitrary exercise; manual choice and preview require explicit Start. Mapping tests and browser preview/rejection evidence pass.
2. **Persistence remains truthful and idempotent:** stopped/completed/interrupted outcomes remain distinct; retrying the same operation cannot duplicate a record or resurrect forgotten preferences. Transaction/replay/recovery tests pass; browser completion and refresh evidence are retained.
3. **History remains scoped and read-only:** foreign-owner records never become retrieved context; proposed writes are rejected before execution; empty retrieval cannot become invented history. RAG/identity tests pass. Selected IDs were compared across persisted data and displayed history/preferences.

A fourth desired invariant, independent support after provider failure, remains only partially verified (S15). It is not reported as passed.

## Live variation, separately from mocks

The host approved exactly 12 calls: three typed cases, two repetitions, two RAG calls each; no speech, transcription or retries. Existing ledger inspection preceded execution and no ledger was reset. [Exact results](evidence/part3/live/results.json) and [comparison](evidence/part3/live/comparison.md) retain questions, responses, citations and usage. All six trials saved successfully. Both grounded-history answers cited the correct owned stopped/23-second record; both empty-history answers acknowledged insufficient data. Educational wording varied, including an unnecessary refusal and general benefit phrasing in different repetitions. These are quality limitations; two repetitions cannot establish reliability or effectiveness.

All 12 approved calls were consumed. The underlying 24-call session retains unused capacity, but this evaluation has no further allowance. Routine and peer tests use mocks. Live failure handling was not exercised because no sampled call failed.

## Surprising finding and limitations

Evidence-backed surprise: rejecting unsafe retrieval does not necessarily require suppressing the entire response. `test_rejected_and_failed_retrieval_can_answer_without_history` verifies a general fallback while disclosing unavailable history; the rejected SQL never executes. The evaluation therefore checks non-execution, explicit uncertainty and absence of invented citations rather than expecting every rejected plan to produce no reply.

Physical mobile sleep/background timer throttling remains untested. Fake-clock tests prove planned 60/75-second sequences, and one real reframe run was observed completed within 65.854 seconds after Start, including observation overhead. Setup time was not instrumented and is not included in that figure. Do not claim every exercise has a measured wall-clock timing. Full browser save-outage/race coverage, exact narrow-screen/keyboard review, and live failure variation remain incomplete.

## Design and demonstration status

Option A top navigation is selected. Historical browser-editor work created 17 native text/vector Figma frames with sampled editability. It was not successful MCP capture, a wired prototype, or a verified Figma-to-Vue implementation. The static fallback is older evidence, not the latest design status. Exact viewport parity and instructor access are unverified; links and differences remain in [design notes](design-pipeline.md).

No demonstration or process screencast has been recorded in this evaluation. A reviewable recording should show: guest quiz → explained suggestion → separate Start/Stop → history ID; explicit remembered preferences; and a failure with its retained test/log evidence and resulting decision. For a process section, use the rejected-query fallback finding above without staging it as a newly observed live failure.

Explain generated `frontend/src/recommendation.js`: `decide` first validates the two finite input sets, derives a candidate only from explicit activity or consent to breathing, checks availability, rejects a breath-focus conflict, and returns either a reason plus approved exercise or a reason plus null. It never calls a model, starts a timer, saves a preference, or changes reviewed steps. The tests cover the input cross-product and fallback outcomes. Screen recording and student explanation are still required for the assignment demonstration deliverable.
