# Part 3.3 repeatable evaluation

Date: November 2, 2026 (America/New_York). Branch codex/exercise-quiz, base 016d251 plus uncommitted implementation. All fictional, mock-only; no paid model calls. Expected results were written to scenarios.json before execution. JSON is the canonical matrix; evaluation.md is its readable rendering.

From project root, run `sh docs/evidence/part3/run_checks.sh` with existing project dependencies. It runs temporary-database backend tests, deterministic frontend tests and build, and saves logs here. It does not update scenario statuses automatically or pretend automated tests operate Vue. Inspect named tests and browser procedures before updating observations. Application source was not edited for this evaluation.

Browser setup: isolated backend factory `create_app(Path('/tmp/mentalhealth-part3-check/fictional.sqlite3'), settings=Settings(), enable_profiles=True)` on 8001; frontend on allowed origin http://127.0.0.1:5173 with a temporary Vite config proxying /api to 8001. Do not use ordinary backend startup with private .env for this evaluation. Use a fresh guest for quiz scenarios; use Fictional Preference Alex for remembered preferences. Do not reset production records or provider ledgers. Database inspection uses Python sqlite3 URI mode=ro. Before/after snapshots contain only fictional test records and omit tokens.

Browser procedures: S01–06 use Exercises → Find a suggestion, the stated answers, Show suggestion, Skip/Change/Choose another controls. Check that preview requires Start. S07–09 use explicit save/reuse/forget and separate fictional profiles. S10–12 use real, unaccelerated practice, history, and refresh after a checkpoint. S13–18 use the named deterministic failure/scoping tests; a browser support check alone cannot prove support during provider failure.

Behavior checks: B1 suggestions respect explicit choices and never automatically start (mapping tests plus browser preview); B2 retries preserve one record and true save status (repository/outbox tests); B3 private history remains scoped and untrusted SQL never executes (RAG/identity tests). B4 independent support after a model failure requires combined browser evidence and remains unverified unless S15 records it.

Live variation is not evaluated here. A later explicitly approved small live sample is required for that assignment element, within host session cap <=50 calls. Clinical effectiveness, physical devices, and full accessibility are not established by this evaluation.
