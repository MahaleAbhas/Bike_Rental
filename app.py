import streamlit as st
import joblib
import pandas as pd
import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Bike Demand Prediction",
    layout="centered"
)

st.title("🚲 Bike Demand Prediction App")
st.write("Fill the details below and click **Predict**")

# ---------- LOAD MODEL ----------
try:
    model = joblib.load("best_model.pkl")
    st.success("✅ Model loaded successfully")
except Exception as e:
    st.error("❌ Model could not be loaded")
    st.write(e)
    st.stop()

# ---------- INPUT SECTION ----------
st.subheader("Input Details")




date = st.date_input("Date", datetime.date.today())
hr = st.slider("Hour", 0, 23, 12)

atemp = st.slider("Feels Like Temperature (normalized)", 0.0, 1.0, 0.5)
windspeed = st.slider("Wind Speed (normalized)", 0.0, 1.0, 0.3)

season = st.selectbox("Season", [1, 2, 3, 4])
holiday = st.selectbox("Holiday", [0, 1])
workingday = st.selectbox("Working Day", [0, 1])
weathersit = st.selectbox("Weather Situation", [1, 2, 3])

# ---------- FEATURE ENGINEERING ----------
day = date.day
month = date.month
year = date.year
weekday = date.weekday()
is_weekend = 1 if weekday >= 5 else 0
is_peak_hour = 1 if hr in [7, 8, 9, 17, 18, 19] else 0

weather_comfort = atemp * (1 - windspeed)


# FINAL INPUT
input_df = pd.DataFrame([{
    "season": season,
    "holiday": holiday,
    "workingday": workingday,
    "weathersit": weathersit,
    "atemp": atemp,
    "windspeed": windspeed,
    "day": day,
    "month": month,
    "year": year,
    "weekday": weekday,
    "hr": hr,
    "is_weekend": is_weekend,
    "is_peak_hour": is_peak_hour,
    "weather_comfort": weather_comfort
}])

# 🔥 CRITICAL FIX: enforce correct column order
input_df = input_df[model.feature_names_in_]

# # PREDICTION
# if st.button("Predict"):
#     st.success(int(model.predict(input_df)[0]))

# # ---------- FINAL INPUT ----------
# input_df = pd.DataFrame([{
#     "season": season,
#     "holiday": holiday,
#     "workingday": workingday,
#     "weathersit": weathersit,
#     "atemp": atemp,
#     "windspeed": windspeed,
#     "day": day,
#     "month": month,
#     "year": year,
#     "weekday": weekday,
#     "hr": hr,
#     "is_weekend": is_weekend,
#     "is_peak_hour": is_peak_hour,
#     "weather_comfort": weather_comfort
# }])

# ---------- DEBUG VIEW ----------
with st.expander("🔍 See model input (debug)"):
    st.dataframe(input_df)

# ---------- PREDICTION ----------
if st.button("🔮 Predict Bike Demand"):
    try:
        prediction = model.predict(input_df)[0]
        st.success(f"🚴 Estimated Bike Rentals: **{int(prediction)}**")
    except Exception as e:
        st.error("❌ Prediction failed")
        st.write(e)
