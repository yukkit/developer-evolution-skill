# Proposal Format

Write one Markdown file per analysis using this structure:

```md
# Developer Evolution Proposal — YYYY-MM-DD

## Scope

- Sessions analyzed: N
- Date range: ...
- Distinct project contexts: N
- Evidence bundle: local path
- Existing instructions compared: yes/no
- Profile skill compared: absent | path and references inspected

## Proposed changes

### P1 — ADD | MODIFY | REMOVE

- Target: global AGENTS | developer-profile skill | project AGENTS
- Files: exact affected paths (including SKILL.md description or references when relevant)
- Scope: global collaboration | global engineering | technology | project
- Confidence: High | Medium | Low
- Proposed wording: "..."
- Rationale: ...
- Evidence:
  - `session-id`, date, context, message fingerprint — short paraphrase
- Counterevidence: none | ...
- Replaces: none | exact existing wording
- Task example: a concrete task and how the changed guidance should affect it

## Watchlist

### W1 — Candidate title

- Current confidence: Medium | Low
- Signal: ...
- Evidence still needed: ...

## No-change confirmations

- Existing instruction — why current evidence still supports it

## Contradictions

- Topic — older position, newer position, and why no automatic resolution was made

## Approval checklist

- [ ] P1
- [ ] P2
```

## Requirements

- Number every actionable proposal.
- Use `ADD`, `MODIFY`, or `REMOVE`; do not hide mutations in prose.
- Quote the exact concise instruction proposed for `AGENTS.md`.
- For profile-skill changes, show the proposed preference, scope, exceptions, confidence, and evidence/approval fields. Show concrete before/after metadata or routing when those change; drafts stay in the private `proposals/` directory during analysis.
- Consider profile evolution and global-rule promotion separately. No new global rule does not imply no useful profile improvement.
- Include counterevidence and conflicts, not only supporting examples.
- Use short paraphrases instead of long transcript quotes.
- Clear Medium-confidence preferences may be proposed for contextual runtime use with their actual scope. Put Low-confidence and ambiguous observations in the Watchlist. Do not elevate confidence merely because an entry was approved.
- Do not include a pre-approved state. The user must name or check each approved item.
- Include the exact absolute evidence bundle path so checkpoint commits can bind the analysis artifact to its input.
- Cite additional evidence bundles when a conclusion depends on earlier batches. Never rewrite a proposal already bound to a checkpoint to record its decision; append approval or rejection to `instruction-history.md` instead.

## No-change reports

When there are no actionable changes, write a compact Markdown report under `proposals/` containing the analysis date, exact absolute evidence bundle path, session counts, parse-error count, and the reason no proposal was created. Use this report as the required `--proposal` argument when committing metadata-only checkpoint candidates.
