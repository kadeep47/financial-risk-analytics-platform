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
