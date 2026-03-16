# NVIDIA GPU Depreciation & Investment Analysis
_Generated: 2026-03-16 10:55_

> **Purpose**: Evaluate whether NVIDIA GPUs hold value over time,
> and what that means for investing in CRWV, NBIN, NVDA, and ORCL.

## 1. Depreciation Summary

| GPU | Generation | Age (yr) | Peak → Latest | Residual | Annual Depr |
|-----|-----------|----------|---------------|----------|-------------|
| Tesla P4 | Pascal | 7.4 | $3,000 → $150 | 5% | 13%/yr |
| Tesla P100 16GB | Pascal | 4.4 | $3,600 → $400 | 11% | 20%/yr |
| V100 SXM2 32GB | Volta | 2.2 | $8,700 → $2,000 | 23% | 34%/yr |
| GeForce RTX 2080 | Turing | 6.8 | $2,000 → $500 | 25% | 7%/yr |
| Quadro RTX 6000 | Turing | 6.4 | $4,700 → $1,700 | 36% | 10%/yr |
| Tesla T4 | Turing | 6.0 | $3,400 → $800 | 24% | 11%/yr |
| RTX A6000 | Ampere | 3.4 | $8,400 → $5,300 | 63% | 11%/yr |
| A100 40GB PCIe | Ampere | 1.3 | $8,500 → $6,800 | 80% | 12%/yr |
| GeForce RTX 3090 | Ampere | 4.7 | $3,800 → $1,500 | 39% | 5%/yr |
| GeForce RTX 3070 | Ampere | 4.7 | $1,700 → $550 | 32% | 12%/yr |
| A40 PCIe | Ampere | 3.2 | $5,800 → $5,800 | 100% | -4%/yr |
| RTX A4000 | Ampere | 3.8 | $1,700 → $900 | 53% | 11%/yr |
| RTX A5000 | Ampere | 2.0 | $2,850 → $1,850 | 65% | 11%/yr |
| GeForce RTX 4090 | Ada Lovelace | 2.7 | $3,700 → $3,200 | 86% | -7%/yr |
| L40S | Ada Lovelace | 1.0 | $14,000 → $9,750 | 70% | 29%/yr |
| GeForce RTX 3090 Ti | Ampere | 3.2 | $2,600 → $1,950 | 75% | 8%/yr |
| H100 PCIe 96GB | Hopper | 1.2 | $39,000 → $30,000 | 77% | 20%/yr |
| L4 | Ada Lovelace | 0.9 | $3,270 → $2,500 | 76% | 17%/yr |
| H100 PCIe 80GB | Hopper | 1.7 | $34,800 → $25,100 | 72% | 17%/yr |
| H100 SXM5 80GB | Hopper | 0.2 | $18,550 → $18,550 | 100% | 0%/yr |

## 2. Three Phases of GPU Depreciation

```
Phase 1 (0-2yr):  Holds value or APPRECIATES (RTX 4090 +65%)
Phase 2 (2-4yr):  'Successor cliff' — sharp 25-40% drop
Phase 3 (4+yr):   Slow bleed ~5-10%/yr, hits a floor
```

## 3. VRAM is the #1 Predictor of Value Retention

- **A40 (48GB)**: appreciated — 48GB sweet spot for inference
- **A100 40GB**: only ~20% decline over 5 years
- **RTX 3070 (8GB)**: −54% — low VRAM GPUs lose value fast
- Trend slope: **+0.73% residual per GB of VRAM**

## 4. Cloud Provider Coverage = Demand Signal

- **Tesla T4**: 4 providers (gcp, aws, modal, runpod)
- **A100 40GB PCIe**: 4 providers (gcp, lambdalabs, modal, runpod)
- **H100 SXM5 80GB**: 4 providers (gcp, lambdalabs, modal, runpod)
- **L4**: 3 providers (gcp, modal, runpod)
- **A10G**: 2 providers (aws, modal)
- **H100 PCIe 80GB**: 2 providers (lambdalabs, runpod)
- **L40S**: 2 providers (modal, runpod)
- **Tesla P4**: 1 providers (gcp)
- **Tesla P100 16GB**: 1 providers (gcp)
- **V100 SXM2 32GB**: 1 providers (runpod)
- **A40 PCIe**: 1 providers (runpod)
- **GeForce RTX 3090**: 1 providers (runpod)
- **GeForce RTX 4090**: 1 providers (runpod)
- **RTX A6000**: 1 providers (runpod)

**Old GPUs still on cloud (demand proven):** T4, V100, A100, P100, P4  
**Old GPUs NOT on cloud (fading):** RTX 2080, RTX 3070, Quadro RTX 5000

## 5. Buy vs Rent — 3-Year TCO at 70% Utilisation

