# Evidence Policy

Use this policy for every history analysis.

## Evidence hierarchy

Rank evidence from strongest to weakest:

1. A direct correction of Codex behavior or output.
2. An explicit preference, prohibition, or stated decision criterion.
3. Repeated acceptance or rejection of the same tradeoff across sessions.
4. A repeated implementation choice with a clear alternative available.
5. Assistant-authored summaries or generated memories.

Items 1–4 can support a conclusion. Item 5 can help locate or interpret primary evidence but cannot independently support a conclusion.

## Counting rules

- Count distinct source sessions, not message count.
- Count repeated text copied into a fork or resumed transcript once. Use message fingerprints to detect duplicates.
- Count several examples from one project as one context unless the user explicitly states the preference is global.
- Do not count tool outputs, system/developer instructions, repository documentation, or assistant suggestions as user preferences.
- Do not treat absence of disagreement as acceptance.

## Confidence

- **High**: At least three distinct sessions, normally across two contexts, with explicit or consistent evidence and no material unresolved contradiction.
- **Medium**: Two distinct sessions, or one unusually explicit statement, with no strong contradiction.
- **Low**: One session, an inferred behavior, weak acceptance, or material ambiguity.

Only High-confidence conclusions are eligible for a new global `AGENTS.md` instruction. Keep Medium- and Low-confidence candidates on the watchlist unless the user explicitly promotes them.

## Scope classification

Classify every candidate as one of:

- **Global collaboration**: How Codex should communicate or work with the user everywhere.
- **Global engineering**: A technology-independent engineering principle.
- **Technology preference**: Applies when a named language, framework, or tool is relevant.
- **Project-specific**: Belongs in that repository's `AGENTS.md`, not the global file.
- **Temporary/contextual**: Do not persist.

## Contradictions and recency

- Preserve both sides of a contradiction in the profile.
- Prefer a newer position only when the user explicitly changed their mind or repeated the newer behavior across sessions.
- Propose modifying or removing an instruction only when evidence meets the same threshold required to add one.
- Avoid converting situational tradeoffs into absolute instructions.

## Privacy

- Analyze the redacted evidence bundle rather than raw transcripts whenever possible.
- Summarize evidence in persistent files. Do not copy long transcript passages.
- Cite evidence with session ID, date, working-directory label, and message fingerprint.
- Never persist credentials, private keys, bearer tokens, signed URLs, or unrelated personal information.
- Keep evidence bundles out of Git repositories and warn before sharing them.

