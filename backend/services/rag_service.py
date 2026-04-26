from backend.services.gemini_service import ask_gemini_about_medicine


# 🔥 RAG KNOWLEDGE BASE
EXPLANATIONS = {
    "paracetamol": {
        "use": "Reduces fever and relieves mild to moderate pain.",
        "dosage_note": "Usually taken after food.",
        "side_effects": "Overuse may affect liver."
    },
    "amoxicillin": {
        "use": "Antibiotic used to treat bacterial infections.",
        "dosage_note": "Complete full course even if symptoms improve.",
        "side_effects": "May cause nausea or diarrhea."
    },
    "levocetirizine": {
        "use": "Antihistamine for allergies, sneezing, runny nose.",
        "dosage_note": "Usually taken once daily, often at night.",
        "side_effects": "May cause mild drowsiness."
    },
    "fexofenadine": {
        "use": "Non-drowsy antihistamine for allergies.",
        "dosage_note": "Take before food for better absorption.",
        "side_effects": "Headache or dizziness (rare)."
    },
    "rantac": {
        "use": "Reduces stomach acid (used for acidity).",
        "dosage_note": "Usually taken before meals.",
        "side_effects": "Rare headaches or constipation."
    },
    "augmentin": {
        "use": "Broad-spectrum antibiotic.",
        "dosage_note": "Take after food to avoid stomach upset.",
        "side_effects": "Diarrhea or nausea."
    },
    "montair": {
        "use": "Used for allergies and asthma control.",
        "dosage_note": "Often taken at night.",
        "side_effects": "Rare mood changes."
    },
    "ascoril": {
        "use": "Cough syrup that helps clear mucus.",
        "dosage_note": "Taken as syrup (tsp-based dosage).",
        "side_effects": "May cause mild drowsiness."
    },
    "ors": {
        "use": "Prevents dehydration.",
        "dosage_note": "Take in small frequent sips.",
        "side_effects": "Generally safe."
    },
    "metformin": {
        "use": "Used to control blood sugar in diabetes.",
        "dosage_note": "Usually taken with meals.",
        "side_effects": "May cause stomach upset."
    },
    "atorvastatin": {
        "use": "Lowers cholesterol and reduces heart risk.",
        "dosage_note": "Usually taken at night.",
        "side_effects": "Muscle pain (rare)."
    },
    "cetirizine": {
        "use": "Antihistamine for allergies.",
        "dosage_note": "Usually taken once daily.",
        "side_effects": "May cause mild drowsiness."
    },
    "azithromycin": {
        "use": "Antibiotic used to treat bacterial infections.",
        "dosage_note": "Take once daily as prescribed.",
        "side_effects": "May cause nausea or diarrhea."
    }
}


# 🔥 FINAL FUNCTION (RAG + GEMINI HYBRID)
def explain_medicine(name: str):
    med = name.lower()

    # ✅ 1. RAG FIRST (FAST)
    if med in EXPLANATIONS:
        data = EXPLANATIONS[med]

        return (
            f"💊 Use: {data['use']}\n"
            f"📌 Note: {data['dosage_note']}\n"
            f"⚠️ Side Effects: {data['side_effects']}"
        )

    # 🤖 2. GEMINI FALLBACK (SMART)
    try:
        return ask_gemini_about_medicine(name)
    except Exception:
        return f"{name} is a commonly prescribed medication."