"""
Milestone 2: Feature Engineering & Data Wrangling
==================================================
Goal: Transform cleaned Azure demand data into a model-ready, feature-rich dataset.

Input:  outputs/azure_demand_cleaned.csv
Output: outputs/azure_demand_features.csv
        outputs/milestone2_usage_trends.png
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
INPUT_FILE  = "outputs/azure_demand_cleaned.csv"
OUTPUT_CSV  = "outputs/azure_demand_features.csv"
OUTPUT_PLOT = "outputs/milestone2_usage_trends.png"

os.makedirs("outputs", exist_ok=True)

# ─────────────────────────────────────────────
# STEP 1 — Load & Sort Data
# ─────────────────────────────────────────────
print("Step 1: Loading and sorting data...")
try:
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    raise FileNotFoundError(
        f"Input file not found: {INPUT_FILE}\n"
        "Please run data_preprocessing.py (Milestone 1) first."
    )

# Robust column detection
compute_col = "compute_usage_units" if "compute_usage_units" in df.columns else "usage_units"
storage_col = "storage_usage_gb"    if "storage_usage_gb"    in df.columns else "storage_usage"

df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed", dayfirst=True)

# Sort by region first, then time — required for correct per-region lag/rolling
df = df.sort_values(["region", "timestamp"]).reset_index(drop=True)

print(f"  Loaded {len(df)} rows | Regions: {df['region'].unique().tolist()}")

# ─────────────────────────────────────────────
# STEP 2 — Time-Based (Seasonality) Features
# ─────────────────────────────────────────────
print("Step 2: Creating time-based features...")
df["day_of_week"] = df["timestamp"].dt.dayofweek          # 0=Mon … 6=Sun
df["is_weekend"]  = df["day_of_week"].isin([5, 6]).astype(int)
df["month"]       = df["timestamp"].dt.month
df["quarter"]     = df["timestamp"].dt.quarter

# ─────────────────────────────────────────────
# STEP 3 — Lag Features (Memory of the Past)
# ─────────────────────────────────────────────
print("Step 3: Creating lag features (per region)...")
df["compute_lag_1"] = df.groupby("region")[compute_col].shift(1)
df["compute_lag_7"] = df.groupby("region")[compute_col].shift(7)

# ─────────────────────────────────────────────
# STEP 4 — Rolling / Trend Features
# ─────────────────────────────────────────────
print("Step 4: Creating rolling average features (per region)...")
df["compute_rolling_7"] = (
    df.groupby("region")[compute_col]
      .transform(lambda x: x.rolling(window=7, min_periods=1).mean())
)
df["storage_rolling_7"] = (
    df.groupby("region")[storage_col]
      .transform(lambda x: x.rolling(window=7, min_periods=1).mean())
)

# ─────────────────────────────────────────────
# STEP 5 — Spike Detection (Anomaly Signals)
# ─────────────────────────────────────────────
print("Step 5: Detecting usage spikes...")
compute_p95 = df[compute_col].quantile(0.95)
storage_p95 = df[storage_col].quantile(0.95)

df["compute_spike"] = (df[compute_col] > compute_p95).astype(int)
df["storage_spike"]  = (df[storage_col]  > storage_p95).astype(int)

print(f"  Compute spike threshold (95th pct): {compute_p95:.2f}")
print(f"  Storage spike threshold (95th pct): {storage_p95:.2f}")

# ─────────────────────────────────────────────
# STEP 6 — Drop Rows with NaN from Lag Features
# ─────────────────────────────────────────────
print("Step 6: Dropping rows with NaN from lag features...")
before = len(df)
df.dropna(subset=["compute_lag_7"], inplace=True)
df.reset_index(drop=True, inplace=True)
print(f"  Dropped {before - len(df)} rows | Remaining: {len(df)}")

# ─────────────────────────────────────────────
# STEP 7 — Save Model-Ready Dataset
# ─────────────────────────────────────────────
print(f"Step 7: Saving feature dataset to {OUTPUT_CSV}...")
df.to_csv(OUTPUT_CSV, index=False)
print(f"  Saved! Shape: {df.shape}")
print(f"  Columns: {df.columns.tolist()}")

# ─────────────────────────────────────────────
# STEP 8 — Validation Visualization
# ─────────────────────────────────────────────
print("Step 8: Generating validation plot...")

regions = df["region"].unique()
colors  = ["#4C72B0", "#DD8452", "#55A868"]  # one per region

fig, axes = plt.subplots(2, 1, figsize=(14, 9), sharex=False)
fig.suptitle("Milestone 2 — Azure Demand Feature Engineering Validation",
             fontsize=14, fontweight="bold", y=0.98)

# ── Plot 1: Raw compute usage + 7-day rolling average ──
ax1 = axes[0]
for i, region in enumerate(regions):
    sub = df[df["region"] == region]
    ax1.plot(sub["timestamp"], sub[compute_col],
             alpha=0.35, linewidth=1, color=colors[i % len(colors)])
    ax1.plot(sub["timestamp"], sub["compute_rolling_7"],
             linewidth=2, label=f"{region} (7d avg)", color=colors[i % len(colors)])

ax1.set_title("Compute Usage — Raw vs 7-Day Rolling Average")
ax1.set_ylabel("Compute Usage Units")
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax1.xaxis.set_major_locator(mdates.MonthLocator())

# ── Plot 2: Spike markers ──
ax2 = axes[1]
for i, region in enumerate(regions):
    sub = df[df["region"] == region]
    ax2.plot(sub["timestamp"], sub[compute_col],
             linewidth=1.2, label=region, color=colors[i % len(colors)])
    spikes = sub[sub["compute_spike"] == 1]
    ax2.scatter(spikes["timestamp"], spikes[compute_col],
                color="red", zorder=5, s=20, alpha=0.7)

ax2.set_title("Compute Usage with Spike Indicators (red dots = > 95th percentile)")
ax2.set_ylabel("Compute Usage Units")
ax2.set_xlabel("Date")
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax2.xaxis.set_major_locator(mdates.MonthLocator())

plt.tight_layout()
plt.savefig(OUTPUT_PLOT, dpi=150, bbox_inches="tight")
print(f"  Plot saved to {OUTPUT_PLOT}")

print("\n✅ Milestone 2 Complete!")
print(f"   Features CSV : {OUTPUT_CSV}")
print(f"   Trends Plot  : {OUTPUT_PLOT}")
