from typing import Optional

def dosage_alerts(medicine: str, dosage_mg: Optional[int], age: Optional[int]):

    alerts = []  

    if age is None or dosage_mg is None:
        return alerts

    # Paracetamol rules
    if medicine.lower() == "paracetamol":
        if age < 12 and dosage_mg > 500:
            alerts.append(
                "Paracetamol dosage may be high for a pediatric patient."
            )
        if age >= 18 and dosage_mg > 1000:
            alerts.append(
                "Single adult dose of Paracetamol exceeds recommended limit."
            )

    # Amoxicillin rules
    if medicine.lower() == "amoxicillin":
        if age < 12 and dosage_mg >= 500:
            alerts.append(
                "Pediatric Amoxicillin dosage requires weight-based adjustment."
            )

    return alerts