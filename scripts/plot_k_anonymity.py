"""Information loss & prosecutor risk as a function of k."""

from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt

from _style import RESULTS, PALETTE, apply_style, save


def main() -> None:
    apply_style()
    df = pd.read_csv(RESULTS / "k_sweep.csv", sep=";")

    fig, ax1 = plt.subplots(figsize=(6.2, 3.6))

    ax1.plot(
        df["k"], df["info_loss_pct"],
        marker="o", color=PALETTE["primary"], linewidth=2,
        label="Information loss (%)",
    )
    ax1.set_xlabel("k (k-anonymity parameter)")
    ax1.set_ylabel("Information loss (%)", color=PALETTE["primary"])
    ax1.set_xscale("log")
    ax1.set_xticks(df["k"])
    ax1.set_xticklabels([str(k) for k in df["k"]])
    ax1.tick_params(axis="y", labelcolor=PALETTE["primary"])
    ax1.set_ylim(0, 100)

    ax2 = ax1.twinx()
    ax2.plot(
        df["k"], df["prosecutor_risk"] * 100,
        marker="s", color=PALETTE["accent"], linewidth=2,
        label="Prosecutor risk (%)",
    )
    ax2.set_ylabel("Maximum prosecutor risk (%)", color=PALETTE["accent"])
    ax2.tick_params(axis="y", labelcolor=PALETTE["accent"])
    ax2.set_yscale("log")
    ax2.grid(False)

    fig.suptitle("Privacy-utility trade-off for k-anonymity on Adult",
                 fontsize=11, y=1.02)
    fig.tight_layout()
    save(fig, "k_sweep.png")


if __name__ == "__main__":
    main()
