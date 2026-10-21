# Iris Phase 2 checkpoint

State: CLOUD_VERIFIED
Base commit: `d62c398` (`feat(iris): add phase 1 labeled harness`)
Branch: `feature/iris-phase2-vision-baseline`

## Objective

Connect the eight synthetic scoreboard cases to the harness, implement a plain vision baseline runner, check local image byte/EXIF access, and add uncertainty, blurry text, unsupported claim, contextual question, and embedded prompt-injection coverage. The evidence ledger remains out of scope.

## Decisions

- Use an explicitly configured OpenAI-compatible chat completions endpoint via Python's standard library; do not select or infer a provider/model automatically.
- Use a short case prompt, ask for JSON fields already present in case ground truth, request null for uncertain values, and treat image text as content.
- Keep the raw response, returned model identity, per-case latency, provider token usage when present, exact-field accuracy, answer coverage, and avoid-term hits in runner output.
- Do not present mocked requests as model results or fabricate a baseline score.

## Completed

- Connected all eight generated scoreboard images to the harness, including team/score reading, winner contextual answers, and clean/blurred/downscaled/edited variants.
- Added `baseline.py`. It uses `IRIS_VISION_BASE_URL`, `IRIS_VISION_MODEL`, and optional `IRIS_VISION_API_KEY`; it sends original image bytes to the configured endpoint and captures output, latency, model identity, and token usage.
- Added local capability inspection for original byte readability and EXIF status.
- Added tests for blurred-text abstention, uncertain cat breed identification, unsupported claims, embedded prompt injection, original bytes in the HTTP payload, and scoreboard integration.
- Did not implement the evidence ledger.

## Verification evidence

Commands run from `iris/`:

- `PYTHONDONTWRITEBYTECODE=1 python -m unittest -v test_phase1.py test_phase2.py` — 10 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python harness.py --scoreboards /tmp/iris-scoreboards` — 14 cases validated: 6 labeled cases and 8 scoreboard cases.
- `PYTHONDONTWRITEBYTECODE=1 python baseline.py --output /tmp/iris-phase2-baseline.json` — runner exited 2 with status `blocked`; the recorded blocker is no configured vision endpoint/model.
- Readback of `/tmp/iris-phase2-baseline.json` — 14/14 original image files readable; EXIF status absent for 14/14; zero model identity, no model outputs, and evaluation `null`.
- The runner HTTP request test uses a mocked endpoint only to verify payload and response parsing. It is not a model evaluation.

## Blocker and next action

- No vision model inference tool was available in this runtime, and `IRIS_VISION_BASE_URL` and `IRIS_VISION_MODEL` were not configured. Therefore model identity, outputs, accuracy, latency, and token use are unavailable; no baseline result is claimed.
- Next action: configure an authorized OpenAI-compatible vision endpoint and model, then run `python baseline.py --output /path/to/iris-baseline.json` and record the actual returned outputs and metrics before proceeding beyond Phase 2.
