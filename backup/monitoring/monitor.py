import pandas as pd
import numpy as np
import json
import os
from sklearn.metrics import mean_squared_error, mean_absolute_error


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORECAST_CSV = os.path.join(BASE_DIR, "outputs", "forecast_output.csv")
METRICS_FILE = os.path.join(BASE_DIR, "outputs", "monitoring_metrics.json")

RMSE_THRESHOLD = 150.0

def compute_metrics():

    if not os.path.exists(FORECAST_CSV):
        return None

    df = pd.read_csv(FORECAST_CSV)

    if "actual" not in df.columns or "forecast" not in df.columns:
        return None

    rmse = float(np.sqrt(mean_squared_error(df["actual"], df["forecast"])))
    mae = float(mean_absolute_error(df["actual"], df["forecast"]))
    mape = float(np.mean(np.abs((df["actual"] - df["forecast"]) / df["actual"])) * 100)

    r_squared = float(1 - (np.sum((df["actual"] - df["forecast"])**2) / np.sum((df["actual"] - df["actual"].mean())**2)))

    region_metrics = {}
    if "region" in df.columns:
        for region in df["region"].unique():
            rdf = df[df["region"] == region]
            region_metrics[region] = {
                "rmse": round(float(np.sqrt(mean_squared_error(rdf["actual"], rdf["forecast"]))), 2),
                "mae": round(float(mean_absolute_error(rdf["actual"], rdf["forecast"])), 2),
                "count": len(rdf)
            }

    alert = rmse > RMSE_THRESHOLD

    metrics = {
        "rmse": round(rmse, 2),
        "mae": round(mae, 2),
        "mape": round(mape, 2),
        "r_squared": round(r_squared, 4),
        "total_records": len(df),
        "alert": alert,
        "threshold": RMSE_THRESHOLD,
        "region_metrics": region_metrics
    }

    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=2)




    return metrics

if __name__ == "__main__":
    metrics = compute_metrics()
    if metrics:
        print(json.dumps(metrics, indent=2))
