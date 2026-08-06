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

## Proposed changes

### P1 — ADD | MODIFY | REMOVE

- Target: global AGENTS | developer profile | project AGENTS
- Scope: global collaboration | global engineering | technology | project
- Confidence: High | Medium | Low
- Proposed wording: "..."
- Rationale: ...
- Evidence:
  - `session-id`, date, context, message fingerprint — short paraphrase
- Counterevidence: none | ...
- Replaces: none | exact existing wording

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
- Include counterevidence and conflicts, not only supporting examples.
- Use short paraphrases instead of long transcript quotes.
- Put Medium- and Low-confidence observations in the Watchlist unless the user explicitly requested otherwise.
- Do not include a pre-approved state. The user must name or check each approved item.

