# Manual Figma reference pack — October27

Figma MCP is blocked by the current Starter-plan tool allowance. These are approved **static, source-informed reference boards**, not screenshots, exact Vue reproductions, editable component captures or a completed Figma round trip. No Figma file or baseline was changed. PNGs can be placed in the existing file manually; SVG sources are supplied for resizing, but importing them does not establish component semantics, interaction wiring or verified editability.

Create a new page/section named `October27 static reference fallback` in Assignment-3, preserve all baseline pages, then drag the PNG files onto that new area. Keep the filenames as labels. Desktop boards use1440×1000; phone boards use390×1200. They summarize hierarchy and behavior; they do not prove physical-phone rendering. The app’s actual styling uses Arial/Georgia, cream background, green controls and restrained borders. These references reuse that palette but simplify the working forms/controls. Treat them as annotated wireframes, not pixel-fidelity evidence.

| View | Desktop PNG | Phone PNG |
| --- | --- | --- |
| Profile entry | [Desktop](desktop-1440-entry.png) | [390px](phone-390-entry.png) |
| Practice | [Desktop](desktop-1440-practice.png) | [390px](phone-390-practice.png) |
| Profile | [Desktop](desktop-1440-profile.png) | [390px](phone-390-profile.png) |
| Calendar | [Desktop](desktop-1440-calendar.png) | [390px](phone-390-calendar.png) |
| Exercise library | [Desktop](desktop-1440-library.png) | [390px](phone-390-library.png) |
| Voice chat | [Desktop](desktop-1440-voice.png) | [390px](phone-390-voice.png) |
| Independent support | [Desktop](desktop-1440-support.png) | [390px](phone-390-support.png) |

## Flow and state notes

Entry → Continue as guest OR select/create local profile → Practice. Navigation offers Practice, Session history, Voice chat, Exercises, Calendar, Profile. Crisis support is available from entry and every view, including empty/loading/failure states.

Practice → Start → six4/6 cycles → completed result → saved history and calendar. Pause/support/hidden-tab interruption → explicit Resume; Stop → stopped history only. Profile switching during practice offers Continue practice or Stop and switch. Library placeholders cannot start anything.

Voice → explicit Start (live mode only) → permission → listening → silence submits → transcription → scoped RAG → save actual reply → speaking. While speaking, microphone frames are ignored. End/hide/support/switch stops capture. Typed input remains in the same tab. Saved conversation history is ordered; audio failure does not erase text. Permission denied/no mic/silence/transcription/provider/save/playback failures remain distinguishable. No silent restart. Current peer-test mode is labeled mock, using a fixed transcript/test tone rather than real recognition/speech.

Profile/guest history survives refresh. Transfer guest activity only on explicit request. Exit guest or confirmed discard clears guest activity. Profile deletion confirms deletion of its saved activity. Calendar uses actual completed records, completion time and device timezone. Empty calendars show no events; these boards invent no activity.

Tradeoffs: wrapping phone navigation avoids a fixed bar covering controls, at the cost of extra vertical space. Profile fields remain optional except display name; guest entry avoids disclosure. Static support references deliberately omit helpline content rather than presenting an unverified export as current resources. Still cue and reduced motion remain in the app.

No MCP quota bypass, paid plan, new dependency or cloud upload was used. Readability/overlap was visually reviewed on a rendered contact sheet; real-browser/device and Figma comparison remain separate checks. The fallback does not close the assignment workflow's editable-design gap.
