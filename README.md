# Developer Evolution

An auditable Codex skill that turns local coding conversations into evidence-backed developer preferences and working agreements.

It analyzes repeated decisions, corrections, frustrations, and collaboration patterns across prior sessions. It proposes changes for review instead of silently rewriting its own instructions.

## What it does

- Reads completed local Codex session transcripts.
- Removes host context, tool output, credentials, authentication headers, and signed URL parameters before analysis.
- Distinguishes durable preferences from project constraints and one-off experiments.
- Requires evidence from multiple sessions before proposing a global instruction.
- Records contradictions instead of forcing them into one preference.
- Produces numbered proposals that require explicit human approval.
- Updates only a managed block in the global `AGENTS.md` after approval.
- Uses incremental checkpoints to skip unchanged sessions.
- Runs only when explicitly invoked as `$developer-evolution`.

## How it works

```text
Codex sessions
      ↓
redacted evidence bundle
      ↓
developer profile + watchlist comparison
      ↓
numbered proposal
      ↓
human approval
      ↓
managed global AGENTS.md instructions
```

Collection and checkpoint updates use a two-phase workflow. The collector creates a checkpoint candidate, but processing state advances only after the analysis or no-change report is safely written. A failed analysis is retried on the next run.

The collector writes to a unique private file under the skill's `evidence/` directory when no output path is supplied. Explicit output paths outside that directory and attempts to overwrite an existing bundle are rejected, and evidence is never printed to stdout.

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

Use a full reconciliation when needed:

```text
Use $developer-evolution to perform a full reconciliation scan and propose updates.
```

## Modes

| Mode | Behavior |
| --- | --- |
| Analyze | Collect new or changed history and generate proposals. This is the default. |
| Bootstrap | Initialize the personalization workspace, then analyze available history. |
| Apply | Apply only explicitly approved proposal items. |
| Status | Report the current profile, watchlist, proposals, and managed instructions. |

## Local data

Generated personal state stays outside this repository under `CODEX_HOME` (normally `~/.codex`):

```text
~/.codex/personalization/
└── developer-evolution/
    ├── developer-profile.md
    ├── instruction-history.md
    ├── watchlist.md
    ├── processing-state.json
    ├── evidence/
    └── proposals/
```

The `developer-evolution/` namespace makes ownership explicit and avoids collisions with other personalization skills.

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
- Active instructions change only after explicit approval of numbered proposals.

## Repository layout

```text
developer-evolution/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── evidence-policy.md
│   └── proposal-format.md
└── scripts/
    ├── collect_history.py
    ├── commit_checkpoint.py
    ├── init_workspace.py
    └── _checkpoint.py

tests/
└── test_scripts.py
```

## Development

Run the test suite with Python 3.10 or newer:

```bash
python3 -m unittest discover -s tests -v
```
