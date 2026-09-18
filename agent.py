from prediction import predict_patient


def analyze_risk(patient_data):

    # Get prediction from Phase 1 model
    prediction, probability = predict_patient(patient_data)

    # Decide risk level
    if probability >= 70:
        risk_level = "HIGH"

    elif probability >= 40:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    return {
        "prediction": int(prediction),
        "risk_probability": round(probability, 2),
        "risk_level": risk_level
    }