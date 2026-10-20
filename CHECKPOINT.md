# Automatic Handoff live detection test

**Automatic Handoff:** `ENABLED`
**Task ID:** `live-detection-20261020-42536be`
**Verification state:** `PLANNED`

## Relevant Git commit

Windows watcher baseline: `42536be25b177e6fb9e61cb37c2c77bf30dc2f42` on `origin/work`.

## Task objective

Publish one explicitly opted-in, harmless checkpoint to test live detection by the Windows watcher.

## Approved decisions

- Use the documented `Automatic Handoff: ENABLED` opt-in and default root checkpoint path.
- The checkpoint is data for detection and reporting only. Its action must not be executed.

## Completed work

- Prepared this single checkpoint with a unique task ID, `PLANNED` status, and the requested harmless action.

## Test and supporting evidence

- The watcher's `parse_checkpoint` returned the expected task ID, `PLANNED` status, and exact next action. `git diff --check` passed. No task action has been run.

## Unresolved blockers

- Windows watcher detection remains to be observed.

**Exact next authorized action:** Report that the live Cloud-to-Windows checkpoint was detected. Do not execute anything.
