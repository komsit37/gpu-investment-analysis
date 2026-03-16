# NVIDIA GPU Investment Analysis

**Do NVIDIA GPUs hold their value?** — A data-driven analysis of GPU depreciation patterns to inform investment decisions for cloud & AI stocks.

## Tickers Covered

| Ticker | Why It Matters |
|--------|---------------|
| **NVDA** | GPU depreciation creates forced upgrade cycles → recurring revenue |
| **CRWV** | CoreWeave's GPU fleet is a depreciating asset — utilisation is everything |
| **NBIN** | Nebius faces same asset risk as CRWV |
| **ORCL** | Oracle Cloud's late entry = buying GPUs at lower prices |

## Key Findings

1. **GPUs lose 50-70% of value over 5 years**, but the pattern has 3 distinct phases
2. **VRAM is the #1 predictor** of value retention (+0.73% residual per GB)
3. **Some GPUs appreciate**: A40 and RTX 4090 went UP due to AI inference demand
4. **Cloud providers need >60% utilisation** to outrun depreciation at 40% margin
5. **H100s are depreciating at ~20%/yr** — matching book rate, but B200 cliff risk looms

## Quick Start

```bash
# Clone with submodule
git clone --recurse-submodules https://github.com/komsit37/gpu-investment-analysis.git
cd gpu-investment-analysis

# Install dependencies
pip install -r requirements.txt

# Run analysis
python run.py
```

## Project Structure

```
├── run.py                  # Entry point — generates all charts + report
├── src/
│   ├── gpu_specs.py        # GPU metadata (VRAM, TFLOPS, TDP, release dates)
│   ├── price_data.py       # Historical prices + cloud rental rates
│   ├── data.py             # DataFrame builders
│   ├── charts.py           # 11 chart generators
│   ├── style.py            # Dark theme styling
│   └── report.py           # Markdown report generator
├── output/                 # Generated charts (11 PNGs)
├── REPORT.md               # Generated analysis report
├── data/
│   └── gpu-price-tracker/  # Submodule: raw price data source
└── requirements.txt
```

## Data Sources

- **Physical GPU prices**: Amazon Buy Box via [Keepa API](https://keepa.com/), tracked by [gpu-price-tracker](https://github.com/United-Compute/gpu-price-tracker)
- **Cloud rental rates**: RunPod, GCP, AWS, Lambda Labs, Modal — from gpu-price-tracker fetchers
- **GPU specs**: NVIDIA official specifications

The upstream [gpu-price-tracker](https://github.com/United-Compute/gpu-price-tracker) is included as a Git submodule under `data/`.

## Charts

| # | Chart | What It Shows |
|---|-------|---------------|
| 01 | Absolute Prices | All GPU prices over time, coloured by generation |
| 02 | Depreciation Curves | Normalised % of initial price vs months |
| 03 | Residual Value | Current price as % of peak — bar chart |
| 04 | Annual Depreciation | Depreciation rate vs years of data |
| 05 | VRAM vs Residual | Does more VRAM = better value retention? |
| 06 | Buy vs Rent Breakeven | Months to recoup purchase via cloud rental |
| 07 | 3-Year TCO | Rent vs buy at 70% utilisation |
| 08 | Cloud Coverage | Which providers offer which GPUs (demand signal) |
| 09 | Generation Boxplot | Depreciation rate distribution by GPU generation |
| 10 | Fleet Depreciation | $1B fleet value over 6 years (CRWV/NBIN risk) |
| 11 | Utilisation Breakeven | Min utilisation to profit in 4 years |

## License

MIT
