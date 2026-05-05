# Final Verification Summary

Use this reference when testing whether Codex closes public, harness, or high-trust work with enough evidence.

## Rule

Start as a manual shadow review. Do not create an enforcing hook until the checklist catches real gaps without encouraging verbose, formulaic final answers.

## Required Summary Contract

For non-trivial public, harness, or migration work, the final response should make these clear:

1. What changed.
2. Where the important changes live.
3. What verification ran and what passed.
4. What was intentionally not enabled, enforced, published, or changed.
5. What remains unverified.
6. What the next staged state is.

This does not require a rigid template. The final answer can be short, but it should not hide uncertainty or imply stronger enforcement than exists.

## Manual Shadow Review

Review the final answer and mark each item:

| Gate | Pass Criteria |
| --- | --- |
| Change summary | Names the substantive change, not just activity. |
| File evidence | Links or names the key changed files. |
| Verification evidence | Names real commands/checks and results. |
| Activation honesty | States whether a candidate is parked, explicit-only, pilot, shadow, or enforced. |
| Boundary clarity | States public/private boundary when the work touches public content or private harness details. |
| Unverified work | Explicitly says what remains unverified, or says nothing remains beyond listed future work. |
| Next state | Gives the next action only when it follows from evidence. |

Verdict:

- `pass`: all relevant gates are satisfied without bloating the answer.
- `revise`: one or more gates are missing but the work is otherwise sound.
- `block`: the answer overclaims completion, hides a failed check, or implies enforcement that is not active.

## Promotion Gate

Keep this candidate in `shadow` until it has reviewed at least three real completions:

- one public writing task
- one harness migration task
- one routine engineering task

Do not promote it to a hook if it mostly produces ceremonial wording. It should catch overclaims, missing verification, hidden uncertainty, or public/private boundary mistakes.

After the first shadow reviews, prefer folding minimal deterministic checks into an existing quality Stop hook instead of adding a second final-summary Stop hook. A narrow hollow-completion block can be useful; a parser that forces every final answer into a rigid template is not. Create a separate enforcing final-verification hook only if real completions show repeated gaps that the existing Stop gate cannot catch without noisy, formulaic output.
