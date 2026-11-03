# Proposed live-model variation sample — November 2, 2026

Status: historical proposal, subsequently explicitly approved and executed. All 12 calls consumed; see [live results](live/comparison.md). The ledger values below are the pre-run inspection, not current usage. Existing mock evidence remains separate in evaluation.md.

Read-only ledger inspection (sqlite3 mode=ro, no initialize/migration/reset): data/app.sqlite3 session4078a5d0-8b28-4dc4-8aac-324d5dc16cc9 active, immutable cap24 calls/$1.20 local reservations,0 attempted/0 reserved.49 historical unassigned voice attempts and6 legacy text attempts retained. Isolated mock database has no live sessions/attempts. Valid configuration and credential presence confirmed without printing the credential; this does not establish provider availability. Existing local voice-enabled flag is true, whereas isolated test backend uses explicit mock Settings.

## Exact cases and fixed fixtures

Use only fictional fixture records. Each repetition uses a fresh conversation with the same fixture context so repetition1 cannot contaminate repetition2. Stable fixture record IDs must be recorded before execution. Do not expose existing personal transcripts to the provider.

| Case | Exact typed question | Setup | Repetitions | Max calls |
|---|---|---|---:|---:|
| L01 grounded history (S16) | What happened in my most recent saved exercise? Give its status and active duration. | Fictional owner with older completed breathing60000ms and newest stopped STOP23000ms; second owner's records excluded |2|4|
| L02 insufficient history (S17) | What happened in my most recent saved exercise? Give its status and active duration. | Fresh fictional owner with no exercise sessions |2|4|
| L03 general education | What is the difference between a grounding exercise and a breathing exercise? Explain briefly without recommending a treatment. | Fresh fictional owner with no sessions; approved skill context unchanged |2|4|

Budget: six typed attempts, up to two calls per attempt (SQL planning+answer), maximum12 provider calls. Transcription0, speech0, retries0. Failed attempts/timeouts count and are not refunded. A failed planning call can leave fewer than12 actual calls. Unused allowance is not used for replacement cases. Use the existing selected session and preserve its ledger; enforce an additional12-call run ceiling, within its24-call session cap and the assignment50-call maximum. Existing reservation system uses $0.05 per call, hence at most$0.60 local reservations; this is not a provider invoice guarantee. Approval is specific to this run, not permission to consume all remaining session allowance.

## Comparison and stopping rules

For each attempt retain case/repetition, exact input, provider/model, request ID, stage outcomes, ledger delta, retrieved record IDs and actual saved reply. Compare repetitions on: exact agreement with saved status/duration; no foreign/unsupported records or invented emotional effects; explicit insufficient-history disclosure; consistent core facts with permitted wording variation; no treatment/monitoring claims; accurate failed/saved status. L03 may answer general education without pretending history supplied those facts.

Check current model availability/configuration before the first paid attempt; report any blocker without spending on probes. Use bounded existing requests, no automatic retry, and never label a mock as live. Stop on exhausted allowance or unavailable configuration. New requests return to labeled mocks on exhaustion; an in-flight blocked live turn remains an honest failure. Compare failure handling with deterministic mock tests; do not deliberately purchase failures. If no natural failure occurs, live failure handling remains untested. Existing S15 combined browser failure/support check is not replaced by this sample.

Host approval required before live activation/calls. If declined or blocked, retain UNTESTED and the reason; no mock substitution. Clean-checkout/recordings/full clinical efficacy are outside this sample.
