# Local capability integration specification

## Scope and current evidence

This document specifies how a future local integration can resolve and invoke existing Codex capabilities. It does not change the Phase 1 router, invoke capabilities, install software, or change Codex configuration. Capability selection and native invocation are separate operations. Skill text is not copied into this project or treated as executable code.

The current development session is Codex Cloud. Its visible skill catalog did not contain Superpowers, ADHD, or Drill-Me; no Codebase Memory MCP tools or resources were exposed; and the executor skill catalog was empty. The workspace scan did not reveal local installations of these named capabilities. This establishes only that they were not exposed in this Cloud session/workspace. It does not establish whether they are installed on the user's Windows machine. The project `AGENTS.md` records intended usage rules, not proof of installation or a native invocation contract. Codex on Crack's actual contents and behavior have not been inspected, so it has no assigned role.

The existing router classifies tasks and loads configured instruction files. It is not evidence that a third-party skill/plugin/MCP capability was natively invoked. Do not mark a capability `INVOKED` or `VERIFIED` based on catalog visibility, reading its skill file, or routing to its name.

## Registry

Use [`capability-registry.schema.json`](capability-registry.schema.json) for a portable JSON registry. Keep one record per distinct installed capability/entry point. Do not assume the requested display names match installed names. Preserve the exact observed name, package identifier, path, server identifier, and tool identifier. Unknown values remain `null` or `unknown`; do not fill them from guesses.

Each record includes:

- A stable project-local `id` and the observed `actual_name`.
- `integration_type`: `skill`, `plugin`, `MCP`, `other`, or `unknown` until confirmed.
- `native_invocation`: the documented and observed native mechanism, exact entry point, and any supported explicit or implicit invocation mode.
- `installation`: observed path or package/tool/server identifier, with the discovery scope.
- `restrictions`: invocation policy and any documented constraints.
- `status`: one of the lifecycle values below, plus evidence fields.

Statuses describe evidence, not preference:

| Status | Meaning |
| --- | --- |
| `DISCOVERED` | A local catalog, manifest, or installation record identifies the capability; callability has not been established. |
| `AVAILABLE` | The native Codex surface exposes a supported invocation entry point in the recorded environment. No call has yet been observed. |
| `INVOKED` | A native call/activation was observed and captured, but its intended effect has not yet been verified. |
| `VERIFIED` | Native invocation and the capability-specific expected effect were both observed. |
| `UNAVAILABLE` | A bounded, recorded scan found no usable installation or entry point in the specified scope. This is not a global absence claim. |
| `BLOCKED` | The capability was found, but a documented restriction, permission boundary, or runtime failure prevents invocation. Record the reason. |

Status is assigned per environment and Codex surface. A Windows result must not be inferred from Cloud evidence or vice versa. Move from `AVAILABLE` to `INVOKED` only with invocation evidence; move to `VERIFIED` only with effect evidence. If an earlier result becomes stale (version, account, installation, or policy changed), repeat verification and update the evidence.

## Resolution architecture

Keep these stages independent:

1. **Task classification**: the existing deterministic router emits supported task classes and any ambiguity. It does not inspect installed capability packages and does not decide that a capability was invoked.
2. **Capability resolution**: a future resolver maps classified task classes and user/project policy to zero or more registry records. It filters out records that are not `AVAILABLE`, `INVOKED`, or `VERIFIED` for the active environment, and respects each record's restrictions. It reports unresolved requirements as `UNAVAILABLE` or `BLOCKED`; it does not load replacement instructions or impersonate an integration.
3. **Native invocation**: a future dispatcher uses only the mechanism and entry point recorded for a capability (for example, Codex native skill activation or a named MCP tool call). The dispatcher must not simulate activation by reading skill files. No dispatcher/adapter is specified or implemented here because the actual local contracts are not yet inventoried.
4. **Evidence and audit**: record classified task, candidate and selected capability IDs, selection reason, status before and after, native entry point, invocation evidence, expected-effect evidence, errors, and environment/version. Avoid recording sensitive prompt or repository content unless the test requires it and the user has approved that retention.

The resolver may select multiple capabilities when their roles are complementary. It should assign one capability per workflow step, avoid running duplicate ideation/review/learning workflows, and retain the reason for each selected capability. A capability being selected is not evidence of its invocation.

## Initial routing policy

Apply this policy only after each capability's actual installation, native mechanism, and restrictions have been inspected and recorded:

| Capability | Intended resolution rule |
| --- | --- |
| **Superpowers** | Preferred engineering workflow for applicable engineering tasks, subject to its actual installed skill descriptions and invocation restrictions. Do not assume every task class maps to every Superpowers skill. |
| **ADHD** | May replace Superpowers brainstorming for a task where its inspected description/preflight says it is appropriate. For that ideation step, select one of ADHD or Superpowers brainstorming, never both. ADHD does not replace unrelated Superpowers engineering workflows. |
| **Drill-Me** | Select only when the task is learning, retrieval practice, explanation, or a requested understanding check. Do not attach it to ordinary implementation merely because it is available. |
| **Codebase Memory MCP** | Optional repository-context supplement. Invoke only through its observed MCP server/tool names and restrictions. It does not replace engineering workflows and is not authoritative; corroborate relevant findings against the checkout. If absent, proceed with normal repository inspection. |
| **Codex on Crack** | No role is assigned until its installed package, bundled skills, tools, instructions, side effects, and invocation restrictions are inspected. After inspection, document a proposed role and evidence for review before adding it to routing policy. |
| **Other locally discovered capabilities** | Record and inspect them before routing. Assign only a narrow, complementary role supported by their actual native description and observed invocation contract. Do not recreate or bundle their instructions. |

