# Native Codex Skill Gate: compatibility and design report

**Checked:** 2026-10-21
**Scope:** Codex Cloud (this managed cloud workspace) and future Codex on Windows
**Decision:** No prototype was created. Official docs do not establish plugin-hook support for Codex Cloud and explicitly exclude plugin hooks from cloud-orchestrated ChatGPT Work; this environment exposes no Codex plugin runtime or hook test facility. Per project stop conditions, a local-only simulation would not establish Cloud enforcement.

## Verdict

| Target | Verdict | Evidence |
|---|---|---|
| Codex Cloud / cloud-orchestrated Work | **UNSUPPORTED** for deterministic skill gating | Official docs do not document Codex Cloud plugin-hook support and state plugin hooks are not supported in cloud-orchestrated ChatGPT Work. This managed environment reported `provider: cloud`, `connectivity: offline`, no capabilities, and `observed_phase: pending`. No hook execution or fail-closed test was possible here. |
| Codex on Windows | **PARTIAL** (documented integration, unverified deployment) | Codex documents plugin lifecycle hooks and a Windows-specific `commandWindows` override, plus `windows_managed_dir` for enterprise-managed hooks. Docs describe plugin lifecycle hooks as supported when manually installed in Codex desktop. Windows execution, hook trust, prompt blocking, and skill injection were not tested on a Windows Codex runtime. |

“PARTIAL” does not mean enforcement is proven. Do not claim deterministic gating on Windows until a real Codex Windows run observes hook execution, successful context injection, missing-skill blocking, and hook-failure behavior.

## Official documentation findings

Sources, checked on 2026-10-21:

