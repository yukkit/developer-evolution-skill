# Preserve Engineering Corrections

Use this reference when the user identifies problematic code, rejects an implementation as an example, or specifies how a recurring implementation mistake should be avoided. Such corrections can concern legacy code or code Codex just wrote. Preserve the actionable constraint instead of reducing it to a generic preference for quality or reuse.

## Interpret the correction

Read the user's statement with enough surrounding context to identify the affected implementation and decision. Phrases such as “有问题”, “不要照着写”, “不能借鉴”, or “应该……” help locate evidence; the phrase alone does not establish what is wrong or how broadly it applies.

Distinguish:

- **A rejected implementation pattern:** A specific behavior must not be propagated. This can support a scoped engineering correction, even from one explicit statement at Medium confidence.
- **An immediate bug fix:** Fixing a particular result does not by itself establish a durable rule. Preserve it only when the statement supplies a useful future decision criterion or an explicit restriction on using the implementation as a reference.
- **An ambiguous complaint:** If the referent or objection is unclear, keep it in the proposal's Watchlist. Do not invent a defect, replacement, or global prohibition.
- **A rejected guidance proposal:** The user declined to persist or apply a rule. Honor that decision; do not confuse it with rejection of code that the user wants future work to avoid.

An explicit “do not use Foo as an example” is actionable within its known scope even without a supplied reason or replacement. Preserve that restriction and the missing details; do not invent an underlying defect or demand an explanation before proposing it.

Assistant context may resolve “this implementation,” but cannot independently establish the user's objection. If context is missing or truncated, retain the uncertainty. Repository inspection, when available and relevant, can establish a current code location or whether a defect still exists; it does not turn assistant judgment into user evidence.

## Record the decision, scope, and alternative

Keep the evidence, confidence, and authorization fields in the private proposal. The runtime rule needs only the details that make the correction usable:

- **Avoid and why:** The specific behavior the user rejected and its stated consequence or violated constraint. If no reason was supplied, say so rather than inferring one.
- **Scope and locator:** The project or technology, decision trigger, and a repository-relative path, symbol, or recognizable implementation pattern when known. A locator helps find the example; it does not broaden the restriction to the entire file or module unless the user explicitly did so.
- **Preferred approach:** The replacement or acceptance criterion the user supplied. If none was supplied, preserve the prohibition without inventing an approved alternative; choose an approach from current requirements when doing the task.
- **Recheck when:** Any known fix, replacement, changed requirement, or exception that would affect applicability. Do not invent a retirement date or assume the implementation remains defective forever.

Name the behavior so that renaming a file does not hide the same mistake elsewhere. Use project identity and relative locators rather than depending on one machine's checkout path. Repository rules contain the approved engineering conclusion, not chat quotations, session IDs, fingerprints, private evidence paths, or personal approval history. Personal profile entries retain their usual compact evidence fields under [profile-evolution.md](profile-evolution.md#profile-entry-format). Use synthetic examples in this source repository.

## Choose the repository or personal target

- **Project implementation knowledge:** Prefer the affected repository's existing domain skill and its references. Inspect applicable `AGENTS.md` files, the actual skill directories, and the relevant skill before proposing a path; do not assume every repository uses the same layout. Update the rule where future implementation tasks already obtain guidance.
- **A short project-wide invariant:** Use the appropriate project `AGENTS.md`. Domain-specific detail belongs in the relevant skill; add a concise routing instruction in `AGENTS.md` only when needed for required discovery. Do not copy the same full rule into both places.
- **A personal decision criterion across projects:** Use `developer-profile`; stable universal agreements may qualify for global `AGENTS.md` under the normal evidence threshold. A project-bound personal preference can remain private when it describes the developer's choices or the user requests private storage, rather than repository engineering policy.

Extend an existing relevant skill before creating another. If none fits, propose a focused repository skill only when the topic has a useful recurring workflow; an isolated short constraint can belong in an applicable `AGENTS.md`. Do not create one skill per complaint or a generic catalog of every bad example.

