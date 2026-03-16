"""Markdown report generator."""

import os
from datetime import datetime
import pandas as pd
from .price_data import CLOUD_RENTAL_RATES


def generate_report(
    summary: pd.DataFrame,
    tco_df: pd.DataFrame,
    out_dir: str,
    report_path: str,
):
    lines = []
    lines.append("# NVIDIA GPU Depreciation & Investment Analysis")
    lines.append(f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n")
    lines.append("> **Purpose**: Evaluate whether NVIDIA GPUs hold value over time,")
    lines.append("> and what that means for investing in CRWV, NBIN, NVDA, and ORCL.\n")

    # ── Key findings ─────────────────────────────────────────
    lines.append("## 1. Depreciation Summary\n")
    lines.append("| GPU | Generation | VRAM | FP16 TFLOPS | Age (yr) | Peak → Latest | Residual | Annual Depr | $/TFLOPS |")
    lines.append("|-----|-----------|------|-------------|----------|---------------|----------|-------------|----------|")
    for _, r in summary.iterrows():
        lines.append(
            f'| {r["gpu"]} | {r["generation"]} | {r["vram_gb"]:.0f}GB | '
            f'{r["fp16_tflops"]:.1f} | {r["age_years"]:.1f} | '
            f'${r["peak_price"]:,.0f} → ${r["latest_price"]:,.0f} | '
            f'{r["residual_pct_of_peak"]:.0f}% | {r["annual_depr_pct"]:.0f}%/yr | '
            f'${r["usd_per_tflops"]:,.0f} |'
        )

    lines.append("\n## 2. Three Phases of GPU Depreciation\n")
    lines.append("```")
    lines.append("Phase 1 (0-2yr):  Holds value or APPRECIATES (RTX 4090 +65%)")
    lines.append("Phase 2 (2-4yr):  'Successor cliff' — sharp 25-40% drop")
    lines.append("Phase 3 (4+yr):   Slow bleed ~5-10%/yr, hits a floor")
    lines.append("```\n")

    lines.append("## 3. VRAM is the #1 Predictor of Value Retention\n")
    lines.append("- **A40 (48GB)**: appreciated — 48GB sweet spot for inference")
    lines.append("- **A100 40GB**: only ~20% decline over 5 years")
    lines.append("- **RTX 3070 (8GB)**: −54% — low VRAM GPUs lose value fast")
    lines.append("- Trend slope: **+0.73% residual per GB of VRAM**\n")

    lines.append("## 4. Cloud Provider Coverage = Demand Signal\n")
    for gpu_key, providers in sorted(CLOUD_RENTAL_RATES.items(), key=lambda x: -len(x[1])):
        lines.append(f"- **{gpu_key}**: {len(providers)} providers ({', '.join(providers.keys())})")
    lines.append("")
    lines.append("**Old GPUs still on cloud (demand proven):** T4, V100, A100, P100, P4  ")
    lines.append("**Old GPUs NOT on cloud (fading):** RTX 2080, RTX 3070, Quadro RTX 5000\n")

    lines.append("## 5. Buy vs Rent — 3-Year TCO at 70% Utilisation\n")
    if len(tco_df) > 0:
        util70 = tco_df[tco_df["utilisation"] == 0.7].sort_values("savings_buy", ascending=False)
        lines.append("| GPU | Buy Price | Rent $/hr | 3yr Rent | 3yr Buy+Elec | Savings (Buy) |")
        lines.append("|-----|-----------|-----------|----------|--------------|---------------|")
        for _, r in util70.iterrows():
            lines.append(
                f'| {r["gpu"]} | ${r["buy_price"]:,.0f} | ${r["avg_rental_hr"]:.2f} | '
                f'${r["rent_3yr"]:,.0f} | ${r["buy_3yr_total"]:,.0f} | '
                f'${r["savings_buy"]:,.0f} |'
            )

    # ── Investment implications ──────────────────────────────
    lines.append("\n## 6. Investment Implications\n")

    lines.append("### CRWV (CoreWeave) & NBIN (Nebius)\n")
    lines.append("| Factor | Finding | Impact |")
    lines.append("|--------|---------|--------|")
    lines.append("| H100 depreciation | ~20%/yr observed — matching book rate | 🟡 Neutral |")
    lines.append("| A100 depreciation | ~8%/yr — MUCH slower than book (20%) | 🟢 Hidden asset value |")
    lines.append("| Utilisation requirement | 30-60% breakeven at 40% margin | 🟢 Achievable |")
    lines.append("| Blackwell consumer | RTX 5090 32GB launched $2K, peaked $3.2K — strong demand signal | 🟢 Positive |")
    lines.append("| Successor risk | B200/GB200 arriving → H100 cliff coming | 🔴 Watch 2025-2026 |")
    lines.append("| Long-term contracts | Insulates from resale risk | 🟢 Key mitigant |")
    lines.append("")
    lines.append("**Risk**: If CRWV bought H100s at $35K peak and B200 drives them to $15K,")
    lines.append("that's a potential **$20K/GPU impairment** not covered by straight-line depreciation.\n")

    lines.append("### NVDA (NVIDIA)\n")
    lines.append("| Factor | Finding | Impact |")
    lines.append("|--------|---------|--------|")
    lines.append("| Depreciation cycle | Forces replacement every 2-3 years | 🟢 Recurring revenue |")
    lines.append("| Pricing power | H100 held at $35K for 8+ months before dropping | 🟢 Strong |")
    lines.append("| Ecosystem lock-in | Even dead GPUs (P4=$150) still sell | 🟢 No AMD secondary market |")
    lines.append("| ASP risk | H100 $35K→$25K in 18mo = pricing pressure | 🟡 Watch margins |")
    lines.append("| Blackwell launch | RTX 5090 MSRP $2K, selling >$3K — validates pricing power | 🟢 Strong |")

    lines.append("\n### ORCL (Oracle Cloud)\n")
    lines.append("- Late entrant advantage: buying at LOWER prices (post-peak H100)")
    lines.append("- Less legacy GPU baggage vs AWS/GCP")
    lines.append("- Risk: same depreciation applies; needs high utilisation to justify capex\n")

    lines.append("### Overall Thesis\n")
    lines.append("```")
    lines.append("BULL CASE: GPUs depreciate ~10-20%/yr, but cloud rental margins")
    lines.append("           (40-60%) easily outpace depreciation IF utilisation >60%.")
    lines.append("           Old GPUs find second life in inference (A40, T4 still rented).")
    lines.append("           NVDA benefits from forced upgrade cycles.")
    lines.append("")
    lines.append("BEAR CASE: H100→B200 transition could cause cliff-depreciation (like V100")
    lines.append("           which fell 77% in 2 years). Overleveraged neo-cloud companies")
    lines.append("           (CRWV) face impairment risk if contracts don't cover full life.")
    lines.append("           Rental rate compression from competition reduces margins.")
    lines.append("")
    lines.append("KEY METRIC: Watch utilisation rates in earnings reports.")
    lines.append("            >70% = healthy, <50% = trouble for asset-heavy players.")
    lines.append("```\n")

    # ── Chart gallery ────────────────────────────────────────
    lines.append("## Charts\n")
    for f in sorted(os.listdir(out_dir)):
        if f.endswith(".png"):
            title = f.replace(".png", "").replace("_", " ").title()
            lines.append(f"### {title}")
            lines.append(f"![{f}](output/{f})\n")

    report = "\n".join(lines)
    with open(report_path, "w") as fh:
        fh.write(report)
    return report
