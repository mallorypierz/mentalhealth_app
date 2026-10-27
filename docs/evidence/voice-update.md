# Updated Part 2 evidence — October 27, 2026

This is a curated redacted summary, not a new live test or a raw conversation dump. No credentials, audio, private transcripts or runtime database are included.

| Evidence | Observation | Limits |
| --- | --- | --- |
| Original submission | [Record extract](part2-final-records.json) and [evidence index](README.md) retain measured breathing, persistence/replay/restart and failure evidence | Historical October22 UI, not latest voice layout |
| Live voice test | Agent supplied locally synthesized fictional question; actual transcription and RAG answer were saved. Speech initially failed validation, then an approved speech-only retry yielded browser Speaking → Playback finished and still exactly two messages | Synthetic input, not physical microphone; test profile was subsequently deleted by the student, so its rows are historical, not reproducible current rows |
| User feedback | Student reported a truncated spoken answer; code inspection found sound-onset interruption active during playback | Echo explanation was plausible, not confirmed from audio telemetry |
| Revised playback | Ignore microphone frames during loading/playback, retain explicit Stop speaking, resume input only in active visible session | Automated lifecycle checks; no agent physical-device claim |
| Student confirmation | October27: “the chatbot is all finished and verified i approve everything” | Explicit user verification of chatbot, not proof they ran all test commands or checked every device |
| Current automated verification |74 backend unittest tests;26 frontend Node tests; Vite production build passed | Provider calls mocked/intercepted; not model-quality or clinical validation |
| Final read-only runtime inspection |49 durable attempted stages:14 transcription,14 planning (one interrupted),10 answer,11 speech (one interrupted); total reservations$2.45 against approved cumulative$3.25/65-call ceiling | HTTP success does not prove usable audio or accurate answers. No raw content published. Counters may change with subsequent user activity |
| Source preservation | Part1e958bdcf and original Part2f133bf99 remain unchanged; pre-publication expansion HEAD6f995d4 | New voice work has no published commit yet |

Selected prompt → implementation → decision:

1. “Actual live AI chat” → real transcription, two-call RAG, speech adapter and durable reservations → retain typed input and saved text on audio failure.
2. “Rejected query” → explicit narrow SQL examples and fixed-category diagnostic logs → never execute invalid SQL; no raw query/value logging.
3. “Not just responses about the app” → approved educational wellbeing scope and unavailable-history fallback → general knowledge separated from personal-history claims, citations still checked.
4. “Only two words” → playback input gate → explicit manual interruption replaces unreliable automatic barge-in.
5. “Add everything ... onto Part2” → consolidated report, corrected current-state docs, new audit → publication/hash/link steps remain pending rather than invented.

[Design contracts](../design-pipeline.md), [verification](../verification.md), [AI disclosure](../../AI-USE.md), [updated report](../../report.md).
