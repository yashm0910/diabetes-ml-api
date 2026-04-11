import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("Diabetes Prediction System")

# ---------------------------
# ADD PATIENT
# ---------------------------
st.header("Add Patient")

with st.form("patient_form"):
    pregnancies = int(st.number_input("Pregnancies", step=1))
    glucose = int(st.number_input("Glucose", step=1))
    bp = int(st.number_input("Blood Pressure", step=1))
    skin = int(st.number_input("Skin Thickness", step=1))
    insulin = int(st.number_input("Insulin", step=1))
    bmi = float(st.number_input("BMI"))
    pedigree = float(st.number_input("Diabetes Pedigree"))
    age = int(st.number_input("Age", step=1))

    submit = st.form_submit_button("Add Patient")

    if submit:
        payload = {
            "Pregnancies": pregnancies,
            "Glucose": glucose,
            "BloodPressure": bp,
            "SkinThickness": skin,
            "Insulin": insulin,
            "BMI": bmi,
            "DiabetesPedigree": pedigree,
            "Age": age
        }

        res = requests.post(f"{BASE_URL}/add_patient", json=payload)

        if res.status_code == 200:
            st.success("Patient added successfully")
            st.json(res.json())
        else:
            st.error("Error adding patient")
            st.text(res.text)


# ---------------------------
# VIEW PATIENTS
# ---------------------------
st.header("All Patients")

if st.button("Load Patients"):
    res = requests.get(f"{BASE_URL}/patients")

    if res.status_code == 200:
        patients = res.json()
        st.dataframe(patients)
    else:
        st.error(res.text)


# ---------------------------
# PREDICT
# ---------------------------
st.header("Predict Diabetes")

patient_id = int(st.number_input("Enter Patient ID", step=1))

if st.button("Predict"):
    with st.spinner("Running prediction..."):
        res = requests.post(f"{BASE_URL}/predict/{patient_id}")

    if res.status_code == 200:
        result = res.json()

        if result["prediction"] == 1:
            st.error("High risk of Diabetes")
        else:
            st.success("Low risk of Diabetes")

        st.json(result)
    else:
        st.error(res.text)