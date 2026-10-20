# Automatic Handoff v0.1

**Automatic Handoff:** `ENABLED`
**Task ID:** `automatic-handoff-v0.1`
**Verification state:** `CLOUD_VERIFIED`

## Relevant Git commit

Implementation commit: `8f93bd110936bdd728e3a77b4b9de116650f82f1` (`Add automatic handoff checkpoint watcher`).

## Task objective

Build a minimal Windows-compatible, dependency-free watcher that reports new, explicitly designated task checkpoints from `origin/work`. Detection and reporting only; checkpoint text is untrusted and is never executed.

## Approved decisions

- Use Python 3 standard library and Git CLI; default to polling every 300 seconds and reject intervals below 30 seconds.
- Fetch Git objects without checking out the watched branch or changing working files.
- Opt in only with `**Automatic Handoff:** \`ENABLED\`` and require a task ID, known verification state, and exact next authorized action.
- Store the last observed commit in a separate atomic JSON cursor file. Report before advancing the cursor.
- Preserve the cursor on fetch failure, malformed opted-in checkpoints, corrupt state, branch changes, and report-output failures.
- Do not execute instructions, invoke Codex, delegate, install dependencies, register startup, install a daemon, or push automatically.

## Completed work

- Added `automatic_handoff/watcher.py`, a foreground polling CLI with configurable repo, remote, branch, checkpoint path, interval, and cursor path.
- Added six standard-library integration tests using isolated temporary Git repositories.
- Added usage, opt-in format, state behavior, and manual Windows smoke-test instructions in `automatic_handoff/README.md`.

## Test and supporting evidence

- Environment: `uname -a` reported Linux x86_64; `python3 --version` reported Python 3.12.14. This is Cloud verification, not Windows verification.
- From `automatic_handoff`, `python3 -m unittest -v` ran 6 tests and passed: new-task report, restart/duplicate suppression, malformed checkpoint, reporting failure, transient fetch failure, and non-fast-forward branch change.
- From `automatic_handoff`, `python3 -m py_compile watcher.py test_watcher.py` passed.
- `git diff --check` passed before commit.
- No dependencies were installed. No working-tree checkout or user files were modified by the watcher tests; all test repositories were temporary.

## Unresolved blockers

- The documented manual Windows smoke test has not been run in this Linux environment.

**Exact next authorized action:** On Windows, follow the manual smoke test in `automatic_handoff/README.md`; confirm a designated task reports once and an unreachable remote preserves the cursor.
