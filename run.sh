#!/bin/bash
set -e

echo "Starting Financial Risk Analytics Platform Pipeline..."

# 1. Generate Raw Data
echo "[1/4] Generating raw data..."
python data_platform/generator.py

# 2. Extract, Transform, Validate
echo "[2/4] Validating and cleaning data..."
python data_platform/validator.py

