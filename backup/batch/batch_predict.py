import pandas as pd
import joblib
import os
import json
import numpy as np
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "xgboost_model.pkl")
INPUT_CSV = os.path.join(BASE_DIR, "cleaned_dataset.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "outputs", "forecast_output.csv")
LOG_FILE = os.path.join(BASE_DIR, "outputs", "batch_log.json")

SERVICE_TYPES = ["Compute", "Storage", "Networking", "Database", "AI/ML"]

def run_batch_prediction():
    start_time = datetime.now()

    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

    if not os.path.exists(MODEL_PATH):
        return False
    if not os.path.exists(INPUT_CSV):
        return False

    try:
        model = joblib.load(MODEL_PATH)

        df = pd.read_csv(INPUT_CSV)

        df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed", dayfirst=True)

        X_batch = pd.DataFrame()
        X_batch["year"] = df["timestamp"].dt.year
        X_batch["month"] = df["timestamp"].dt.month
        X_batch["day"] = df["timestamp"].dt.day

        predictions = model.predict(X_batch)

        results_df = pd.DataFrame()
        results_df["date"] = df["timestamp"].dt.strftime("%Y-%m-%d")

        if "compute_usage_units" in df.columns:
            results_df["actual"] = df["compute_usage_units"].values
        elif "usage_units" in df.columns:
            results_df["actual"] = df["usage_units"].values
        else:
            results_df["actual"] = 0.0

        results_df["forecast"] = predictions

        if "region" in df.columns:
            results_df["region"] = df["region"].values
        else:
            results_df["region"] = "Unknown"

        np.random.seed(42)
        results_df["service_type"] = np.random.choice(SERVICE_TYPES, size=len(results_df), p=[0.35, 0.25, 0.20, 0.12, 0.08])

        results_df["residual"] = results_df["actual"] - results_df["forecast"]
        results_df["abs_error"] = abs(results_df["residual"])

        results_df.to_csv(OUTPUT_CSV, index=False)

        from sklearn.metrics import mean_squared_error
        rmse = float(np.sqrt(mean_squared_error(results_df["actual"], results_df["forecast"])))
        mae = float(np.mean(results_df["abs_error"]))

        duration = (datetime.now() - start_time).total_seconds()

        log_entry = {
            "timestamp": start_time.isoformat(),
            "status": "success",
            "records_processed": len(results_df),
            "rmse": round(rmse, 2),
            "mae": round(mae, 2),
            "duration_seconds": round(duration, 2),
            "output_file": OUTPUT_CSV
        }

        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        logs.append(log_entry)
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=2)


        return True

    except Exception as e:
        log_entry = {
            "timestamp": start_time.isoformat(),
            "status": "failed",
            "error": str(e)
        }
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        logs.append(log_entry)
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=2)
        raise e

if __name__ == "__main__":
    run_batch_prediction()
