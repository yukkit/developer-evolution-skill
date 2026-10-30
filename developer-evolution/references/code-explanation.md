# Generate and Evolve Code Explanation Skills

Use this reference when the user wants a reusable code explanation skill, a project or subsystem guide, or improvements based on feedback about explanations. Support general explanation methods, project knowledge, and personal explanation preferences together without making them three copies of the same guidance.

## Choose the output and scope

- **General explanation:** Create or evolve a daily-use `code-explanation` skill under `<CODEX_HOME>/skills/`, unless the user chooses another destination. Start with [the skill template](../assets/code-explanation-skill.md) and [UI metadata](../assets/code-explanation-openai.yaml). It works without history, a personal profile, or a precomputed project map.
- **Project explanation:** Inspect the repository's actual instructions, documentation, and skills. Extend a relevant existing skill with an explanation reference and a matching discovery/reading route when that fits its purpose. Otherwise create a focused repository skill such as `<project>-code-explanation` in its established skill layout. Adapt the template's name, description, and UI prompt to the project or subsystem. Keep it usable without a collaborator's personal skills.
- **Personal explanation preferences:** Use the relevant approved `developer-profile` entries. Propose additions or refinements through [profile-evolution.md](profile-evolution.md), rather than keeping a second preference store in the explanation skill. A general or project skill must still work when no profile is available.

A request can cover all three. Reuse existing project guidance and personal preferences before proposing additions. Do not create one skill per source file or import every module into a single reference. Scope initial project knowledge to the feature or flow the user named; a later request can expand it.

The generated skill is for explaining code, tracing behavior, and answering follow-up questions. Ordinary implementation work does not need a separate explanation pass unless requested or already required by the task. Generating a skill does not authorize running the application, accessing production data, invoking configured models, or installing another service.

## Separate preferences from code facts

Use history to identify what the user wanted explained, where explanations failed, and any stated presentation preferences. Apply the evidence policy to those preferences; assistant explanations and silence do not establish the user's preferred style. If the current request supplies the preference, apply it to this task while checking persistence authorization separately.

Project behavior needs current repository evidence. Read the relevant entrypoints, callers, implementations, types/contracts, persistence boundaries, and tests as needed to establish the requested flow. Prefer existing design records for documented intent and check them against implementation. Do not infer current behavior or design rationale from an old assistant answer, a filename, or the user's question alone. Record unverified intent as unknown or inference, rather than inventing a reason.

The history collector intentionally excludes tool output and host context; its evidence bundle is not a source-code snapshot. Do not change collection or relax redaction to recover code. Inspect the authorized repository separately. When it is unavailable, a general skill or a private project draft can still be prepared, but do not present a source-verified project guide or install into an uninspected repository.

Source-verified facts do not need the multi-session preference confidence threshold. Keep the source basis distinct from private preference evidence. Do not copy chat excerpts, session IDs, evidence paths, credentials, production records, or personal approval history into repository skills.

## Keep project knowledge small and checkable

A project explanation reference should help the next agent find and explain a flow. Include only the parts useful for its scope:

- The user-visible behavior, subsystem boundary, and important domain terms.
- Repository-relative entrypoints and symbol names, followed by the main calls or events in execution order.
- Important inputs, transformations, outputs, and ownership of state or persisted data.
- Branches, asynchronous handoffs, failures, retries, or transaction boundaries that materially change the result.
- Non-obvious constraints and documented design decisions, linked to their authoritative source instead of copied as a second rule.
- The source revision when available, verification date, inspected paths/symbols, and any unverified behavior. A dirty tree must be identified as such; a commit ID alone cannot identify its content.

Reuse authoritative project documents by linking to them. Avoid pasted implementations and volatile line-number indexes; paths plus symbols survive ordinary edits better. Add a reference only when there is useful project knowledge beyond a few locators, and give it an explicit reading trigger in `SKILL.md`. Do not add an empty `references/code-map.md` just to fill a template.

For example, an explanation skill for a synthetic import service might route “how does an import finish?” to `src/imports/api.py:create_import`, then the queue consumer, parser, and persistence service. Its reference would record the relevant state changes and failure boundary, rather than listing every directory in the repository. This example supplies no facts about the user's project.

The runtime skill must recheck the relevant current source before making code-specific claims. If a locator is missing or the implementation differs, use the current code for the answer and flag the stale reference. Do not silently update stored guidance during ordinary explanation. This workflow does not add a background repository watcher or automatic refresh on each code edit.

## Use the existing proposal and application workflow

**Analyze** stages the proposed skill content, project references, routing, and preference changes under private `proposals/`, naming exact eventual targets. The proposal must distinguish source-verified facts, inferred or unverified claims, and personal preferences. Follow [proposal-format.md](proposal-format.md). It must not install or update active skills.

When the user requests skill generation without history analysis, inspect the requested scope and stage the result without collecting sessions. No history bundle means no history checkpoint to commit. The absence of new history does not block a useful code explanation proposal. Keep the existing Analyze/Bootstrap/Apply/Status modes; this capability is another output, not a new mode.

**Apply** creates or updates only the targets already authorized by the user. An explicit request to create a named skill at a concrete scope and destination is sufficient authorization for that work; do not demand a second approval for the same content. A request to explore options or analyze history alone is not authorization to install runtime guidance. Approval of a general explanation skill does not also authorize project or profile changes.

For an authorized new skill, use `skill-creator` when available, or create the skill files from the bundled templates. Preserve normal automatic selection unless the user requests explicit-only invocation. Inspect existing destinations before writing; update approved sections in place and preserve unrelated content, dependencies, and invocation policy. Do not use `create_profile_skill.py` for explanation or repository skills. Keep personal outputs private and keep repository outputs free of private evidence.

For later requested runs, compare the relevant current code, existing explanation skill, and feedback. Update useful routes or affected flows, retire superseded claims only within authorization, and preserve working knowledge outside the change. Record applied or rejected proposals in the private decision history using the existing workflow. Do not advance history checkpoints merely because a code map was refreshed.

## Validate the capability

Validate new or changed skills, metadata, and reference routes. Source checks establish what code says; do not claim execution or target-environment verification without performing it within authorization. For substantial changes, independently exercise realistic tasks in a temporary workspace:

- A general request explains a small function without requiring a project map or collecting history.
- A project request finds the relevant reference, follows current calls and state changes, and gives source locators for the explanation.
- A stale reference is corrected in the answer from current code and reported, without silently rewriting the skill.
- An available approved preference changes the relevant presentation; an absent profile does not block explanation, and an inferred preference is not activated.
- An unrelated task does not start a code tour, history scan, runtime update, or application execution.

Check the behavior and artifacts, not exact headings or phrasing. Keep synthetic examples in this distributable repository; live project maps and personal preferences belong only in their intended targets.
