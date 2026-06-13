"""
Build the EventLens trust-vs-Brier validation report.

Primary statistics use one observation per resolved market, selected by the
pre-registered METHODOLOGY.md rule: the latest validation-eligible snapshot
observed at least 24 hours before close/resolution. Markets whose only
eligible snapshots fall inside that 24h window are excluded from the primary
headline and reported separately as short-horizon descriptive evidence.
Score-version cuts use one latest snapshot per market per version so
methodology comparisons remain visible.
"""

import argparse
import json
import math
import os
from collections import defaultdict
from datetime import datetime, timedelta, timezone

DEFAULT_INPUT = os.path.join("data", "validation", "brier_rows.json")
DEFAULT_JSON = os.path.join("data", "validation", "validation_report.json")
DEFAULT_MARKDOWN = os.path.join("data", "validation", "validation_report.md")
DEFAULT_CHART = os.path.join("data", "validation", "trust_vs_brier.svg")

PRIMARY_SNAPSHOT_BUFFER_HOURS = 24
PRIMARY_SNAPSHOT_RULE = "latest eligible snapshot at least 24h before close"

TRUST_BUCKETS = [
    ("0-40", 0, 40),
    ("40-55", 40, 55),
    ("55-70", 55, 70),
    ("70-85", 70, 85),
    ("85-100", 85, 101),
]


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_float(value):
    try:
        if value is None or value == "":
            return None
        number = float(value)
        return number if math.isfinite(number) else None
    except (TypeError, ValueError):
        return None


def load_rows(path):
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    rows = payload.get("rows", []) if isinstance(payload, dict) else []
    return rows if isinstance(rows, list) else []


def valid_analysis_row(row):
    if not isinstance(row, dict):
        return False
    trust = safe_float(row.get("composite_trust_score"))
    brier = safe_float(row.get("brier"))
    return bool(
        row.get("validation_eligible", True)
        and trust is not None and 0 <= trust <= 100
        and brier is not None and 0 <= brier <= 1
        and row.get("market_id")
        and row.get("observed_at")
    )


def parse_ts(s):
    """Tolerates both '2026-06-12T22:40:52Z' and '2026-06-12 22:40:52+00'."""
    if not s:
        return None
    s = str(s).strip().replace(" ", "T", 1).replace("Z", "+00:00")
    if s.endswith("+00"):
        s += ":00"
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def latest_rows(rows, key_fields=("market_id",)):
    latest = {}
    for row in rows:
        key = tuple(str(row.get(field)) for field in key_fields)
        current = latest.get(key)
        if current is None or str(row["observed_at"]) > str(current["observed_at"]):
            latest[key] = row
    return list(latest.values())


def primary_rows_24h_buffer(rows):
    """Pre-registered primary selection (METHODOLOGY.md): per market, the
    latest eligible snapshot observed at least 24h before close/resolution.
    Guards the headline against last-minute price-collapse contamination."""
    latest = {}
    buffer = timedelta(hours=PRIMARY_SNAPSHOT_BUFFER_HOURS)
    for row in rows:
        observed = parse_ts(row.get("observed_at"))
        closed = parse_ts(row.get("closed_time"))
        if observed is None or closed is None:
            continue
        if observed > closed - buffer:
            continue
        key = str(row.get("market_id"))
        current = latest.get(key)
        if current is None or str(row["observed_at"]) > str(current["observed_at"]):
            latest[key] = row
    return list(latest.values())


def mean(values):
    return sum(values) / len(values) if values else None


def pearson(rows):
    pairs = [
        (safe_float(row.get("composite_trust_score")), safe_float(row.get("brier")))
        for row in rows
    ]
    pairs = [(x, y) for x, y in pairs if x is not None and y is not None]
    if len(pairs) < 2:
        return {"correlation": None, "n": len(pairs)}
    xs, ys = zip(*pairs)
    x_mean, y_mean = mean(xs), mean(ys)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in pairs)
    x_ss = sum((x - x_mean) ** 2 for x in xs)
    y_ss = sum((y - y_mean) ** 2 for y in ys)
    correlation = numerator / math.sqrt(x_ss * y_ss) if x_ss > 0 and y_ss > 0 else None
    return {"correlation": correlation, "n": len(pairs)}


def grouped_summary(rows, field):
    groups = defaultdict(list)
    for row in rows:
        groups[str(row.get(field) or "Unknown")].append(float(row["brier"]))
    return [
        {"group": group, "mean_brier": mean(values), "n": len(values)}
        for group, values in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0]))
    ]


def trust_bucket_summary(rows):
    summary = []
    for label, lower, upper in TRUST_BUCKETS:
        values = [
            float(row["brier"])
            for row in rows
            if lower <= float(row["composite_trust_score"]) < upper
        ]
        summary.append({"bucket": label, "mean_brier": mean(values), "n": len(values)})
    return summary


def score_version_summary(rows):
    version_rows = latest_rows(rows, ("market_id", "score_version"))
    grouped = defaultdict(list)
    for row in version_rows:
        grouped[str(row.get("score_version") or "Unknown")].append(row)
    result = []
    for version, items in sorted(grouped.items()):
        result.append(
            {
                "score_version": version,
                "mean_brier": mean([float(item["brier"]) for item in items]),
                "trust_vs_brier": pearson(items),
                "n": len(items),
            }
        )
    return result


