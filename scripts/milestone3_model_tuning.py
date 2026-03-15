
Milestone 3: Model Training & Hyperparameter Tuning

Goal: Train baseline ARIMA & XGBoost models, perform hyperparameter
      tuning, compare results, and visualize forecast predictions.

Input:  data/azure_usage_data.csv
Output: Console RMSE metrics + Demand Forecast Comparison plot
"""

# ── Step 1 — Imports 
import pandas as pd
import numpy as np

from statsmodels.tsa.arima.model import ARIMA
from xgboost import XGBRegressor

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error

import matplotlib.pyplot as plt

# ── Step 2 — Load Dataset 
df = pd.read_csv("data/azure_usage_data.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])

# ── Step 3 — Feature Engineering 
df["year"] = df["timestamp"].dt.year
df["month"] = df["timestamp"].dt.month
df["day"] = df["timestamp"].dt.day

df = df.drop("timestamp", axis=1)

# ── Step 4 — Define Features and Target 
X = df.drop("usage_units", axis=1)
y = df["usage_units"]

# ── Step 5 — Train Test Split 
train_size = int(len(df) * 0.8)

X_train = X[:train_size]
X_test = X[train_size:]

y_train = y[:train_size]
y_test = y[train_size:]

# ── Step 6 — Baseline ARIMA Model 
arima_model = ARIMA(y_train, order=(1, 1, 1))
arima_model_fit = arima_model.fit()

arima_pred = arima_model_fit.forecast(steps=len(y_test))

# ── Step 7 — Baseline XGBoost Model 
xgb_model = XGBRegressor(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    random_state=42,
    objective="reg:squarederror"
)

xgb_model.fit(X_train, y_train)

xgb_pred = xgb_model.predict(X_test)

# ── Step 8 — Baseline Model Evaluation 
rmse_arima = np.sqrt(mean_squared_error(y_test, arima_pred))
rmse_xgb = np.sqrt(mean_squared_error(y_test, xgb_pred))

print("Baseline ARIMA RMSE:", rmse_arima)
print("Baseline XGBoost RMSE:", rmse_xgb)

# ── Step 9 — ARIMA Hyperparameter Tuning 
p = range(0, 4)
d = range(0, 2)
q = range(0, 4)

best_score = float("inf")
best_order = None

for i in p:
    for j in d:
        for k in q:

            try:
                model = ARIMA(y_train, order=(i, j, k))
                model_fit = model.fit()

                pred = model_fit.forecast(steps=len(y_test))

                rmse = np.sqrt(mean_squared_error(y_test, pred))

                if rmse < best_score:
                    best_score = rmse
                    best_order = (i, j, k)

            except:
                continue

print(f"\nBest ARIMA order: {best_order}")

# ── Step 10 — Train Best ARIMA Model 
best_arima_model = ARIMA(y_train, order=best_order).fit()

arima_tuned_pred = best_arima_model.forecast(steps=len(y_test))

# ── Step 11 & 12 — XGBoost Hyperparameter Tuning (GridSearchCV) 
param_grid = {

    "n_estimators": [100, 200, 300],
    "max_depth": [3, 5, 7],
    "learning_rate": [0.01, 0.1],
    "subsample": [0.8, 1]

}

grid_search = GridSearchCV(
    estimator=XGBRegressor(objective="reg:squarederror", random_state=42),
    param_grid=param_grid,
    scoring="neg_mean_squared_error",
    cv=3,
    verbose=1
)

grid_search.fit(X_train, y_train)

print(f"\nBest XGBoost params: {grid_search.best_params_}")

# ── Step 13 — Best XGBoost Model 
best_xgb = grid_search.best_estimator_

xgb_tuned_pred = best_xgb.predict(X_test)

# ── Step 14 — Final Model Evaluation 
rmse_arima_tuned = np.sqrt(mean_squared_error(y_test, arima_tuned_pred))
rmse_xgb_tuned = np.sqrt(mean_squared_error(y_test, xgb_tuned_pred))

print("\nTuned ARIMA RMSE:", rmse_arima_tuned)
print("Tuned XGBoost RMSE:", rmse_xgb_tuned)

plt.figure(figsize=(10, 5))

plt.plot(y_test.values, label="Actual")
plt.plot(arima_tuned_pred.values, label="ARIMA")
plt.plot(xgb_tuned_pred, label="XGBoost")

plt.legend()
plt.title("Demand Forecast Comparison")

plt.savefig("outputs/milestone3_forecast_comparison.png", dpi=150, bbox_inches="tight")
print("\nPlot saved to outputs/milestone3_forecast_comparison.png")
plt.show()
