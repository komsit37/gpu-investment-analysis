"""All chart generators. Each function returns a Figure and saves to disk."""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from .style import GEN_COLORS, CAT_MARKERS
from .gpu_specs import GPU_SPECS
from .price_data import PHYSICAL_PRICES, CLOUD_RENTAL_RATES


def _save(fig, out_dir: str, name: str):
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, name), dpi=150)
    plt.close(fig)


# ─────────────────────────────────────────────────────────────
# 01 — Absolute prices over time
# ─────────────────────────────────────────────────────────────
def chart_absolute_prices(df: pd.DataFrame, out_dir: str):
    fig, ax = plt.subplots(figsize=(16, 9))
    for gpu, grp in df.groupby("gpu"):
        gen = grp["generation"].iloc[0]
        cat = grp["category"].iloc[0]
        ax.plot(grp["date"], grp["price"],
                marker=CAT_MARKERS.get(cat, "o"), markersize=4,
                color=GEN_COLORS.get(gen, "#888"),
                label=f"{gpu} ({gen})", alpha=0.85, linewidth=1.5)
    ax.set_title("NVIDIA GPU Prices Over Time — All Generations",
                 fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Date")
    ax.set_ylabel("Amazon Buy Box Price (USD)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7, ncol=3, loc="upper right")
    _save(fig, out_dir, "01_absolute_prices.png")


# ─────────────────────────────────────────────────────────────
# 02 — Depreciation curves (% of initial)
# ─────────────────────────────────────────────────────────────
def chart_depreciation_curves(df: pd.DataFrame, out_dir: str):
    fig, ax = plt.subplots(figsize=(16, 9))
    for gpu, grp in df.sort_values("date").groupby("gpu"):
        gen = grp["generation"].iloc[0]
        cat = grp["category"].iloc[0]
        first_price = grp["price"].iloc[0]
        pct = grp["price"] / first_price * 100
        months = grp["months"] - grp["months"].iloc[0]
        ax.plot(months, pct,
                marker=CAT_MARKERS.get(cat, "o"), markersize=4,
                color=GEN_COLORS.get(gen, "#888"),
                label=gpu, alpha=0.8, linewidth=1.5)

    ax.axhline(100, color="#8b949e", ls="--", lw=0.8, alpha=0.5)
    ax.axhline(50, color="#e74c3c", ls="--", lw=0.8, alpha=0.4)
    ax.text(2, 52, "50% value remaining", fontsize=8, color="#e74c3c", alpha=0.6)
    ax.set_title("GPU Depreciation Curves — % of Initial Price vs Months Observed",
                 fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Months Since First Price Observation")
    ax.set_ylabel("% of Initial Price")
    ax.set_ylim(0, 180)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7, ncol=3, loc="upper right")
    _save(fig, out_dir, "02_depreciation_curves.png")


# ─────────────────────────────────────────────────────────────
# 03 — Residual value bar chart
# ─────────────────────────────────────────────────────────────
def chart_residual_value(summary: pd.DataFrame, out_dir: str):
    rdf = summary.copy()
    fig, ax = plt.subplots(figsize=(16, 9))
    x = range(len(rdf))
    colors = [GEN_COLORS.get(g, "#888") for g in rdf["generation"]]
    ax.barh(list(x), rdf["residual_pct_of_peak"], color=colors, alpha=0.85, height=0.7)

    for i, (_, row) in enumerate(rdf.iterrows()):
        pct = row["residual_pct_of_peak"]
        ax.text(pct + 1, i, f'{pct:.0f}%  (${row["latest_price"]:,.0f})',
                va="center", fontsize=9, color="#c9d1d9")

    ax.set_yticks(list(x))
    ax.set_yticklabels([f'{r["gpu"]}  [{r["generation"]}]' for _, r in rdf.iterrows()], fontsize=9)
    ax.axvline(50, color="#e74c3c", ls="--", lw=1, alpha=0.5)
    ax.axvline(100, color="#8b949e", ls="--", lw=0.8, alpha=0.4)
    ax.set_xlim(0, 160)
    ax.set_title("Residual Value — Current Price as % of Peak Price",
                 fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("% of Peak Price Retained")
    ax.grid(True, alpha=0.2, axis="x")
    _save(fig, out_dir, "03_residual_value.png")


# ─────────────────────────────────────────────────────────────
# 04 — Annual depreciation scatter
# ─────────────────────────────────────────────────────────────
def chart_annual_depreciation(summary: pd.DataFrame, out_dir: str):
    rdf = summary[summary["age_months"] >= 12].copy()
    fig, ax = plt.subplots(figsize=(16, 9))
    for gen in rdf["generation"].unique():
        sub = rdf[rdf["generation"] == gen]
        ax.scatter(sub["age_years"], sub["annual_depr_pct"],
                   color=GEN_COLORS.get(gen, "#888"), s=120,
                   edgecolors="white", linewidth=0.5, label=gen, zorder=5, alpha=0.9)
        for _, row in sub.iterrows():
            ax.annotate(row["gpu"], (row["age_years"], row["annual_depr_pct"]),
                        fontsize=7, ha="left", va="bottom",
                        xytext=(5, 3), textcoords="offset points", color="#8b949e")

    ax.axhline(0, color="#8b949e", ls="-", lw=0.8, alpha=0.3)
    ax.axhspan(10, 30, alpha=0.08, color="#e74c3c")
    ax.text(0.2, 20, "Typical cloud provider\ndepreciation zone\n(book 5yr = 20%/yr)",
            fontsize=9, color="#e74c3c", alpha=0.6)
    ax.set_title("Annualised Depreciation Rate vs Observation Period",
                 fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Years of Price Data")
    ax.set_ylabel("Annual Depreciation Rate (%)\n(negative = appreciation)")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    _save(fig, out_dir, "04_annual_depreciation.png")


# ─────────────────────────────────────────────────────────────
# 05 — VRAM vs residual value
# ─────────────────────────────────────────────────────────────
def chart_vram_vs_residual(summary: pd.DataFrame, out_dir: str):
    rdf = summary
    fig, ax = plt.subplots(figsize=(14, 9))
    for gen in rdf["generation"].unique():
        sub = rdf[rdf["generation"] == gen]
        ax.scatter(sub["vram_gb"], sub["residual_pct_of_peak"],
                   color=GEN_COLORS.get(gen, "#888"), s=150,
                   edgecolors="white", linewidth=0.5, label=gen, zorder=5, alpha=0.9)
        for _, row in sub.iterrows():
            ax.annotate(row["gpu"], (row["vram_gb"], row["residual_pct_of_peak"]),
                        fontsize=7, ha="left", va="bottom",
                        xytext=(5, 3), textcoords="offset points", color="#8b949e")

    x = rdf["vram_gb"].values.astype(float)
    y = rdf["residual_pct_of_peak"].values.astype(float)
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() > 2:
        z = np.polyfit(x[mask], y[mask], 1)
        p = np.poly1d(z)
        xs = np.linspace(x.min(), x.max(), 100)
        ax.plot(xs, p(xs), "--", color="#58a6ff", alpha=0.5, lw=1.5,
                label=f"Trend (slope={z[0]:.2f})")

    ax.axhline(50, color="#e74c3c", ls="--", lw=0.8, alpha=0.4)
    ax.set_title("VRAM vs Residual Value — Does More VRAM Hold Value Better?",
                 fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("VRAM (GB)")
    ax.set_ylabel("% of Peak Price Retained")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    _save(fig, out_dir, "05_vram_vs_residual.png")


# ─────────────────────────────────────────────────────────────
# 06 — Buy vs rent breakeven
# ─────────────────────────────────────────────────────────────
def chart_buy_vs_rent(out_dir: str) -> pd.DataFrame:
    records = []
    for gpu_key, providers in CLOUD_RENTAL_RATES.items():
        if gpu_key not in PHYSICAL_PRICES:
            continue
        prices = PHYSICAL_PRICES[gpu_key]
        latest_price = list(prices.values())[-1]
        spec = GPU_SPECS.get(gpu_key, {})
        avg_rental = np.mean(list(providers.values()))
        min_rental = min(providers.values())
        min_provider = [k for k, v in providers.items() if v == min_rental][0]

        breakeven_hrs = latest_price / avg_rental
        breakeven_months = breakeven_hrs / (24 * 30.44)

        for util in [0.5, 0.7, 0.9]:
            hours_3yr = 3 * 365.25 * 24 * util
            rent_cost = hours_3yr * avg_rental
            buy_cost = latest_price * 0.70  # net of 30% residual
            elec = hours_3yr * (spec.get("tdp_watts", 250) / 1000) * 0.10
            records.append({
                "gpu": gpu_key, "generation": spec.get("generation", "?"),
                "buy_price": latest_price, "avg_rental_hr": avg_rental,
                "min_rental_hr": min_rental, "min_provider": min_provider,
                "num_providers": len(providers),
                "breakeven_hrs": breakeven_hrs, "breakeven_months_24x7": breakeven_months,
                "utilisation": util, "rent_3yr": rent_cost,
                "buy_3yr_total": buy_cost + elec, "savings_buy": rent_cost - (buy_cost + elec),
            })

    bdf = pd.DataFrame(records)
    summary = bdf.groupby("gpu").first().reset_index().sort_values("breakeven_months_24x7")

    # ── breakeven bar ────
    fig, ax = plt.subplots(figsize=(16, 9))
    colors = [GEN_COLORS.get(g, "#888") for g in summary["generation"]]
    ax.barh(range(len(summary)), summary["breakeven_months_24x7"], color=colors, alpha=0.85, height=0.7)
    for i, (_, row) in enumerate(summary.iterrows()):
        mo = row["breakeven_months_24x7"]
        ax.text(mo + 0.3, i,
                f'{mo:.1f} mo  (${row["buy_price"]:,.0f} ÷ ${row["avg_rental_hr"]:.2f}/hr)',
                va="center", fontsize=9, color="#c9d1d9")
    ax.set_yticks(range(len(summary)))
    ax.set_yticklabels([f'{r["gpu"]}  ({r["num_providers"]} providers)' for _, r in summary.iterrows()], fontsize=9)
    ax.axvline(12, color="#f1c40f", ls="--", lw=1, alpha=0.6)
    ax.text(12.3, len(summary) - 0.5, "1 year", fontsize=9, color="#f1c40f", alpha=0.7)
    ax.axvline(36, color="#e74c3c", ls="--", lw=1, alpha=0.6)
    ax.text(36.3, len(summary) - 0.5, "3 years", fontsize=9, color="#e74c3c", alpha=0.7)
    ax.set_title("Buy vs Rent Breakeven — Months to Recoup Purchase Price (24/7 usage, avg rental rate)",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Months at 24/7 Utilisation")
    ax.grid(True, alpha=0.2, axis="x")
    _save(fig, out_dir, "06_buy_vs_rent_breakeven.png")

    # ── TCO 3yr ──────────
    util70 = bdf[bdf["utilisation"] == 0.7].sort_values("gpu")
    fig, ax = plt.subplots(figsize=(16, 9))
    x = np.arange(len(util70))
    w = 0.35
    ax.barh(x - w / 2, util70["rent_3yr"], height=w, color="#e74c3c", alpha=0.8, label="Rent 3yr (70% util)")
    ax.barh(x + w / 2, util70["buy_3yr_total"], height=w, color="#2ecc71", alpha=0.8,
            label="Buy 3yr (70% util, 30% residual + elec)")
    ax.set_yticks(x)
    ax.set_yticklabels(util70["gpu"], fontsize=9)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.set_title("3-Year Total Cost of Ownership — Rent vs Buy at 70% Utilisation",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Total Cost (USD)")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.2, axis="x")
    _save(fig, out_dir, "07_tco_3yr_comparison.png")

    return bdf


# ─────────────────────────────────────────────────────────────
# 08 — Cloud provider coverage heatmap
# ─────────────────────────────────────────────────────────────
def chart_cloud_coverage(out_dir: str):
    providers = sorted({p for rates in CLOUD_RENTAL_RATES.values() for p in rates})
    gpus = sorted(CLOUD_RENTAL_RATES.keys(),
                  key=lambda g: GPU_SPECS.get(g, {}).get("gen_year", 9999))
    matrix = np.array([
        [CLOUD_RENTAL_RATES.get(gpu, {}).get(p, 0) for p in providers]
        for gpu in gpus
    ])

    fig, ax = plt.subplots(figsize=(14, 10))
    im = ax.imshow(matrix, aspect="auto", cmap="YlGnBu")
    ax.set_xticks(range(len(providers)))
    ax.set_xticklabels([p.upper() for p in providers], fontsize=10)
    ax.set_yticks(range(len(gpus)))
    ax.set_yticklabels([
        f'{g}  [{GPU_SPECS.get(g, {}).get("generation", "?")} {GPU_SPECS.get(g, {}).get("gen_year", "?")}]'
        for g in gpus
    ], fontsize=9)

    for i in range(len(gpus)):
        for j in range(len(providers)):
            val = matrix[i, j]
            txt = f"${val:.2f}" if val > 0 else "—"
            ax.text(j, i, txt, ha="center", va="center",
                    fontsize=8, color="black" if val < 2 else "white",
                    fontweight="bold" if val > 0 else "normal")

    ax.set_title("Cloud GPU Availability & Pricing ($/hr) — More Providers = Higher Demand Signal",
                 fontsize=14, fontweight="bold", pad=15)
    fig.colorbar(im, ax=ax, label="$/hr", shrink=0.6)
    _save(fig, out_dir, "08_cloud_coverage_heatmap.png")


# ─────────────────────────────────────────────────────────────
# 09 — Generation depreciation boxplot
# ─────────────────────────────────────────────────────────────
def chart_generation_boxplot(df: pd.DataFrame, out_dir: str):
    records = []
    for gpu, grp in df.sort_values("date").groupby("gpu"):
        first_price = grp["price"].iloc[0]
        latest_price = grp["price"].iloc[-1]
        age_months = grp["months"].iloc[-1] - grp["months"].iloc[0]
        if age_months >= 6:
            annual_depr = (1 - latest_price / first_price) / (age_months / 12) * 100
            records.append({
                "gpu": gpu, "generation": grp["generation"].iloc[0],
                "gen_year": grp["gen_year"].iloc[0],
                "annual_depr": annual_depr, "age_years": age_months / 12,
            })
    bdf = pd.DataFrame(records)
    gen_order = bdf.groupby("generation")["gen_year"].first().sort_values().index.tolist()

    fig, ax = plt.subplots(figsize=(14, 8))
    for i, gen in enumerate(gen_order):
        sub = bdf[bdf["generation"] == gen]
        jitter = np.random.uniform(-0.15, 0.15, len(sub))
        ax.scatter([i] * len(sub) + jitter, sub["annual_depr"],
                   color=GEN_COLORS.get(gen, "#888"), s=120,
                   edgecolors="white", linewidth=0.5, zorder=5, alpha=0.9)
        for idx, (_, row) in enumerate(sub.iterrows()):
            ax.annotate(row["gpu"], (i + jitter[idx], row["annual_depr"]),
                        fontsize=6.5, ha="left", va="bottom",
                        xytext=(6, 2), textcoords="offset points", color="#8b949e")
        med = sub["annual_depr"].median()
        ax.plot([i - 0.3, i + 0.3], [med, med], color=GEN_COLORS.get(gen, "#888"), lw=3, alpha=0.8)

    ax.axhline(20, color="#e74c3c", ls="--", lw=1, alpha=0.5)
    ax.text(len(gen_order) - 0.5, 21, "Book depreciation\n(5yr straight-line = 20%/yr)",
            fontsize=8, color="#e74c3c", alpha=0.7, ha="right")
    ax.axhline(0, color="#8b949e", ls="-", lw=0.8, alpha=0.3)
    ax.set_xticks(range(len(gen_order)))
    ax.set_xticklabels(gen_order, fontsize=11)
    ax.set_title("Annual Depreciation Rate by GPU Generation",
                 fontsize=16, fontweight="bold", pad=15)
    ax.set_ylabel("Annual Depreciation Rate (%)\n(negative = appreciation)")
    ax.grid(True, alpha=0.2, axis="y")
    _save(fig, out_dir, "09_generation_boxplot.png")


# ─────────────────────────────────────────────────────────────
# 10 — $1B fleet depreciation timeline
# ─────────────────────────────────────────────────────────────
def chart_fleet_depreciation(out_dir: str):
    scenarios = [
        ("Bought V100s in 2018",  "Volta",        0.11),
        ("Bought A100s in 2020",  "Ampere",       0.08),
        ("Bought H100s in 2023",  "Hopper",       0.20),
        ("Bought L40S in 2023",   "Ada Lovelace", 0.22),
    ]
    initial = 1_000_000_000
    years = np.arange(0, 6.1, 0.25)

    fig, ax = plt.subplots(figsize=(16, 9))

    # book depreciation
    ax.plot(years, np.maximum(initial * (1 - years / 5), 0) / 1e9,
            "--", color="#8b949e", lw=2.5, label="Book depreciation (5yr)", alpha=0.7)

    for label, gen, rate in scenarios:
        values = initial * (1 - rate) ** years
        ax.plot(years, values / 1e9, color=GEN_COLORS.get(gen, "#888"), lw=2.5,
                label=f"{label} ({rate*100:.0f}%/yr observed)", alpha=0.9)

    ax.set_title("Hypothetical $1B GPU Fleet — Asset Value Over Time\n"
                 "(Based on Observed Resale Depreciation Rates)",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Years After Purchase")
    ax.set_ylabel("Fleet Resale Value ($B)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.2f}B"))
    ax.legend(fontsize=10, loc="upper right")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1.1)

    ax.annotate("CRWV/NBIN risk zone:\nH100 fleet depreciating\nfaster than book rate",
                xy=(2, 0.64), fontsize=9, color="#9b59b6",
                arrowprops=dict(arrowstyle="->", color="#9b59b6", lw=1.5),
                xytext=(3.5, 0.75))
    ax.annotate("A100 fleet holds value\nbetter than expected",
                xy=(4, 0.72), fontsize=9, color="#2ecc71",
                arrowprops=dict(arrowstyle="->", color="#2ecc71", lw=1.5),
                xytext=(4.5, 0.55))
    _save(fig, out_dir, "10_fleet_depreciation_timeline.png")


# ─────────────────────────────────────────────────────────────
# 11 — Utilisation breakeven
# ─────────────────────────────────────────────────────────────
def chart_utilisation_breakeven(out_dir: str):
    records = []
    for gpu_key, providers in CLOUD_RENTAL_RATES.items():
        if gpu_key not in PHYSICAL_PRICES:
            continue
        latest_price = list(PHYSICAL_PRICES[gpu_key].values())[-1]
        spec = GPU_SPECS.get(gpu_key, {})
        avg_rental = np.mean(list(providers.values()))
        hours_4yr = 4 * 8760
        breakeven_util = latest_price / (hours_4yr * avg_rental * 0.40)
        records.append({
            "gpu": gpu_key,
            "generation": spec.get("generation", "?"),
            "breakeven_util": min(breakeven_util * 100, 150),
        })

    bdf = pd.DataFrame(records).sort_values("breakeven_util")
    fig, ax = plt.subplots(figsize=(14, 8))
    colors = [GEN_COLORS.get(g, "#888") for g in bdf["generation"]]
    ax.barh(range(len(bdf)), bdf["breakeven_util"], color=colors, alpha=0.85, height=0.7)

    for i, (_, row) in enumerate(bdf.iterrows()):
        u = row["breakeven_util"]
        label = f'{u:.0f}%' if u < 150 else '>100% (unprofitable)'
        ax.text(min(u + 1, 120), i, label, va="center", fontsize=9, color="#c9d1d9")

    ax.set_yticks(range(len(bdf)))
    ax.set_yticklabels(bdf["gpu"], fontsize=9)
    ax.axvline(70, color="#f1c40f", ls="--", lw=1.5, alpha=0.6)
    ax.text(71, len(bdf) - 0.5, "70% util\n(typical target)", fontsize=9, color="#f1c40f", alpha=0.8)
    ax.axvline(100, color="#e74c3c", ls="--", lw=1.5, alpha=0.6)
    ax.text(101, len(bdf) - 1.5, "impossible\nto profit", fontsize=9, color="#e74c3c", alpha=0.8)
    ax.set_xlim(0, 130)
    ax.set_title("Minimum Utilisation to Break Even in 4 Years\n(at 40% gross margin after opex)",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Required Utilisation (%)")
    ax.grid(True, alpha=0.2, axis="x")
    _save(fig, out_dir, "11_utilisation_breakeven.png")
