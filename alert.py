from datetime import datetime


def generate_alert(patient_id, patient_name, risk_level, probability):

    if risk_level == "HIGH":

        alert = {
            "patient_id": patient_id,
            "patient_name": patient_name,
            "alert_type": "EMERGENCY",
            "message": (
                "High heart disease risk detected. "
                "Immediate medical attention is recommended."
            ),
            "risk_probability": probability,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return alert

    return None