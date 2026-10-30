# Developer Evolution

An auditable Codex skill that turns local coding conversations and verified project knowledge into personal preferences, repository engineering guidance, code explanation skills, and concise global working agreements.

It analyzes repeated decisions, corrections, frustrations, and collaboration patterns across prior sessions. It proposes changes for review instead of silently rewriting its own instructions.

## What it does

- Reads completed local Codex session transcripts.
- Removes host context, tool output, credentials, authentication headers, and signed URL parameters before analysis.
- Distinguishes durable preferences from project constraints and one-off experiments.
- Requires evidence from multiple sessions before proposing a global instruction.
- Records contradictions instead of forcing them into one preference.
- Produces numbered proposals that require explicit human approval.
- Creates and continuously improves the profile skill's preferences, trigger description, scope, exceptions, and reference organization on subsequent requested runs.
- Preserves contextual and project-specific preferences without requiring them to become global rules.
- Preserves explicit engineering corrections about legacy or newly generated code, so future reuse decisions can avoid known rejected patterns and find the supplied alternative.
- Routes project engineering corrections to existing repository skills, and short project-wide invariants to project `AGENTS.md`, so the guidance travels with the code.
- Updates the approved personal, repository, or global targets within the user's authorization, keeping private evidence out of repositories.
- Generates general or project code explanation skills, grounding project knowledge in current source and reusing approved personal explanation preferences.
- Uses incremental checkpoints to skip unchanged sessions.
- Runs only when explicitly invoked as `$developer-evolution`.

## How it works

```text
Codex sessions
      ↓
redacted evidence bundle
      ↓
personal + repository + global guidance, private decision history
      ↓
numbered proposal
      ↓
human approval
      ↓
developer-profile      repository skills / AGENTS      global AGENTS
      ↓                            ↓                        ↓
personal preferences     project engineering       stable agreements
```

Collection and checkpoint updates use a two-phase workflow. The collector creates a checkpoint candidate, but processing state advances only after the analysis or no-change report is safely written. A failed analysis is retried on the next run.

The collector writes to a unique private file under the skill's `evidence/` directory when no output path is supplied. Explicit output paths outside that directory and attempts to overwrite an existing bundle are rejected, and evidence is never printed to stdout.

`developer-profile` is the daily-use output for personal preferences: Codex can select it automatically for relevant engineering, product, or communication choices, then read only the applicable profile sections. Project implementation rules live in the repository's relevant skills or `AGENTS.md` and can be used without the author's personal profile. `developer-evolution` remains the explicitly invoked author of reviewed changes; it runs no background process. Automatic skill selection is permitted, not guaranteed on every task.

The profile routes substantive design, implementation, code review, and code explanation to the relevant approved preferences. A task can move between these activities; newly relevant entries are consulted as needed. One preference can serve several activities without maintaining separate copies. A separately authorized global `AGENTS.md` route can require this lookup; profile creation alone does not install that rule. Ordinary factual answers and mechanical actions do not require it.

## Install

Ask Codex to install the `developer-evolution/` subdirectory from this repository:

```text
Use $skill-installer to install developer-evolution from
https://github.com/yukkit/developer-evolution-skill/tree/main/developer-evolution
```

The installed skill becomes available on the next turn.

Implicit invocation is disabled because this skill reads private history and writes local analysis artifacts. Invoke it explicitly with `$developer-evolution` whenever you want it to run.

## Use

Run an initial analysis without changing active instructions:

```text
Use $developer-evolution to initialize my personalization workspace and analyze
my recent Codex history. Generate proposals only; do not modify AGENTS.md.
```

Later runs are incremental by default:

```text
Use $developer-evolution to analyze new or changed sessions and propose updates.
```

To create the daily-use skill from an existing approved descriptive profile:

```text
Use $developer-evolution to migrate my approved developer profile into a
developer-profile skill for daily use, preserving its scope and exceptions.
```

The creation helper consumes a reviewed profile with runtime authorization; it never imports watchlist or rejected candidates. Later approvals edit the existing skill rather than resetting it from a template. Reinstalling `developer-evolution` preserves the separately generated personal skill.

Use a full reconciliation when needed:

```text
Use $developer-evolution to perform a full reconciliation scan and propose updates.
```

## Learn from code that should not be copied

Feedback such as “this implementation has a problem,” “do not follow this example,” or “new code should do this instead” can contain a durable engineering constraint. The analyzer preserves the specific rejected behavior, its reason, project or technology scope, a useful code locator, and the alternative the user supplied. A clear scoped correction can support a proposal from one session; it does not need to qualify as a global working agreement.

