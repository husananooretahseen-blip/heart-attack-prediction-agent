import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Heart Attack Prediction AI Agent",
    page_icon="❤️",
    layout="wide"
)


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

@st.cache_resource
def load_model():

    model = joblib.load("best_model.pkl")
    feature_names = joblib.load("feature_names.pkl")

    return model, feature_names


model, feature_names = load_model()


# ============================================================
# RECORD FILE
# ============================================================

RECORD_FILE = "patient_records.csv"

if not os.path.exists(RECORD_FILE):

    columns = [
        "Patient ID",
        "Patient Name",
        "Date",
        "Age",
        "Sex",
        "Prediction",
        "Risk Probability",
        "Risk Level",
        "Alert"
    ]

    pd.DataFrame(columns=columns).to_csv(
        RECORD_FILE,
        index=False
    )


# ============================================================
# TITLE
# ============================================================

st.title("❤️ Heart Attack Prediction AI Agent")

st.write(
    "Intelligent healthcare risk assessment using "
    "a trained Random Forest machine learning model."
)

st.warning(
    "⚠️ This system is for educational and decision-support "
    "purposes only. It is not a medical diagnosis."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏥 AI Agent")

page = st.sidebar.radio(
    "Navigation",
    [
        "🩺 Patient Assessment",
        "📋 Assessment History",
        "🚨 High-Risk Patients"
    ]
)


# ============================================================
# PATIENT ASSESSMENT
# ============================================================

if page == "🩺 Patient Assessment":

    st.header("🩺 Patient Assessment")

    st.subheader("Patient Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        patient_id = st.text_input(
            "Patient ID",
            placeholder="Example: P001"
        )

    with col2:
        patient_name = st.text_input(
            "Patient Name",
            placeholder="Enter patient name"
        )

    with col3:
        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=50
        )


    st.subheader("❤️ Medical Parameters")

    col1, col2, col3 = st.columns(3)


    # --------------------------------------------------------
    # COLUMN 1
    # --------------------------------------------------------

    with col1:

        sex = st.selectbox(
            "Sex",
            ["Male", "Female"]
        )

        cp = st.selectbox(
            "Chest Pain Type (cp)",
            [0, 1, 2, 3]
        )

        trestbps = st.number_input(
            "Resting Blood Pressure (trestbps)",
            min_value=50,
            max_value=250,
            value=120
        )

        chol = st.number_input(
            "Cholesterol (chol)",
            min_value=50,
            max_value=700,
            value=200
        )


    # --------------------------------------------------------
    # COLUMN 2
    # --------------------------------------------------------

    with col2:

        fbs = st.selectbox(
            "Fasting Blood Sugar (fbs)",
            [0, 1]
        )

        restecg = st.selectbox(
            "Resting ECG (restecg)",
            [0, 1, 2]
        )

        thalach = st.number_input(
            "Maximum Heart Rate (thalach)",
            min_value=50,
            max_value=250,
            value=150
        )

        exang = st.selectbox(
            "Exercise Induced Angina (exang)",
            [0, 1]
        )


    # --------------------------------------------------------
    # COLUMN 3
    # --------------------------------------------------------

    with col3:

        oldpeak = st.number_input(
            "ST Depression (oldpeak)",
            min_value=0.0,
            max_value=10.0,
            value=1.0,
            step=0.1
        )

        slope = st.selectbox(
            "Slope",
            [0, 1, 2]
        )

        ca = st.selectbox(
            "Number of Major Vessels (ca)",
            [0, 1, 2, 3, 4]
        )

        thal = st.selectbox(
            "Thalassemia (thal)",
            [0, 1, 2, 3]
        )


    st.divider()


    # ========================================================
    # ASSESS BUTTON
    # ========================================================

    if st.button(
        "🔍 Assess Patient",
        type="primary",
        use_container_width=True
    ):

        # Check patient information

        if not patient_id.strip():

            st.error("Please enter Patient ID.")

            st.stop()


        if not patient_name.strip():

            st.error("Please enter Patient Name.")

            st.stop()


        # ----------------------------------------------------
        # CONVERT SEX
        # ----------------------------------------------------

        sex_value = 1 if sex == "Male" else 0


        # ----------------------------------------------------
        # CREATE INPUT DATA
        # ----------------------------------------------------

        input_data = pd.DataFrame(
            [[
                age,
                sex_value,
                cp,
                trestbps,
                chol,
                fbs,
                restecg,
                thalach,
                exang,
                oldpeak,
                slope,
                ca,
                thal
            ]],
            columns=[
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
        )


        # ----------------------------------------------------
        # MATCH TRAINING FEATURE ORDER
        # ----------------------------------------------------

        input_data = input_data[
            list(feature_names)
        ]


        # ----------------------------------------------------
        # MODEL PREDICTION
        # ----------------------------------------------------

        prediction = model.predict(
            input_data
        )[0]

        probability = model.predict_proba(
            input_data
        )[0][1]

        probability_percent = probability * 100


        # ----------------------------------------------------
        # RISK LEVEL
        # ----------------------------------------------------

        if probability < 0.40:

            risk_level = "LOW"
            alert = "NORMAL"

        elif probability < 0.70:

            risk_level = "MODERATE"
            alert = "WARNING"

        else:

            risk_level = "HIGH"
            alert = "EMERGENCY"


        # ----------------------------------------------------
        # PREDICTION TEXT
        # ----------------------------------------------------

        if prediction == 1:

            prediction_text = "Heart Disease Risk"

        else:

            prediction_text = "Lower Risk"


        # ====================================================
        # DISPLAY RESULT
        # ====================================================

        st.divider()

        st.header("📊 Assessment Result")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Predicted Risk",
                f"{probability_percent:.2f}%"
            )

        with col2:

            st.metric(
                "Risk Level",
                risk_level
            )

        with col3:

            st.metric(
                "Prediction",
                prediction_text
            )


        # ====================================================
        # ALERT
        # ====================================================

        if risk_level == "HIGH":

            st.error(
                "🚨 HIGH RISK ALERT\n\n"
                "The model indicates a high predicted risk. "
                "Urgent medical evaluation is recommended."
            )

        elif risk_level == "MODERATE":

            st.warning(
                "⚠️ MODERATE RISK\n\n"
                "The model indicates an elevated predicted risk. "
                "Medical consultation is recommended."
            )

        else:

            st.success(
                "✅ LOW RISK\n\n"
                "The model did not identify a high predicted risk."
            )


        # ====================================================
        # SAVE PATIENT RECORD
        # ====================================================

        new_record = pd.DataFrame([
            {
                "Patient ID": patient_id,
                "Patient Name": patient_name,
                "Date": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "Age": age,
                "Sex": sex,
                "Prediction": prediction_text,
                "Risk Probability":
                    f"{probability_percent:.2f}%",
                "Risk Level": risk_level,
                "Alert": alert
            }
        ])


        existing_records = pd.read_csv(
            RECORD_FILE
        )


        updated_records = pd.concat(
            [
                existing_records,
                new_record
            ],
            ignore_index=True
        )


        updated_records.to_csv(
            RECORD_FILE,
            index=False
        )


        st.success(
            "✅ Patient assessment saved successfully!"
        )


