# Beads Eval Summary

## What we tested

Whether Beads (a dependency-graph issue tracker built for AI coding agents) is worth adopting for the planned cookieworks-ai agent factory, versus GitHub Issues or a custom tracker. Rather than evaluate on paper, we built a throwaway 6-task project: a toy CLI unit converter, and ran the same dependency graph through Beads and through GitHub Issues.

The graph: one sequential scaffold task, three independent conversion modules (temperature, length, weight) that fan out from it in parallel, one integration task that converges on all three, and a final README task. Repo: [github.com/smslavin/beads-eval](https://github.com/smslavin/beads-eval).

## How it ran

Every worker agent was a subagent of the same Claude Code session, spawned via the built-in `Agent` tool with `isolation: "worktree"`, not a separate account, service, or process. We verified the model directly by grepping each worker's own transcript rather than assuming: all six ran on `claude-sonnet-5`, the same model as the orchestrating session, because no call overrode it.

Delegation was entirely manual. There is no dispatcher watching `bd ready` and spawning workers on its own. The orchestrating session played that role by hand for all 6 tasks: it read the task spec, wrote a fully self-contained prompt (subagents share none of the parent conversation's context), and claimed the bead. Once a worker finished, the session committed its worktree's output, merged, ran the full test suite, and closed the bead. That loop repeated once per task.

## What happened

All 6 tasks closed. 59 tests passing. Zero merge conflicts across three genuinely concurrent agents. `bd ready` correctly gated every stage: surfacing only the scaffold task at first, then exactly the three parallel modules once it closed, then only the integration task once all three of those closed.

## What we learned

**GitHub Issues is more capable than we assumed.** `gh issue create --blocked-by` gives real dependency edges with live blocker state, not a static label, as our first draft of the cookieworks-ai architecture doc claimed. What Beads has that GitHub doesn't is a *query*: `bd ready` versus a hand-written filter script. Beads still wins, but by less than we thought.

**Two Beads setup gotchas.** `.beads/issues.jsonl`, the file third-party viewer tools (a VSCode extension, a macOS app called PaiR) read, is an opt-in export, off by default. And git tracks `.beads/` state, so a claim only becomes visible to another worktree once it's committed; it isn't a live shared server in Beads' default single-writer mode.

**Worktrees don't auto-commit.** The `Agent` tool's `isolation: "worktree"` hands back files, not a commit. Staging and committing has to be an explicit step.

**A worktree's base commit can be stale relative to its own dependencies.** The README task's worktree branched from a commit that predated the integration task it depended on even being claimed, despite Beads showing that dependency closed, and despite creating the worktree a full conversation turn after the integration work had already merged. The worker only caught it because its definition of done required actually running the CLI, not just writing code against it: it hit a real argument-parsing error, diagnosed the stale base, and worked around it safely. That's the strongest argument to come out of this eval for requiring every task's done-check to execute something real, not just produce a diff.

## What it cost

| Task | Tokens | Tool calls | Wall-clock |
|---|---|---|---|
| Scaffold | 36,489 | 15 | ~71s |
| Temperature | 37,483 | 4 | ~30s |
| Length | 37,043 | 4 | ~28s |
| Weight | 40,878 | 5 | ~34s |
| Integration | 46,300 | 14 | ~52s |
| README | 59,917 | 27 | ~13.2 hrs* |
| **Total** | **~258,110** | **69** | — |

\* Real elapsed time between the task's first and last transcript timestamp, most likely from sitting backgrounded overnight, not 13 hours of billed compute. Billing is token-based, not duration-based; the 59,917 tokens are the figure that matters.

Three ways to check usage going forward:
- Per-task token/tool-call/duration figures return automatically in every task-completion notification.
- Claude Code's `/cost` command gives a running total for the whole session.
- Raw JSONL transcripts (session plus one file per subagent) sit on disk with per-message token usage, for anyone who wants to compute exact cost by hand.

Account-level billing ground truth lives on console.anthropic.com or claude.ai's usage page, depending on billing mode.

## Scaling and what's next

What the eval proved (`bd ready`/claim correctness, zero-collision fan-out) should hold at cookieworks-ai's real scale (roughly 100-300 tasks), on the condition that every task keeps meeting the same sizing discipline that made fan-out collision-free here.

What doesn't scale as run today: a human manually driving the claim-dispatch-merge-close loop for every single task is the same hand-off bottleneck this whole effort set out to reduce, just moved from writing code to babysitting a loop. The stale-worktree failure mode will recur more often at higher volume and needs to become an automated pre-flight check rather than something a worker happens to notice. And the review-gate workflow itself is still untested: every merge in this eval went straight to a local `master`, never through a real pull request.

The fix for the first two is a small, purpose-built dispatcher script: poll `bd ready`, claim, spawn a worker, verify the worktree's base actually contains its dependencies' merge commits before it starts, commit its output, open a PR, run cross-cutting checks, close the task. That's mechanical: no judgment required, so it's a reasonable thing to automate.

Two things stay manual on purpose. Decomposing a plan into correctly-sized tasks is the actual bottleneck this whole design addresses, not something to automate away. And every merge needs a human look before it happens. Automating that away would just rebuild the review-bypass approach this design rejected from the start.
