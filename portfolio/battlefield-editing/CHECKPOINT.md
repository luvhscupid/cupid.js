# Battlefield 6 Highlight Portfolio Checkpoint

**Verification state:** `PLANNED`

## Relevant Git commit

Planning base: `f15b7a5984c5e83edc9bc6b4fcc755fbc79f80f6` (`origin/main` before this task). The documentation commit is reported in the handoff summary.

## Task objective

Create one professional 25–35 second Battlefield 6 highlight video that demonstrates short-form editing skill to potential paying clients.

## Approved decisions

- Cloud Codex handles planning, research, and project documentation.
- Windows Local Codex handles footage inspection, selection, Premiere Pro editing, and export verification.
- The original footage and all media artifacts remain on the PC; Git tracks documentation only.
- Keep the scope to one sample and do not install dependencies or build an automated editor.

## Completed work

- Defined responsibilities, acceptance criteria, handoff boundaries, and a staged plan.
- Local Codex has inventoried 74 video files totaling approximately 63 GiB. Their contents remain unverified.
- FFmpeg availability remains unresolved.

## Verification and evidence

- No footage inspection, clip selection, edit, or export verification has been performed or claimed.
- `PLANNED` means the media workflow has not started; no creative or technical result is asserted.

## Unresolved blockers

- Footage contents and usable moments need local review.
- FFmpeg availability is unknown.
- No Premiere Pro project or export exists yet.

## Exact next action

On Windows, Local Codex: check FFmpeg availability with `Get-Command ffmpeg -ErrorAction SilentlyContinue`; then inspect the existing inventory and review the source clips locally to verify which files contain usable Battlefield 6 footage. Report the result (including whether FFmpeg was found and candidate filenames with time ranges) in this checkpoint without adding media or PC-specific paths to Git. Do not begin the Premiere Pro edit until footage contents and candidate moments are confirmed.
