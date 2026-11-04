# A little space — Part 3 coursework prototype

A local Vue/JavaScript frontend, Python/FastAPI backend, and SQLite application using fictional data. It is not therapy, diagnosis, monitoring, or a crisis service. Exercise timing, Stop, support, saving, and quiz rules are application-owned, not model-controlled.

## Current features

- Paced breathing: six 4/6 cycles, 60 seconds.
- Sensory grounding: five prompts, up to 75 seconds, with optional checkmarks and Next step; STOP: four prompts, 60 seconds; cognitive reframe: three prompts, 60 seconds. Student-reviewed coursework adaptations; elapsed completion does not establish effectiveness or participation.
- Optional two-question deterministic quiz shown one question at a time, explanations, skip/change/retake/reject, and explicit Start after preview.
- Local profiles and guests, saved sessions/history/calendar, typed/voice chat, scoped read-only SQL RAG.
- Profiles can explicitly remember, reuse, change, and forget quiz answers in Exercises. Guests cannot persist quiz answers. Current explicit answers take priority; history is shown separately and does not rank suggestions. Still-cue display choice remains temporary.

## Clean setup (repository root)

Use Python 3.12 and Node 24/npm11 to match the development environment. Check `python3 --version`, `node --version`, and `npm --version` first. Network access to PyPI/npm is needed for installation. Coding agents must obtain installation approval under AGENTS.md.

```sh
python3 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements.txt
npm --prefix frontend ci
```

Do not copy an existing environment, node_modules, database, or private .env into a clean checkout. No credentials or .env are required for the default mock app. Backend requirements are pinned; npm ci uses frontend/package-lock.json.

## Start in mock mode without credentials

On a new checkout with no backend/.env, run in two terminals from the root:

```sh
backend/.venv/bin/python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

```sh
npm --prefix frontend run dev -- --port 5173 --strictPort
```

Open [the local app](http://127.0.0.1:5173/). Use this exact origin consistently; origin protection permits the documented frontend port. Vite proxies /api to8000. Check [API health](http://127.0.0.1:8000/api/health): provider must be mock and voice_enabled false for routine/peer testing. Health does not make a model call. Stop servers with Ctrl+C. If a port is occupied, stop your earlier test server rather than disabling origin protection.

Startup creates data/app.sqlite3 relative to the project, independent of terminal location, and applies idempotent migrations. Existing checkout users should back up their database before upgrading. Do not reseed or delete records at startup. Use one backend worker; restart marks abandoned pending requests interrupted without automatically retrying them.

## Try and verify

1. Continue as guest. Open Exercises; skip the quiz or answer it. A suggestion opens a preview; Start is separate.
2. Start an exercise. Pause/Stop and Crisis support remain application controls. Opening support pauses practice; closing does not resume it.
3. Check Session history for the exercise name, duration, and status. Completed sessions appear in Calendar; stopped/interrupted sessions remain in history.
4. Start another exercise, wait for a checkpoint, then refresh. Recovery should retain the last confirmed checkpoint as interrupted. Retry an uncertain save explicitly.
5. Create/select a fictional profile. In Exercises, choose answers, check Remember, and Save preferences. Refresh/reselect, then Use saved answers. Forget removes remembered answers; it does not erase current unsaved choices.
6. Stop/restart both services; verify saved records still appear. Local chooser profiles are not secure authentication.

```sh
backend/.venv/bin/python -m unittest discover -s backend/tests -q
npm --prefix frontend test
npm --prefix frontend run build
git diff --check
```

Run the retained mock evaluation with `sh docs/evidence/part3/run_checks.sh`. It records test/build output; browser scenarios require the steps and observed evidence in the [evaluation guide](docs/evidence/part3/README.md). Unit/API tests do not replace browser verification.

## Configuration and paid calls

Only the backend reads ignored backend/.env; backend/.env.example contains variable names and dummy values. Never overwrite an existing .env, expose keys in Vue, or assume an older checkout is in mock mode. Configuration loads at process startup and changes require restart. The public health endpoint reports configuration presence, not secret values or proof of provider success.

Peer testing defaults to mocks. Live testing requires a host-approved session allowance, explicit session selection and activation. Each session has a maximum50 calls; planning, answering, transcription, speech, failed attempts, and retries count. No ledger resets or automatic replenishment. New requests use labeled mocks when allowance is unavailable/exhausted; a blocked in-flight live turn reports failure honestly. Local monetary reservations are not invoice guarantees. Do not run the one-off live evaluation script as a routine test.

## Architecture and files

| Location | Responsibility |
|---|---|
| frontend/src | Vue views, quiz decisions, local exercise timer, API calls, recovery journal |
| backend/app/api, controllers, schemas | HTTP validation and request coordination |
| backend/app/repositories, preferences.py, db.py, migrations | Application-owned SQLite reads/writes and persistence contracts |
| backend/app/rag, providers, context | Validated read-only scoped retrieval and bounded mock/live generation |
| data | Ignored runtime SQLite and backups; backend access only |
| docs/design-pipeline.md | Contracts, approved skill sources, design rationale and Figma links |
| docs/verification.md, docs/evidence/part3 | Actual checks, limits, mock/live evaluation evidence |
| handoffs/current.md, AI-USE.md, prompts | Current work state and AI-use disclosure |

## Design and evidence status

Selected Figma alternative: Option A, top navigation. Historical browser-editor work created17 native text/vector frames with sampled editability checks. It was not a successful MCP capture, wired prototype, or verified Figma-to-Vue implementation. Exact viewport matching and instructor access remain unverified. The static PNG/SVG fallback is historical; it does not supersede the later editable browser-created references. See [design notes](docs/design-pipeline.md) for links and differences (including calendar event list versus design grid).

Source revision, clean-install outcomes and unresolved checks are recorded in [clean-checkout evidence](docs/evidence/part3/clean-checkout.md). The new Part3 features remain uncommitted in the working repository until separately checkpointed; a historical published commit does not contain them. See [Part3 evaluation](docs/part3-evaluation.md) for scenario results, changes from the initial rationale, live variation and remaining limitations. Recordings and course submission are not claimed complete.

## Final submission audit

Revision `c6d8377ce4782abd5e3467e78e03eddf25e74d6b` was reproduced in a fresh isolated checkout on November 3: 83 backend tests, 37 frontend tests and build passed. Mock browser checks covered startup, quiz, preferences, exercise/history, refresh, restart and failure recovery. See [audit evidence](docs/evidence/part3/final-audit/results.md). Later audit changes are documentation/evidence only.
