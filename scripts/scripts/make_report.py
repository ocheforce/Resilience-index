#!/usr/bin/env python3

"""
make_report.py

Generate a simple HTML report for the Resilience Index.

Outputs:
- resilience_summary.html
- resilience_hist.png

Future versions may include:
- cohort comparisons
- longitudinal trends
- feature contribution analysis
- resistome-specific summaries
"""

import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def make_html(index_csv, out_html):

idx = pd.read_csv(index_csv, index_col=0)

if idx.empty:
    raise ValueError("Resilience index file is empty.")

report_path = Path(out_html)

report_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

img_path = report_path.parent / "resilience_hist.png"

# Plot distribution
fig, ax = plt.subplots(figsize=(7, 4))

sns.histplot(
    idx["resilience_score"],
    kde=True,
    ax=ax
)

ax.set_title(
    "Resilience Score Distribution"
)

ax.set_xlabel(
    "Resilience Score"
)

fig.tight_layout()

fig.savefig(
    img_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)

# Summary statistics
summary = {
    "Samples": len(idx),
    "Mean": idx["resilience_score"].mean(),
    "Median": idx["resilience_score"].median(),
    "Minimum": idx["resilience_score"].min(),
    "Maximum": idx["resilience_score"].max(),
    "Std Dev": idx["resilience_score"].std()
}

html = f"""
<html>
<head>
    <title>Resilience Index Report</title>
</head>

<body>

    <h1>Resilience Index Demo Report</h1>

    <p>
    Prototype report generated from
    combined clinical and resistome features.
    </p>

    <h2>Summary Statistics</h2>

    <table border="1" cellpadding="6">
        <tr>
            <th>Metric</th>
            <th>Value</th>
        </tr>

        <tr><td>Samples</td><td>{summary['Samples']}</td></tr>
        <tr><td>Mean</td><td>{summary['Mean']:.3f}</td></tr>
        <tr><td>Median</td><td>{summary['Median']:.3f}</td></tr>
        <tr><td>Minimum</td><td>{summary['Minimum']:.3f}</td></tr>
        <tr><td>Maximum</td><td>{summary['Maximum']:.3f}</td></tr>
        <tr><td>Std Dev</td><td>{summary['Std Dev']:.3f}</td></tr>
    </table>

    <h2>Distribution</h2>

    <img src="{img_path.name}"
         width="700">

    <h2>Source</h2>

    <p>
    Input file:
    {index_csv}
    </p>

</body>
</html>
"""

with open(report_path, "w") as f:
    f.write(html)

if name == "main":

parser = argparse.ArgumentParser(
    description="Generate Resilience Index report"
)

parser.add_argument(
    "--index",
    required=True,
    help="Resilience index CSV"
)

parser.add_argument(
    "--out",
    required=True,
    help="Output HTML report"
)

args = parser.parse_args()

make_html(
    args.index,
    args.out
)
