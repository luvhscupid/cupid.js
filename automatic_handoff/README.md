# Automatic Handoff v0.1

A small Python 3 standard-library watcher that fetches `origin/work` and reports explicitly opted-in task checkpoints. It reports only. Checkpoint text is treated as data and is never executed, passed to a shell, or sent to Codex.

## Opt in a checkpoint

The watched branch must contain `CHECKPOINT.md` (or another path supplied with `--checkpoint`) with these fields:

```markdown
**Automatic Handoff:** `ENABLED`
**Task ID:** `task-123`
**Verification state:** `PLANNED`
**Exact next authorized action:** Review the proposed task.
```

Only `PLANNED`, `CLOUD_VERIFIED`, `LOCAL_PENDING`, and `LOCAL_VERIFIED` are accepted. Ordinary checkpoints without the explicit `ENABLED` marker are ignored. Use a new commit for each checkpoint update that should be reported.

## Run

From a local clone that has an `origin` remote and can fetch `work`:

```powershell
py -3 automatic_handoff\watcher.py C:\path\to\clone --once
py -3 automatic_handoff\watcher.py C:\path\to\clone --interval 300
```

The default interval is five minutes and intervals below 30 seconds are rejected. The cursor is stored under `%LOCALAPPDATA%\codex-automatic-handoff\cursor.json` on Windows, or `$XDG_STATE_HOME/codex-automatic-handoff/cursor.json` (default `~/.local/state/...`) elsewhere. Use `--state-file` to select another location. The watcher fetches Git objects only; it does not check out branches or edit the working tree. On first run it considers the current tip. Later runs scan commits after the saved commit. A fetch error, malformed opted-in checkpoint, branch change, or corrupt state file leaves the cursor unchanged and reports the failure.

## Tests

From this directory run `py -3 -m unittest -v` on Windows or `python3 -m unittest -v` elsewhere. Tests create isolated temporary bare and working Git repositories and use no third-party packages.

## Manual Windows smoke test

1. In a disposable local clone, confirm `git status --short` is clean and that `origin/work` is fetchable.
2. Run `py -3 automatic_handoff\watcher.py C:\path\to\clone --once --state-file $env:TEMP\handoff-cursor.json`. On first run, a designated `CHECKPOINT.md` at the remote tip should print its task ID, SHA, status, and next action. A normal checkpoint should print no task.
3. Run the same command again; it should not repeat the same commit.
4. Commit and push a new checkpoint with the opt-in fields to `work`, then run again. It should report that commit once.
5. Change the remote URL to an unreachable test URL and run again. It should print a fetch error and leave the state JSON unchanged. Restore the URL afterward.

The watcher does not execute the reported action. A human reviews and acts on the report separately.
