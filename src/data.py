"""Data loading and DataFrame construction."""

import pandas as pd
from .gpu_specs import GPU_SPECS
from .price_data import PHYSICAL_PRICES, CLOUD_RENTAL_RATES


def build_price_df() -> pd.DataFrame:
    """Build master price DataFrame from all GPU price observations."""
    rows = []
    for gpu_name, prices in PHYSICAL_PRICES.items():
        spec = GPU_SPECS.get(gpu_name, {})
        rel = pd.Timestamp(spec.get("release_date", "2020-01-01"))
        for date_str, price in prices.items():
            ts = pd.Timestamp(date_str)
            months = (ts.year - rel.year) * 12 + (ts.month - rel.month)
            rows.append({
                "gpu": gpu_name,
                "date": ts,
                "price": price,
                "months": months,
                "category": spec.get("category", "unknown"),
                "generation": spec.get("generation", "unknown"),
                "gen_year": spec.get("gen_year", 0),
                "vram_gb": spec.get("vram_gb", 0),
                "fp16_tflops": spec.get("fp16_tflops", 0),
                "tdp_watts": spec.get("tdp_watts", 0),
            })
    return pd.DataFrame(rows)


def build_summary_df(df: pd.DataFrame) -> pd.DataFrame:
    """Per-GPU summary: peak, latest, residual %, age, annual depreciation."""
    records = []
    for gpu, grp in df.sort_values("date").groupby("gpu"):
        peak = grp["price"].max()
        latest = grp["price"].iloc[-1]
        first = grp["price"].iloc[0]
        age_months = grp["months"].iloc[-1]  # months since release date
        age_years = max(age_months / 12, 0.25)
        annual_depr = (1 - latest / first) / age_years * 100

        records.append({
            "gpu": gpu,
            "generation": grp["generation"].iloc[0],
            "category": grp["category"].iloc[0],
            "gen_year": grp["gen_year"].iloc[0],
            "vram_gb": grp["vram_gb"].iloc[0],
            "fp16_tflops": grp["fp16_tflops"].iloc[0],
            "tdp_watts": grp["tdp_watts"].iloc[0],
            "peak_price": peak,
            "first_price": first,
            "latest_price": latest,
            "residual_pct_of_peak": latest / peak * 100,
            "residual_pct_of_first": latest / first * 100,
            "age_months": age_months,
            "age_years": age_years,
            "annual_depr_pct": annual_depr,
        })
    return pd.DataFrame(records).sort_values("gen_year")
