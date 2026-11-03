# Part 3.3 scenario results

17 passed within the stated evidence scope; S15 combined browser check not-run. Mock-only. Automated cases are not browser passes. Expected results were recorded before execution. See README.md for setup, commands and three explicit behavior checks.

## S01 — First-time guest skips quiz

- Setup/input: New fictional guest; choose Find a suggestion then Skip quiz
- Expected: Library remains usable; no exercise starts or saves.
- Observed: Browser: new guest opened quiz, skipped, returned to available library; no Start invoked.
- Mode: mock; status: **pass**
- Evidence: [browser-notes.md](browser-notes.md)

## S02 — Quiz suggests breathing

- Setup/input: Choose breathing rhythm + Yes
- Expected: Breathing suggestion explains the chosen activity; preview requires Start.
- Observed: Browser: breathing + Yes showed breathing and “You chose Follow a breathing rhythm”; separate Continue action. Mapping cross-product passed.
- Mode: mock; status: **pass**
- Evidence: [browser-notes.md](browser-notes.md)

## S03 — Quiz suggests alternative

- Setup/input: Choose surroundings + Avoid
- Expected: Grounding suggested; instructions unchanged.
- Observed: Browser: restored surroundings/Avoid produced grounding and explained non-breath-focus. Mapping test passed.
- Mode: mock; status: **pass**
- Evidence: [browser-notes.md](browser-notes.md)

## S04 — Breath activity uncomfortable

- Setup/input: Choose STOP + Avoid
- Expected: No breath-focused suggestion; conflict explained and alternatives available.
- Observed: Automated decision cross-product: STOP/breathing with Avoid or Not sure returns conflict and no suggestion. Browser conflict screen not separately replayed.
- Mode: mock; status: **pass**
- Evidence: [frontend-output.txt](frontend-output.txt)

## S05 — No clear preference

- Setup/input: Select No preference for both answers
- Expected: No ranked winner; choice list remains available.
- Observed: Automated skips/neutral cases return no exercise; no arbitrary tie-breaker. Browser no-preference case not separately replayed.
- Mode: mock; status: **pass**
- Evidence: [frontend-output.txt](frontend-output.txt)

## S06 — Reject suggestion

- Setup/input: Reject breathing suggestion; manually open reframe
- Expected: Reframe preview opens without automatic start.
- Observed: Browser: rejected breathing recommendation, opened reframe preview; Start still required.
- Mode: mock; status: **pass**
- Evidence: [browser-notes.md](browser-notes.md)

## S07 — Load remembered preferences

- Setup/input: Fictional profile saves surroundings/Avoid; reload and Use saved answers
- Expected: Saved values restored only by explicit action.
- Observed: Browser fresh profile selection and explicit Use saved answers restored surroundings/Avoid.
- Mode: mock; status: **pass**
- Evidence: [browser-preferences.txt](browser-preferences.txt)

## S08 — Change or forget preferences

- Setup/input: Change saved answers then Forget; replay older save
- Expected: Answers cleared; old retry cannot resurrect them.
- Observed: Automated test_preferences_isolation_retry_forget_restart saved then forgot; replay of original save left answers null.
- Mode: mock; status: **pass**
- Evidence: [backend-output.txt](backend-output.txt)

## S09 — Profile isolation

- Setup/input: Fictional A has records; switch/read as Fictional B
- Expected: B cannot read A preferences/activity; stale requests rejected.
- Observed: Automated preferences/identity/calendar/voice tests enforce owner scope and stale context; unrelated profile has no preference answers.
- Mode: mock; status: **pass**
- Evidence: [backend-output.txt](backend-output.txt)

## S10 — Completed exercise history

- Setup/input: Run a guided sequence to completion
- Expected: Correct exercise ID, completed status and duration saved once and displayed.
- Observed: Browser reframe completed and saved; Vue history data-session-id 0ceca131-a343-4098-963c-73c78e1c5777 matches SQLite completed/60000. Start-to-observed completion upper bound 65854ms; setup not timed.
- Mode: mock; status: **pass**
- Evidence: [browser-history.txt](browser-history.txt)

