# AI Collaboration Note

## Did You Use AI?

Yes, Claude Code.

## How You Used It

I had it read the domain packet, challenge, rubric, and sample CSV, then write
`analyze.py` and the report structure in one pass, and add the self-check test.

## One Prompt, Workflow, Or Moment That Helped

Asking it to actually eyeball every row of the 41-row CSV (not just summary stats)
is what surfaced the duplicate row, the `n/a`-as-text confidence value, and the
casing inconsistency — the kind of scan that's easy to skip by hand.

## One Thing You Verified Or Decided Yourself

I checked the confidence-vs-quality claim in the report by hand against the raw
rows (8/7 Reply draft: confidence 0.91 but rating 2.1) before keeping it, and I
decided which single angle to build (workflow x source health check, not a
multi-view dashboard) rather than taking the first structure it produced.
