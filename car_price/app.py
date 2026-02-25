import streamlit as st
import pickle
import pandas as pd

# Load Single PKL File
with open("car_price_complete_model.pkl", "rb") as f:
    data = pickle.load(f)

model = data["model"]
encoder = data["encoder"]
features = data["features"]


st.set_page_config(page_title="Car Price Predictor", layout="centered")

st.title("🚗 Car Price Prediction App")
st.write("Predict Used Car Price (₹ Lakhs)")


# Inputs
brand = st.selectbox("Brand", ["Maruti", "Hyundai", "Tata", "Honda", "Toyota", "Kia", "Mahindra"])
year = st.number_input("Model Year", 2005, 2025, 2018)
fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "Electric"])
trans = st.selectbox("Transmission", ["Manual", "Automatic"])
km = st.number_input("Kilometers Driven", 5000, 200000, 50000)
mileage = st.number_input("Mileage (kmpl)", 8.0, 30.0, 18.0)
engine = st.number_input("Engine CC", 800, 3000, 1200)
owners = st.selectbox("Owners", [0, 1, 2, 3])


# Encode
brand_enc = encoder.fit_transform([brand])[0]
fuel_enc = encoder.fit_transform([fuel])[0]
trans_enc = encoder.fit_transform([trans])[0]


# Input Data
input_df = pd.DataFrame([[
    brand_enc,
    year,
    fuel_enc,
    trans_enc,
    km,
    mileage,
    engine,
    owners
]], columns=features)


# Predict
if st.button("Predict Price 💰"):
    price = model.predict(input_df)[0]

    st.success(f"Estimated Price: ₹ {round(price,2)} Lakhs")
