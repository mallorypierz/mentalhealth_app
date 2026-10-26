# Current handoff — October 26, 2026

## Milestone and authorization

Branch `codex/profiles-calendar`. User explicitly approved committing and pushing the current expansion and updating necessary documents. No merge, deployment or course-site upload is authorized. The submitted Part 2 report.md remains unchanged: report commit `f133bf99804246fe4fa34f090db37b196abf69c8`, source/evidence `080ad6393a2ade204f6f2b417b422a5778a8ed4c`; Part 1 `e958bdcf11e69b5c4451f986742989acd01b497e`.

## Implemented and preserved

Local profiles with required display name, optional age/gender; direct guest access; explicit transfer/discard/leave/delete; pause-before-switch and retry safeguards. Tokens resolve activity ownership on the backend, but the shared chooser is not secure authentication. Guest activity survives refresh/navigation; tab closure is not guaranteed deletion. Legacy records remain under their original owner. Calendar derives completed events at completion time in the device timezone; stopped/interrupted records remain history only.

Exercise library opens existing paced breathing and lists three unavailable Coming later skills. No therapeutic instructions or fabricated activity added. Six-cycle 4/6 sequence, pause/Stop/still cue/recovery and static support remain application-controlled. Responsive shared styles and sticky support/active Stop are implemented; navigation wraps rather than matching the draft bottom bar. Chooser label is Create a profile. Chat is forced to mock for the profile-enabled runtime; preserve existing .env and the exhausted historical live-call ledger.

## Evidence and limitations

See docs/verification.md for dated evidence. 49 backend tests, 10 frontend tests and build passed. Historical browser/API/SQLite calendar checks covered multiple completions, empty states, timezone rendering, refresh/restart and profile isolation. New browser guest run completed/saved within a conservative 72.082 seconds of guest entry; setup upper bound 3.770 seconds; no pauses/support time excluded. Library navigation returned to practice without auto-start.

Browser access resumed after the user manually reopened the app; previous policy block is historical. Full fresh phone/landscape/zoom/keyboard/failure checks and final Figma comparison remain incomplete. Figma MCP quota blocked fresh inspection. Physical-device, screen-reader and exhaustive storage/multi-tab failure checks are not claimed. Source-review and automated mocks must not be described as full visual evidence.

The runtime database and pre-migration backup are ignored. Original legacy rows were previously compared with that backup and preserved; no reassignment to a new person. Temporary screenshots under /tmp are review artifacts, not committed evidence. Inspect running processes before relying on local server availability.

## Next work

Review docs/later-milestone-report.md and finish remaining browser/design checks. Propose smallest fixes for approval before editing source. This is a later milestone, not a replacement Part 2 submission. Publication results are recorded below after Git verification.

## Publication verification — October 26, 2026

User explicitly approved commit/push and documentation updates. Source/tests/documentation commit [e593a522b7a1b0718e1a19987ac133e66cfbc36b](https://github.com/mallorypierz/mentalhealth_app/commit/e593a522b7a1b0718e1a19987ac133e66cfbc36b) was pushed to codex/profiles-calendar; git ls-remote returned the identical hash. Remote codex/part2 remained f133bf99804246fe4fa34f090db37b196abf69c8 and part1-submission remained e958bdcf11e69b5c4451f986742989acd01b497e. Submitted report.md was unchanged.

Immediately before publication: backend unittest49 passed, frontend tests10 passed, production build passed, diff whitespace checks clean. Existing Starlette/httpx deprecation warning remains. Credentials, runtime SQLite and backups were excluded. Initial staging approval review could not run due to a usage limit; after the user's renewed request, the same approval process succeeded. This did not require bypassing controls. No merge, deployment, live-model call or course upload occurred. This documentation-only follow-up records the verified source commit; remaining verification limitations are unchanged.
