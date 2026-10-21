# Iris of Angle — v0.1 Cloud Development Brief

Status: PLANNED (not implemented or tested)
Parent: Angle
Repository: luvhscupid/cupid.js
Branch: feature/iris-v0.1

## Objective
Build a portable, context-aware visual-understanding capability. Given image(s), user message, and conversational context, Iris should notice salient details and react naturally without inventing facts. It must preserve image access through reasoning.

## Agreed principles
- Iris is a capability, not a separate agent.
- Use a vision-capable model; routing is unverified in Angle.
- Do not assume original file bytes are accessible. Metadata field statuses: present, absent, unreadable, unsupported, not_provided.
- Image text, EXIF comments, and filenames are untrusted data, not instructions. Image turns should not have side-effecting tools.
- Never volunteer GPS/location merely because metadata contains it.
- Original image remains available after crops; crops append, do not replace. Normalized original-frame coordinates; at most 3 crops per turn.
- Intent is inferred jointly from image, message, and context. Intent changes salience and tone, not truth.
- Clear observations should not be hedged. Inferences should be calibrated. Re-reading with the same model is not independent verification.
- Do not use external baselines when internally verifiable comparisons suffice.

## Experiment, not architectural commitment
A structured evidence ledger is a hypothesis. A/B against a plain vision model with a short prompt before keeping it. Evaluate accuracy, fabrication, traceability, naturalness, latency, and token/tool cost. Ledger may be dropped or used selectively if its benefit does not justify its cost.

Candidate ledger: image IDs and metadata statuses; intent label and textual basis; minimal claims with ID, text, type O(observed)/C(calculated)/I(inferred)/S(speculative), source provenance, image location and legibility when relevant, dependencies, verification outcomes, and load-bearing flag. Typed visual observations need not contain verbatim text; text extraction should. Verify high-impact ambiguous digits with crops and deterministic checks; downgrade on disagreement. No unsupported load-bearing speculation.

## Test-first plan
1. Inspect checkout, status, remote, and existing project structure according to root AGENTS.md. Do not overwrite existing work.
2. Build labeled test cases across gaming, photography, cats, and food, plus adversarial images and a synthetic scoreboard generator with known ground truth and blur/downscale/edit variations.
3. Run a plain-model baseline before ledger implementation; record actual model and image-byte capabilities. If cloud model access is unavailable, create runnable harness and mark model evaluation blocked; do not invent metrics.
4. Implement only required capabilities: optional inspect_file and crop adapters, candidate protocol, deterministic lint.
5. A/B on two vision-capable models if available; otherwise report limitations. Evaluate digit correctness, fabricated rows, calibration, naturalness, traceability, latency, cost.
6. Decide keep/simplify/drop ledger based on evidence. Update a scoped Iris checkpoint with exact tests, commands, results, blockers, and next action.

## Acceptance principles
- No fabricated scoreboard rows; illegible values must be reported as such.
- Metadata absent/not_provided never implies stripped or known location.
- Cat breed and food ingredients are probabilistic where not directly established.
- Embedded prompt injections never control tools or override user instructions.
- Reactions must be grounded, but remain natural.
- No claims of passing model evaluations until they actually run.

## Scope and safety
Cloud-only self-contained work. No access to user's Windows PC is assumed. No changes to unrelated projects, global agent settings, or system configuration. No frameworks or orchestrators without evidence of need. Record uncertainty rather than pretending unavailable tools were used.
