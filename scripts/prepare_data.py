import pandas as pd
import numpy as np


input_path = "../data/your_dataset.csv"
output_path = "../data/cleaned_dataset.csv"

print(f"Loading data from {input_path}...")
df = pd.read_csv(input_path, parse_dates=["timestamp"])


print("Sorting data by timestamp...")
df = df.sort_values("timestamp")


print("Interpolating missing values...")
numerical_cols = df.select_dtypes(include=[np.number]).columns
df[numerical_cols] = df[numerical_cols].interpolate()


print(f"Saving cleaned data to {output_path}...")
df.to_csv(output_path, index=False)

print("Data cleaned and saved successfully!")
