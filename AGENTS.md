# Hybrid Codex workflow

## Git synchronization and safety

- Before editing repository files, inspect the current branch, `git status`, and configured remotes; fetch `origin/main` and compare it with local `HEAD`.
- If local `HEAD` is behind and the update is a fast-forward, synchronize before editing. Preserve all uncommitted and untracked work; never reset, overwrite, or discard it automatically. If safe preservation is unclear, stop and explain.
- If local and remote branches have diverged, stop and explain their commits and status before choosing a reconciliation strategy.
- Before pushing, fetch again and confirm the push is a normal fast-forward. If the remote advanced unexpectedly, stop and explain before reconciling.
- Never force-push or rewrite remote history without explicit approval.

## Start each task

- Use the active selected repository as the project context. Follow its root `AGENTS.md` and relevant nested instructions. If no project is selected, use `cupid.js` as the default Cloud planning workspace.
- Inspect `CHECKPOINT.md` when continuing its task, when it records unfinished work or blockers, or when a handoff is requested. Do not treat an unrelated checkpoint as a new task.
- Identify the execution context from explicit runtime/platform evidence: `CLOUD`, `LOCAL`, or `UNKNOWN`. Do not infer Local from a repository path or available shell. If uncertain, use `UNKNOWN` and avoid assuming access to the user's PC, hardware, or operating system.
- Use Codebase Memory MCP opportunistically when relevant tools are available. If unavailable, use Git-tracked records and inspect the checkout. MCP memory is supplementary and never authoritative.

## Workflow and skill selection

- Cloud handles brainstorming, requirements clarification, planning, and preparation. Cloud may also implement and test self-contained work when the selected checkout and available tools are sufficient.
- Local handles work requiring local files, hardware, operating-system integration, or verification that can only run on the user's machine. Do not send ordinary self-contained work to Local solely because it involves implementation or tests.
- Use Superpowers as the primary method when its brainstorming, planning, debugging, test-driven development, or verification workflow fits the task. Brainstorm once for a genuinely new idea or significant feature; ask only unresolved questions that matter to the decision.
- Preserve approved decisions. Do not repeat brainstorming or answered questions unless new evidence reveals a material problem. Explain that evidence and revisit only the affected decision.
- ADHD is optional ideation. Use it only when its own preflight indicates it will materially help and it can replace Superpowers brainstorming for that ideation; never run both as consecutive brainstorming phases. If the preflight does not fit, continue with Superpowers or proceed directly.
- Use Drill-Me only when the user asks for learning, retrieval practice, explanation practice, or an understanding check. The request can be expressed in ordinary language; the user need not name the skill.
- Prefer native Codex instructions and installed skills. Do not add an orchestration framework or enable global/multi-agent configuration for this workflow.

## Project record and verification

- Keep plans, approved decisions, evidence, blockers, and handoffs in Git-tracked project files. `CHECKPOINT.md` is the current task handoff record; update it after meaningful milestones and at completion when a handoff is relevant.
- A checkpoint includes one verification state, relevant Git commit, task objective, approved decisions, completed work, test and supporting evidence, unresolved blockers, and one exact next action.
- Use exactly one state: `PLANNED` (planned, no checks claimed), `CLOUD_VERIFIED` (Cloud ran and recorded the stated checks), `LOCAL_PENDING` (work requires local files, hardware, OS integration, or local-only verification and that work remains), or `LOCAL_VERIFIED` (Local completed and recorded the stated verification).
- Cloud may claim `CLOUD_VERIFIED` only for checks actually run in Cloud. Never claim `LOCAL_VERIFIED` based on Cloud results. Do not use `LOCAL_PENDING` merely because Local is the usual implementation environment.
- State the exact commands or observable evidence supporting verification, along with results. If a required check was not run, record it as a blocker or next action rather than implying success.

## Authorization and stopping

- Work within the user's request and explicit authorization. Do not automatically execute commands on the user's PC, change sensitive configuration, or shut down a computer.
- Do not perform destructive or privileged actions, or modify sensitive/system configuration, without appropriate authorization. Preserve unrelated changes and stop before overwriting unexpected work.
- Finish when the requested objective is complete or genuinely blocked. Do not invent follow-on tasks.
