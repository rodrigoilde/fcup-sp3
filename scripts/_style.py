"""Shared matplotlib styling for the assignment figures."""

from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "report" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

# Colour-blind friendly palette (Wong, 2011)
PALETTE = {
    "primary": "#0072B2",
    "accent": "#D55E00",
    "secondary": "#009E73",
    "muted": "#56B4E9",
    "warn": "#CC79A7",
    "dark": "#000000",
}


def apply_style() -> None:
    plt.rcParams.update({
        "figure.dpi": 110,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linestyle": "--",
        "legend.frameon": False,
        "legend.fontsize": 9,
    })


def save(fig, name: str) -> Path:
    path = FIGURES / name
    fig.savefig(path)
    print(f"wrote {path.relative_to(ROOT)}")
    return path