def build_report(rows):
    eligible_rows = [row for row in rows if valid_analysis_row(row)]
    primary_rows = primary_rows_24h_buffer(eligible_rows)
    no_missing_spread = [row for row in primary_rows if row.get("spread_is_missing") is False]

    # Markets with eligible rows but no snapshot >=24h before close: excluded
    # from the headline, reported as short-horizon descriptive evidence only.
    primary_ids = {str(row["market_id"]) for row in primary_rows}
    short_horizon_rows = latest_rows(
        [row for row in eligible_rows if str(row["market_id"]) not in primary_ids]
    )

    return {
        "generated_at": utc_now(),
        "analysis_unit": "one snapshot per resolved market, selected by the primary snapshot rule",
        "primary_snapshot_rule": PRIMARY_SNAPSHOT_RULE,
        "n_brier_rows": len(rows),
        "n_eligible_brier_rows": len(eligible_rows),
        "n_unique_resolved_markets": len({str(row["market_id"]) for row in eligible_rows}),
        "n_analysis_rows": len(primary_rows),
        "n_markets_excluded_no_24h_snapshot": len(short_horizon_rows),
        "short_horizon_descriptive": {
            "note": "markets without any eligible snapshot >=24h before close; not part of the primary validation",
            "n": len(short_horizon_rows),
            "mean_brier": mean([float(row["brier"]) for row in short_horizon_rows]),
            "trust_vs_brier": pearson(short_horizon_rows),
        },
        "mean_brier": mean([float(row["brier"]) for row in primary_rows]),
        "trust_buckets": trust_bucket_summary(primary_rows),
        "horizon_buckets": grouped_summary(primary_rows, "horizon_bucket"),
        "categories": grouped_summary(primary_rows, "category"),
        "market_types": grouped_summary(primary_rows, "market_type"),
        "trust_vs_brier": pearson(primary_rows),
        "trust_vs_brier_excluding_missing_spread": pearson(no_missing_spread),
        "by_score_version": score_version_summary(eligible_rows),
    }


def fmt_number(value, digits=4):
    return "N/A" if value is None else f"{value:.{digits}f}"


def markdown_table(headers, rows):
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(str(value) for value in row) + " |" for row in rows)
    return "\n".join(lines)


def render_markdown(report):
    correlation = report["trust_vs_brier"]
    correlation_no_spread = report["trust_vs_brier_excluding_missing_spread"]
    sections = [
        "# EventLens Validation Report",
        "",
        f"Generated: `{report['generated_at']}`",
        "",
        f"- Brier rows: {report['n_brier_rows']}",
        f"- Eligible Brier rows: {report['n_eligible_brier_rows']}",
        f"- Unique resolved markets: {report['n_unique_resolved_markets']}",
        f"- Primary analysis rows: {report['n_analysis_rows']}",
        f"- Markets excluded from primary (no 24h-prior snapshot): {report['n_markets_excluded_no_24h_snapshot']}",
        f"- Mean Brier: {fmt_number(report['mean_brier'])}",
        f"- Trust vs Brier correlation: {fmt_number(correlation['correlation'])} (n={correlation['n']})",
        (
            "- Trust vs Brier excluding missing spreads: "
            f"{fmt_number(correlation_no_spread['correlation'])} (n={correlation_no_spread['n']})"
        ),
        "",
        "Primary statistics use the latest eligible snapshot observed at least "
        "24 hours before close/resolution (pre-registered in METHODOLOGY.md). "
        "Markets with only same-day snapshots appear in the short-horizon "
        "descriptive section, not the headline.",
        "",
        "## Trust Buckets",
        "",
        markdown_table(
            ["Trust bucket", "Mean Brier", "n"],
            [
                [item["bucket"], fmt_number(item["mean_brier"]), item["n"]]
                for item in report["trust_buckets"]
            ],
        ),
    ]

    for title, column, key in (
        ("Horizon Buckets", "Horizon bucket", "horizon_buckets"),
        ("Categories", "Category", "categories"),
        ("Market Types", "Market type", "market_types"),
    ):
        sections.extend(
            [
                "",
                f"## {title}",
                "",
                markdown_table(
                    [column, "Mean Brier", "n"],
                    [
                        [item["group"], fmt_number(item["mean_brier"]), item["n"]]
                        for item in report[key]
                    ],
                ),
            ]
        )

    short = report["short_horizon_descriptive"]
    sections.extend(
        [
            "",
            "## Short-Horizon Descriptive (excluded from primary)",
            "",
            f"- Markets: {short['n']}",
            f"- Mean Brier: {fmt_number(short['mean_brier'])}",
            f"- Trust vs Brier correlation: {fmt_number(short['trust_vs_brier']['correlation'])} (n={short['trust_vs_brier']['n']})",
            "",
            "These markets had no eligible snapshot at least 24 hours before close. "
            "Descriptive only — not part of the pre-registered primary validation.",
        ]
    )

    sections.extend(["", "## Score Versions", ""])
    sections.append(
        markdown_table(
            ["Score version", "Mean Brier", "Trust correlation", "n"],
            [
                [
                    item["score_version"],
                    fmt_number(item["mean_brier"]),
                    fmt_number(item["trust_vs_brier"]["correlation"]),
                    item["n"],
                ]
                for item in report["by_score_version"]
            ],
        )
    )
    return "\n".join(sections) + "\n"