If a task is ambiguous or combines intents, preserve the classifier's ambiguity and resolve only clearly applicable workflow steps. Do not silently choose multiple competing workflows to hide ambiguity. If a required capability is unavailable or blocked, report that state explicitly; do not substitute a locally created skill without an explicit policy decision.

## Local discovery procedure

Perform discovery read-only on the target Windows installation. Record the date, Windows user context, Codex product/surface and version, workspace scope, and the exact locations and catalogs inspected.

1. Inspect the Codex-supported skill and plugin listings available in that installation. Record exact displayed names, IDs, descriptions, source/package identifiers, activation controls (including whether implicit invocation is permitted), and any native invocation guidance. A visible name alone yields at most `DISCOVERED`.
2. Inspect user and project skill/plugin directories that Codex documents for that installed version. Record resolved paths and package manifests. Do not follow links outside the intended discovery scope without noting the resolved destination. Do not edit files or configuration.
3. Inspect the Codex-supported MCP server/tool listing. For Codebase Memory, record exact server name, tool names, schemas/descriptions, connection state, and read/write effects. A project instruction mentioning MCP is not proof that the server is connected.
4. Inspect Superpowers, ADHD, Drill-Me, and Codex on Crack package contents and descriptions as installed. Record each bundled skill/tool and its stated restrictions. For Codex on Crack, inspect the full package surface and side effects before proposing any role.
5. Search the same documented local catalogs for other relevant user-installed third-party skills and tools. Include only capabilities with an identifiable local record; do not infer installed status from web listings or names in project documentation.
6. Assign `UNAVAILABLE` only after recording a bounded scan that finds no usable entry point in that scope. Use `BLOCKED` when present but restricted or permission-denied. Do not describe either as globally absent.
7. Populate the registry with evidence references. Keep user-specific paths and identifiers local; redact them before sharing the registry externally.

If a surface does not provide a supported listing or activation interface, record that limitation. Do not use undocumented files, runtime patches, shell launchers, or private APIs to manufacture an integration.

## Windows invocation and verification plan

This plan verifies the installed capabilities through Codex's own supported mechanisms. It does not authorize installation or configuration changes. Use a disposable workspace and test data; perform any setup only under a separate approved task.

1. **Freeze the test context.** Record Codex version/channel, Windows version, signed-in profile, workspace, active policy, and test date. Export or copy the current registry for evidence; do not change Codex settings.
2. **Discover and classify.** Follow the local discovery procedure. For each target, capture its exact native mechanism and restrictions before attempting invocation. Keep unknown contracts unknown.
3. **Check availability.** Confirm that Codex exposes the actual native entry point in this context: the skill's supported activation path, the plugin's supported surface, or the connected MCP server and tool. Mark `AVAILABLE` only then. Record errors as `BLOCKED` or `UNAVAILABLE` with scope and reason.
4. **Test automatic activation where supported.** In a fresh disposable conversation/workspace, issue a representative natural-language task without naming the capability. Capture the native activation/tool event or other first-party trace. Use a task that maps narrowly to one inspected capability. If implicit activation is disallowed or unsupported, record that; test the documented explicit native invocation separately, without claiming automatic routing.
5. **Test explicit native invocation.** Invoke each capability through the exact UI/API/tool call documented by the installed Codex surface. For Codebase Memory, make a read-only query against a disposable repository containing a known marker and confirm that the MCP tool call and returned evidence are attributable to the expected server/tool. Do not use a project-side file read as a substitute.
6. **Verify effect separately.** Check an observable capability-specific result: e.g. the expected Superpowers workflow step, ADHD ideation output when selected, a Drill-Me retrieval prompt for a learning request, or a relevant Codebase Memory result. Skill visibility or an activation event alone is insufficient. Mark `INVOKED` after the call is observed; mark `VERIFIED` only after the expected effect is observed.
7. **Exercise routing boundaries.** Test an engineering task (Superpowers preferred), a brainstorming task where ADHD's inspected preflight applies (ADHD replaces only that brainstorming step), a learning task (Drill-Me), an unrelated task (none selected), and a mixed/ambiguous task (ambiguity retained and no duplicate workflow). Verify optional Codebase Memory can be omitted without blocking ordinary repository work.
8. **Check restrictions and failures.** Test a task that should not activate each capability, confirm restrictions are honored, and record a blocked/failed native call. Test unavailable entry points using the resolver's reported status, not by breaking the user's installation. A routing error should fail closed for a capability explicitly required by policy; optional Codebase Memory failure should be reported and allow repository inspection to continue.
9. **Inspect Codex on Crack before role assignment.** Do not route a task to it during this test until its package content, tools, restrictions, and side effects have been reviewed. Then document its candidate role and obtain review of the policy before any subsequent routing test.
10. **Retain evidence.** Store registry snapshots and minimal native activation/tool traces with test inputs, expected results, actual results, status, and relevant version identifiers. Remove disposable test data after recording results. Do not claim `VERIFIED` without a native invocation record and an expected-effect observation.

## Current disposition

No local Windows installation inventory or native invocation test was possible from the current Codex Cloud workspace. The named targets remain unverified for Windows. The Cloud observations above are scoped to this session. The registry schema and plan are ready for a local read-only inventory; integration implementation should wait until that inventory establishes the supported native contracts.
