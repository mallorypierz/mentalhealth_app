# A little space — updated Assignment 3 Part 2

Localhost coursework prototype using Vue, FastAPI and SQLite. Available skill: six cycles of4-second inhalation and6-second exhalation. Profiles/guest access, saved session history, a completed-session calendar, names-only exercise library and optional live voice/typed chat extend the original Part2 milestone. This is not therapy, diagnosis, monitoring or a crisis service. Use fictional scenarios for testing.

**October27 status:** student explicitly states the chatbot is finished and verified and approves the completed work for updated Part2 documentation. Voice source/evidence is published at [1b7b834](https://github.com/mallorypierz/mentalhealth_app/commit/1b7b834978c78051655bb25e273ff58101e3e4a7). The updated [report](report.md) pins verified evidence links; the Figma gap remains disclosed. This confirmation does not imply the student ran every automated or physical-device check.

**Preserved history:** original Part2 [source080ad63](https://github.com/mallorypierz/mentalhealth_app/commit/080ad6393a2ade204f6f2b417b422a5778a8ed4c), [reportf133bf9](https://github.com/mallorypierz/mentalhealth_app/blob/f133bf99804246fe4fa34f090db37b196abf69c8/report.md), and [Part1 report](https://github.com/mallorypierz/mentalhealth_app/blob/e958bdcf11e69b5c4451f986742989acd01b497e/report.md). Working branch: `codex/profiles-calendar`; prior published profiles/calendar sourcee593a52, prior documentation HEAD6f995d4. No submitted commit was rewritten.

Voice chat replaces Optional chat in the same tab. Explicit Start requests microphone permission; silence submits a turn, with typed input always available. Text is saved before speech generation. Microphone frames are ignored during playback; Stop speaking is explicit, then listening can resume within the active session. Hiding/leaving/support/profile changes stop capture; it never silently restarts. General educational wellbeing discussion is allowed; personal-history claims require scoped evidence. This is turn-based speech processing with gaps, not a duplex realtime model.

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

Configuration is explicitly loaded from ignored `backend/.env` at startup. Without approved live configuration the profile-enabled app uses labeled mocks. The current local demo has live voice enabled; the template keeps it disabled. Keys stay on the backend. Never overwrite an existing environment file or paste credentials into chat.

Live voice uses `gpt-4o-mini-transcribe`, two `gpt-5.4-mini-2026-03-17` RAG calls and `gpt-4o-mini-tts` with voice `marin`. Speech model deprecation was disclosed and retained by the student for the short demo. Each attempted stage reserves $0.05 locally, including failures; reservations are not an actual invoice. The historical six-call ledger is separate from the voice ledger. Current explicitly approved cumulative ceilings are65 calls/$3.25 reservations; default startup settings remain20/$1. Do not reset ledgers or automatically replenish allowances. Exact restart command for the approved local demo:

```sh
backend/.venv/bin/python -c 'from dataclasses import replace; from backend.app.config import load; from backend.app.main import create_app; import uvicorn; uvicorn.run(create_app(settings=replace(load(),voice_call_limit=65,voice_budget_microdollars=3250000),enable_profiles=True),host="127.0.0.1",port=8000)'
```

For coursework peer testing, use mocks by default. The assignment permits no more than50 live model calls per peer-testing session; the cumulative demo ceiling above is not a per-session implementation of that requirement. No live peer-testing session is claimed.

Once entered, the exercise timer runs without awaiting the API/model. Initial identity bootstrap and profile/guest selection require the backend; the chooser still exposes static support. Saves are asynchronous and honestly show pending/saved/failed states with retry. Five-second checkpoints support same-origin recovery to interrupted after refresh/closure; only confirmed saved duration is retained. Cleared browser storage, another browser, and legacy ownerless records cannot be automatically recovered. Display choice is temporary; preference persistence is unfinished.

## Files and responsibilities

| Path | Responsibility |
| --- | --- |
| `frontend/src/App.vue`, `exercise.js` | Views, six-cycle pacing, controls, fullscreen and independent support |
| `frontend/src/sessionPersistence.js`, `api.js` | Browser recovery journal and HTTP/JSON requests |
| `frontend/src/ProfileGate.vue`, `identityAccess.js`, `components/ProfileView.vue` | Local chooser, identity state and approved profile fields |
| `frontend/src/components/CalendarView.vue`, `ExerciseLibrary.vue` | Saved completion events and unavailable skill placeholders |
| `backend/app/identity.py`, `api/identities.py`, `repositories/identities.py`, `calendar.py` | Identity validation, transactions, ownership and read-only calendar projection |
| `frontend/src/components/ChatView.vue` | Voice chat, typed alternative, playback and saved conversation history |
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

Current checks and dated historical evidence are recorded in [verification](docs/verification.md). A fresh browser guest run completed and showed saved within a conservative 72.082 seconds of guest entry, including setup and observation delays (entry/setup upper bound 3.770 seconds). Browser/API/SQLite verification includes a completed practice, stopped practice, mock history answer, exact replay without duplication, refresh and backend restart. Full details and historical failure/live evidence are in [verification](docs/verification.md).

## Remaining work

Full fresh phone/landscape/zoom/keyboard/failure checks, final Figma editability and viewport comparison, explicit preference remembering/forgetting, and clean-checkout reproduction remain unfinished. The normal-view support/active Stop header is now sticky in source; comprehensive failure-state reachability is not verified. Navigation wraps in document flow rather than matching the selected draft's bottom bar.

Paced breathing (4–6) is the only usable skill. 5-4-3-2-1 sensory grounding, STOP and One-minute cognitive reframe are noninteractive Coming later placeholders. No clinical effectiveness, complete accessibility audit, physical-device validation, native app, PWA, real authentication, deployment or full Part 3 evaluation is claimed.
