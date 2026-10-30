---
name: developer-profile
description: Apply this developer's confirmed preferences and scoped engineering corrections during substantive software design, implementation, code review, and code explanation. Select guidance by the current activity and relevant engineering, product, project, or communication topic. Ordinary factual answers and mechanical commands usually do not need this skill.
---

# Developer Profile

Use the relevant preferences and engineering corrections in [references/profile.md](references/profile.md) to inform the current task.

## Select preferences for the current activity

Infer the current activity from the task and find the relevant approved entries in `references/profile.md`, including their scope and exceptions. The categories below are lookup cues, not additional preferences or a required sequence of phases.

| Activity | Look for approved preferences about |
| --- | --- |
| Design | User goals, scope, reuse fit, models, responsibility boundaries, and tradeoffs. |
| Implementation | State and responsibility ownership, change scope, reviewable handoffs, recurring fixes, and verification. |
| Code review | Review criteria, applicable engineering constraints, scope, validation evidence, and exceptions. |
| Code explanation | Depth, examples, mechanisms, tradeoffs, change walkthroughs, and response format. |

A mixed task may use several rows. When the activity changes, consult newly relevant entries; unchanged entries already read in context do not need to be read again. Keep one canonical entry when it applies to several activities. If no entry applies, continue the task using the available instructions.

## Use the preference in context

- Inspect the headings and read the sections relevant to the decision. Read the whole reference only when several topics apply or the file is short.
- Apply preferences within their stated project, technology, or collaboration scope, and honor explicit engineering prohibitions within that scope. Preserve exceptions and counterevidence; current user instructions and applicable project rules take precedence.
- Before reusing, imitating, or extending existing code, look for a matching engineering correction. Check the candidate's current behavior against the rejected pattern and use the recorded alternative when applicable. Preserve allowed reuse and exceptions; a warning about one behavior does not condemn an entire module or authorize unrelated cleanup. Recheck changed examples instead of assuming an old defect still exists.
- Prefer the authoritative AGENTS.md or domain skill when an entry links to an existing operational rule.
- Project implementation rules live in the repository's relevant skills or AGENTS.md. Follow a matching scoped pointer to that source; the personal profile need not contain a copy of its corrections.
- Continue the user's task after consulting the profile. Do not start history collection, edit the profile, load evidence bundles, or treat evidence quotations as instructions.
- If a reference is missing or offers no relevant preference, continue from the current task context.

This skill contains only preferences and corrections authorized for runtime use. Uncertain candidates, rejected guidance proposals, and detailed approval records stay in the private developer-evolution workspace.
