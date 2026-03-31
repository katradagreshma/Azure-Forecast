from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, conint
import joblib
import pandas as pd
import os
from functools import lru_cache


app = FastAPI(
    title="Azure Demand Forecast API",
    description="Real-time and batch inference API for Azure resource demand forecasting",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    year: conint(ge=2020, le=2030)
    month: conint(ge=1, le=12)
    day: conint(ge=1, le=31)

class PredictionResponse(BaseModel):
    predicted_demand: float
    capacity_action: str
    risk_level: str

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "xgboost_model.pkl")

@lru_cache(maxsize=1)
def load_model():
    resolved = os.path.abspath(MODEL_PATH)
    if not os.path.exists(resolved):
        raise FileNotFoundError(f"Model file not found at {resolved}")
    model = joblib.load(resolved)
    return model

@app.on_event("startup")
async def startup_event():
    try:
        load_model()
    except Exception as e:
        pass

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "model_loaded": True, "version": "2.0.0"}

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(request: PredictionRequest):
    try:
        model = load_model()
        input_data = pd.DataFrame([{
            "year": request.year,
            "month": request.month,
            "day": request.day
        }])
        prediction = float(model.predict(input_data)[0])

        if prediction > 1200:
            action = "CRITICAL — Immediate Scale-Up Required"
            risk = "critical"
        elif prediction > 1000:
            action = "Scale Up Resources"
            risk = "high"
        elif prediction > 700:
            action = "Monitor — Resources Normal"
            risk = "medium"
        else:
            action = "Scale Down Resources"
            risk = "low"

        return PredictionResponse(
            predicted_demand=round(prediction, 2),
            capacity_action=action,
            risk_level=risk
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/forecast-data", tags=["Dashboard"])
async def get_forecast_data():
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "forecast_output.csv"))
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Forecast output not found. Run batch pipeline first.")
    df = pd.read_csv(csv_path)
    return df.to_dict(orient="records")

@app.get("/monitoring", tags=["Monitoring"])
async def get_monitoring():
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "forecast_output.csv"))
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Forecast output not found.")
    df = pd.read_csv(csv_path)
    if "actual" in df.columns and "forecast" in df.columns:
        from sklearn.metrics import mean_squared_error
        import numpy as np
        rmse = float(np.sqrt(mean_squared_error(df["actual"], df["forecast"])))
        mae = float(np.mean(np.abs(df["actual"] - df["forecast"])))
        mape = float(np.mean(np.abs((df["actual"] - df["forecast"]) / df["actual"])) * 100)
        alert = rmse > 150
        return {
            "rmse": round(rmse, 2),
            "mae": round(mae, 2),
            "mape": round(mape, 2),
            "alert": alert,
            "alert_message": "⚠️ High RMSE detected — model may need retraining" if alert else "✅ Model performance within acceptable range",
            "total_records": len(df)
        }
    raise HTTPException(status_code=400, detail="Missing actual/forecast columns")

DASHBOARD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dashboard"))
if os.path.exists(DASHBOARD_DIR):
    app.mount("/dashboard", StaticFiles(directory=DASHBOARD_DIR, html=True), name="dashboard")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)
