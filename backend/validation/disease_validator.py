import pandas as pd
from backend.config.settings import DATA_DIR

df = pd.read_csv(DATA_DIR / "drug_disease.csv")

def validate_medicine(medicines, disease):
    alerts = []

    for med in medicines:
        match = df[df["medicine"].str.lower() == med.lower()]
        if not match.empty:
            expected = match.iloc[0]["disease"]
            if expected.lower() != disease.lower():
                alerts.append(
                    f"{med} is usually prescribed for {expected}"
                )
    return alerts
