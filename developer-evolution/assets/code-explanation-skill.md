---
name: code-explanation
description: Explain code logic, trace calls and data or state changes, and clarify how a feature works from current source. Use for code walkthroughs, unfamiliar modules, implementation behavior questions, and explaining a diff or PR for review. Ordinary coding tasks do not require a separate walkthrough.
---

# Code Explanation

Explain the behavior the user is trying to understand, grounded in the current code. Adjust depth to the question and follow-up feedback rather than giving every answer the same checklist or a line-by-line paraphrase.

## Find the relevant behavior

- Resolve the requested project, feature, file, or symbol from the current task. Ask only when an ambiguity materially changes the explanation; a small snippet does not require whole-repository exploration.
- Follow applicable repository instructions. Consult relevant project skills, explanation references, and authoritative documents when available, then verify the relevant current source. A saved code map is a navigation aid, not proof that behavior is unchanged.
- Follow callers and callees far enough to establish the result. For a cross-module flow, locate the trigger, important transformations, state owners, and observable outcome. Include branches, asynchronous handoffs, persistence, failures, or retries when they change the answer.
- Use approved explanation preferences from an available `developer-profile` when relevant. Work normally without it. Current user instructions take precedence; do not infer a permanent preference from a follow-up question.

## Make the logic understandable

Start with what the code achieves and the key mechanism. Walk through a concrete input or user action when it helps connect the steps. Distinguish the normal flow from the exceptions that matter to the question.

Connect important claims to file and symbol locators, using clickable current line links when supported. Explain ownership and consequences: which component makes a decision, what data changes, and what the next step receives. Choose a small code excerpt or Mermaid diagram when it makes the flow easier to understand; neither is required for every answer.

Explain a design reason when the code, an authoritative decision record, or the user establishes it. Label a plausible rationale as inference. State what remains unknown when external services, configuration, or missing source prevent a complete answer. Separate observed code behavior from runtime behavior that has actually been tested.

On a follow-up, address the missing connection with a concrete example or a closer look at the relevant code. Avoid repeating the same abstraction in more words. Match the requested level of detail without turning an explanation into an unsolicited code review or rewrite.

## Explain a change for review

For a diff, PR, or implementation handoff, establish the requested comparison scope and base/head or working-tree state. A supplied excerpt may cover only part of the change. Resolve a materially ambiguous comparison before making before/after claims; do not silently mix staged, unstaged, and committed changes.

Read the actual diff, relevant old and new implementations, callers, contracts, and tests as needed. Ground intended behavior in the user's request or authoritative requirements; the implementation and its tests do not independently establish that the requirement was understood correctly. Treat the author's summary as a navigation aid and distinguish documented intent, source behavior, and inference.

Give a concise review guide scaled to the change and its risk:

- Explain the intended observable before/after behavior, using a concrete input or user action when helpful.
- Point to the code locations and constraints that determine the result, including unchanged callers or boundaries when relevant.
- Link verifiable validation evidence and describe what it establishes. Distinguish test code from a test run, source inspection from execution, and simulated checks from target-environment observations. State what was not checked and why the remaining uncertainty matters.

Use the existing PR description, conversation, or established project artifact. A small change may need only a few sentences; avoid creating a standalone report or one skill per PR unless explicitly requested. This guide supports review and does not certify correctness. A reviewer must assess the actual requirements, diff, and connected code independently; agreement between agents is not proof. If reporting a concrete defect, identify its location, trigger, incorrect behavior, impact, and supporting source or reproduction evidence; separate unresolved hypotheses from confirmed findings.

## Keep explanations and maintenance separate

Explanation is read-only unless the user also requests changes. Do not start history collection, rewrite skills or preferences, run the application, or invoke configured models just to explain source code. If a saved reference conflicts with current code, explain the current behavior and identify the stale reference; propose maintenance only when useful or requested.