- [Plugins](https://developers.openai.com/codex/plugins) — plugins work across supported surfaces; Codex plugins can include skills, MCP servers, browser extensions, and hooks. It explicitly says plugin hooks are not supported in cloud-orchestrated ChatGPT Work. Installing a plugin on the web does not deploy hook scripts to an execution environment.
- [Build plugins](https://developers.openai.com/plugins/build/plugins) — portable packages use a root `plugin.json`, `skills/`, and optional `hooks/`; Codex-specific hook configuration can be referenced under `extensions.com.openai.hooks`. Bundled hook scripts must exist in the execution environment and remain untrusted until reviewed. Lifecycle hooks are described as supported for manually installed Codex desktop plugins; lifecycle-hook plugins are ineligible for the public plugin directory.
- [Hooks](https://developers.openai.com/codex/hooks) — describes events, schemas, local command and MCP handlers, trust, and failure behavior. The page distinguishes cloud-orchestrated Work from local execution and states that personal accounts and Work Cloud without local access do not use enterprise remote MCP hooks. Plugin/local command hooks are not supported by that cloud orchestration path.

### Hook contract relevant to this design

- Events documented include `SessionStart`, `SubagentStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SubagentStop`, `Stop`, `Interrupt`, and `SessionEnd`.
- `SessionStart` runs on session startup/resume/clear/compact/fork. It does **not** execute before every user prompt, so it cannot alone satisfy per-task gating.
- `UserPromptSubmit` runs on each prompt submission in a supported local hook runtime. It receives JSON on stdin including `prompt`, `cwd`, session identifiers, and permission mode. Plain stdout is added as developer context; JSON `hookSpecificOutput.additionalContext` also injects developer context. `{ "decision": "block", "reason": "..." }` or exit code 2 with a reason on stderr can block the prompt.
- `PreToolUse` can block supported local tool calls through a supported deny decision or exit code 2, but it is after the prompt has entered the agent loop. Its event-specific deny shape is not a general skill-loading gate.
- A command-hook error/timeout is reported as a hook failure. The docs do not describe arbitrary command failure as an automatic deny. Fail-closed behavior must be explicit: the hook must catch missing/unreadable skill inputs and return a supported prompt-block decision. For remote MCP hooks, missing servers, errors, timeouts, and malformed responses do not block; only an explicit supported denial does. Therefore MCP is not a suitable fail-closed loader.
- A SessionStart MCP hook can run before its MCP server is ready and does not block the session.
- Hooks receive cwd and event metadata; session transcript path is available but documented as unstable. They do not receive a native “load this skill by name” API. A command hook could read a packaged skill file and add its contents as `additionalContext`; this is context injection, not proof that Codex's native skill activation/selection occurred.
- Matching command hooks for the same event start concurrently. One cannot depend on another matching hook to finish first. Non-managed hooks require review/trust. Some specialized tool paths can opt out of the normal hook path, so tool hooks are guardrails rather than a complete enforcement boundary.

### Capability answers

| Question | Finding |
|---|---|
| Does Cloud run plugin hooks? | Not in cloud-orchestrated ChatGPT Work per the official plugin docs. This environment did not expose a plugin runtime that could contradict or qualify that statement. |
| Is there a before-each-task event? | `UserPromptSubmit` is the documented per-prompt event for supported hook runtimes. `SessionStart` is session-scoped, not per prompt. Cloud-orchestrated Work does not support plugin hooks, so the event does not provide Cloud integration here. |
| Can hooks add skill instructions? | A local `UserPromptSubmit` command can add developer context as text. There is no documented hook API that invokes the native skill loader by skill identifier. Reading a packaged `SKILL.md` and injecting its content is possible as a design, subject to local file availability and context limits. |
| Can hooks fail closed? | A local `UserPromptSubmit` hook can explicitly block when it detects a missing skill. The docs do not make hook process failure itself fail closed; the hook must return the supported block result. No observed fail-closed test was run. Cloud cannot use this plugin-hook mechanism. |

## Minimal portable design (not implemented)

If a supported local target is later available for verification, the smallest candidate package is:

```text
native-codex-skill-gate/
  plugin.json
  routing.json
  skills/
    <required-skill>/SKILL.md
  hooks/
    hooks.json
    route_and_load.py
  audit/                 # runtime writable location, outside immutable package as needed
```

- **Manifest:** portable root `plugin.json`; OpenAI hook reference under `extensions.com.openai.hooks`. Keep plugin identity separate from Codex-specific hook configuration.
- **Catalog/policy:** `routing.json` maps task classes to skill IDs, relative skill paths, and required status. Plugin-owned implementation skills remain manual-only; the router selects and injects instructions but does not execute skill procedures on its own.
- **Classification:** conservative deterministic rules over the submitted prompt (explicit task verbs, file/code references, test/build/debug terms). Ambiguous classification should map to a configured safe default or block when a required skill cannot be established. LLM-based classification would not be deterministic and should not be treated as enforcement.
- **Loading:** on `UserPromptSubmit`, resolve the selected skill under `PLUGIN_ROOT`, validate it is a readable regular file within the plugin root, then inject concise instructions from its `SKILL.md` using `additionalContext`. Treat absent, malformed, unreadable, or policy-mismatched required skills as an explicit prompt block. This is hook-based context injection, not native skill-loader invocation.
- **Audit:** append JSONL records in `PLUGIN_DATA` with session/turn ID, task class, selected skill ID, content digest, outcome (`injected`, `blocked`, `unclassified`, `error`), and UTC time. Avoid storing raw prompts or skill contents by default. Audit write failure must block if audit is a required assurance.
- **Execution:** selection and injection are separate from actually following the selected skill. A hook cannot prove that later model behavior complied with the instructions. Post-turn checks could report evidence but cannot retroactively enforce skill use.

The hook-integrated plugin and disposable Codex fixture remain unimplemented because a supported Codex Cloud integration point was not established. A separate hook-free Phase 1 router was implemented afterward; it can classify, validate, and return instruction text in standalone tests and CLI runs, but it does not activate Codex skills or establish Cloud/Windows hook behavior. See `README.md`, `engine.py`, `routing.json`, and `test_engine.py` for that portable engine.

## Windows deployment plan (future, conditional)

1. Use Codex desktop on Windows with a manually installed local plugin; verify the relevant build-plugin and Windows hook support remains current at deployment time.
2. Keep the portable manifest, routing catalog, skills, and policy implementation platform-neutral. Use the documented `commandWindows` override (or `command_windows` in TOML) only for interpreter/path invocation differences.
3. Ensure scripts and packaged skills are present on disk; plugin installation from a web surface does not deploy them. Keep all referenced paths inside the plugin root. For enterprise-managed deployment, admins can deploy scripts separately via MDM and configure `windows_managed_dir` in managed configuration.
4. Install/enable, then explicitly review and trust the hook. A plugin being enabled does not automatically trust its hooks.
5. On a disposable fixture, verify: implicit prompt classification without skill name; correct skill digest/context; missing skill yields a visible prompt block; unreadable file and nonzero hook error behavior; repeated prompts trigger the hook; audit records exist; and behavior when hook trust is absent or revoked.
6. Only mark Windows PASS after an observed fail-closed missing-skill case and a separate observed hook-execution record on the actual Windows Codex runtime. Current result remains PARTIAL.

## Tests and results

- Official documentation fetch: **PASS**; pages above retrieved from `developers.openai.com` on 2026-10-21.
- Environment capability snapshot: **observed, unsuitable for runtime testing** — cloud provider, connectivity offline, empty capabilities, observed phase pending.
- Automatic loading without naming a skill: **NOT RUN** in Codex. The standalone router has unit-tested deterministic classification and text loading only.
- Missing-skill behavior: **NOT RUN**.
- Fail-closed behavior: **NOT RUN**.
- Hook execution and loading evidence: **NONE**.
- Hook-integrated plugin source/fixture: **NOT CREATED** by design, because Codex Cloud plugin-hook support is not documented and the requested Cloud prototype gate is unmet.

## Limits

The documentation supports a local Codex hook design, but it does not establish that local Windows hook execution works in this workspace. The current Cloud-specific verdict is based on the absence of a documented Codex Cloud plugin-hook integration, the explicit cloud-orchestrated Work limitation, and this task's observed managed-cloud context. No claim is made about undocumented internal runtimes or future product changes.
