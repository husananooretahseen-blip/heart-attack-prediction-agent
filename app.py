from agent import analyze_risk
from alert import generate_alert
from records import save_assessment


def main():

    print("=" * 60)
    print("       HEART ATTACK AI HEALTHCARE ALERT AGENT")
    print("=" * 60)

    # Patient information
    patient_id = input("Patient ID: ")
    patient_name = input("Patient Name: ")

    print("\nEnter Patient Health Details")
    print("-" * 40)

    age = float(input("Age: "))
    sex = float(input("Sex (0 = Female, 1 = Male): "))
    cp = float(input("Chest Pain Type (0-3): "))
    trestbps = float(input("Resting Blood Pressure: "))
    chol = float(input("Cholesterol: "))
    fbs = float(input("Fasting Blood Sugar (0/1): "))
    restecg = float(input("Rest ECG (0-2): "))
    thalach = float(input("Maximum Heart Rate: "))
    exang = float(input("Exercise Induced Angina (0/1): "))
    oldpeak = float(input("Oldpeak: "))
    slope = float(input("Slope (0-2): "))
    ca = float(input("Number of Major Vessels (0-4): "))
    thal = float(input("Thal (0-3): "))

    # Create patient data
    patient_data = {
        "age": age,
        "sex": sex,
        "cp": cp,
        "trestbps": trestbps,
        "chol": chol,
        "fbs": fbs,
        "restecg": restecg,
        "thalach": thalach,
        "exang": exang,
        "oldpeak": oldpeak,
        "slope": slope,
        "ca": ca,
        "thal": thal
    }

    # AI risk analysis
    result = analyze_risk(patient_data)

    print("\n" + "=" * 60)
    print("              RISK ASSESSMENT")
    print("=" * 60)

    print("Risk Probability :", result["risk_probability"], "%")
    print("Risk Level       :", result["risk_level"])

    # Generate emergency alert
    alert = generate_alert(
        patient_id,
        patient_name,
        result["risk_level"],
        result["risk_probability"]
    )

    if alert:

        print("\n🚨 EMERGENCY ALERT")
        print("-" * 40)
        print("Patient:", alert["patient_name"])
        print("Alert Type:", alert["alert_type"])
        print("Risk Probability:", alert["risk_probability"], "%")
        print("Message:", alert["message"])
        print("Time:", alert["time"])

    else:

        print("\n✅ No Emergency Alert Generated.")

    # Save patient assessment
    save_assessment(patient_data, result)

    print("\n✅ Patient assessment record saved successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()