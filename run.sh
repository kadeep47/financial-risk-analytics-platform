#!/bin/bash
set -e

echo "Starting Financial Risk Analytics Platform Pipeline..."

# 1. Generate Raw Data
echo "[1/4] Generating raw data..."
python data_platform/generator.py

# 2. Extract, Transform, Validate
echo "[2/4] Validating and cleaning data..."
python data_platform/validator.py

# 3. Cashflow Calculation (C++ Engine wrapped in Python runner)
echo "[3/4] Running C++ Cashflow Engine..."
python cashflow_engine/runner.py

# 4. Generate Liquidity metrics
echo "[4/4] Calculating Liquidity Metrics..."
python reporting_engine/liquidity_metrics.py

# 5. Stress Testing
echo "[5/5] Running Scenario Stress Tests..."
python stress_testing/scenario_runner.py

echo "Pipeline complete! Outputs are located in data/processed/"
