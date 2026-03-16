#!/usr/bin/env python3
"""
NVIDIA GPU Investment Analysis — Main Entry Point
==================================================
Generates all charts and the markdown report.

Usage:
    python run.py
    python run.py --output-dir custom/path

Outputs:
    output/          — 11 PNG charts
    REPORT.md        — Full analysis with tables and investment thesis
"""

import argparse
import os

from src.style import apply_theme
from src.data import build_price_df, build_summary_df
from src.charts import (
    chart_absolute_prices,
    chart_depreciation_curves,
    chart_residual_value,
    chart_annual_depreciation,
    chart_vram_vs_residual,
    chart_compute_value,
    chart_buy_vs_rent,
    chart_cloud_coverage,
    chart_generation_boxplot,
    chart_fleet_depreciation,
    chart_utilisation_breakeven,
    chart_cloud_rental_rates,
)
from src.report import generate_report


def main():
    parser = argparse.ArgumentParser(description="NVIDIA GPU Investment Analysis")
    parser.add_argument("--output-dir", default="output", help="Directory for chart PNGs")
    args = parser.parse_args()

    out_dir = args.output_dir
    os.makedirs(out_dir, exist_ok=True)

    apply_theme()

    print("Building dataset...")
    df = build_price_df()
    summary = build_summary_df(df)
    print(f"  {len(df)} price observations across {df['gpu'].nunique()} GPUs\n")

    print("Generating charts:")
    chart_absolute_prices(df, out_dir)
    print("  ✓ 01  Absolute prices over time")

    chart_depreciation_curves(df, out_dir)
    print("  ✓ 02  Depreciation curves")

    chart_residual_value(summary, out_dir)
    print("  ✓ 03  Residual value")

    chart_annual_depreciation(summary, out_dir)
    print("  ✓ 04  Annual depreciation scatter")

    chart_vram_vs_residual(summary, out_dir)
    print("  ✓ 05  VRAM vs residual value")

    chart_compute_value(summary, out_dir)
    print("  ✓ 05b Compute value ($/TFLOPS)")

    tco_df = chart_buy_vs_rent(out_dir)
    print("  ✓ 06  Buy vs rent breakeven")
    print("  ✓ 07  3-year TCO comparison")

    chart_cloud_coverage(out_dir)
    print("  ✓ 08  Cloud provider coverage heatmap")

    chart_generation_boxplot(df, out_dir)
    print("  ✓ 09  Generation depreciation boxplot")

    chart_fleet_depreciation(out_dir)
    print("  ✓ 10  $1B fleet depreciation timeline")

    chart_utilisation_breakeven(out_dir)
    print("  ✓ 11  Utilisation breakeven")

    chart_cloud_rental_rates(out_dir)
    print("  ✓ 12  Cloud rental rates (verified, provider breakdown)")
    print("  ✓ 13  Cloud rental verified historical snapshots")

    print("\nGenerating report...")
    report_path = "REPORT.md"
    generate_report(summary, tco_df, out_dir, report_path)
    print(f"  ✓ {report_path}")

    print(f"\nDone! Charts in {out_dir}/, report at {report_path}")


if __name__ == "__main__":
    main()
