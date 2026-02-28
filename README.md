#Azure Demand Forecasting & Capacity Optimization System
 #Milestone 1: Data Collection & Preparation
1. Introduction

Modern cloud platforms such as Microsoft Azure must continuously balance infrastructure capacity with dynamic customer demand. Inaccurate capacity planning can lead to increased operational costs or degraded service performance.

This project aims to build a data-driven system to forecast Azure compute and storage demand across multiple regions.
Milestone 1 focuses exclusively on establishing a high-quality data foundation that will support forecasting and optimization in later stages.

2. Milestone 1 Objective

The objective of Milestone 1: Data Collection & Preparation is to:

Prepare historical demand data over a meaningful time horizon

Integrate relevant external influencing variables

Clean, validate, and standardize the dataset

Ensure the dataset is suitable for downstream time-series forecasting models

A reliable dataset at this stage is critical for ensuring accuracy and robustness in future predictive modeling.

3. Dataset Overview

The dataset represents Azure demand patterns over a 9-month period, with daily observations across multiple regions.

Time Characteristics

Time Range: 9 months

Frequency: Daily

Timestamp Format: Standardized datetime format

Dataset Features

timestamp – Date of observation

region – Azure deployment region

compute_usage_units – Compute resource consumption

storage_usage_gb – Storage resource utilization

cpu_utilization_percent – CPU utilization percentage

storage_utilization_percent – Storage utilization percentage

estimated_cost_usd – Estimated cost derived from usage

is_holiday – Holiday indicator (0 = No, 1 = Yes)

economic_index – Simulated economic influence factor

These features reflect realistic drivers of cloud infrastructure demand.

4. Data Source

Primary Data: Synthetic dataset designed to simulate real Azure usage trends

External Variables: Simulated indicators based on common demand drivers such as:

Holidays

Regional usage behavior

Economic activity

Although synthetic, the dataset structure closely follows industry-standard cloud analytics practices.

5. Data Preprocessing Methodology

The following preprocessing steps were performed as part of Milestone 1:

Conversion of timestamp fields to datetime format

Chronological sorting of time-series data

Handling missing numerical values using interpolation

Validation of numeric consistency across features

Generation of a cleaned and structured output dataset

Visualization of compute usage trends to validate data integrity

These steps ensure the dataset is clean, consistent, and analysis-ready.

6. Tools & Technologies

Programming Language: Python

Libraries:

Pandas

NumPy

Matplotlib

Development Environment: Visual Studio Code (VS Code)

7. Project Structure
Azure_Demand_Forecast_Output/
│
├── scripts/
│   └── prepare_data.py
│
├── outputs/
│   ├── azure_demand_cleaned.csv
│   ├── azure_demand_cleaned_final.csv
│   └── usage_over_time.png
│
├── requirements.txt
└── README.md

8. Execution Instructions

To run Milestone 1:

Open the project folder in Visual Studio Code

Activate the virtual environment (optional):

venv\Scripts\activate


Install required dependencies:

pip install -r requirements.txt


Execute the preprocessing script:

python scripts/prepare_data.py

9. Milestone 1 Deliverables

Cleaned and validated Azure demand dataset

Structured time-series data suitable for forecasting

Visualization of compute usage trends by region

Reproducible preprocessing pipeline

10. Current Project Status

 Milestone 1: Completed

 #Milestone 2: Feature Engineering & Data Wrangling
1. Milestone Overview

Following the successful preparation of a clean and reliable dataset in Milestone 1,
Milestone 2 focuses on transforming the data into a model-ready format by engineering meaningful features that capture demand patterns, trends, and anomalies.

This stage enriches the dataset with temporal, statistical, and behavioral signals required for accurate forecasting.

2. Milestone 2 Objectives

The objectives of Milestone 2 are to:

Identify demand-driving patterns in compute and storage usage

Engineer time-based and statistical features for seasonality and trends

Create lag and rolling-window features to capture historical dependencies

Detect abnormal demand spikes for anomaly awareness

Prepare a consistent, feature-rich dataset suitable for machine learning models

3. Feature Engineering Process

The following feature engineering steps were applied:

Time-Based Features

Day of week

Weekend indicator

Month

Quarter

These features help capture weekly and seasonal usage behavior.

Lag Features

1-day lag of compute usage

7-day lag of compute usage

Lag features allow models to learn from historical demand dependencies.

Rolling Statistics

7-day rolling average of compute usage

7-day rolling average of storage usage

Rolling features smooth short-term noise and highlight long-term trends.

Spike Detection

Compute usage spike indicator (above 95th percentile)

Storage usage spike indicator (above 95th percentile)

These features flag unusually high demand periods.

4. Input & Output Artifacts

Input Dataset

outputs/azure_demand_cleaned.csv (from Milestone 1)

Generated Outputs

outputs/azure_demand_features.csv – Feature-engineered dataset

outputs/milestone2_usage_trends.png – Validation visualization of trends and spikes

5. Tools & Technologies Used

Programming Language: Python

Libraries:

Pandas

NumPy

Matplotlib

Development Environment: Visual Studio Code

6. Project Structure (Updated)
Azure_Demand_Forecast_Output/
│
├── scripts/
│   ├── prepare_data.py
│   └── feature_engineering.py
│
├── outputs/
│   ├── azure_demand_cleaned.csv
│   ├── azure_demand_features.csv
│   ├── usage_over_time.png
│   └── milestone2_usage_trends.png
│
├── requirements.txt
└── README.md
7. Execution Instructions (Milestone 2)

To run Milestone 2:

venv\Scripts\activate
python scripts/feature_engineering.py
8. Milestone 2 Deliverables

Feature-engineered Azure demand dataset

Lag, rolling, seasonality, and spike features

Validation plots confirming correct feature generation

Model-ready dataset for forecasting algorithms