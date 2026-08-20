# SignalDesk Weekly Health Check

Rows used: 40 (dropped 1 exact-duplicate export row(s))

## Workflow x Source Breakdown

| Workflow | Source | Sessions | Completion | Acceptance | Flag rate | Avg min saved | Avg confidence | Avg rating |
|---|---|---|---|---|---|---|---|---|
| Feedback clustering | csv upload | 149 | 64% | 68% | 13% | 13.8 | 0.63 | 3.8 |
| Feedback clustering | manual | 58 | 72% | 62% | 12% | 11.0 | 0.55 | 3.5 |
| Lead summary | email | 450 | 84% | 85% | 5% | 9.0 | 0.80 | 4.3 |
| Lead summary | manual | 140 | 70% | 70% | 9% | 6.4 | 0.65 | 3.9 |
| Reply draft | manual | 84 | 74% | 66% | 10% | 3.3 | 0.71 | 3.8 |
| Reply draft | queue | 426 | 82% | 77% | 14% | 3.8 | 0.86 | 3.8 |

## What Looks Suspicious

- Found 1 exact-duplicate export row(s) (e.g. 2026-08-05 Lead summary/email) — dropped before aggregating.
- 2026-08-05 Sales/Lead summary/email has 140 sessions vs a ~45-60 baseline, and its own note says "traffic spike from demo account." Left in the table above but it is not representative of normal internal usage — a real health check should exclude demo-account traffic or track it separately.
- 2026-08-07 Support/Reply draft/queue: completion rate drops to ~57% (vs ~80-85% all week), flag rate jumps to 40%, and rating craters to 2.1. The note ("review policy changed mid-day") suggests this is a policy effect (more human review triggered), not necessarily worse AI output — but it's the single biggest one-day swing in the dataset and deserves a look before drawing conclusions.

## Which Metric To Trust Least

`median_confidence` — it climbs steadily across the week for every workflow even on the day quality/rating clearly got worse (Reply draft, 8/7: confidence 0.91, its highest of the week, while rating fell to 2.1). Confidence tracks the model's own certainty, not whether the output was actually good, and this dataset is a clean example of that gap. `avg_minutes_saved` is also self-reported/estimated and should be read as directional only.

## Which Workflow Looks Most Useful Right Now

Lead summary (email) has the highest acceptance rate (~75-85%), the lowest flag rate, and the highest ratings of any group not distorted by the demo-account spike or the policy-change day. Feedback clustering is the weakest: acceptance sits around 60-65% even though sessions are still low, which is worth watching as usage grows.

## What To Look At Next

1. Confirm the 8/7 Reply draft drop is a review-policy effect, not a quality regression.
2. Exclude or separately tag demo-account traffic before trusting session-volume trends.
3. Stop treating `median_confidence` as a quality proxy in any dashboard.
4. Watch Feedback clustering's acceptance rate as it scales past small-sample volume.
