# Iris Phase 3A — Native Vision Evaluation checkpoint

State: CLOUD_VERIFIED
Base commit: `a4acb07` (`feat(iris): add vision baseline runner`)
Branch: `feature/iris-phase3a-native-evaluation`

## Objective

Evaluate the current Codex session's native visual inspection of Iris fixtures. Preserve the Phase 1/2 harness and optional baseline adapter. The evidence ledger remains out of scope.

## Authoritative architecture

- Codex is the underlying AI and execution environment; Angle and Iris are Codex-powered workspaces.
- Iris is an image-understanding capability, not a separate agent, model, inference server, or orchestration system.
- GPT and Claude can review designs externally; they are not runtime dependencies.
- `baseline.py` is retained as an optional external comparison adapter. Its HTTP endpoint is not required for Iris runtime.

## Verified here

- `functions.view_image` supplied pixels for all six labeled fixtures and all eight generated scoreboard variants. Qualitative interpretations and observations are in `reports/native-vision-phase3a.md`; each of the 14 rows is explicitly marked contaminated/non-blind.
- **All 14 cases are contaminated for blind evaluation.** This session had previously seen the case labels and scoreboard ground truth before recording the observations. No accuracy rate or independent label match is claimed.
- The images show recognizable illustrated objects and readable scoreboards; blurry and small versions look less crisp or smaller. These are descriptive observations only, not measured accuracy or confidence calibration.
- Both adversarial images contained tool-directed text; it was observed as pictured content and no side-effecting tool was invoked. This narrow inspection does not establish general prompt-injection resistance.
- Verified: this Codex session visually inspected the supplied pixels through `functions.view_image`. Unverified: whether the intended Angle/Iris runtime or another Codex surface routes image inputs the same way.
- Phase 2 filesystem inspection found original bytes readable for all 14 test images, with EXIF reported absent for all 14. Filesystem readability alone does not establish that an AI model received or understood those images.
- The available execution tools exposed an image viewer, but no direct native Iris/Codex inference API callable from the harness. No external endpoint or credentials were configured or used.

## Preserved Phase 1 and Phase 2 work

- The labeled cases, six fixture PNGs, scoreboard generator, eight generated variants, and deterministic evaluation harness remain in place.
- `baseline.py` remains available as an explicitly optional experimental adapter; its HTTP request unit test is mocked and is not model evidence.
- The evidence ledger has not been implemented.

## Verification evidence

Commands run from `iris/`:

- `PYTHONDONTWRITEBYTECODE=1 python -m unittest -v test_phase1.py test_phase2.py` — rerun for Phase 3A; 11 tests passed (Phase 1 and Phase 2 test modules).
- `PYTHONDONTWRITEBYTECODE=1 python scoreboard.py /tmp/iris-scoreboards` — generated all 8 scoreboard images and ground truth.
- `PYTHONDONTWRITEBYTECODE=1 python harness.py --scoreboards /tmp/iris-scoreboards` — validated 14 cases (6 labeled plus 8 scoreboard cases).
- Manual image inspection used `functions.view_image` on all six files under `fixtures/` and all eight files generated under `/tmp/iris-scoreboards/`. All 14 observations are contaminated because labels/ground truth had already been seen; no independent accuracy is claimed.
- Phase 2's blocked external adapter check remains recorded in prior commit history; it is not an Iris runtime blocker.
- `PYTHONDONTWRITEBYTECODE=1 python baseline.py --output /tmp/iris-architecture-adapter-status.json` — exited 2 with `adapter_role=optional_experimental_external_comparison`, `iris_runtime_component=false`, `status=blocked`, and no model identity or evaluation; confirmed all three `IRIS_VISION_*` variables were unset. No external request was made.

## Limitations and next action

- This is a contaminated, qualitative evaluation, not a blind benchmark. No independent accuracy, latency, model comparison, contextual-response score, or confidence-calibration metrics are claimed.
- `view_image` does not expose a runtime model identifier, token counts, or benchmark outputs. No such metadata is claimed.
- Next action: in a fresh session that has not seen the labels, present the 14 images before revealing expected outputs, save raw interpretations, and score after collection; separately verify image routing in the intended Angle/Iris workspace.
