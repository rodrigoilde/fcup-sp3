"""Effect of the suppression limit on information loss and record loss."""

from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt

from _style import RESULTS, PALETTE, apply_style, save


def main() -> None:
    apply_style()
    df = pd.read_csv(RESULTS / "suppression_sweep.csv", sep=";")

    fig, ax1 = plt.subplots(figsize=(6.2, 3.6))
    ax1.plot(df["suppression_limit_pct"], df["info_loss_pct"],
             marker="o", color=PALETTE["primary"], linewidth=2,
             label="Information loss (%)")
    ax1.set_xlabel("Suppression limit (%)")
    ax1.set_ylabel("Information loss (%)", color=PALETTE["primary"])
    ax1.tick_params(axis="y", labelcolor=PALETTE["primary"])
    ax1.set_ylim(0, 45)

    ax2 = ax1.twinx()
    ax2.bar(df["suppression_limit_pct"], df["records_suppressed_pct"],
            width=0.7, color=PALETTE["accent"], alpha=0.35,
            label="Records suppressed (%)")
    ax2.set_ylabel("Records suppressed (%)", color=PALETTE["accent"])
    ax2.tick_params(axis="y", labelcolor=PALETTE["accent"])
    ax2.grid(False)
    ax2.set_ylim(0, max(df["records_suppressed_pct"]) * 1.4 + 1)

    fig.suptitle("Suppression-limit effect at k=5 (Adult, full-domain coding)",
                 fontsize=11, y=1.02)
    fig.tight_layout()
    save(fig, "suppression_sweep.png")


if __name__ == "__main__":
    main()
