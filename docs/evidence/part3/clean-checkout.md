> Subsequent grounding Next/checkmark changes also postdate this candidate; see current verification notes for the updated timing/save contract.

> Later change: November 3 quiz presentation refinement modifies ExerciseLibrary.vue and recommendation.js after this test. The source comparison below describes the earlier verification only. See current verification notes for frontend/browser checks of the new UI.

# Clean-checkout verification — November 3, 2026

**Passed within the scope below.** Agent followed README commands in `/tmp/mentalhealth-part3-clean`. This is a reproducibility check, not an independent human peer test. No credentials, working database, installed environments or node_modules were copied.

## Exact source

Tested local candidate commit **b3d8087c3e16e16d880c8a6230e5d43976ac4d6c**. An isolated source-only snapshot of root base `016d251a957870f9196de4a9b96e705801c644d5` plus its existing uncommitted changes was committed in `/tmp/mentalhealth-part3-candidate`, then cloned with `git clone --no-hardlinks /tmp/mentalhealth-part3-candidate /tmp/mentalhealth-part3-clean`. Root branch remains `codex/exercise-quiz`; no root commit/push occurred. This candidate is local, not a published revision another person can yet fetch remotely.

The tested commit includes the revised README and application/tests, but only an in-progress clean-checkout evidence page. Final Part 3 evaluation, this completed evidence, latest disclosure/handoff/verification changes and new browser/log artifacts were written afterward and are **not in the tested commit**. [Source comparison](clean-source-check.json) confirms all candidate frontend/backend files are byte-identical to the working application after testing. No application corrections were needed.

## CHECK → TAKE ACTION → VERIFY

Host explicitly approved these installations in this directory only:

```sh
python3 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements.txt
npm --prefix frontend ci
```

Python 3.12.5, Node 24.20.0, npm 11.19.0. Declared Python pins and npm lock tree installed successfully. Pip reused downloaded wheel cache; installed dependency folders were newly created, not copied. This was not a cold-network-cache test. npm reported 35 packages added, 36 audited, zero vulnerabilities; install-script policy notice did not prevent the verified build. `backend/.venv/bin/python -m pip check` reported no broken requirements. Existing Starlette/httpx deprecation warning remains; no unapproved replacement dependency was installed.

README startup commands, from the clean root:

```sh
backend/.venv/bin/python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
npm --prefix frontend run dev -- --port 5173 --strictPort
```

Sandbox initially prevented binding localhost; elevated execution succeeded without application/configuration changes. Default startup created fresh `data/app.sqlite3`; `backend/.env` is absent. Proxied GET `http://127.0.0.1:5173/api/health` returned provider=mock, voice_enabled=false, testing_session=not_selected and zero live calls. No provider credentials were needed.

| Check | Expected | Observed / evidence |
|---|---|---|
| Fresh entry and connection | Guest available without credentials | Browser showed no saved profiles, entered guest, loaded library through API |
| Quiz | Actual choices explain an available suggestion; no automatic Start | Thought from another angle + avoid breath focus suggested reframe with explanation, then separate preview/Start |
| Exercise | Approved sequence completes and saves accurately | Three-step reframe completed; UI showed saved, 60 seconds, completed. No new wall-clock bound claimed |
| Database | Backend persists one matching record | Read-only SQLite ID `7a52c388-0797-414b-b75d-d3a9c06a2ba9`, cognitive_reframe/completed/60000; integrity ok, no FK violations |
| Refresh and both service restarts | Same record, no duplication | Stopped/restarted both README commands; reloaded same browser guest; history DOM data-session-id matched same ID, 60s Completed; before/after SQLite snapshots each contain exactly one session |
| Backend checks | Pass in new environment | 82 passed in 17.016s, [log](clean-backend-output.txt) |
| Frontend checks | Pass | 33 passed, [log](clean-frontend-output.txt) |
| Build | Pass | Vite production build passed, [log](clean-build-output.txt) |
| Checkout cleanliness | No tracked generated files | `git status --short` empty; runtime directories ignored |

Commands: `backend/.venv/bin/python -m unittest discover -s backend/tests -q`, `npm --prefix frontend test`, `npm --prefix frontend run build`, `git diff --check`. Browser evidence: [before](clean-browser-before.txt), [after](clean-browser-after.txt), [screenshot](clean-history.png). Database evidence: [before](clean-database-before.json), [after](clean-database-after.json).

Refresh interruption, failed-save replay and remembered-profile behavior retain the separately scoped original evaluation/automated evidence; they were not all repeated manually in this clean guest. No real peer, physical-device check or recording was performed. Publishing a reviewed source checkpoint remains necessary before claiming remote clean-checkout availability.