For example, if the user says that `sample-app`'s `LegacyPanel` copies display props into state and becomes stale, then asks new panels to derive display values from props, the proposal puts that state-ownership constraint in the repository's relevant panel-development skill. It preserves any exception for editable drafts and does not ban reuse of everything in `LegacyPanel` or extend the rule to unrelated projects.

Choose where guidance belongs by what it governs:

| Guidance | Preferred home |
| --- | --- |
| A project implementation pattern, negative example, or replacement approach | Existing relevant repository skill and its references |
| A short invariant that must apply throughout a project | Project `AGENTS.md` |
| A personal decision criterion, including explicitly private contextual preferences | Personal `developer-profile` |
| A stable universal working agreement meeting the evidence threshold | Global `AGENTS.md` |

Inspect the repository's actual skill layout and reuse an existing domain skill before proposing a new one. Substantial examples can live in a reference linked from its `SKILL.md`. Keep one authoritative rule; a personal profile may link to it, but should not maintain a duplicate copy. Repository files contain the engineering conclusion; chat evidence, confidence records, and approval history remain in the private analysis workspace.

Ask for a focused analysis with:

```text
Use $developer-evolution to review my recent corrections about problematic code
and examples that should not be copied. Propose updates to the affected
repositories' relevant skills, preserving what to avoid, why, and what to do
instead, and make them discoverable when choosing reuse candidates or extending
existing code. Keep personal preferences separate.
```

After authorized application, the relevant repository skill routes implementation decisions to these rules, including for collaborators without the author's personal profile. Codex should check the current code before applying a behavior-specific warning: a fixed implementation can become a valid example again, while a renamed file can still contain the rejected behavior. An unconditional ban remains in effect until the user changes it. Vague complaints with no identifiable objection remain uncertain observations, and a rejected proposal to add guidance stays rejected.

This uses the existing Analyze/Apply workflow. Analyze inspects repository instructions read-only and stages proposals privately; Apply updates only authorized targets. Feedback still governs the current coding task immediately, but ordinary coding does not automatically persist it or start history analysis. Re-run `developer-evolution` to extract later feedback. Updating this repository changes the authoring skill and the template for new profiles; it does not migrate already installed personal entries into project skills. Such a migration must cover both the destination and the old active copy. No background listener or additional memory store is introduced.

To revisit corrections in sessions that were already processed, explicitly request a full reconciliation; ordinary incremental collection will skip unchanged sessions.

## Generate code explanation skills

Generate a reusable explanation method, project knowledge, and personal adaptation together or independently:

```text
Use $developer-evolution to propose a code explanation skill for this project.
Cover its main feature flow, calls, data and state changes, and important failure
paths from current source. Reuse my approved explanation preferences. Show the
skill content and destination before installing it; do not analyze history.
```

A general `code-explanation` skill works with a snippet or an unfamiliar repository. A project version reuses an existing relevant repository skill or creates a focused explanation skill, with small references linking entrypoints, symbols, and important flows. It checks the relevant current source when answering, so saved project maps do not silently replace changed code. Personal explanation preferences remain in `developer-profile`; project skills also work for collaborators without that profile.

The generated skill also explains a diff or PR for review: establish the comparison scope, explain observable before/after behavior, point to decisive code and constraints, and connect claims to validation evidence and its limits. Use the existing PR description or conversation, with detail proportional to the change. This supports independent review and human judgment without creating a report or skill for every PR.

After generating the skill, ask for a review walkthrough with:

```text
Use $code-explanation to explain this PR for review. Show the behavior change,
the key source locations and constraints, the available validation evidence,
and what remains unverified. Keep the guide proportional to the change.
```

To explicitly authorize creation, name the scope and destination, for example:

```text
Use $developer-evolution to create a general code-explanation skill under my
Codex skills directory from the bundled template. Reuse any relevant approved
profile preferences; do not read history or change my profile.
```

To learn presentation preferences as well:

```text
Use $developer-evolution to analyze my recent code explanation conversations,
propose explanation preference updates to developer-profile, and propose a
general explanation skill plus project guidance for the import flow in this
repository. Verify project behavior from current source before drafting it.
```

The existing evidence and approval rules apply to those preferences. Code facts are verified from the repository and do not need repeated user statements. History alone cannot establish current code behavior. Creating a general skill does not also authorize project skill or profile changes.

This capability uses the existing modes and proposal workflow. Code-only generation does not collect sessions or advance history checkpoints. Ordinary explanation uses the generated skill without running evolution, updating stored knowledge, or executing the application. No extra model service or background watcher is required.

## Modes

