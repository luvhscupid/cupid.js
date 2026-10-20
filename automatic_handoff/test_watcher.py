import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from watcher import WatchError, poll


CHECKPOINT = """# Task checkpoint

**Automatic Handoff:** `ENABLED`
**Task ID:** `sample-42`
**Verification state:** `PLANNED`
**Exact next authorized action:** Review the task plan.
"""


def run(*args: str, cwd: Path | None = None) -> str:
    return subprocess.run(args, cwd=cwd, text=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip()


class WatcherIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.remote = self.root / "remote.git"
        self.source = self.root / "source"
        self.clone = self.root / "clone"
        self.state = self.root / "state.json"
        run("git", "init", "--bare", "--initial-branch=work", str(self.remote))
        run("git", "init", "--initial-branch=work", str(self.source))
        run("git", "-C", str(self.source), "remote", "add", "origin", str(self.remote))
        run("git", "-C", str(self.source), "config", "user.name", "Tests")
        run("git", "-C", str(self.source), "config", "user.email", "tests@example.invalid")
        self.write_checkpoint(CHECKPOINT)
        self.commit_and_push("initial")
        run("git", "clone", "--branch", "work", str(self.remote), str(self.clone))

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_checkpoint(self, content: str) -> None:
        (self.source / "CHECKPOINT.md").write_text(content, encoding="utf-8")

    def commit_and_push(self, message: str) -> str:
        run("git", "-C", str(self.source), "add", "CHECKPOINT.md")
        run("git", "-C", str(self.source), "commit", "-m", message)
        run("git", "-C", str(self.source), "push", "origin", "work")
        return run("git", "-C", str(self.source), "rev-parse", "HEAD")

    def test_first_observation_reports_designated_task_and_saves_cursor(self) -> None:
        tasks = poll(self.clone, self.state)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["task_id"], "sample-42")
        self.assertEqual(tasks[0]["status"], "PLANNED")
        self.assertEqual(tasks[0]["next_action"], "Review the task plan.")
        self.assertEqual(tasks[0]["commit"], run("git", "-C", str(self.source), "rev-parse", "HEAD"))
        self.assertEqual(json.loads(self.state.read_text())["commit"], tasks[0]["commit"])

    def test_new_commit_reports_once_and_restart_suppresses_duplicate(self) -> None:
        poll(self.clone, self.state)
        self.write_checkpoint(CHECKPOINT.replace("Review the task plan.", "Review implementation evidence."))
        commit = self.commit_and_push("update checkpoint")
        tasks = poll(self.clone, self.state)
        self.assertEqual([item["commit"] for item in tasks], [commit])
        self.assertEqual(poll(self.clone, self.state), [])
        self.assertEqual(poll(self.clone, self.state), [])  # fresh process, same cursor file

    def test_malformed_opted_in_checkpoint_does_not_advance_cursor(self) -> None:
        poll(self.clone, self.state)
        before = json.loads(self.state.read_text())
        self.write_checkpoint("**Automatic Handoff:** `ENABLED`\n**Task ID:** `broken`\n")
        self.commit_and_push("malformed checkpoint")
        with self.assertRaisesRegex(WatchError, "Verification state"):
            poll(self.clone, self.state)
        self.assertEqual(json.loads(self.state.read_text()), before)

    def test_reporting_failure_does_not_consume_task(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "output failed"):
            poll(self.clone, self.state, reporter=lambda _task: (_ for _ in ()).throw(RuntimeError("output failed")))
        self.assertFalse(self.state.exists())
        self.assertEqual(len(poll(self.clone, self.state)), 1)

    def test_transient_fetch_failure_preserves_cursor(self) -> None:
        poll(self.clone, self.state)
        before = self.state.read_bytes()
        run("git", "-C", str(self.clone), "remote", "set-url", "origin", str(self.root / "missing.git"))
        with self.assertRaises(WatchError):
            poll(self.clone, self.state)
        self.assertEqual(self.state.read_bytes(), before)

    def test_non_fast_forward_branch_change_preserves_cursor(self) -> None:
        poll(self.clone, self.state)
        before = self.state.read_bytes()
        initial = run("git", "-C", str(self.source), "rev-parse", "HEAD")
        self.write_checkpoint(CHECKPOINT.replace("Review the task plan.", "Second commit."))
        self.commit_and_push("second commit")
        poll(self.clone, self.state)
        before = self.state.read_bytes()
        run("git", "-C", str(self.source), "reset", "--hard", initial)
        run("git", "-C", str(self.source), "push", "--force", "origin", "work")
        with self.assertRaisesRegex(WatchError, "does not contain the saved commit"):
            poll(self.clone, self.state)
        self.assertEqual(self.state.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
