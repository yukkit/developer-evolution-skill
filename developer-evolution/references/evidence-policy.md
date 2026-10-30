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
- Treat checkpoint entries as processing metadata, never as preference evidence.
- Count repeated text copied into a fork or resumed transcript once. Use message fingerprints to detect duplicates.
- Count several examples from one project as one context unless the user explicitly states the preference is global.
- Do not count tool outputs, system/developer instructions, repository documentation, or assistant suggestions as user preferences.
- Do not treat absence of disagreement as acceptance.

## Confidence

- **High**: At least three distinct sessions, normally across two contexts, with explicit or consistent evidence and no material unresolved contradiction.
- **Medium**: Two distinct sessions, or one unusually explicit statement, with no strong contradiction.
- **Low**: One session, an inferred behavior, weak acceptance, or material ambiguity.

Only High-confidence conclusions are eligible for a new global `AGENTS.md` instruction, normally supported by at least three sessions across two contexts. This threshold does not apply to all profile entries or repository rules: a clear explicit preference or correction can support a Medium-confidence proposal for the appropriate scoped target. Apply such entries only after authorization for runtime use and preserve their scope and exceptions. Approval does not increase evidence confidence. Low-confidence, ambiguous, and unconfirmed candidates remain in the analysis watchlist, outside runtime guidance.

Keyword matches are discovery aids, not semantic evidence. Read statements and surrounding context to distinguish a user's preference from pasted reports, quoted suggestions, questions, code examples, and descriptions of application behavior. Review novel messages beyond preselected keywords before concluding there is no change.

When a correction identifies code that should not be imitated, use [engineering-corrections.md](engineering-corrections.md). Preserve the rejected behavior, reason, scope, and supplied alternative instead of reducing it to generic quality advice. Rejection of an implementation can be evidence for a correction; rejection of a proposal to persist guidance is an authorization decision and must still be honored.

## Scope classification

Classify every candidate as one of:

- **Global collaboration**: How Codex should communicate or work with the user everywhere.
- **Global engineering**: A technology-independent engineering principle.
- **Technology preference**: Applies when a named language, framework, or tool is relevant.
- **Project-specific**: Engineering corrections normally go to the repository's existing relevant skill; short project-wide invariants go to its `AGENTS.md`. Personal contextual preferences may remain in the private profile. Follow [engineering-corrections.md](engineering-corrections.md) for target selection; never generalize project evidence into the global file.
- **Temporary/contextual**: Do not persist.

## Contradictions and recency

- Preserve relevant exceptions to confirmed preferences in the profile. Keep unresolved competing claims in analysis until the applicable distinction is clear.
- Prefer a newer position only when the user explicitly changed their mind or repeated the newer behavior across sessions.
- Propose modifying or removing an instruction only when evidence meets the same threshold required to add one.
- Avoid converting situational tradeoffs into absolute instructions.
- Check decision history before proposing or applying changes. Do not reintroduce a rejected proposal through a profile entry, description, or renamed rule. Reconsider only if the user reopens it or explicitly changes the relevant preference.

## Privacy

- Analyze the redacted evidence bundle rather than raw transcripts whenever possible.
- Summarize evidence in persistent files. Do not copy long transcript passages.
- Cite evidence with session ID, date, working-directory label, and message fingerprint in private analysis artifacts. Repository skills and `AGENTS.md` receive only approved engineering conclusions, without private quotations, evidence identifiers, local analysis paths, or approval history.
- Never persist credentials, private keys, authentication headers, signed URL parameters, or unrelated personal information.
- Keep evidence bundles out of Git repositories and warn before sharing them.
- Keep evidence bundles in the private developer-evolution workspace and out of tool output.
- Commit a checkpoint only after the corresponding analysis artifact is safely written. A committed checkpoint means “analyzed,” not “accepted by the user.”
