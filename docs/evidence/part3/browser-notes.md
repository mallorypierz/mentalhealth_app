# Browser observations — November 2, 2026

Mock test origin http://127.0.0.1:5173, backend 8001. New guest used for S01/S02/S06/S10/S11/S12. No user data or provider calls.

S01: Find a suggestion → Skip quiz removed questions and left library available. No exercise started.
S02: breathing rhythm + Yes → Show suggestion displayed Paced breathing and actual-choice explanation. Continue was separate.
S06: Choose a different exercise → Open One-minute cognitive reframe displayed preview, with Start practice. It did not automatically start.
S10: clicked Start, observed first step, later second step at 31.283s, completed and Session saved at 65.854s after pre-click timestamp. No acceleration/pause; setup not separately timed. History displayed completed/60s and data-session-id 0ceca131-a343-4098-963c-73c78e1c5777. SQLite after snapshot matches.
S11: Practice again → Stop; observed 36 seconds and Session saved. SQLite exact active duration36427ms.
S12: Practice again; keyboard refresh shortcut did not reload, then supported reload API did. History showed interrupted/29s. SQLite29615ms. No duplicated session IDs.
S07: fresh tab selected Fictional Preference Alex. Quiz absent until Use saved answers; checked surroundings and Avoid values restored.
S03: Show suggestion then displayed grounding and “You chose Notice my surroundings. This activity does not focus on breathing.”

See browser-history.png and text snapshots. These are observations from this run; earlier verification entries retain their historical scope.
