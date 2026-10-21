# Iris

## Architecture

- Codex is the underlying AI and execution environment.
- Angle is a Codex-powered engineering workspace.
- Iris is a Codex-powered image-understanding workspace and capability. It is not a separate agent, model, inference server, or orchestration system.
- GPT and Claude are external design reviewers, not Iris runtime dependencies.

Iris uses image understanding available in its Codex environment. Whether a particular Angle or Iris surface routes image inputs into Codex is an environment capability to verify; access to an image file on disk alone does not prove visual understanding.

## Phase 1 and 2 evaluation tools

The labeled cases use small synthetic images in `fixtures/`, with labels in `labeled_cases.json`. The scoreboard generator creates eight PNG variants with exact ground truth. Pillow is needed to generate images.

If Pillow is missing from the Python environment, install it with `python -m pip install Pillow` before generating fixtures.

From this directory:

```sh
python make_labeled_fixtures.py
python harness.py
python -m unittest -v test_phase1.py test_phase2.py
python scoreboard.py /tmp/iris-scoreboards
python harness.py --scoreboards /tmp/iris-scoreboards
```

To score structured predictions, pass a JSON object keyed by case ID:

```sh
python harness.py --predictions predictions.json
```

The evaluator reports exact-field accuracy, answer coverage, unresolved fields, and avoid-term hits. These deterministic checks do not substitute for human review or a model evaluation.

## Optional experimental adapter

`baseline.py` is an optional adapter for a separate OpenAI-compatible model comparison. It is not part of Iris's runtime and is not required to use Iris or run the labeled harness. It is retained for the Phase 2 experiment; if endpoint and model variables are not configured, it records that this external comparison is blocked. No external API is configured or required by Iris.

The adapter's HTTP request test is mocked and verifies payload encoding and result parsing only. It is not evidence of an available external model or of Iris's native image routing.
