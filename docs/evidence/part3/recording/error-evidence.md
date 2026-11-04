# Process evidence: recovering local access

Prepared from the project conversation and retained source/test evidence, November 3, 2026. This is a retrospective evidence summary, not an original error screenshot. No original screenshot or network trace was retained.

## 1. Actual reported failure

The user reported in this project conversation:

> why does it say that and wont let me on the pageLocal access is invalid or revoked.

This happened after the backend switched from the isolated mock database to the original live database. The browser still held a local identity from the earlier database. The user could not enter the app. The database switch and inspected startup code supported this diagnosis; no original token-level trace was retained.

## 2. Expected behavior

If the server rejects the saved browser identity, the application should return to a usable profile chooser. It should preserve saved records and let the user select a profile or guest. Temporary network failures should not clear valid access.

## 3. Evidence and decision

The previous startup in `frontend/src/ProfileGate.vue`, function `boot`, requested `/identity` whenever a browser token existed. When that failed, it displayed the error; Retry connection reused the same token.

The fix calls `restoreIdentity()` in `frontend/src/identityRecovery.js`. On HTTP401 only, it clears the browser's access reference and makes one request for a new chooser identity. It does not delete saved database records or replay a pending save. Other errors remain errors. The fix is included in published commit `bdf3f84`.

Actual generated code:

```javascript
export async function restoreIdentity(request, getAccess, clearAccess) {
  if (getAccess()?.access_token) {
    try { return await request('/identity'); }
    catch (error) {
      if (error.status !== 401) throw error;
      clearAccess();
    }
  }
  return request('/identity/bootstrap', 'POST', {
    bootstrap_id: crypto.randomUUID()
  });
}
```

Inputs: request function, current-access reader and access-clearing callback. Output: the restored identity or a new chooser identity; failures propagate. Safeguards: only401 clears access, bootstrap occurs at most once per attempt, and there are no record-deletion or provider calls. Limitation: this recovers browser access; it does not merge profiles across databases.

## 4. Retest evidence — MOCKED AUTOMATED TESTS

Retained output from `node --test frontend/tests/identityRecovery.test.js`:

```text
PASS revoked browser access is cleared once and returns a fresh chooser without replaying writes
PASS network and server failures preserve credentials and do not bootstrap
PASS valid identity is retained; failed bootstrap is not retried in a loop
3 tests passed; 0 failed
```

The text above summarizes the original output in [identity-retest.txt](identity-retest.txt). Tests use fictional credentials and mocked HTTP responses, with no paid AI calls. They verify the recovery behavior in code. They do not prove recovery in the original affected browser tab; that automated browser retest was unavailable. The user later reported that the error no longer appeared, which is user observation rather than a controlled reproduction.

## 5. Short narration

“During development, I could not enter the app because it said local access was invalid or revoked. This happened after switching databases. The expected behavior was to return me to the profile chooser. Inspecting the startup code showed that Retry kept using the same rejected session. The fix clears only rejected browser access and requests a fresh chooser, without deleting saved records. These three mocked regression tests passed. The original failure screenshot was not saved, so I am showing the recorded report and code/test evidence. The error no longer appears for me.”

## How to show this

Keep the finished-app video focused on the frontend. For the separate process recording, open this document and scroll through sections1–4 while reading the narration. If demonstrating the test run, open a terminal and run:

```sh
cd /Users/mallorypierz/mentalhealth_app
node --test frontend/tests/identityRecovery.test.js
```

Do not deliberately break the live app or create a screenshot pretending to be the historical error. Recordings remain pending.
