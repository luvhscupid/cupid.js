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
```

To score a model's structured predictions, pass a JSON object keyed by case ID:

```sh
python harness.py --predictions predictions.json
```

The evaluator compares expected fields exactly and reports avoid-term hits. This is a deterministic harness, not a model evaluation or a substitute for human review.
