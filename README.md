# Financial Risk Analytics Platform (Basel III + ALM)

This is a production-grade internal project that models Asset Liability Management (ALM) cashflows and calculates liquidity risk metrics natively (LCR and NSFR proxies). 

## Architecture
- **Data Platform**: Generates synthetic schema-validated data using statistical distributions.
- **Cashflow Engine (C++17)**: A highly-performant C++ engine that schedules and amortizes flows for multiple instruments using multi-threading.
- **Reporting Engine (Python)**: Validates outputs using pandas and implements the regulatory rulebook for calculating Liquidity ratios.
- **Stress Testing Engine (Python)**: Modifies default rates and deposit run-offs systematically to see LCR sensitivities based on macro-economic shocks.

## Setup
We recommend using Conda:
```bash
conda env create -f environment.yml
conda activate financial_risk
```

## Running the Pipeline
Simply run:
```bash
chmod +x run.sh
./run.sh
```

## Running Tests
```bash
pytest tests/
```

## Future Improvements
- Integrate FastAPI server for on-demand stress testing.
- Replace CSV outputs for engine bridging with raw PyArrow bindings.
- Fully expand date math instead of generic period assumptions.
