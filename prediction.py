import joblib
import pandas as pd

# Load the Phase 1 trained model
model = joblib.load("models/best_model.pkl")

# Feature names and their correct order from Phase 1
feature_names = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal"
]


def predict_patient(patient_data):

    # Convert patient data into DataFrame
    patient_df = pd.DataFrame(
        [patient_data],
        columns=feature_names
    )

    # Make prediction
    prediction = model.predict(patient_df)[0]

    # Get probability
    probability = model.predict_proba(patient_df)[0]

    risk_probability = probability[1] * 100

    return prediction, risk_probability




