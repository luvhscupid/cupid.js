# Cloud ↔ Local Codex Calculator Handoff

**Verification state:** `LOCAL_PENDING`

## Relevant Git commit

Current base commit: `bf303d06f08ae9c09de8d65f205fc0d278293fd0` (`Clarify calculator handoff checkpoint`, published as `origin/work`). Specification commit: `8fa4b49` (`Add calculator Codex handoff spec`). Implementation and test changes are uncommitted and have not been pushed.

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
- Added `calculator.py` with the four specified arithmetic functions and `test_calculator.py` with five `unittest` cases.
- Ran the portable test suite in the available Linux Cloud runtime; this is not Windows Local verification.

## Verification requirements

Cloud runtime evidence: `uname -a` reported `Linux 4cc9d1afdbfa 6.18.55 #1 SMP Wed Oct 14 19:45:18 UTC 2026 x86_64 GNU/Linux`; `python --version` reported `Python 3.12.14`. From `experiments/codex-handoff`, `PYTHONDONTWRITEBYTECODE=1 python -m unittest -v` ran 5 tests and passed (add, subtract, multiply, divide, and division by zero). `git diff --check` passed. The implementation uses only the Python standard library.

This evidence verifies behavior in Cloud/Linux only. The experiment's Windows Local verification and Cloud review through GitHub remain incomplete.

## Unresolved blockers

- Windows Local execution of the test suite is pending. The current implementation and tests are uncommitted in the Cloud checkout, so they are not yet available through `origin/work`.
- Cloud review through GitHub is pending the Local handoff.

## Exact next authorized Local action

Once these uncommitted changes are made available to the Windows Local checkout, run `python -m unittest -v` from `experiments/codex-handoff`, record the Windows version, Python version, test count, and result here, and report the result for Cloud review. Keep changes within `experiments/codex-handoff/`; do not modify `portfolio/battlefield-editing/`.
