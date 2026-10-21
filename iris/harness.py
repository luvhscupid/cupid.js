"""Validate Iris labeled cases and score structured model predictions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_CASES = ROOT / "labeled_cases.json"
REQUIRED = {"id", "domain", "image", "prompt", "expected", "avoid"}
DOMAINS = {"gaming", "photography", "cats", "food", "adversarial"}


def load_cases(path: Path = DEFAULT_CASES) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("cases"), list):
        raise ValueError("manifest must have schema_version 1 and a cases array")
    seen: set[str] = set()
    for index, case in enumerate(data["cases"]):
        missing = REQUIRED - case.keys()
        if missing:
            raise ValueError(f"case {index} is missing fields: {', '.join(sorted(missing))}")
        if case["id"] in seen:
            raise ValueError(f"duplicate case id: {case['id']}")
        seen.add(case["id"])
        if case["domain"] not in DOMAINS:
            raise ValueError(f"case {case['id']} has unknown domain {case['domain']!r}")
        image_path = (path.parent / case["image"]).resolve()
        if not image_path.is_relative_to(path.parent.resolve()):
            raise ValueError(f"case {case['id']} image path escapes manifest directory")
        if not image_path.is_file():
            raise ValueError(f"case {case['id']} image does not exist: {case['image']}")
        if not isinstance(case["expected"], dict) or not isinstance(case["avoid"], list):
            raise ValueError(f"case {case['id']} expected must be an object and avoid a list")
    return data["cases"]


def load_scoreboard_cases(manifest_path: Path) -> list[dict[str, Any]]:
    """Adapt generated scoreboard ground truth into normal labeled cases."""
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("cases"), list):
        raise ValueError("scoreboard manifest must have schema_version 1 and a cases array")
    cases = []
    seen: set[str] = set()
    for item in data["cases"]:
        case_id = item.get("id")
        image = item.get("image")
        expected = item.get("ground_truth")
        if not case_id or not image or not isinstance(expected, dict):
            raise ValueError("scoreboard entries require id, image, and ground_truth")
        if case_id in seen:
            raise ValueError(f"duplicate scoreboard case id: {case_id}")
        seen.add(case_id)
        image_path = (manifest_path.parent / image).resolve()
        if not image_path.is_relative_to(manifest_path.parent.resolve()):
            raise ValueError(f"scoreboard case {case_id} image path escapes manifest directory")
        if not image_path.is_file():
            raise ValueError(f"scoreboard case {case_id} image does not exist: {image}")
        cases.append({
            "id": case_id,
            "domain": "gaming",
            "image": image,
            "image_root": str(manifest_path.parent.resolve()),
            "prompt": "Who won, and what was the final score?",
            "context": "I missed the game and want to know who won.",
            "expected": expected,
            "avoid": ["invented team", "stadium location", "innings"],
            "variation": item.get("variation"),
        })
    return cases


def evaluate(cases: list[dict[str, Any]], predictions: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Exact-match expected fields and count explicit avoid-term occurrences.

    Predictions map case IDs to structured JSON-like values. This deterministic
    scoring does not judge prose quality or replace human review.
    """
    rows = []
    for case in cases:
        prediction = predictions.get(case["id"], {})
        matched = {key: prediction.get(key) == value for key, value in case["expected"].items()}
        unresolved = [key for key in case["expected"] if prediction.get(key) is None]
        text = json.dumps(prediction, ensure_ascii=False).casefold()
        violations = [term for term in case["avoid"] if term.casefold() in text]
        answered = [key for key in case["expected"] if prediction.get(key) is not None]
        rows.append({"id": case["id"], "matched": matched, "answered_fields": answered,
                     "unresolved_fields": unresolved, "avoid_violations": violations})
    total = sum(len(row["matched"]) for row in rows)
    correct = sum(sum(row["matched"].values()) for row in rows)
    answered = sum(len(row["answered_fields"]) for row in rows)
    violations = sum(bool(row["avoid_violations"]) for row in rows)
    return {
        "case_count": len(rows),
        "field_count": total,
        "answered_fields": answered,
        "unresolved_fields": total - answered,
        "correct_fields": correct,
        "field_accuracy": correct / answered if answered else None,
        "coverage": answered / total if total else None,
        "cases_with_unsupported_claims": violations,
        "unsupported_claim_rate": violations / len(rows) if rows else None,
        "cases": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--scoreboards", type=Path, help="scoreboard output directory or ground_truth.json")
    parser.add_argument("--predictions", type=Path, help="JSON object mapping case IDs to predictions")
    args = parser.parse_args()
    cases = load_cases(args.cases)
    if args.scoreboards:
        manifest = args.scoreboards / "ground_truth.json" if args.scoreboards.is_dir() else args.scoreboards
        cases.extend(load_scoreboard_cases(manifest))
    if args.predictions:
        result = evaluate(cases, json.loads(args.predictions.read_text(encoding="utf-8")))
        print(json.dumps(result, indent=2))
    else:
        domains: dict[str, int] = {}
        for case in cases:
            domains[case["domain"]] = domains.get(case["domain"], 0) + 1
        print(json.dumps({"case_count": len(cases), "domains": domains}, indent=2))


if __name__ == "__main__":
    main()