def linear_fit(rows):
    pairs = [
        (float(row["composite_trust_score"]), float(row["brier"]))
        for row in rows
    ]
    if len(pairs) < 2:
        return None
    x_mean = mean([x for x, _ in pairs])
    y_mean = mean([y for _, y in pairs])
    denominator = sum((x - x_mean) ** 2 for x, _ in pairs)
    if denominator == 0:
        return None
    slope = sum((x - x_mean) * (y - y_mean) for x, y in pairs) / denominator
    return slope, y_mean - slope * x_mean


def render_svg(rows):
    width, height = 900, 560
    left, right, top, bottom = 80, 30, 45, 70
    plot_width = width - left - right
    plot_height = height - top - bottom
    y_max = max(0.25, max(float(row["brier"]) for row in rows))

    def sx(value):
        return left + (float(value) / 100) * plot_width

    def sy(value):
        return top + (1 - float(value) / y_max) * plot_height

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="450" y="25" text-anchor="middle" font-family="sans-serif" font-size="20">Trust score vs realized Brier error</text>',
    ]
    for tick in range(0, 101, 20):
        x = sx(tick)
        elements.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{height-bottom}" stroke="#e5e7eb"/>')
        elements.append(f'<text x="{x:.1f}" y="{height-bottom+24}" text-anchor="middle" font-family="sans-serif" font-size="12">{tick}</text>')
    for index in range(6):
        value = y_max * index / 5
        y = sy(value)
        elements.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" stroke="#e5e7eb"/>')
        elements.append(f'<text x="{left-12}" y="{y+4:.1f}" text-anchor="end" font-family="sans-serif" font-size="12">{value:.2f}</text>')

    for row in rows:
        elements.append(
            f'<circle cx="{sx(row["composite_trust_score"]):.1f}" cy="{sy(row["brier"]):.1f}" '
            'r="4" fill="#2563eb" fill-opacity="0.65"/>'
        )

    fit = linear_fit(rows)
    if fit:
        slope, intercept = fit
        y0 = min(y_max, max(0, intercept))
        y1 = min(y_max, max(0, slope * 100 + intercept))
        elements.append(
            f'<line x1="{sx(0):.1f}" y1="{sy(y0):.1f}" x2="{sx(100):.1f}" y2="{sy(y1):.1f}" '
            'stroke="#dc2626" stroke-width="3"/>'
        )

    bucket_points = []
    for item, (_, lower, upper) in zip(trust_bucket_summary(rows), TRUST_BUCKETS):
        if item["mean_brier"] is not None:
            bucket_points.append(f'{sx((lower + min(upper, 100)) / 2):.1f},{sy(item["mean_brier"]):.1f}')
    if bucket_points:
        elements.append(
            f'<polyline points="{" ".join(bucket_points)}" fill="none" stroke="#16a34a" stroke-width="3"/>'
        )

    elements.extend(
        [
            f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#111827"/>',
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#111827"/>',
            f'<text x="{left + plot_width/2:.1f}" y="{height-18}" text-anchor="middle" font-family="sans-serif" font-size="14">Composite trust score</text>',
            (
                f'<text x="20" y="{top + plot_height/2:.1f}" text-anchor="middle" '
                'font-family="sans-serif" font-size="14" '
                f'transform="rotate(-90 20 {top + plot_height/2:.1f})">Realized Brier error</text>'
            ),
            "</svg>",
        ]
    )
    return "\n".join(elements)


def write_text(path, content):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description="Build EventLens Brier validation outputs.")
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--json-output", default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    parser.add_argument("--chart-output", default=DEFAULT_CHART)
    args = parser.parse_args()

    rows = load_rows(args.input)
    report = build_report(rows)
    write_text(args.json_output, json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    write_text(args.markdown_output, render_markdown(report))

    primary_rows = primary_rows_24h_buffer([row for row in rows if valid_analysis_row(row)])
    chart_status = "not generated (need at least 2 resolved markets)"
    if len(primary_rows) >= 2:
        write_text(args.chart_output, render_svg(primary_rows))
        chart_status = args.chart_output

    print(f"Brier rows:              {report['n_brier_rows']}")
    print(f"Unique resolved markets: {report['n_unique_resolved_markets']}")
    print(f"Analysis rows:           {report['n_analysis_rows']}")
    print(f"Trust/Brier correlation: {fmt_number(report['trust_vs_brier']['correlation'])}")
    print(f"JSON report:             {args.json_output}")
    print(f"Markdown report:         {args.markdown_output}")
    print(f"Chart:                   {chart_status}")


if __name__ == "__main__":
    main()
