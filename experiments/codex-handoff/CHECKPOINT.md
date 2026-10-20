# Cloud ↔ Local Codex Calculator Handoff

**Verification state:** `LOCAL_VERIFIED`

## Relevant Git commit

Implementation and test commit: `8eee27079a0b5804de6fdf63ec6ca6ac8147c7e0` (`Add verified calculator handoff implementation`), based on `bf303d06f08ae9c09de8d65f205fc0d278293fd0` (`Clarify calculator handoff checkpoint`, published as `origin/work`). Specification commit: `8fa4b49` (`Add calculator Codex handoff spec`).

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
- Committed the implementation and tests in the detached handoff worktree.
- Ran the portable test suite in the available Linux Cloud runtime; this is not Windows Local verification.
- Verified the committed implementation and tests from `origin/work` on Windows Local. The existing detached worktree contains different untracked copies of both Python files; those were preserved and not used for this verification.

## Verification requirements

Cloud runtime evidence: `uname -a` reported `Linux 4cc9d1afdbfa 6.18.55 #1 SMP Wed Oct 14 19:45:18 UTC 2026 x86_64 GNU/Linux`; `python --version` reported `Python 3.12.14`. From `experiments/codex-handoff`, `PYTHONDONTWRITEBYTECODE=1 python -m unittest -v` ran 5 tests and passed (add, subtract, multiply, divide, and division by zero). `git diff --check` passed.

Windows Local evidence: `[System.Runtime.InteropServices.RuntimeInformation]::OSDescription` reported `Microsoft Windows 10.0.26300`; `[System.Environment]::OSVersion.VersionString` reported `Microsoft Windows NT 10.0.26300.0`; the Python executable `C:\Users\cupid\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe --version` reported `Python 3.12.14`. The committed `experiments/codex-handoff/` files were extracted from `origin/work` commit `7a45bfd32eff329ccc695e9875482a785ec4cad3` into a temporary directory; from that extracted directory the exact command `& 'C:\Users\cupid\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest -v` produced:

```text
test_add (test_calculator.CalculatorTests.test_add) ... ok
test_divide (test_calculator.CalculatorTests.test_divide) ... ok
test_divide_by_zero_raises (test_calculator.CalculatorTests.test_divide_by_zero_raises) ... ok
test_multiply (test_calculator.CalculatorTests.test_multiply) ... ok
test_subtract (test_calculator.CalculatorTests.test_subtract) ... ok

Ran 5 tests in 0.000s
OK
Exit code: 0
```

The verified test files and calculator source were the versions committed on `origin/work`; no changes were made to `calculator.py` or `test_calculator.py` for this correction.

## Unresolved blockers

- Cloud review through GitHub of the corrected Windows evidence is pending.

## Exact next authorized Local action

Cloud Codex should review the corrected checkpoint evidence on `origin/work`. No further Local implementation is authorized by this checkpoint.