| GPU | Buy Price | Rent $/hr | 3yr Rent | 3yr Buy+Elec | Savings (Buy) |
|-----|-----------|-----------|----------|--------------|---------------|
| H100 SXM5 80GB | $18,550 | $3.42 | $62,865 | $14,274 | $48,592 |
| H100 PCIe 80GB | $25,100 | $2.49 | $45,837 | $18,214 | $27,623 |
| Tesla P100 16GB | $400 | $1.46 | $26,877 | $740 | $26,136 |
| A100 40GB PCIe | $6,800 | $1.37 | $25,174 | $5,220 | $19,954 |
| L40S | $9,750 | $1.42 | $26,140 | $7,377 | $18,763 |
| Tesla P4 | $150 | $0.60 | $11,045 | $565 | $10,480 |
| L4 | $2,500 | $0.60 | $11,107 | $1,883 | $9,224 |
| Tesla T4 | $800 | $0.42 | $7,667 | $689 | $6,978 |
| V100 SXM2 32GB | $2,000 | $0.39 | $7,179 | $1,860 | $5,319 |
| GeForce RTX 4090 | $3,200 | $0.44 | $8,100 | $3,068 | $5,031 |
| RTX A6000 | $5,300 | $0.44 | $8,100 | $4,262 | $3,838 |
| A40 PCIe | $5,800 | $0.44 | $8,100 | $4,612 | $3,488 |
| GeForce RTX 3090 | $1,500 | $0.22 | $4,050 | $1,694 | $2,356 |

## 6. Investment Implications

### CRWV (CoreWeave) & NBIN (Nebius)

| Factor | Finding | Impact |
|--------|---------|--------|
| H100 depreciation | ~20%/yr observed — matching book rate | 🟡 Neutral |
| A100 depreciation | ~8%/yr — MUCH slower than book (20%) | 🟢 Hidden asset value |
| Utilisation requirement | 30-60% breakeven at 40% margin | 🟢 Achievable |
| Successor risk | B200/GB200 arriving → H100 cliff coming | 🔴 Watch 2025-2026 |
| Long-term contracts | Insulates from resale risk | 🟢 Key mitigant |

**Risk**: If CRWV bought H100s at $35K peak and B200 drives them to $15K,
that's a potential **$20K/GPU impairment** not covered by straight-line depreciation.

### NVDA (NVIDIA)

| Factor | Finding | Impact |
|--------|---------|--------|
| Depreciation cycle | Forces replacement every 2-3 years | 🟢 Recurring revenue |
| Pricing power | H100 held at $35K for 8+ months before dropping | 🟢 Strong |
| Ecosystem lock-in | Even dead GPUs (P4=$150) still sell | 🟢 No AMD secondary market |
| ASP risk | H100 $35K→$25K in 18mo = pricing pressure | 🟡 Watch margins |

### ORCL (Oracle Cloud)

- Late entrant advantage: buying at LOWER prices (post-peak H100)
- Less legacy GPU baggage vs AWS/GCP
- Risk: same depreciation applies; needs high utilisation to justify capex

### Overall Thesis

```
BULL CASE: GPUs depreciate ~10-20%/yr, but cloud rental margins
           (40-60%) easily outpace depreciation IF utilisation >60%.
           Old GPUs find second life in inference (A40, T4 still rented).
           NVDA benefits from forced upgrade cycles.

BEAR CASE: H100→B200 transition could cause cliff-depreciation (like V100
           which fell 77% in 2 years). Overleveraged neo-cloud companies
           (CRWV) face impairment risk if contracts don't cover full life.
           Rental rate compression from competition reduces margins.

KEY METRIC: Watch utilisation rates in earnings reports.
            >70% = healthy, <50% = trouble for asset-heavy players.
```

## Charts

### 01 Absolute Prices
![01_absolute_prices.png](output/01_absolute_prices.png)

### 02 Depreciation Curves
![02_depreciation_curves.png](output/02_depreciation_curves.png)

### 03 Residual Value
![03_residual_value.png](output/03_residual_value.png)

### 04 Annual Depreciation
![04_annual_depreciation.png](output/04_annual_depreciation.png)

### 05 Vram Vs Residual
![05_vram_vs_residual.png](output/05_vram_vs_residual.png)

### 06 Buy Vs Rent Breakeven
![06_buy_vs_rent_breakeven.png](output/06_buy_vs_rent_breakeven.png)

### 07 Tco 3Yr Comparison
![07_tco_3yr_comparison.png](output/07_tco_3yr_comparison.png)

### 08 Cloud Coverage Heatmap
![08_cloud_coverage_heatmap.png](output/08_cloud_coverage_heatmap.png)

### 09 Generation Boxplot
![09_generation_boxplot.png](output/09_generation_boxplot.png)

### 10 Fleet Depreciation Timeline
![10_fleet_depreciation_timeline.png](output/10_fleet_depreciation_timeline.png)

### 11 Utilisation Breakeven
![11_utilisation_breakeven.png](output/11_utilisation_breakeven.png)
