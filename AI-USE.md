# AI-use disclosure — Assignment 3 Part 1

Prepared from the project files and available conversation/tool record on October 15, 2026. This disclosure describes the work actually recorded; it does not certify student review or tests that have not been reported. The student should review this file before submitting it.

## Tools, identifiers, and roles

| Tool / service | Known identifier or version | Recorded role |
| --- | --- | --- |
| OpenAI Codex coding assistant in the desktop app | Product known; exact serving model/snapshot and app build were not verified in the project record. No precise model version is claimed. | Generated initial Vue/JavaScript source, CSS, timing/stale-response controller, tests, and documentation; inspected files; executed build/tests; operated the browser; helped connect supplied study findings to design decisions. |
| Shell / local development tools | Observed Node v24.20.0, npm 11.19.0, Python 3.12.5. Dependency versions: Vue 3.5.44, Vite 7.3.7, @vitejs/plugin-vue 6.0.10. | Installed approved project-local dependencies, ran commands/tests/build, created SVG/docs with Python standard-library tooling, and performed file/hash checks. These are tool/dependency versions, not AI model identifiers. |
| Browser automation (`cua_repl`, in-app browser) | Exact automation/browser build not recorded. | Operated fictional prototype flows, checked visible states, keyboard activation/focus and viewport width, and saved screenshots. It is an observation tool, not an independent human evaluation. |
| Figma MCP connector | `whoami`, `get_design_context`; exact connector/server build not verified. | Checked connection/account plan and tool availability; read Activity frame 1:6 and its returned screenshot. Frame was blank. No Figma capture or design modification was completed. Account email and plan identifiers are omitted as unnecessary personal information. |
| Helpline lookup connector | `get_local_hotline`; exact version not verified. | Retrieved region-labeled US/territories resource details used in the support panel. No calls, texts, or chats with that service were made as tests. |
| Web documentation lookup | Tool build not verified. | Consulted official OpenAI browser-permission documentation while troubleshooting local browser access. This was not a source for the assignment's research findings. |
| macOS Quick Look and local image viewing | Exact utility versions not recorded. | Rendered the original SVG flow diagram to a PNG and inspected layout; reviewed saved prototype screenshots. No image-generation model or external stock imagery was used. |

The application itself has **no live conversational model integration**. Introduction replies are fixed, local mock strings. Assistant-generated source/documentation must not be confused with an AI service running inside the prototype. No paid model/API calls were initiated for the evidence-preparation task; this does not assert that the coding-assistant session has no account cost.

## Student input, decisions, and review evidence

The recorded student actions were:

- Supplied project instructions and assignment material, including the complete R1–R4/D1–D6 research table.
- Requested the initial prototype after clarifying that no source code existed; approved the specific project-local Vue/Vite installation.
- Provided the Assignment-3 Figma link and chose it as the future capture destination.
- Requested a research-grounded, documentation-only proposal, the initial flow diagram, planned architecture, and curated evidence.
- Explicitly selected a persistent bottom bar with Crisis support and active-practice Stop, hidden general navigation during active practice with restoration afterward, and optional “Remember my display choice.” Confirmed that system reduced motion should override a saved animated preference.

Those choices demonstrate review of the presented design questions. The record does **not** establish that the student personally ran every test, inspected every generated code line, reviewed every screenshot/document, or approved all draft API/schema/crisis-text details. Browser and automated checks in verification.md were carried out by the agent. Unresolved proposal details remain labeled in the design notes; they must not be attributed to the student as settled decisions.

## Generated material and reuse

- Agent-generated work: initial frontend components/controller/styles/configuration/tests; supporting design, verification, handoff and prompt notes; initial SVG/Mermaid flow and its PNG preview; this disclosure and evidence index.
- Existing project inputs: README.md and AGENTS.md were already present. The README supplied paced-breathing direction and stack boundaries; the agent did not independently establish the student's original authorship of all starter text. AGENTS.md was preserved, while README received verified run instructions.
- Research: the assignment overview and student-supplied R/D table supplied the design evidence. Counts describe mentions in that study, not prototype clinical outcomes. No study participant records or separate clinical research dataset were imported.
- Code/assets: no earlier hotel/travel-app code reuse is documented or claimed. Vue/Vite/plugin-vue are package dependencies with their own upstream terms. The interface uses CSS shapes, text/Unicode symbols, and system font stacks; no stock photos, downloaded icon pack, generated raster art, or Figma assets were imported. The Figma response was a blank-frame example, not a populated design reused in Vue.
- Screenshots are browser captures of the local fictional prototype. The diagram is an original generated design artifact, explicitly not a completed Figma capture. Referenced resource links are external destinations, not copied therapist conversations or a training dataset.

## Selected evidence and revised approaches

The [curated evidence index](docs/evidence/README.md) links three screenshots and a small set of prior observations, stating what each establishes and its limits. It traces selected prompt summaries to changes and decisions, including the incomplete Figma reference, the clock-synchronized motion refinement, and the support-visibility limitation that led to a proposed bottom bar.

[Verification notes](docs/verification.md) record actual prior commands and observations, including a wrong-directory npm invocation and the corrected command, sandbox server-binding failure and approved local run, refresh reset, and test limitations. [Initial prototype prompt](prompts/01-prototype.md) preserves the reusable scope. A full chat export is neither included nor needed.

## Limits and submission review

Current records are in memory and reset on refresh. FastAPI, SQLite persistence, RAG, real provider calls, persistent preferences, and the selected bottom bar/navigation revisions remain unfinished. The Part 1 architecture is a proposal, not implementation evidence. No clinical efficacy, real distress detection, or monitored support service is claimed.

The evidence review found no common credential patterns, personal email addresses, or absolute user-home paths in repository-owned text, and no unnecessary private content visible in the three selected screenshots. This is a scoped review, not a complete security audit. See the evidence index for exclusions and access limitations. Before submission, the student should review these disclosures, explain the relevant generated code, verify report/repository links and permissions, and correct any missing personal review or reuse information rather than marking it complete without evidence.
