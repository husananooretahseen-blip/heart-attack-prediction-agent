import pandas as pd
from agent import analyze_risk
from alert import generate_alert

DATASET_PATH = "data/heart.csv"

df = pd.read_csv(DATASET_PATH)

features = [
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

# Only actual positive patients
positive_patients = df[df["target"] == 1].copy()

results = []

for index, patient in positive_patients.iterrows():

    patient_data = {
        feature: patient[feature]
        for feature in features
    }

    result = analyze_risk(patient_data)

    results.append({
        "index": index,
        "probability": result["risk_probability"],
        "risk_level": result["risk_level"],
        "patient_data": patient_data
    })

# Find patient with highest predicted probability
highest_risk = max(
    results,
    key=lambda x: x["probability"]
)

print("\n" + "=" * 60)
print("HIGHEST-RISK PATIENT FOUND BY AI AGENT")
print("=" * 60)

print("Dataset Row:", highest_risk["index"])
print("Risk Probability:", highest_risk["probability"], "%")
print("Risk Level:", highest_risk["risk_level"])

print("\nPatient Details:")
for key, value in highest_risk["patient_data"].items():
    print(key, ":", value)

print("=" * 60)
alert = generate_alert(
    "P003",
    "High Risk Patient",
    highest_risk["risk_level"],
    highest_risk["probability"]
)

if alert:

    print("\n🚨 EMERGENCY ALERT")
    print("=" * 60)
    print("Patient ID:", alert["patient_id"])
    print("Patient Name:", alert["patient_name"])
    print("Alert Type:", alert["alert_type"])
    print("Risk Probability:", alert["risk_probability"], "%")
    print("Message:", alert["message"])
    print("Time:", alert["time"])

else:

    print("\nNo emergency alert generated.")