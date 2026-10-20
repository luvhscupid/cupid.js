# Cloud ↔ Local Codex Calculator Handoff

**Verification state:** `PLANNED`

## Relevant Git commit

Specification commit: `8fa4b49` (`Add calculator Codex handoff spec`). Synchronized parent/base: `90a5af0f8c32e597751924404e0c3f0ad9f51cbb` (`origin/main` before the specification was added).

## Task objective

Verify that Cloud Codex can define a small task, Local Codex can independently implement and test it, and Cloud Codex can review the result through GitHub.

## Approved decisions

- Implement the interface and behavior in `SPEC.md`.
- Use Python 3 and the standard library only.
- Local Codex owns implementation and test execution; Cloud Codex owns this spec and later GitHub review.
- Keep this integration test limited to this directory.

## Acceptance criteria

- `calculator.py` provides `add`, `subtract`, `multiply`, and `divide` with the behavior in `SPEC.md`.
- `test_calculator.py` uses `unittest` and covers the four operations plus division by zero.
- The tests pass using Python 3 and its standard library only.
- Local Codex records the exact verification command and result here.
- No files outside `experiments/codex-handoff/` are changed for implementation or verification.

## Current phase and completed work

- Cloud planning phase: interface, behavior, acceptance criteria, and Local verification requirements are defined.
- Calculator implementation and tests have not been created; no calculator tests have been run.
- No implementation result is claimed.

## Verification requirements

Local Codex must implement `calculator.py` and `test_calculator.py` in this directory, then run `python -m unittest -v` from `experiments/codex-handoff` (or an equivalent Python 3 launcher command on Windows). Record the exact command, Python version, test count, and pass/fail result here. The test suite must cover all four operations and division by zero. Cloud has not verified the implementation.

## Unresolved blockers

- Local implementation and test execution are pending.
- Cloud review through GitHub is pending the Local handoff.

## Exact next authorized Local action

Safely synchronize with `origin/main` under the root `AGENTS.md` rules, preserving existing worktree changes. Then, using only Python 3 standard-library features, implement `calculator.py` and `test_calculator.py` exactly as specified in `SPEC.md`, run the required unittest command, and record the implementation files, exact verification command, Python version, test count, and result in this checkpoint. Keep changes within `experiments/codex-handoff/`; do not modify `portfolio/battlefield-editing/`. After verification, commit and push through a normal fast-forward so Cloud Codex can review the implementation and test evidence through GitHub.
