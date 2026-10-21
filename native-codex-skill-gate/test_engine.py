import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import engine
from engine import classify_task, route_task


class RouterTests(unittest.TestCase):
    def setUp(self):
        self.package = Path(__file__).resolve().parent

    def fixture(self, root: Path, *, skill_text: bytes = b"# Skill\nUse this guidance.\n", **catalog_updates):
        catalog = json.loads((self.package / "routing.json").read_text(encoding="utf-8"))
        catalog.update(catalog_updates)
        (root / "routing.json").write_text(json.dumps(catalog), encoding="utf-8")
        skill = root / "skills/implementation/SKILL.md"
        skill.parent.mkdir(parents=True, exist_ok=True)
        skill.write_bytes(skill_text)
        return catalog, skill

    def test_successful_route_and_structured_audit(self):
        with tempfile.TemporaryDirectory() as temp:
            audit = Path(temp) / "audit.jsonl"
            result = route_task("Implement a new endpoint", self.package, audit_path=audit)
            self.assertEqual(result["decision"], "ALLOW")
            self.assertEqual(result["classification"]["class"], "implementation")
            self.assertEqual(result["selected_skills"], ["implementation"])
            self.assertIn("smallest coherent", result["instructions"]["implementation"])
            self.assertEqual(result["loading_results"][0]["status"], "loaded")
            record = json.loads(audit.read_text(encoding="utf-8"))
            self.assertEqual(record["classification"]["class"], "implementation")
            self.assertEqual(record["selected_skills"], ["implementation"])
            self.assertEqual(record["loading_results"][0]["status"], "loaded")
            self.assertEqual(record["errors"], [])
            self.assertNotIn("instructions", record)

    def test_representative_classes_and_mixed_intent(self):
        cases = {
            "Debug why the test crashes with an exception": "debugging",
            "Review this patch for regressions": "review",
            "Plan the implementation steps for the migration": "planning",
            "What is the weather forecast tomorrow?": "unrelated",
            "Review the bug and implement a fix": "ambiguous",
            "Do not implement it; only review the change": "ambiguous",
        }
        for task, expected in cases.items():
            with self.subTest(task=task):
                self.assertEqual(classify_task(task)["class"], expected)

    def test_ambiguous_and_empty_tasks_block(self):
        for task in ("Review this bug and implement a fix", " "):
            with self.subTest(task=task):
                result = route_task(task, self.package)
                self.assertEqual(result["decision"], "BLOCK")
                self.assertEqual(result["errors"][0]["code"], "ambiguous_task")

    def test_unrelated_has_distinct_decision_and_loads_no_skills(self):
        result = route_task("Tell me a short joke", self.package)
        self.assertEqual(result["decision"], "UNRELATED")
        self.assertEqual(result["classification"]["class"], "unrelated")
        self.assertEqual(result["selected_skills"], [])
        self.assertEqual(result["instructions"], {})

    def test_malformed_json_duplicate_keys_and_nonstandard_constants_block(self):
        invalid_documents = (
            '{"schema_version":',
            '{"schema_version":1,"schema_version":1}',
            '{"value":NaN}',
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for document in invalid_documents:
                with self.subTest(document=document):
                    (root / "routing.json").write_text(document, encoding="utf-8")
                    result = route_task("Implement a feature", root)
                    self.assertEqual(result["decision"], "BLOCK")
                    self.assertEqual(result["errors"][0]["code"], "invalid_catalog")

    def test_invalid_metadata_blocks(self):
        updates = (
            {"max_skill_bytes": True},
            {"max_skill_bytes": engine.MAX_CONFIGURED_SKILL_BYTES + 1},
            {"skill_roots": ["../outside"]},
            {"skill_roots": ["docs"]},
            {"classifier_patterns": {"implementation": "("}},
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for update in updates:
                with self.subTest(update=update):
                    self.fixture(root, **update)
                    result = route_task("Implement a feature", root)
                    self.assertEqual(result["decision"], "BLOCK")
                    self.assertTrue(result["errors"])

    def test_missing_required_skill_blocks(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            catalog = json.loads((self.package / "routing.json").read_text(encoding="utf-8"))
            (root / "routing.json").write_text(json.dumps(catalog), encoding="utf-8")
            (root / "skills").mkdir()
            result = route_task("Implement a feature", root)
            self.assertEqual(result["decision"], "BLOCK")
            self.assertEqual(result["loading_results"][0]["error"], "missing_skill")

    def test_configurable_max_skill_file_size(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root, skill_text=b"# skill text longer than limit\n", max_skill_bytes=8)
            result = route_task("Implement a feature", root)
            self.assertEqual(result["decision"], "BLOCK")
            self.assertEqual(result["errors"][0]["code"], "oversized_skill")

    def test_invalid_utf8_empty_and_unreadable_skills_block(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root, skill_text=b"\xff")
            result = route_task("Implement a feature", root)
            self.assertEqual(result["errors"][0]["code"], "invalid_skill_encoding")

            skill = root / "skills/implementation/SKILL.md"
            skill.write_bytes(b" \n")
            result = route_task("Implement a feature", root)
            self.assertEqual(result["errors"][0]["code"], "invalid_skill_file")

            skill.write_text("# readable\n", encoding="utf-8")
            original_open = Path.open

            def deny_skill_open(path, *args, **kwargs):
                if path.name == "SKILL.md":
                    raise PermissionError("test permission denial")
                return original_open(path, *args, **kwargs)

            with mock.patch.object(Path, "open", deny_skill_open):
                result = route_task("Implement a feature", root)
            self.assertEqual(result["decision"], "BLOCK")
            self.assertEqual(result["errors"][0]["code"], "unreadable_skill")

    def test_path_traversal_and_outside_approved_root_block(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            catalog, _ = self.fixture(root)
            catalog["skills"]["implementation"]["path"] = "../outside/SKILL.md"
            (root / "routing.json").write_text(json.dumps(catalog), encoding="utf-8")
            result = route_task("Implement a feature", root)
            self.assertEqual(result["decision"], "BLOCK")
            self.assertEqual(result["errors"][0]["code"], "invalid_metadata")

            catalog["skills"]["implementation"]["path"] = "docs/SKILL.md"
            (root / "docs").mkdir()
            (root / "docs/SKILL.md").write_text("# outside approved root", encoding="utf-8")
            (root / "routing.json").write_text(json.dumps(catalog), encoding="utf-8")
            result = route_task("Implement a feature", root)
            self.assertEqual(result["decision"], "BLOCK")

    def test_skill_file_symlink_escape_blocks(self):
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            root = Path(temp)
            _, skill = self.fixture(root)
            external = Path(outside) / "SKILL.md"
            external.write_text("# outside", encoding="utf-8")
            skill.unlink()
            try:
                skill.symlink_to(external)
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            result = route_task("Implement a feature", root)
            self.assertEqual(result["decision"], "BLOCK")
            self.assertEqual(result["errors"][0]["code"], "invalid_skill_path")

    def test_approved_root_symlink_escape_blocks(self):
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            root = Path(temp)
            (root / "routing.json").write_text(
                (self.package / "routing.json").read_text(encoding="utf-8"), encoding="utf-8"
            )
            try:
                (root / "skills").symlink_to(Path(outside), target_is_directory=True)
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            result = route_task("Implement a feature", root)
            self.assertEqual(result["decision"], "BLOCK")
            self.assertEqual(result["errors"][0]["code"], "invalid_skill_path")

    def test_unexpected_loader_exception_blocks_without_raising(self):
        with mock.patch("engine._read_skill", side_effect=RuntimeError("simulated")):
            result = route_task("Implement a feature", self.package)
        self.assertEqual(result["decision"], "BLOCK")
        self.assertEqual(result["errors"][0]["code"], "internal_error")
        self.assertEqual(result["instructions"], {})

    def test_partial_audit_write_is_rolled_back_and_blocks(self):
        with tempfile.TemporaryDirectory() as temp:
            audit = Path(temp) / "audit.jsonl"
            real_write = os.write

            def short_write(fd, data):
                return real_write(fd, data[: max(1, len(data) // 2)])

            with mock.patch("engine.os.write", side_effect=short_write):
                result = route_task("Implement a feature", self.package, audit_path=audit)
            self.assertEqual(result["decision"], "BLOCK")
            self.assertTrue(result["audit_write_failed"])
            self.assertEqual(audit.stat().st_size, 0)

            def short_write_with_failed_rollback(fd, data):
                return real_write(fd, data[: max(1, len(data) // 2)])

            with mock.patch("engine.os.write", side_effect=short_write_with_failed_rollback), mock.patch(
                "engine.os.ftruncate", side_effect=OSError("simulated rollback failure")
            ):
                result = route_task("Implement a feature", self.package, audit_path=audit)
            self.assertEqual(result["decision"], "BLOCK")
            self.assertTrue(result["audit_write_failed"])
            self.assertGreater(audit.stat().st_size, 0)

    def test_audit_os_error_blocks(self):
        with tempfile.TemporaryDirectory() as temp:
            audit = Path(temp) / "audit.jsonl"
            with mock.patch("engine.os.write", side_effect=OSError("simulated disk failure")):
                result = route_task("Implement a feature", self.package, audit_path=audit)
            self.assertEqual(result["decision"], "BLOCK")
            self.assertEqual(result["errors"][-1]["code"], "audit_write_failed")

    def test_regexes_compile_and_use_only_bounded_wildcards(self):
        for patterns in engine.RULES.values():
            for pattern in patterns:
                with self.subTest(pattern=pattern.pattern):
                    recompiled = re.compile(pattern.pattern, pattern.flags)
                    self.assertEqual(recompiled.pattern, pattern.pattern)
                    self.assertNotIn(".*", pattern.pattern)
                    self.assertNotIn(".+", pattern.pattern)
        self.assertEqual(classify_task("x" * 100_000 + " review this")["class"], "review")


if __name__ == "__main__":
    unittest.main()
