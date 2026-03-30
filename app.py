import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Load model
model = joblib.load("models/xgboost_model.pkl")

st.title("Azure Demand Forecast System")

st.write("Predict demand using date input")

# Inputs
year = st.number_input("Year", 2020, 2030)
month = st.number_input("Month", 1, 12)
day = st.number_input("Day", 1, 31)

if st.button("Predict Demand"):

    # Input dataframe
    data = pd.DataFrame([{
        "year": year,
        "month": month,
        "day": day
    }])

    # Prediction
    prediction = model.predict(data)[0]

    st.success(f"Predicted Demand: {prediction:.2f}")

    # ✅ Capacity Planning Logic
    if prediction > 1000:
        st.warning("⚠️ High Demand → Scale Up Resources")
    elif prediction > 700:
        st.info("🔄 Moderate Demand → Keep Resources Normal")
    else:
        st.success("✅ Low Demand → Scale Down Resources")

   # 📊 GRAPH (Correct version)
st.subheader("Demand Visualization")

import matplotlib.pyplot as plt

sample_days = list(range(1, 8))
sample_predictions = []

for d in sample_days:
    temp = pd.DataFrame([{
        "year": year,
        "month": month,
        "day": d
    }])
    pred = model.predict(temp)[0]
    sample_predictions.append(pred)

# Create plot
fig, ax = plt.subplots()
ax.plot(sample_days, sample_predictions)

# Labels (important)
ax.set_xlabel("Day")
ax.set_ylabel("Demand")
ax.set_title("Weekly Demand Forecast")

# Show graph
st.pyplot(fig)