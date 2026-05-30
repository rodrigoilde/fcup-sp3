"""Run every plot script in order."""

from __future__ import annotations

import plot_risk_original
import plot_k_anonymity
import plot_suppression
import plot_information_loss
import plot_risk_utility


def main() -> None:
    plot_risk_original.main()
    plot_k_anonymity.main()
    plot_suppression.main()
    plot_information_loss.main()
    plot_risk_utility.main()


if __name__ == "__main__":
    main()
