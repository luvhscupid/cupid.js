# Hybrid Codex workflow upgrade

**Verification state:** `CLOUD_VERIFIED`

## Relevant Git commit

Base commit: `1a839b7a2979daf9df30cd6e0b47d056b508a39b` (`origin/main` before this change).

## Task objective

Configure native Codex instructions and skill selection for a project-aware hybrid Cloud/Local workflow, with Git-tracked checkpoints as the authoritative handoff.

## Approved decisions

- Use the active selected repository and its instructions; use `cupid.js` as the default Cloud planning workspace only when no project is selected.
- Cloud may implement and test self-contained work. Reserve `LOCAL_PENDING` for local files, hardware, operating-system integration, or local-only verification.
- Superpowers is primary. ADHD is an optional replacement for one ideation phase, never an additional phase. Drill-Me is only for user-requested learning or understanding checks.
- Codebase Memory MCP is opportunistic and supplementary; Git-tracked plans and checkpoints are authoritative.
- Preserve approved decisions and avoid repeated brainstorming absent material new evidence.
- Never claim local verification from Cloud evidence. Keep authorization boundaries and Local PC configuration unchanged.

## Completed work

- Updated `AGENTS.md` with project-aware discovery, Cloud/Local/Unknown classification, workflow ownership, skill-selection rules, checkpoint evidence, and authorization limits.
- Updated the Cloud startup and installer draft to persist those rules and enable contextual skill discovery for the installed Cloud skills.
- Updated the current Cloud skill metadata for debugging, test-driven development, verification, optional ADHD ideation, and Drill-Me. No Local PC files or settings were changed.

## Test and supporting evidence

- `codex debug prompt-input` passed for generic feature, debugging, and learning prompts from the selected repository. Each prompt included this repository's `AGENTS.md` and all eight skills in the activation set.
- Read each installed `agents/openai.yaml`; `using-superpowers`, `brainstorming`, `writing-plans`, `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `adhd`, and `drill-me` all have `allow_implicit_invocation: true`. The contextual rules in `AGENTS.md` decide when ADHD and Drill-Me are appropriate.
- `bash -n` and Python `compile()` passed for the saved Cloud install script and its embedded skill-installer block.
- `codex mcp list` reports the supplementary `codebase-memory` stdio server as enabled; its authentication status is unsupported in this runtime, so Git remains the fallback.
- No application tests apply to this instruction/configuration-only change.
- Cloud environment draft saved successfully with `requires_publish: true`; fresh-task persistence of the new Cloud startup and installer is pending publication.

## Unresolved blockers

- Fresh-task restoration of the updated Cloud environment has not yet been verified.
- Local Codex configuration is intentionally untouched and cannot be verified from this Cloud environment.

## Exact next action

Review and publish the saved Cloud environment draft in Environment settings so fresh Cloud tasks receive the updated startup and installer instructions.