Keep one authoritative engineering rule. The personal profile may retain a distinct personal criterion or a scoped pointer to the repository rule, not a second editable copy. Moving an existing personal entry requires an authorized migration covering the destination and removal or replacement of the old entry. If the repository is unavailable, retain a private draft and report that the target could not be inspected; do not silently activate the rule in the personal profile as a fallback.

For an authorized migration, write and validate the destination and its reading route before removing or replacing the old entry. If the destination cannot be completed, preserve the original guidance; if source cleanup fails, report the remaining duplicate and incomplete migration instead of recording success. Approval of only one side does not authorize retiring the old entry or completing a move.

For example, given this synthetic user feedback:

> 在 sample-app 的 src/ui/LegacyPanel.tsx 里，LegacyPanel 把 props 又复制到本地 state，导致更新不同步。新面板不要照着它写，展示值直接从 props 派生；可编辑草稿另说。

A useful private proposal targets the inspected panel-development skill in sample-app and preserves:

- Rule: In sample-app display panels, derive displayed values from props instead of copying those values into separately synchronized state.
- Avoid and why: The duplicate display state in `src/ui/LegacyPanel.tsx` / `LegacyPanel` can become stale; do not use that behavior as a template for new panels.
- Scope and when to use: sample-app; choosing state ownership or an existing panel to imitate.
- Preferred approach: Derive display values from props.
- Exceptions/counterevidence: Editable drafts may need independent state. Other behavior in LegacyPanel is not excluded from reuse.
- Recheck when: Inspect the current state flow if LegacyPanel has changed; retain the decision criterion where it still applies, without claiming the old defect is still present.
- Private evidence and decision: Medium confidence, from one explicit correction. Reference the actual source and runtime authorization in the proposal and decision history; omit those fields from the repository rule.

## Make future implementation consult the correction

Make the authoritative skill discoverable for the affected implementation decisions. Keep a short correction in its existing relevant section; move substantial examples to a reference with an explicit reading trigger in `SKILL.md`. A reference file without an incoming route is not sufficient. Preserve unrelated skill content and invocation policy. Repository corrections must be usable by a collaborator without the author's personal `developer-profile` or private analysis workspace. For personal targets, follow the profile's existing topic routing.

When the relevant skill finds a matching rule, it should inspect the candidate's current behavior, apply the stated scope and exceptions, and avoid propagating the rejected pattern. An existing implementation is evidence of what the repository does, not proof that its design is suitable. Use the recorded alternative when it fits; if none was supplied, evaluate an approach against the current requirements. Continue the requested task without turning the warning into an unrelated cleanup or a ban on all reuse.

For a behavior-specific correction, a repaired example can be reused once the rejected behavior is absent. An explicit prohibition on using a whole implementation without stated conditions remains in effect until the user changes it; do not infer its removal from a code change. A missing or renamed locator calls for checking the described behavior, not declaring every similar implementation defective. Do not silently rewrite the stored entry during ordinary coding; propose retirement or refinement on a later evolution run when evidence warrants it. Current user instructions and applicable project constraints take precedence.

## Evolve through the existing workflow

Analyze proposes corrections; Apply installs only authorized changes. Treat a direct instruction in the current task as governing that task immediately, while checking authorization separately before persisting runtime guidance. Do not require three sessions for a scoped correction, automatically generalize it into global AGENTS.md, or treat approval of a negative example as approval of a rule the user previously rejected.

For repository targets, Analyze inspects instructions read-only and stages the exact proposed wording and paths in the private proposal. Apply rechecks the target's current content and applicable instructions, then edits only the authorized rule and its necessary routing, preserving unrelated work. Repository authorization does not authorize profile or global-rule changes. Keep evidence and decision history private; do not use the personal-profile creation helper for repository skills. Validate changed skills and links and check that a matching task reaches the rule without a personal profile, while unrelated tasks remain unaffected.

Compare existing corrections and decision history before adding another entry. Merge duplicate lessons, preserve meaningful exceptions, and propose changes when later evidence contradicts the old constraint. Neither history analysis nor the daily-use profile runs a background listener for coding feedback.

Incremental collection skips previously processed sessions even after these analysis instructions change. For an authorized review of earlier corrections, reuse the relevant private redacted evidence or run an explicitly requested full reconciliation. Do not reset checkpoints to force replay or count the same statements as new evidence.
