#!/usr/bin/env python3
"""Report explicitly designated task checkpoints from a Git remote."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Callable


TASK_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$")
STATES = {"PLANNED", "CLOUD_VERIFIED", "LOCAL_PENDING", "LOCAL_VERIFIED"}


class WatchError(Exception):
    """A poll could not safely advance its cursor."""


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode:
        raise WatchError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result


def parse_checkpoint(content: str) -> dict[str, str] | None:
    """Return an opted-in checkpoint, ignoring ordinary checkpoints."""
    if not re.search(r"(?m)^\*\*Automatic Handoff:\*\*\s*`ENABLED`\s*$", content):
        return None

    task = re.search(r"(?m)^\*\*Task ID:\*\*\s*`([^`]+)`\s*$", content)
    status = re.search(r"(?m)^\*\*Verification state:\*\*\s*`([^`]+)`\s*$", content)
    action = re.search(
        r"(?m)^\*\*Exact next (?:authorized (?:Local )?)?action:\*\*\s*(.+?)\s*$",
        content,
    )
    if not task or not TASK_ID.fullmatch(task.group(1)):
        raise WatchError("opted-in checkpoint has a missing or invalid Task ID")
    if not status or status.group(1) not in STATES:
        raise WatchError("opted-in checkpoint has a missing or invalid Verification state")
    if not action or not action.group(1).strip():
        raise WatchError("opted-in checkpoint has no exact next authorized action")
    return {"task_id": task.group(1), "status": status.group(1), "next_action": action.group(1).strip()}


def _load_state(path: Path) -> dict[str, str] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except (OSError, json.JSONDecodeError) as exc:
        raise WatchError(f"cannot read state file {path}: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("commit"), str) or not isinstance(data.get("branch"), str):
        raise WatchError(f"invalid state file: {path}")
    return data


def _save_state(path: Path, state: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
            temp_name = stream.name
            json.dump(state, stream, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)


def _checkpoint(repo: Path, commit: str, checkpoint_path: str) -> str | None:
    object_name = f"{commit}:{checkpoint_path}"
    if git(repo, "cat-file", "-e", object_name, check=False).returncode:
        # A commit without the checkpoint file is not a task checkpoint.
        return None
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "cat-file", "blob", object_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode:
            message = result.stderr.decode("utf-8", errors="replace").strip()
            raise WatchError(message or f"cannot read checkpoint at {commit}")
        parsed = parse_checkpoint(result.stdout.decode("utf-8"))
    except UnicodeError as exc:
        raise WatchError(f"checkpoint at {commit} is not valid UTF-8") from exc
    if parsed is None:
        return None
    safe_action = "".join(char for char in parsed["next_action"] if char.isprintable()).strip()
    if not safe_action:
        raise WatchError(f"checkpoint at {commit} has no printable next authorized action")
    parsed["next_action"] = safe_action
    return json.dumps({"commit": commit, **parsed}, sort_keys=True)


def poll(
    repo: Path,
    state_file: Path,
    remote: str = "origin",
    branch: str = "work",
    checkpoint_path: str = "CHECKPOINT.md",
    reporter: Callable[[dict[str, str]], None] | None = None,
) -> list[dict[str, str]]:
    """Fetch once, report new opted-in checkpoints, then atomically advance state."""
    old = _load_state(state_file)
    git(repo, "fetch", "--no-tags", remote, f"refs/heads/{branch}")
    tip = git(repo, "rev-parse", "FETCH_HEAD").stdout.strip()
    if not re.fullmatch(r"[0-9a-fA-F]{40,64}", tip):
        raise WatchError("remote returned an invalid commit ID")

    if old and old["branch"] != branch:
        raise WatchError(f"watched branch changed from {old['branch']} to {branch}; cursor preserved")

    if old:
        ancestor = git(repo, "merge-base", "--is-ancestor", old["commit"], tip, check=False)
        if ancestor.returncode:
            raise WatchError(f"{branch} moved to a history that does not contain the saved commit; cursor preserved")
        commits = git(repo, "rev-list", "--reverse", f"{old['commit']}..{tip}").stdout.splitlines()
    else:
        # First run establishes a baseline at the current tip.
        commits = [tip]

    found: list[dict[str, str]] = []
    for commit in commits:
        encoded = _checkpoint(repo, commit, checkpoint_path)
        if encoded:
            found.append(json.loads(encoded))

    if reporter:
        for task in found:
            reporter(task)
    _save_state(state_file, {"branch": branch, "commit": tip})
    return found


def default_state_path() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
    else:
        base = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state"))
    return base / "codex-automatic-handoff" / "cursor.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path, help="existing local Git clone to fetch into")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--branch", default="work")
    parser.add_argument("--checkpoint", default="CHECKPOINT.md")
    parser.add_argument("--interval", type=float, default=300, help="poll interval in seconds (default: 300)")
    parser.add_argument("--state-file", type=Path, default=default_state_path())
    parser.add_argument("--once", action="store_true", help="poll once and exit")
    args = parser.parse_args(argv)
    if args.interval < 30:
        parser.error("--interval must be at least 30 seconds")
    if Path(args.checkpoint).is_absolute() or ".." in Path(args.checkpoint).parts:
        parser.error("--checkpoint must be a repository-relative path without '..'")

    while True:
        try:
            def report(task: dict[str, str]) -> None:
                print(
                    f"Task ID: {task['task_id']}\n"
                    f"Commit SHA: {task['commit']}\n"
                    f"Checkpoint status: {task['status']}\n"
                    f"Next authorized action: {task['next_action']}\n"
                    "---",
                    flush=True,
                )

            poll(args.repo.resolve(), args.state_file, args.remote, args.branch, args.checkpoint, report)
        except (WatchError, OSError) as exc:
            print(f"Automatic Handoff poll failed; saved cursor preserved: {exc}", file=sys.stderr, flush=True)
            if args.once:
                return 1
        if args.once:
            return 0
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
