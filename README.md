# Submission README

## Track Chosen

Track A: Fictional Domain Packet (SignalDesk).

## What I Built

`analyze.py` cleans `product_usage_events.csv` and writes `health_check_report.md`
— a weekly health check for the three AI workflows, broken down by workflow *and*
source (sessions aren't comparable across sources), plus "what looks suspicious /
what to look at next." Run with `python3 analyze.py`. `test_analyze.py` is a small
self-check on the cleaning logic.

## Who It Is For

The teammate who asked what's working and what's suspicious — a 2-minute read
before a standup, not a dashboard.

## Data Or Source Used

`sample-data/product_usage_events.csv` from this repo (fictional, 41 rows, one
week of daily workflow usage across Sales/Support/Product).

## Assumptions I Made

- Sessions across different `source`s aren't directly comparable, so I
  aggregated by (workflow, source), not workflow alone.
- `median_confidence` isn't a quality signal — checked it against `user_rating`;
  no correlation (see report).
- The 8/5 demo-account spike and duplicate row are data artifacts, not real
  usage — dropped the duplicate, called out the spike instead of smoothing it in.

## Data Issues Or Caveats I Noticed

- One exact-duplicate export row (2026-08-05 Lead summary/email).
- Inconsistent team casing (`product` vs `Product`).
- `median_confidence` stored as text `"n/a"` on one row, not blank.
- One blank `user_rating`.
- A traffic spike explicitly tagged in `notes` as a demo account.
- A same-day policy change (8/7) that moves completion, flag rate, and rating
  sharply — ambiguous whether that's a quality problem or review working as
  intended.

## What I Would Do Next With More Time

Track day-over-day trend, not just the week's total, to see if Lead summary's
acceptance rate is still rising after the 8/4 prompt change, and add a second
week of data to tell a policy effect apart from a one-day blip.
