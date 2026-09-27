import streamlit as st
import pandas as pd
import pickle

data = pd.read_csv(r"D:\my_python\33_investment_dataset_practice\House_data.csv")

with open(r"D:\my_python\33_investment_dataset_practice\house_model.pkl", "rb") as file:
    saved = pickle.load(file)

x = data.drop(data.columns[4], axis=1)

st.title("House Price Prediction")

values = {}

for column in x.columns:
    if x[column].dtype == "object":
        values[column] = st.selectbox(column, x[column].dropna().unique())
    else:
        values[column] = st.number_input(column, value=0.0)

if st.button("Predict"):
    new_house = pd.DataFrame([values])
    new_house = pd.get_dummies(new_house, dtype=int)
    new_house = new_house.reindex(
        columns=saved["feature_columns"],
        fill_value=0
    )

    prediction = saved["model"].predict(new_house)
    st.write("Predicted house price:", prediction[0])