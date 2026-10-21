# Native Codex Skill Gate: routing engine

This phase implements a standalone Python router. It does not install plugins,
configure Codex, call Codex hooks, or execute skill content.

## Run

From this directory:

```sh
python -m unittest -v
python engine.py "Implement a new API endpoint"
python engine.py "Debug why the API crashes" --audit /tmp/skill-routing.jsonl
```

The CLI prints the structured JSON result and exits `0` for `ALLOW` or
`UNRELATED`, and `2` for `BLOCK`. In Python, call
`route_task(task, package_root, audit_path=...)`. Loaded text is returned under
`instructions`; an optional JSONL audit record includes classification,
selected skill IDs, loading statuses, digests, and errors, but omits instruction
contents. Audit write errors block the result.

## Classification contract

`engine.py` uses a fixed set of case-insensitive regular expressions. A task
matching exactly one supported class routes to that class. A task matching
multiple classes is `ambiguous` and blocked. Empty input is also blocked.
No match is `unrelated` and allowed without a skill. This is explicit phrase
routing, not general natural-language understanding.

The skill-to-task mapping and required flags are defined in `routing.json`.
Every supported engineering class must have a required route. The catalog's
`skill_roots` lists approved roots, and `max_skill_bytes` sets the per-file
limit (1 byte to 8 MiB; default 256 KiB). Required skill files must resolve
inside an approved root, be regular UTF-8 files named `SKILL.md`, and be
non-empty. Missing, invalid, unreadable, or oversized required skills block
the result. Skill files are untrusted data: their contents are only read and
returned as text.

Catalog JSON rejects duplicate keys, non-standard constants, unknown fields,
and inconsistent mappings. Static classifier patterns are compiled in the
module; they are not supplied by the catalog. The patterns use bounded
wildcards. Multiple matched classes, including mixed positive/negative intent,
are conservatively classified as ambiguous and blocked.

## Limits

The engine decides classification and prepares instruction text; it cannot
prove that a model follows that text. It does not provide automatic Codex
skill activation or enforcement, and it is independent of Cloud and Windows
hook/runtime behavior. Classification precision is limited to the patterns
in `RULES`; unrecognized engineering phrasing can be treated as unrelated.
Review and extend those rules with tests when the supported vocabulary
changes. Symlinks are rejected in approved roots and skill paths; as with
ordinary portable filesystem checks, concurrent hostile filesystem mutation
during validation and open is outside this engine's threat model. Audit writes
use a single append operation and attempt rollback after a reported short
write; concurrent writers or storage failure can prevent safe rollback, and
the engine returns `BLOCK` when it cannot confirm a complete audit record.
