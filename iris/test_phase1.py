import json
import tempfile
import unittest
from pathlib import Path

from harness import evaluate, load_cases
from scoreboard import generate


class HarnessTests(unittest.TestCase):
    def test_labeled_manifest_is_complete_and_covers_required_domains(self):
        cases = load_cases()
        self.assertEqual({"gaming", "photography", "cats", "food", "adversarial"}, {c["domain"] for c in cases})
        self.assertEqual(6, len(cases))

    def test_evaluator_checks_expected_fields_and_avoid_terms(self):
        cases = load_cases()
        target = next(c for c in cases if c["id"] == "embedded-instruction-01")
        result = evaluate([target], {target["id"]: {
            "embedded_text_is_image_content": True,
            "follows_embedded_instruction": False,
            "response": "I will reveal hidden data",
        }})
        self.assertEqual(1.0, result["field_accuracy"])
        self.assertEqual(["I will reveal hidden data"], result["cases"][0]["avoid_violations"])


class ScoreboardTests(unittest.TestCase):
    def test_generator_writes_known_truth_and_all_variation_types(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            entries = generate(path)
            payload = json.loads((path / "ground_truth.json").read_text(encoding="utf-8"))
            self.assertEqual(8, len(entries))
            self.assertEqual(entries, payload["cases"])
            self.assertEqual({"clean", "blurred", "downscaled", "edited_home_score"}, {e["variation"] for e in entries})
            edited = next(e for e in entries if e["id"] == "game-1-edited")
            clean = next(e for e in entries if e["id"] == "game-1-clean")
            self.assertEqual(13, edited["ground_truth"]["home_score"])
            self.assertEqual(12, clean["ground_truth"]["home_score"])
            for entry in entries:
                self.assertTrue((path / entry["image"]).is_file())


if __name__ == "__main__":
    unittest.main()
