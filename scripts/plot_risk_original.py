"""Bar chart of re-identification risk metrics on the original Adult table."""

from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt

from _style import RESULTS, PALETTE, apply_style, save


def main() -> None:
    apply_style()
    df = pd.read_csv(RESULTS / "risk_original.csv", sep=";")
    keys = ["prosecutor_avg_risk", "marketer_risk",
            "sample_uniqueness", "records_with_risk_above_20pct"]
    labels = ["Prosecutor (avg)", "Marketer", "Sample uniqueness",
              "Records at risk > 20%"]
    vals = [float(df[df["metric"] == k]["value"].iloc[0]) * 100 for k in keys]

    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    bars = ax.barh(labels, vals,
                   color=[PALETTE["accent"], PALETTE["muted"],
                          PALETTE["warn"], PALETTE["primary"]])
    ax.set_xlabel("Population fraction / risk (%)")
    ax.set_xlim(0, max(vals) * 1.2)
    for bar, value in zip(bars, vals):
        ax.text(value + 0.6, bar.get_y() + bar.get_height() / 2,
                f"{value:.1f}%", va="center", fontsize=9)
    ax.set_title("Re-identification risk of the original Adult dataset (6 QIDs)")
    fig.tight_layout()
    save(fig, "risk_original.png")


if __name__ == "__main__":
    main()
