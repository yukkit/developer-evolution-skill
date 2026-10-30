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
- Explanation skill compared: not relevant | absent | paths and references inspected
- Project instructions compared: not relevant | repository and relevant AGENTS/skill paths inspected | unavailable
- Source verification: not relevant | repository, revision/dirty state, inspected paths and symbols, limitations

## Proposed changes

### P1 — ADD | MODIFY | REMOVE

- Target: global AGENTS | developer-profile skill | repository skill | project AGENTS | code explanation skill
- Files: exact affected paths (including SKILL.md description or references when relevant)
- Scope: global collaboration | global engineering | technology | project
- Confidence: High | Medium | Low | not applicable (source-verified code facts)
- Proposed wording: "..."
- Rationale: ...
- Evidence:
  - `session-id`, date, context, message fingerprint — short paraphrase; or source paths/symbols for code-only generation
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
- For engineering corrections, include the rejected behavior and reason, project or technology scope, known code locator, supplied alternative or its absence, and when applicability needs rechecking. Follow [engineering-corrections.md](engineering-corrections.md); make the task example exercise a future implementation or reuse decision.
- For repository targets, identify the existing authoritative skill or AGENTS file, show the exact engineering wording separately from private evidence and approval fields, and include necessary reading triggers or reference links. Explain why a new skill is needed if none fits. A migration must name both the destination and the removal or replacement of the previous active copy.
- For explanation skills, show the proposed entrypoint, metadata, project reference content, and reading routes as applicable. Separate source-verified behavior from personal preferences and unverified rationale. Cite repository-relative paths/symbols and the inspected revision/dirty state for code facts; use preference confidence only for preferences. A code-only proposal has no session evidence bundle or history checkpoint. Include an example explanation task and how stale references will be handled.
- Consider personal profile evolution, repository guidance, and global-rule promotion separately. No new global rule does not imply no useful scoped change.
- Include counterevidence and conflicts, not only supporting examples.
- Use short paraphrases instead of long transcript quotes.
- Clear Medium-confidence preferences may be proposed for contextual runtime use with their actual scope. Put Low-confidence and ambiguous observations in the Watchlist. Do not elevate confidence merely because an entry was approved.
- Do not include a pre-approved state. The user must name or check each approved item.
- For history analysis, include the exact absolute evidence bundle path so checkpoint commits can bind the analysis artifact to its input. For code-only generation, mark session fields and the evidence bundle as not applicable and do not commit a history checkpoint.
- Cite additional evidence bundles when a conclusion depends on earlier batches. Never rewrite a proposal already bound to a checkpoint to record its decision; append approval or rejection to `instruction-history.md` instead.

## No-change reports

When there are no actionable changes, write a compact Markdown report under `proposals/` containing the analysis date, exact absolute evidence bundle path, session counts, parse-error count, and the reason no proposal was created. Use this report as the required `--proposal` argument when committing metadata-only checkpoint candidates.
