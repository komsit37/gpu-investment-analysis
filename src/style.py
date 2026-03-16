"""Chart styling constants."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Dark theme
DARK_THEME = {
    "figure.facecolor": "#0d1117",
    "axes.facecolor": "#0d1117",
    "axes.edgecolor": "#30363d",
    "axes.labelcolor": "#c9d1d9",
    "text.color": "#c9d1d9",
    "xtick.color": "#8b949e",
    "ytick.color": "#8b949e",
    "grid.color": "#21262d",
    "legend.facecolor": "#161b22",
    "legend.edgecolor": "#30363d",
    "font.size": 11,
}

GEN_COLORS = {
    "Pascal": "#e74c3c",
    "Volta": "#e67e22",
    "Turing": "#f1c40f",
    "Ampere": "#2ecc71",
    "Ada Lovelace": "#3498db",
    "Hopper": "#9b59b6",
    "Blackwell": "#e91e63",
}

CAT_MARKERS = {
    "datacenter": "o",
    "professional": "s",
    "consumer": "^",
}


def apply_theme():
    plt.rcParams.update(DARK_THEME)