| Mode | Behavior |
| --- | --- |
| Analyze | Compare relevant personal, repository, explanation, and global guidance and propose scoped changes. This is the default. |
| Bootstrap | Initialize the personalization workspace, then analyze available history. |
| Apply | Create or evolve authorized personal, repository, explanation, and global targets; record rejections. |
| Status | Report profile and explanation skills, repository guidance, watchlist, proposal decisions, and managed instructions. |

## Local data

Generated personal state stays outside this repository under `CODEX_HOME` (normally `~/.codex`):

```text
~/.codex/
├── skills/developer-profile/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/profile.md
├── skills/code-explanation/       # optional generated general explanation skill
│   ├── SKILL.md
│   └── agents/openai.yaml
└── personalization/developer-evolution/
    ├── instruction-history.md
    ├── watchlist.md
    ├── processing-state.json
    ├── evidence/
    └── proposals/
```

The `developer-evolution/` namespace makes ownership explicit and avoids collisions with other personalization skills.

The canonical profile lives inside the generated skill. Legacy `personalization/developer-evolution/developer-profile.md` is left untouched during analysis; an authorized migration replaces it with a pointer after validating the runtime copy. Only generic scaffolding is distributed in this repository. Personal entries, skill descriptions tailored to the user, drafts, and evidence stay local.

Approved project engineering rules live in the affected repository's instruction layout, such as its existing `.codex/skills/` directory or project `AGENTS.md`. They contain no private evidence or dependency on this personal workspace.

Evidence bundles can contain private conversation content even after automated redaction. Review them before sharing, and never commit them to a repository.

New workspace directories use owner-only permissions and generated state files use mode `0600` on platforms that support POSIX permissions.

## Incremental checkpoints

`processing-state.json` records:

- session ID and source file;
- file size and modification time;
- extracted conversation fingerprint;
- extraction configuration signature;
- processing time, associated analysis artifacts, and their SHA-256 digests.

A session is processed again when its transcript or extraction settings change. Metadata-only transcript changes update the checkpoint without sending unchanged conversation content through analysis again. Sessions with JSON parse errors are retried instead of being marked as processed. Checkpoint commits serialize writers and reject stale state rather than overwriting concurrent updates.

## Codex coupling and portability

The current implementation is **Codex-first and moderately to strongly coupled at its integration boundaries**. It is not a drop-in history analyzer for other coding agents yet.

| Layer | Coupling |
| --- | --- |
| Evidence thresholds and confidence policy | Portable |
| Human-reviewed proposal workflow | Portable |
| Checkpoint and fingerprint model | Mostly portable |
| Transcript discovery and JSONL parsing | Codex-specific |
| `CODEX_HOME` personalization workspace | Codex-specific |
| Global `AGENTS.md` managed-block updates | Codex-specific |
| Skill packaging | Agent Skills compatible, with OpenAI UI metadata |

Supporting another agent would require two adapters:

1. A transcript source that normalizes that agent's history into sessions and messages.
2. An instruction target that maps approved working agreements to that agent's persistent configuration.

The evidence policy, proposal format, checkpoint lifecycle, and privacy rules can remain shared.

## Safety properties

- Transcript content is treated as untrusted data, never as instructions.
- Developer/system messages and tool outputs are excluded from evidence.
- Common private keys, API keys, access tokens, authentication headers, cookies, and signed URL parameters are redacted.
- Assistant-authored summaries cannot independently establish a user preference.
- A global instruction normally requires evidence from at least three distinct sessions.
- Checkpoints mean “analyzed,” not “approved.”
- Active instructions change only within explicit user authorization, normally through numbered proposals.
- A concrete user request to migrate an already confirmed profile also authorizes that migration. Bootstrap alone never installs runtime guidance, and rejection cannot be bypassed through a profile entry or trigger description.

## Repository layout

```text
developer-evolution/
├── SKILL.md
├── agents/openai.yaml
├── assets/
│   ├── profile-skill.md
│   ├── profile-openai.yaml
│   ├── code-explanation-skill.md
│   └── code-explanation-openai.yaml
├── references/
│   ├── evidence-policy.md
│   ├── engineering-corrections.md
│   ├── code-explanation.md
│   ├── profile-evolution.md
│   └── proposal-format.md
└── scripts/
    ├── collect_history.py
    ├── commit_checkpoint.py
    ├── create_profile_skill.py
    ├── init_workspace.py
    └── _checkpoint.py

tests/
├── test_scripts.py
└── test_profile_skill.py
```

## Development

Run the test suite with Python 3.10 or newer:

```bash
python3 -m unittest discover -s tests -v
```
