# Live sample results — November 2, 2026

Host approved12 calls. Six typed trials used exactly12 calls, planning+answer for each. No transcription, speech, retry or failed attempt. All replies saved through the normal conversation controller/repository in fresh fictional databases; production ledger reserved12 calls/$0.60, retaining historical entries. The evaluation's12-call ceiling is exhausted; no more calls authorized. The underlying24-call session is not itself exhausted. The isolated peer-test server remains mock. API model snapshot gpt-5.4-mini-2026-03-17 was checked against https://developers.openai.com/api/docs/models/gpt-5.4-mini before execution.

See results.json for exact questions, replies, record IDs, outcomes and per-attempt calls. Fixture semantics match across repetitions, but UUIDs differ because each repetition uses a fresh database/conversation. A test-only ledger adapter routes reservations to the existing approved session while keeping fictional messages in isolated databases; no private transcript is copied.

| Case | Grounding / unsupported claims | Variation | Outcome |
|---|---|---|---|
| L01 latest history, twice | Both cite exactly their expected owned STOP record, stopped/23000ms; foreign-owner later record excluded. Neither infers improvement. | Wording varies, core facts identical. |2/2 saved, records retrieved |
| L02 empty history, twice | Both acknowledge no verifiable saved session; no invented duration/status/citations. | One adds an offer to explain/start; the other is shorter. |2/2 saved, empty retrieval |
| L03 general education, twice | Neither invents personal history or cites nonexistent records. Both distinguish senses/present attention from breath focus. | One says breathing may help the body settle (general benefit phrasing, not evidenced by stored data); the other adds an unnecessary treatment-plan refusal and simplifies grounding to external awareness. These are quality limitations, not proof of efficacy. |2/2 saved, empty retrieval |

No failure occurred in this small live sample: live timeout/refusal/save-failure variation is UNTESTED. Mock failure tests remain separate. Two repetitions are descriptive evidence, not a reliability estimate. No clinical assessment or effectiveness conclusion follows.
