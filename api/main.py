import os
import subprocess
import json
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Mount frontend
os.makedirs("frontend", exist_ok=True)
app.mount("/ui", StaticFiles(directory="frontend", html=True), name="ui")

# Pydantic models for responses
class StageResponse(BaseModel):
    status: str
    message: str

def run_script(script_path: str):
    try:
        # Use conda run to ensure correct environment 
        # Alternatively, we could just rely on the active environment running uvicorn
        result = subprocess.run(
            ["python", script_path], 
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
            text=True,
            capture_output=True,
            check=True
        )
        return {"status": "success", "message": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr + "\n" + e.stdout}

@app.post("/api/run/data-generation")
def run_data_gen():
    res = run_script("data_platform/generator.py")
    if res["status"] == "error":
        raise HTTPException(status_code=500, detail=res["message"])
    return res

@app.post("/api/run/data-validation")
def run_data_val():
    res = run_script("data_platform/validator.py")
    if res["status"] == "error":
        raise HTTPException(status_code=500, detail=res["message"])
    return res

@app.post("/api/run/cashflow")
def run_cashflow():
    res = run_script("cashflow_engine/runner.py")
    if res["status"] == "error":
        raise HTTPException(status_code=500, detail=res["message"])
    return res

@app.post("/api/run/reporting")
def run_reporting():
    res = run_script("reporting_engine/liquidity_metrics.py")
    if res["status"] == "error":
        raise HTTPException(status_code=500, detail=res["message"])
    return res

@app.post("/api/run/stress-testing")
def run_stress():
    res = run_script("stress_testing/scenario_runner.py")
    if res["status"] == "error":
        raise HTTPException(status_code=500, detail=res["message"])
    return res

@app.get("/api/data/raw-instruments")
def get_raw_instruments():
    try:
        df = pd.read_csv("data/raw/raw_instruments.csv")
        return {"data": df.head(50).to_dict(orient="records"), "total": len(df)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/data/clean-instruments")
def get_clean_instruments():
    try:
        df = pd.read_parquet("data/processed/clean_instruments.parquet")
        return {"data": df.head(50).to_dict(orient="records"), "total": len(df)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/data/cashflows")
def get_cashflows():
    try:
        df = pd.read_parquet("data/processed/cashflows.parquet")
        return {"data": df.head(50).to_dict(orient="records"), "total": len(df)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/data/reports")
def get_reports():
    try:
        lcr = pd.read_csv("data/processed/liquidity_report.csv").to_dict(orient="records")
        nsfr = pd.read_csv("data/processed/nsfr_report.csv").to_dict(orient="records")
        return {"lcr": lcr, "nsfr": nsfr}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/data/stress-results")
def get_stress_results():
    try:
        with open("data/processed/stress_results.json", "r") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}
