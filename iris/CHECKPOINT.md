# Iris Phase 1 checkpoint

State: CLOUD_VERIFIED
Commit at start: `b89e1eb` (after fast-forward from `origin/main`)

## Objective

Implement the labeled test harness and synthetic scoreboard generator from `DEVELOPMENT_BRIEF.md`. Evidence ledger work is out of scope.

## Decisions

- Keep Phase 1 self-contained in `iris/` and use Python with Pillow for generated PNG fixtures.
- Keep expected labels and scoreboard ground truth in JSON so image cases can be reused by later model evaluations.
- Do not claim model evaluation: this phase exercises fixture generation and deterministic harness behavior only.

## Completed

- Added a validated labeled manifest for gaming, photography, cats, food, and two adversarial embedded-text cases, plus small synthetic PNG fixtures.
- Added a structured prediction evaluator with exact expected-field matches and explicit avoid-term reporting.
- Added deterministic scoreboard generation with clean, blurred, downscaled, and edited-score variants and per-image ground truth.
- No evidence ledger, model routing, or model evaluation was implemented.

## Verification evidence

- `python make_labeled_fixtures.py` — completed successfully; generated six labeled PNG fixtures.
- `python -m unittest -v test_phase1.py` — 3 tests passed.
- `python harness.py` — validated 6 cases across gaming, photography, cats, food, and adversarial (two cases).
- `python scoreboard.py /tmp/iris-scoreboards` — generated 8 images and `ground_truth.json`.
- Readback of `/tmp/iris-scoreboards/ground_truth.json` — 8 cases with all four variations (`clean`, `blurred`, `downscaled`, `edited_home_score`).

## Blockers and next action

- Vision-model evaluation and any model/image-byte capability assessment remain unrun; the harness does not connect to a model.
- Next action: run the labeled cases and scoreboard set through the selected vision model when model access is available, then record the actual results before considering later phases.
