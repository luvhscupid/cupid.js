# Iris Phase 1 harness

The labeled cases use small synthetic images; the manifest and expected labels are in `labeled_cases.json`. The scoreboard generator writes PNGs and exact `ground_truth.json` alongside them. Install Pillow for image generation:

```sh
python -m pip install Pillow
```

From this directory:

```sh
python make_labeled_fixtures.py
python harness.py
python -m unittest -v test_phase1.py
python scoreboard.py /tmp/iris-scoreboards
python harness.py --scoreboards /tmp/iris-scoreboards
python -m unittest -v test_phase1.py test_phase2.py
```

To score a model's structured predictions, pass a JSON object keyed by case ID:

```sh
python harness.py --predictions predictions.json
```

The evaluator compares expected fields exactly and reports avoid-term hits. This is a deterministic harness, not a model evaluation or a substitute for human review.

## Vision baseline

`baseline.py` evaluates the six labeled cases and generates/connects all eight scoreboard variants. It uses a short plain prompt and an explicitly configured OpenAI-compatible chat completions endpoint. Configure `IRIS_VISION_BASE_URL` and `IRIS_VISION_MODEL`; `IRIS_VISION_API_KEY` is optional for local endpoints. No provider or model is assumed.

```sh
export IRIS_VISION_BASE_URL="https://api.openai.com/v1"
export IRIS_VISION_MODEL="your-vision-model-id"
export IRIS_VISION_API_KEY="your-api-key"
python baseline.py --output /tmp/iris-baseline.json
```

Without endpoint/model configuration, the runner inspects image-byte and EXIF access, writes a blocked result, and exits with status 2. It reports no model metrics in that case. Results include raw model responses, exact-field accuracy and coverage, unsupported-claim checks, per-case latency, and API token usage when the endpoint returns it.
