# A little space — Assignment 3 Part 2

A localhost coursework prototype for one skill: six cycles of four seconds in and six seconds out. A fictional student can start without typing, pause, stop, use a still cue, and review saved practice. Optional chat explains permitted saved history. This is not therapy, diagnosis, monitoring, or a service to rely on during distress. Tests use fictional scenarios only.

**Current:** Vue → FastAPI → SQLite, persistent sessions/conversations, bounded two-call SQL RAG, and independent crisis-support information. Chat currently uses clearly labeled **mock replies**. A prior live OpenAI example is separately documented; configuration alone is not evidence of a successful call. See [Part 2 report](report.md), [verification](docs/verification.md), and [evidence](docs/evidence/README.md).

**Submission:** the student reviewed and approved commit/push. The source/evidence milestone `080ad6393a2ade204f6f2b417b422a5778a8ed4c` is pushed on `codex/part2`; the finalized report follows as a documentation-only update. Course-site upload remains the student’s action. Part 1 remains at [part1-submission](https://github.com/mallorypierz/mentalhealth_app/tree/part1-submission), report commit `e958bdcf11e69b5c4451f986742989acd01b497e`. Do not label that Part 1 hash as the Part 2 submission.

## Run locally

Verified installed environment: Python 3.12.5, SQLite 3.45.3, Node 24.20.0, npm 11.19.0, Vue 3.5.44, Vite 7.3.7, FastAPI 0.158.1, Uvicorn 0.54.0, HTTPX 0.28.1. Dependencies are declared in `backend/requirements.txt` and `frontend/package-lock.json`.

From the repository root, initial setup on a new checkout:

```sh
python3 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements.txt
npm --prefix frontend ci
```

Use Python 3.12 and Node 24 to match the verified environment. These clean-checkout reinstall commands have not been independently reproduced; installed-environment imports/tests/build and server commands were verified. Do not replace an existing environment or install packages in an agent session without the required approval.

Run in two terminals:

```sh
backend/.venv/bin/python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

```sh
npm --prefix frontend run dev -- --port 5173
```

Open http://127.0.0.1:5173/ consistently. Vite proxies `/api` to port 8000. Stop each server with Ctrl+C. Use one Uvicorn worker: startup marks abandoned pending chat requests interrupted instead of silently retrying them. SQLite initializes at project-relative `data/app.sqlite3`; startup preserves activity records. Local browser recovery metadata is origin-specific, so `localhost` and `127.0.0.1` are different for recovery.

## Configuration and data

With no `backend/.env`, the backend defaults to mock. If an existing file selects another provider, inspect its nonsecret provider choice locally; do not overwrite it. `backend/.env.example` documents the settings. Configuration is explicitly loaded at startup; changes require backend restart. Keep keys only in ignored `backend/.env`, never in Vue, Git, logs or screenshots. Do not paste keys into chat.

The current local file selects mock. The historical live configuration used OpenAI `gpt-5.4-mini-2026-03-17` with a six-attempt ceiling. All six attempts have been consumed; failed attempts and both RAG stages count. No budget increase or further live calls is authorized. A durable SQLite ledger enforces the cap. Do not reset the database to evade it.

Practice runs without the API/model. Saves are asynchronous and honestly show pending/saved/failed states with retry. Five-second checkpoints support same-origin recovery to interrupted after refresh/closure; only confirmed saved duration is retained. Cleared browser storage, another browser, and legacy ownerless records cannot be automatically recovered. Display choice is temporary; preference persistence is unfinished.

## Files and responsibilities

| Path | Responsibility |
| --- | --- |
| `frontend/src/App.vue`, `exercise.js` | Views, six-cycle pacing, controls, fullscreen and independent support |
| `frontend/src/sessionPersistence.js`, `api.js` | Browser recovery journal and HTTP/JSON requests |
| `frontend/src/components/ChatView.vue` | Optional chat, request states and saved conversation history |
| `backend/app/main.py`, `api/`, `controllers/` | Validation, routes and generation coordination |
| `backend/app/repositories/`, `db.py`, `migrations/` | Parameterized transactions, relationships and SQLite initialization |
| `backend/app/rag/`, `providers/`, `context/` | Validated read-only retrieval and mock/live generation |
| `data/` | Ignored runtime database; no private or clinical datasets |
| `docs/`, `handoffs/current.md`, `AI-USE.md` | Contracts, evidence, current state and disclosure |

Only backend code opens SQLite and contacts the provider. The model cannot control timing, saving, exits or support.

## Checks

```sh
backend/.venv/bin/python -m unittest discover -s backend/tests -q
npm --prefix frontend test
npm --prefix frontend run build
git diff --check
```

Final preparation: 35 backend and 10 frontend tests passed; production build passed. Browser/API/SQLite verification includes a completed practice, stopped practice, mock history answer, exact replay without duplication, refresh and backend restart. Full details and historical failure/live evidence are in [verification](docs/verification.md).

## Remaining work

Explicit remembered/forgotten preferences, editable Figma capture/selected-frame round trip, the proposed normal-view persistent support/Stop bar and navigation refinement remain unfinished. Fullscreen has a sticky support header; normal-view support can scroll out of the viewport. No clinical effectiveness, comprehensive accessibility audit, physical-mobile fullscreen verification, full Part 3 evaluation, clean-checkout reproduction or screencast is claimed. No questionnaires, click-based emotional inference, extra skills, datasets, deployment or multi-user authentication were added.
