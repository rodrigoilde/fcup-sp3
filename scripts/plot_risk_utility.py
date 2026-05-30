"""Pareto-style risk vs. utility scatter, all runs combined."""

from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt

from _style import RESULTS, PALETTE, apply_style, save

MODEL_STYLE = {
    "Original": dict(marker="X", color=PALETTE["dark"], s=120),
    "k-anonymity": dict(marker="o", color=PALETTE["primary"], s=70),
    "k-anon+l-div": dict(marker="^", color=PALETTE["accent"], s=70),
    "local-recoding": dict(marker="D", color=PALETTE["secondary"], s=70),
}


def main() -> None:
    apply_style()
    df = pd.read_csv(RESULTS / "pareto.csv", sep=";")

    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    for model, style in MODEL_STYLE.items():
        sub = df[df["model"] == model]
        ax.scatter(sub["prosecutor_risk"] * 100, sub["info_loss_pct"],
                   label=model, edgecolor="white", linewidth=0.7, **style)
        for _, row in sub.iterrows():
            ax.annotate(row["label"],
                        (row["prosecutor_risk"] * 100, row["info_loss_pct"]),
                        textcoords="offset points", xytext=(7, -2),
                        fontsize=8, color="#333333")

    ax.axvspan(0, 5, color=PALETTE["secondary"], alpha=0.08)
    ax.text(0.2, 92, "low-risk\nregion", fontsize=8,
            color=PALETTE["secondary"], ha="left")

    ax.set_xscale("symlog", linthresh=1)
    ax.set_xlabel("Maximum prosecutor re-identification risk (%)")
    ax.set_ylabel("Information loss (%)")
    ax.set_ylim(-3, 100)
    ax.legend(loc="upper right")
    ax.set_title("Risk-vs-utility Pareto landscape (Adult, 6 QIDs)")
    fig.tight_layout()
    save(fig, "pareto.png")


if __name__ == "__main__":
    main()
