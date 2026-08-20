"""Smallest possible self-check: dedup + missing-value handling behave as expected."""
from analyze import load_rows, summarize, safe_mean


def test_dedup_and_missing_values():
    rows, dupes = load_rows("sample-data/product_usage_events.csv")
    assert len(dupes) == 1, "expected exactly one exact-duplicate export row"
    assert len(rows) == 41 - len(dupes)

    # "n/a" confidence and blank rating must become None, not crash or become 0
    na_conf_row = next(r for r in rows if r["date"] == "2026-08-05" and r["notes"] == "confidence missing as text")
    assert na_conf_row["median_confidence"] is None

    blank_rating_row = next(r for r in rows if r["notes"] == "missing rating")
    assert blank_rating_row["user_rating"] is None

    assert safe_mean([1.0, None, 3.0]) == 2.0
    assert safe_mean([None, None]) is None

    summary = summarize(rows)
    assert ("Lead summary", "email") in summary
    assert summary[("Lead summary", "email")]["sessions"] == 450


if __name__ == "__main__":
    test_dedup_and_missing_values()
    print("ok")
