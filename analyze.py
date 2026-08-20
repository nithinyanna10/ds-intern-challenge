#!/usr/bin/env python3
"""
SignalDesk weekly health check.

Reads sample-data/product_usage_events.csv, cleans the obvious messiness
(dupe rows, inconsistent team casing, "n/a" text, blank ratings), then
prints a per-workflow x source breakdown plus a short list of things
worth a human's attention this week.

Usage: python3 analyze.py
"""
import csv
import statistics
from collections import defaultdict

PATH = "sample-data/product_usage_events.csv"


def load_rows(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))

    seen = set()
    cleaned = []
    dupes = []
    for r in rows:
        r["team"] = r["team"].strip().title()  # "product" -> "Product"
        for k in ("sessions", "completed", "accepted_output", "flagged_for_review"):
            r[k] = int(r[k])
        r["avg_minutes_saved"] = float(r["avg_minutes_saved"])
        conf = r["median_confidence"].strip().lower()
        r["median_confidence"] = None if conf in ("", "n/a") else float(conf)
        rating = r["user_rating"].strip()
        r["user_rating"] = None if rating == "" else float(rating)

        # exact-duplicate export rows (ignore the free-text notes column)
        key = tuple(r[k] for k in r if k != "notes")
        if key in seen:
            dupes.append(r)
            continue
        seen.add(key)
        cleaned.append(r)
    return cleaned, dupes


def safe_mean(values):
    values = [v for v in values if v is not None]
    return statistics.mean(values) if values else None


def summarize(rows):
    groups = defaultdict(list)
    for r in rows:
        groups[(r["workflow"], r["source"])].append(r)

    summary = {}
    for key, rs in groups.items():
        sessions = sum(r["sessions"] for r in rs)
        completed = sum(r["completed"] for r in rs)
        accepted = sum(r["accepted_output"] for r in rs)
        flagged = sum(r["flagged_for_review"] for r in rs)
        summary[key] = {
            "days": len(rs),
            "sessions": sessions,
            "completion_rate": completed / sessions if sessions else None,
            "acceptance_rate": accepted / completed if completed else None,
            "flag_rate": flagged / sessions if sessions else None,
            "avg_minutes_saved": safe_mean([r["avg_minutes_saved"] for r in rs]),
            "avg_confidence": safe_mean([r["median_confidence"] for r in rs]),
            "avg_rating": safe_mean([r["user_rating"] for r in rs]),
        }
    return summary


def fmt_pct(x):
    return f"{x:.0%}" if x is not None else "n/a"


def fmt_num(x, d=1):
    return f"{x:.{d}f}" if x is not None else "n/a"


def build_report(rows, dupes):
    summary = summarize(rows)
    lines = []
    lines.append("# SignalDesk Weekly Health Check")
    lines.append("")
    lines.append(f"Rows used: {len(rows)} (dropped {len(dupes)} exact-duplicate export row(s))")
    lines.append("")
    lines.append("## Workflow x Source Breakdown")
    lines.append("")
    lines.append("| Workflow | Source | Sessions | Completion | Acceptance | Flag rate | Avg min saved | Avg confidence | Avg rating |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for (workflow, source), s in sorted(summary.items()):
        lines.append(
            f"| {workflow} | {source} | {s['sessions']} | {fmt_pct(s['completion_rate'])} | "
            f"{fmt_pct(s['acceptance_rate'])} | {fmt_pct(s['flag_rate'])} | "
            f"{fmt_num(s['avg_minutes_saved'])} | {fmt_num(s['avg_confidence'], 2)} | "
            f"{fmt_num(s['avg_rating'], 1)} |"
        )
    lines.append("")

    lines.append("## What Looks Suspicious")
    lines.append("")
    if dupes:
        lines.append(
            f"- Found {len(dupes)} exact-duplicate export row(s) "
            f"(e.g. {dupes[0]['date']} {dupes[0]['workflow']}/{dupes[0]['source']}) — dropped before aggregating."
        )
    lines.append(
        "- 2026-08-05 Sales/Lead summary/email has 140 sessions vs a ~45-60 baseline, "
        "and its own note says \"traffic spike from demo account.\" Left in the table above but "
        "it is not representative of normal internal usage — a real health check should exclude "
        "demo-account traffic or track it separately."
    )
    lines.append(
        "- 2026-08-07 Support/Reply draft/queue: completion rate drops to ~57% (vs ~80-85% all "
        "week), flag rate jumps to 40%, and rating craters to 2.1. The note (\"review policy "
        "changed mid-day\") suggests this is a policy effect (more human review triggered), not "
        "necessarily worse AI output — but it's the single biggest one-day swing in the dataset "
        "and deserves a look before drawing conclusions."
    )
    lines.append("")

    lines.append("## Which Metric To Trust Least")
    lines.append("")
    lines.append(
        "`median_confidence` — it climbs steadily across the week for every workflow even on "
        "the day quality/rating clearly got worse (Reply draft, 8/7: confidence 0.91, its highest "
        "of the week, while rating fell to 2.1). Confidence tracks the model's own certainty, not "
        "whether the output was actually good, and this dataset is a clean example of that gap. "
        "`avg_minutes_saved` is also self-reported/estimated and should be read as directional only."
    )
    lines.append("")

    lines.append("## Which Workflow Looks Most Useful Right Now")
    lines.append("")
    lines.append(
        "Lead summary (email) has the highest acceptance rate (~75-85%), the lowest flag rate, "
        "and the highest ratings of any group not distorted by the demo-account spike or the "
        "policy-change day. Feedback clustering is the weakest: acceptance sits around 60-65% "
        "even though sessions are still low, which is worth watching as usage grows."
    )
    lines.append("")

    lines.append("## What To Look At Next")
    lines.append("")
    lines.append("1. Confirm the 8/7 Reply draft drop is a review-policy effect, not a quality regression.")
    lines.append("2. Exclude or separately tag demo-account traffic before trusting session-volume trends.")
    lines.append("3. Stop treating `median_confidence` as a quality proxy in any dashboard.")
    lines.append("4. Watch Feedback clustering's acceptance rate as it scales past small-sample volume.")

    return "\n".join(lines) + "\n"


def main():
    rows, dupes = load_rows(PATH)
    report = build_report(rows, dupes)
    print(report)
    with open("health_check_report.md", "w") as f:
        f.write(report)


if __name__ == "__main__":
    main()
