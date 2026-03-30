"""
Prepare data/azure_usage_data.csv from the cleaned dataset.
Maps column names to the format expected by the Milestone-3 script:
  - timestamp  (datetime)
  - usage_units (= compute_usage_units)
"""

import pandas as pd

df = pd.read_csv("outputs/azure_demand_cleaned.csv")

# Standardise the timestamp column
df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed", dayfirst=True)
df = df.sort_values("timestamp").reset_index(drop=True)

# Create the simplified dataset
out = df[["timestamp"]].copy()
out["usage_units"] = df["compute_usage_units"]

out.to_csv("data/azure_usage_data.csv", index=False)
print(f"Saved data/azure_usage_data.csv  |  {len(out)} rows")
print(out.head())
