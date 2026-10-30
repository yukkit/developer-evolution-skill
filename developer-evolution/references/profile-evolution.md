# Evolve the Developer Profile Skill

The personal `developer-profile` skill is a maintained runtime artifact. History analysis should consider creating it when absent, updating its preferences, and improving how relevant information is discovered and disclosed. Installing a static reader once does not complete this responsibility. Evolution happens on requested runs of `developer-evolution`, not in a background process or on every coding turn.

## Choose the right output

Keep universal, stable instructions short in global `AGENTS.md`. Use the profile skill for richer conditional preferences: engineering tradeoffs, product judgment, communication, collaboration, technology choices, and project-specific exceptions. Record scope rather than discarding useful evidence because it is confined to one project.

A preference already addressed by another skill may still describe the user. Preserve the distinctive decision criterion and link to the authoritative instruction where useful; do not copy a domain workflow into the profile. Broadly sensible advice without evidence about this developer adds no value.

Project implementation corrections normally belong in the affected repository's existing domain skill, or its `AGENTS.md` for a short project-wide invariant. Follow [engineering-corrections.md](engineering-corrections.md) to choose the target. Keep a distinct personal decision criterion or scoped pointer in the profile only when useful; do not duplicate repository rules here. A project-specific personal preference can remain private without becoming shared engineering policy.

Code explanation preferences, such as useful examples or the level of detail needed, also belong here when supported and authorized. Current project behavior and call maps belong in project guidance, not the personal profile. Follow [code-explanation.md](code-explanation.md) when generating a general or project explanation skill; it can use relevant approved profile entries without duplicating them.

## Evolve content and discovery together

On each analysis, inspect the current skill and decide whether any of these changes is useful:

- **Create:** Prepare the runtime skill from preferences authorized for daily use.
- **Add or refine:** Capture a new preference, narrow its scope, or add a counterexample that changes how it applies.
- **Merge or remove:** Consolidate equivalent entries and retire superseded guidance while preserving the decision in history. Do not remove preferences just because the current batch did not mention them.
- **Improve discovery:** Update the frontmatter description when approved topics change, or when actual usage shows missed or excessive activation. Describe recognizable task situations, not an instruction to activate on every turn.
- **Improve activity routing:** Make substantive design, implementation, code review, and code explanation reach their relevant approved entries. Adapt the template's lookup categories to actual profile headings, using direct links where useful. Read newly relevant entries when the activity changes within a task, without making activities a fixed sequence or approval gate. One preference can serve several activities; do not duplicate its content or invent a preference to fill a category.
- **Improve disclosure:** Keep `SKILL.md` short with topic routing to substantive references. Start with one `references/profile.md`; split it only when different tasks would benefit from loading different substantial sections. Update incoming links and remove duplicated active copies after a split.

Represent every actionable change as `ADD`, `MODIFY`, or `REMOVE`, including metadata or organization changes. Explain the observed problem, exact affected files, before/after wording, and a realistic task showing why it matters. Use no-change confirmations when existing content works; do not force a new proposal per batch.

If skill selection repeatedly misses the approved profile, propose a short global `AGENTS.md` route requiring the relevant activity and topic lookup for substantive work. Add it only within the user's authorization, preserving unrelated global instructions. Keep the actual preferences in the profile and applicable repository rules in their authoritative locations; factual answers and mechanical actions do not need the lookup. Creating a profile alone does not authorize changing global instructions.

## Profile entry format

Use meaningful topic headings. Each entry should include:

- **Preference:** A concise, actionable decision criterion grounded in the user's statements.
- **Scope and when to use:** Global, technology, or named project context and the kind of decision it affects.
- **Exceptions/counterevidence:** Conditions under which the preference does not apply.
- **Confidence:** High or Medium, reflecting the evidence independently of approval.
- **Evidence and decision:** Compact session/date/context/fingerprint references and the approval date or proposal reference. Keep transcripts and detailed decision history outside the runtime skill.

For example, a project-specific preference for a smaller migration may inform that project's unreleased feature work without becoming a global prohibition on compatibility layers. Low-confidence or ambiguous observations remain outside the runtime skill. Rejection must not be turned into a preference in the opposite direction.

## Create and migrate after authorization

Use the installed skill at `<CODEX_HOME>/skills/developer-profile/` as the canonical runtime source. A preexisting skill at that path may be user-authored: inspect it, compare the proposed changes, and preserve unrelated content and invocation policy. Do not replace an existing skill with fresh boilerplate.

For a new skill:

1. Stage the reviewed profile under the private `proposals/` directory. Include only entries authorized for runtime use, with scopes and exceptions. Approval to store an old descriptive profile did not automatically authorize runtime activation; check the current request or proposal for migration authorization.
2. Run the creation helper with the staged profile:

   ```bash
   python3 <skill-dir>/scripts/create_profile_skill.py \
     --codex-home <codex-home> \
     --profile <workspace>/proposals/<reviewed-profile>.md
   ```

   The helper creates private `SKILL.md`, `agents/openai.yaml`, and `references/profile.md`. It refuses an existing destination, leaves the input untouched, and never reads sessions or changes global instructions. It scaffolds from reviewed input; it does not infer preferences or certify approval.

3. Adapt the generated description, activity routes, and topic routing to the approved profile. Keep automatic selection enabled for the newly created daily-use skill; `developer-evolution` remains explicit-only. Preserve any later user-selected invocation policy when updating.
4. Validate the created skill, its links, and copied content before migrating the legacy path. Keep a private snapshot if needed for recovery. Replace the old workspace `developer-profile.md` with a short link to the canonical reference only after successful validation, avoiding two editable profiles. Preserve old proposals/evidence for audit; do not rewrite artifacts already bound to checkpoints.
5. Record the migration and authorized changes in `instruction-history.md`, including canonical paths and superseded files. Keep files `0600` and personal directories `0700` where supported.

On later approved updates, edit the existing skill and references in place. Do not rerun the creation helper, overwrite a personalized entrypoint from a template, or silently broaden the skill's scope. References and routing must agree after edits. If an update fails partway, report what applied and what remains; do not record an incomplete update as complete.

## Check actual behavior

Before finishing, check the changed behavior using realistic tasks:

- A matching decision reaches the relevant preference, applies its scope/exception, and continues the original task.
- A task that moves from design into implementation or review consults newly relevant entries without duplicating preferences or adding a confirmation step. Explanation requests reach the applicable communication preferences.
- An unrelated fact or mechanical action does not trigger needless profile/history work.
- A project-specific entry stays within its project and does not override current instructions or technical constraints.
- A task extending existing code reaches any matching engineering correction, avoids the rejected behavior, and preserves allowed reuse and exceptions. Check an updated example where the original defect has been fixed as well.
- A rejected or uncertain candidate is not present in entrypoint guidance, references, or discovery metadata.

Use `skill-creator` validation when available. Structural checks do not prove correct retrieval or judgment; inspect the actual entrypoint and simulate the task when evaluating behavioral changes. Personal content stays local; the distributable repository contains only generic templates, scripts, and documentation.