## S11 — Stop partway

- Setup/input: Start STOP, then Stop
- Expected: Stopped status and actual active duration saved, not completed.
- Observed: Browser reframe stopped/36427ms (Vue floors to 36s); new ID f5d08ef6-bab3-4896-a562-c2f7cb38a0ba. Automated alternatives test also covers STOP stop.
- Mode: mock; status: **pass**
- Evidence: [database-after.json](database-after.json)

## S12 — Refresh interrupts

- Setup/input: Refresh an unfinished practice after a checkpoint
- Expected: Recovered interrupted record uses last confirmed checkpoint; no duplicates.
- Observed: Browser reload recovered interrupted/29615ms, ID 47b8c6b8-eadf-4c69-ac19-ea93d6b03f9e; Vue shows 29s. Outbox test confirms last confirmed checkpoint and no duplicate recovery.
- Mode: mock; status: **pass**
- Evidence: [browser-history.txt](browser-history.txt)

## S13 — Failed save retry

- Setup/input: Inject receipt failure or lose commit response; retry same operation
- Expected: Honest failed/unknown state; rollback or idempotent replay; one record.
- Observed: Mocked receipt failure rolled back; retry saved one preference row. Outbox lost-response test replayed same operation without duplication.
- Mode: mock; status: **pass**
- Evidence: [backend-output.txt](backend-output.txt)

## S14 — Delayed response

- Setup/input: Resolve request after switching identity or leaving screen
- Expected: Old response ignored; new identity/view unaffected.
- Observed: Frontend late preference response rejected after identity change; LatestRequest and voice tests ignore cancelled/replaced responses.
- Mode: mock; status: **pass**
- Evidence: [frontend-output.txt](frontend-output.txt)

## S15 — Model failure and support

- Setup/input: Inject failed provider request; open support
- Expected: No invented reply; support independently accessible.
- Observed: Provider-failure automated checks passed, but support access in the same failed-model browser state was not executed in this evaluation. Combined case not-run; do not infer pass from separate checks.
- Mode: mock; status: **not-run**
- Evidence: [backend-output.txt](backend-output.txt)

## S16 — Scoped history RAG

- Setup/input: Ask fictional latest-practice question with two owners
- Expected: Only active owner records retrieved; actual answer grounded in IDs.
- Observed: RAG tests returned owned stopped/23s record with matching source/citation IDs, denied foreign owner, and scoped guest among two profiles.
- Mode: mock; status: **pass**
- Evidence: [backend-output.txt](backend-output.txt)

## S17 — Empty retrieval

- Setup/input: Ask history question with no saved matches
- Expected: Empty outcome and insufficient-history reply; no invented records.
- Observed: test_empty_is_distinct_from_rejection returned empty and no matching saved records reply, with no citations.
- Mode: mock; status: **pass**
- Evidence: [backend-output.txt](backend-output.txt)

## S18 — Untrusted write query

- Setup/input: Mock planner proposes DELETE FROM exercise_sessions
- Expected: Rejected before execution; stored rows unchanged; rejection distinguishable.
- Observed: Parser rejects write structures; pipeline rejected-query test asserts retrieval never called; read-only authorizer denies DELETE; fixture remains readable.
- Mode: mock; status: **pass**
- Evidence: [backend-output.txt](backend-output.txt)

## Findings and limits

Surprising finding: rejected retrieval can still yield a general answer with unavailable history disclosed. The invariant is no execution of the rejected query and no invented retrieved evidence, rather than requiring every rejection to suppress all replies (test_rejected_and_failed_retrieval_can_answer_without_history).

Untested limitation: real device sleep and timer throttling on physical mobile hardware. No live calls or clean installation were part of this original mock run. Subsequent [live results](live/comparison.md) and [clean-checkout checks](clean-checkout.md) are separate evidence; recordings remain unfinished. Reframe timing only was observed this run; setup was not instrumented. Full Part 3.3 completion is not claimed.
