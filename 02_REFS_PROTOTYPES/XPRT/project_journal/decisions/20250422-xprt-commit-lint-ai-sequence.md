# Decision Log: XPRT-Commit Lint/AI Sequence

**Date:** 2025-04-22

## Decision

For Task XPRTC-002, the recommended sequence for AI-assisted commits is:

1.  Run `lint-staged` on the currently staged files.
2.  Handle any failures reported by `lint-staged`.
3.  If `lint-staged` succeeds (potentially after autofixes), get the _final_ staged diff.
4.  Pass the final diff to the AI (Ollama) to generate the commit message suggestion.
5.  Present the suggestion to the user for editing/confirmation.

## Rationale

- **Accuracy:** Generating the message based on the _final_ staged diff (post-autofix) ensures the message accurately reflects the code being committed.
- **Workflow Integrity:** Prevents situations where a user approves a commit message, only for the commit to fail later due to lint errors or for the message to become inaccurate due to autofixes applied by `lint-staged` during the commit hook phase (if configured).
- **Clear Feedback:** Allows for clear user feedback if `lint-staged` fails, prompting necessary fixes before proceeding. While potentially slower if fixes are needed, it leads to a cleaner overall commit process.

## Alternatives Considered

- **Generate Message First:** Generate the message based on the initial diff, then run lint-staged. Rejected because the message might not reflect autofixes, and late-breaking lint failures disrupt the user flow after message approval.
