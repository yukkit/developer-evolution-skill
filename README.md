# Developer Evolution

An auditable Codex skill that turns local coding conversations into an evolving personal `developer-profile` skill and concise global working agreements.

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
- Updates the profile skill and/or a managed block in global `AGENTS.md` within the user's authorization.
- Uses incremental checkpoints to skip unchanged sessions.
- Runs only when explicitly invoked as `$developer-evolution`.

## How it works

```text
Codex sessions
      ↓
redacted evidence bundle
      ↓
profile skill + global rules + watchlist + decision history
      ↓
numbered proposal
      ↓
human approval
      ↓
developer-profile skill      global AGENTS.md agreements
      ↓                              ↓
contextual task guidance     concise stable rules
```

Collection and checkpoint updates use a two-phase workflow. The collector creates a checkpoint candidate, but processing state advances only after the analysis or no-change report is safely written. A failed analysis is retried on the next run.

The collector writes to a unique private file under the skill's `evidence/` directory when no output path is supplied. Explicit output paths outside that directory and attempts to overwrite an existing bundle are rejected, and evidence is never printed to stdout.

`developer-profile` is the daily-use output: Codex can select it automatically for relevant engineering, product, or communication choices, then read only the applicable profile sections. Its content evolves through reviewed additions, refinements, merges, and removals. `developer-evolution` remains the explicitly invoked author of those changes; neither skill runs a background process. Automatic selection of the profile is permitted, not guaranteed on every task.

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

## Modes

| Mode | Behavior |
| --- | --- |
| Analyze | Compare both outputs and propose profile-skill and/or global-rule changes. This is the default. |
| Bootstrap | Initialize the personalization workspace, then analyze available history. |
| Apply | Create or evolve the profile skill and/or global rules within explicit authorization; record rejections. |
| Status | Report the profile skill, watchlist, proposal decisions, and managed instructions. |

## Local data

Generated personal state stays outside this repository under `CODEX_HOME` (normally `~/.codex`):

```text
~/.codex/
├── skills/developer-profile/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/profile.md
└── personalization/developer-evolution/
    ├── instruction-history.md
    ├── watchlist.md
    ├── processing-state.json
    ├── evidence/
    └── proposals/
```

The `developer-evolution/` namespace makes ownership explicit and avoids collisions with other personalization skills.

The canonical profile lives inside the generated skill. Legacy `personalization/developer-evolution/developer-profile.md` is left untouched during analysis; an authorized migration replaces it with a pointer after validating the runtime copy. Only generic scaffolding is distributed in this repository. Personal entries, skill descriptions tailored to the user, drafts, and evidence stay local.

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
│   └── profile-openai.yaml
├── references/
│   ├── evidence-policy.md
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
