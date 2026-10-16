# Part 1 flow — initial design

**Initial design, not a completed Figma capture.** Coursework prototype; fictional scenarios only.

[View the complete SVG diagram](part1-flow.svg) · [PNG preview](part1-flow.png) · [Research rationale](../design-pipeline.md)

The SVG is the standalone visual; the Mermaid blocks below provide editable text versions of the same flow. They are grouped to avoid a web of crossing safety arrows.

## 1. Main practice flow

```mermaid
flowchart LR
    entry["Entry: direct Start; optional introduction"] -->|"Start"| running["Practice: six 4-second in / 6-second out cycles"]
    running -->|"Pause"| paused["Paused: timer stopped"]
    paused -->|"Explicit Resume, support closed"| running
    running -->|"Stop"| stopped["Record stopped once: active duration"]
    paused -->|"Stop"| stopped
    running -->|"60 active seconds: final cycle ends"| completed["Record completed once: 60 seconds"]
    stopped --> result["Result: neutral status and duration"]
    completed --> result
    result -->|"View history"| history["History: status, duration, ID; labeled fixture"]
    result -->|"Practice again, support closed"| running
    history -->|"Back to practice"| entry
```

Pause and support time are excluded; entry/setup time is reported separately. The result remains until a person chooses another action. History is accessible after stopping or completing. The prototype can retain the result when returning from history; “entry” in the diagram denotes the practice view, not a mandatory reset or new session.

## 2. Optional mock introduction

```mermaid
flowchart LR
    entryIntro["Entry or result"] -->|"Show introduction"| waiting["Waiting: Success / Failed about 0.5s; Delayed about 8s"]
    waiting -->|"Success"| success["Fixed app guidance"]
    waiting -->|"Failure"| failure["Honest failure; retry available"]
    failure -->|"Retry, same or changed mode"| waiting
    success -->|"Retry if desired"| waiting
    entryIntro -.->|"Start directly"| start["Start practice; cancel pending request and ignore late replies"]
    waiting -.->|"Start without waiting"| start
    failure -.->|"Start without retry"| start
    success -.->|"Start"| start
```

The introduction is never required. Start (or Practice again from a result) and Crisis support remain available throughout these states. Loading prevents duplicate requests; changing modes invalidates the old response. The selected Failed mode keeps failing until the person changes mode; Retry does not imply automatic recovery. No real AI provider is involved. While support is open, Start is disabled until it is closed.

## 3. Universal crisis-support path

```mermaid
flowchart TD
    entrySupport["Entry"] --> support["Support open: pause running practice; preserve other context"]
    waitingSupport["Introduction waiting or delayed"] --> support
    successSupport["Introduction success"] --> support
    failedSupport["Introduction failure / retry"] --> support
    runningSupport["Running practice"] --> support
    pausedSupport["Paused practice"] --> support
    resultSupport["Stopped / completed result"] --> support
    historySupport["History"] --> support
    support -->|"Close after active practice"| remainPaused["Remain paused; never auto-resume"]
    remainPaused -->|"Explicit Resume"| resumeRunning["Running practice"]
    support -->|"Close from non-exercise view"| returnContext["Return to underlying state; do not start practice"]
    support -->|"Stop if exercise active"| stopResult["Record stopped once; result behind still-open support panel"]
    stopResult -->|"Close support"| showResult["Stopped result; history available"]
```

This is a global route, not a classifier decision or model-generated link. Opening support during practice pauses it. Resume stays disabled while support is open. Closing support leaves it paused; only an explicit Resume restarts timing. If a mock request finishes while support is open, it may update its underlying introduction state, but must not close support or start practice. Stop remains available within support whenever practice is active.

## Selected design direction versus current implementation

- **Selected, not implemented:** persistent bottom bar with Crisis support in every relevant state and Stop during running/paused practice; hide general navigation during practice and restore it on Stop/completion; optional “Remember my display choice.”
- **Confirmed design rule:** the system reduced-motion setting takes precedence over a saved animated preference. Persistence is future work; live OS-setting changes and associated wording require implementation checks.
- **Implemented baseline:** six cycles, pause/resume/stop, mock success/failure/delay with stale-response protection, independent support panel, temporary history, and still cue. The current support button scrolls with the page.
- **Current limitation:** history and preferences reset on refresh; the labeled fixture returns. No database, backend or live AI. Neither a persistent bar nor persistent preferences are claimed complete.

The figure communicates transitions and selected direction, not proof that every state, viewport, or accessibility behavior has passed a test. See [verification notes](../verification.md) for actual prior observations and diagram review.