# ============================================================
# ASSESSMENT HISTORY
# ============================================================

elif page == "📋 Assessment History":

    st.header("📋 Patient Assessment History")

    records = pd.read_csv(
        RECORD_FILE
    )


    if records.empty:

        st.info(
            "No patient assessment records available yet."
        )

    else:

        st.dataframe(
            records,
            use_container_width=True
        )


# ============================================================
# HIGH-RISK PATIENTS
# ============================================================

elif page == "🚨 High-Risk Patients":

    st.header("🚨 High-Risk Patients")

    records = pd.read_csv(
        RECORD_FILE
    )


    if records.empty:

        st.info(
            "No patient records available yet."
        )

    else:

        high_risk = records[
            records["Risk Level"] == "HIGH"
        ]


        if high_risk.empty:

            st.success(
                "✅ No high-risk patients found."
            )

        else:

            st.error(
                f"🚨 {len(high_risk)} high-risk "
                "patient(s) detected."
            )

            st.dataframe(
                high_risk,
                use_container_width=True
            )


# ============================================================
# SIDEBAR INFORMATION
# ============================================================

st.sidebar.divider()

st.sidebar.info(
    "❤️ Heart Attack Prediction AI Agent\n\n"
    "ML Model: Random Forest\n\n"
    "Purpose: Healthcare Risk Assessment"
)