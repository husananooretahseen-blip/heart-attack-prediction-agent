import pandas as pd
import os


FILE_PATH = "data/patient_records.csv"


def save_assessment(patient_data, result):

    # Patient details copy
    record = patient_data.copy()

    # Add AI assessment results
    record["prediction"] = result["prediction"]
    record["risk_probability"] = result["risk_probability"]
    record["risk_level"] = result["risk_level"]

    # Convert to DataFrame
    new_record = pd.DataFrame([record])

    # Check whether records file already exists
    if os.path.exists(FILE_PATH):

        old_records = pd.read_csv(FILE_PATH)

        all_records = pd.concat(
            [old_records, new_record],
            ignore_index=True
        )

    else:

        all_records = new_record

    # Save records
    all_records.to_csv(FILE_PATH, index=False)

    return True