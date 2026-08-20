# Submission README

## Track Chosen

Track A: Fictional Domain Packet (SignalDesk).

## What I Built

A single script (`analyze.py`) that cleans `product_usage_events.csv` and produces
`health_check_report.md` — a weekly health check for the three AI workflows, broken
down by workflow *and* source (since sessions across sources aren't comparable),
plus a short "what looks suspicious / what to look at next" section. Run it with
`python3 analyze.py`. `test_analyze.py` is a small self-check on the cleaning logic.

## Who It Is For

The teammate who asked "what's working, what's suspicious, what should we look at
next" — someone who wants a 2-minute read, not a dashboard, before their next
standup or planning call.

## Data Or Source Used

`sample-data/product_usage_events.csv` from this repo (fictional, 41 rows, one week
of daily workflow usage across Sales/Support/Product).

## Assumptions I Made

- Sessions across different `source`s (email vs. manual vs. queue vs. csv upload)
  are not directly comparable, so I aggregated by (workflow, source), not just
  workflow.
- `median_confidence` should not be treated as a quality signal — I checked whether
  it moved with `user_rating` and it didn't (see report), which supports the domain
  packet's warning.
- The 2026-08-05 demo-account spike and the 2026-08-07 duplicate row are data
  artifacts, not real usage — I dropped the exact duplicate and called out the spike
  rather than silently smoothing either into the aggregates.

## Data Issues Or Caveats I Noticed

- One exact-duplicate export row (2026-08-05 Lead summary/email).
- Inconsistent team casing (`product` vs `Product`).
- `median_confidence` stored as text `"n/a"` on one row, not blank.
- One blank `user_rating`.
- A traffic spike explicitly flagged in `notes` as coming from a demo account.
- A same-day policy change (8/7) that moves completion, flag rate, and rating
  sharply — genuinely ambiguous whether that's a quality problem or the review
  policy doing its job.

## What I Would Do Next With More Time

Track day-over-day trend within the week (not just the week's total) to see if
Lead summary's acceptance rate is still rising after the 8/4 prompt change, and
add a second week of data to tell a policy effect apart from a one-day blip.
