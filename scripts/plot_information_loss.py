"""Two information-loss perspectives:
  (a) k-anonymity-only vs k-anonymity + l-diversity at matched k.
  (b) coding-model comparison (global full-domain vs subtree vs local).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from _style import RESULTS, PALETTE, apply_style, save


def main() -> None:
    apply_style()
    k = pd.read_csv(RESULTS / "k_sweep.csv", sep=";").set_index("k")
    l = pd.read_csv(RESULTS / "l_sweep.csv", sep=";").set_index("l")
    cm = pd.read_csv(RESULTS / "coding_model_sweep.csv", sep=";")

    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.7))

    # --- (a) k-anonymity vs l-diversity at k=5
    ax = axes[0]
    ls = l.index.tolist()
    x = np.arange(len(ls))
    w = 0.38
    ax.bar(x - w / 2, [k.loc[5, "info_loss_pct"]] * len(ls), w,
           color=PALETTE["primary"], label="k-anonymity only (k=5)")
    ax.bar(x + w / 2, l["info_loss_pct"].values, w,
           color=PALETTE["accent"], label="k=5 + l-diversity")
    ax.set_xticks(x)
    ax.set_xticklabels([f"l={v}" for v in ls])
    ax.set_ylabel("Information loss (%)")
    ax.set_title("Cost of adding l-diversity at k=5")
    ax.set_ylim(0, 100)
    ax.legend(loc="upper left")

    # --- (b) coding model comparison
    ax = axes[1]
    colors = [PALETTE["primary"], PALETTE["muted"], PALETTE["secondary"]]
    bars = ax.bar(cm["model"], cm["info_loss_pct"], color=colors,
                  edgecolor="white")
    ax.set_ylabel("Information loss (%)")
    ax.set_title("Coding model at k=5, suppression=5%")
    ax.set_ylim(0, 30)
    for bar, value in zip(bars, cm["info_loss_pct"]):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.6,
                f"{value:.1f}%", ha="center", fontsize=9)

    fig.tight_layout()
    save(fig, "information_loss.png")


if __name__ == "__main__":
    main()
