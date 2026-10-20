# Hybrid Codex workflow

## Responsibilities

- Cloud Codex handles brainstorming, requirements clarification, planning, and preparation.
- Local Codex handles implementation, testing, debugging, and verification.
- Local Codex preserves approved Cloud decisions. Do not repeat brainstorming unless new evidence identifies a genuine problem; explain that evidence and revisit only the affected decision.

## Verification states

Use exactly one state in each `CHECKPOINT.md`:

- `PLANNED`: work is planned; no verification is claimed.
- `CLOUD_VERIFIED`: Cloud Codex ran and recorded the stated checks; this does not imply local verification.
- `LOCAL_PENDING`: cloud preparation is complete and Local Codex verification is still outstanding.
- `LOCAL_VERIFIED`: Local Codex completed and recorded the stated verification. Never set or claim this state based only on Cloud results.

## Project record

- Keep objectives, approved decisions, plans, evidence, blockers, and next actions in Git-tracked files.
- Treat Codebase Memory MCP as supplementary retrieval only. Git-tracked project records are authoritative; verify source facts in the checkout.
- Keep `CHECKPOINT.md` as the current task handoff record. Include the verification state, relevant Git commit, task objective, approved decisions, completed work, test and supporting evidence, unresolved blockers, and one exact next action. Update it as evidence or status changes.
