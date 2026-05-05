from backend.services.gemini_service import ask_gemini_about_medicine


# 🔥 RAG KNOWLEDGE BASE (EXPANDED)
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
        "use": "Antihistamine for allergies.",
        "dosage_note": "Usually taken once daily, often at night.",
        "side_effects": "May cause drowsiness."
    },
    "fexofenadine": {
        "use": "Non-drowsy antihistamine for allergies.",
        "dosage_note": "Take before food for better absorption.",
        "side_effects": "Headache (rare)."
    },
    "rantac": {
        "use": "Reduces stomach acid (ranitidine).",
        "dosage_note": "Usually taken before meals.",
        "side_effects": "Headache (rare)."
    },
    "augmentin": {
        "use": "Combination antibiotic (amoxicillin + clavulanic acid).",
        "dosage_note": "Take after food.",
        "side_effects": "Diarrhea or nausea."
    },
    "montair": {
        "use": "Used for allergies and asthma control.",
        "dosage_note": "Often taken at night.",
        "side_effects": "Rare mood changes."
    },
    "ascoril": {
        "use": "Cough syrup that helps clear mucus.",
        "dosage_note": "Dose measured in teaspoons.",
        "side_effects": "Mild drowsiness."
    },
    "ors": {
        "use": "Prevents dehydration.",
        "dosage_note": "Take in small frequent sips.",
        "side_effects": "Generally safe."
    },
    "metformin": {
        "use": "Controls blood sugar in diabetes.",
        "dosage_note": "Take with meals.",
        "side_effects": "Stomach upset."
    },
    "atorvastatin": {
        "use": "Lowers cholesterol.",
        "dosage_note": "Usually taken at night.",
        "side_effects": "Muscle pain (rare)."
    },
    "cetirizine": {
        "use": "Antihistamine for allergies.",
        "dosage_note": "Usually once daily.",
        "side_effects": "Drowsiness."
    },
    "azithromycin": {
        "use": "Antibiotic for infections.",
        "dosage_note": "Once daily course.",
        "side_effects": "Nausea."
    },

    # 🔥 NEW ADDITIONS
    "ibuprofen": {
        "use": "Pain reliever and anti-inflammatory drug.",
        "dosage_note": "Take after food.",
        "side_effects": "Stomach irritation."
    },
    "omeprazole": {
        "use": "Reduces stomach acid.",
        "dosage_note": "Take before breakfast.",
        "side_effects": "Headache (rare)."
    },
    "pantoprazole": {
        "use": "Reduces stomach acid.",
        "dosage_note": "Take before breakfast.",
        "side_effects": "Headache."
    },
    "ceftum": {
        "use": "Antibiotic (cefuroxime).",
        "dosage_note": "Take after food.",
        "side_effects": "Nausea."
    },
    "allegra": {
        "use": "Antihistamine for allergies.",
        "dosage_note": "Usually once daily.",
        "side_effects": "Headache."
    },
    "ambroxol": {
        "use": "Helps loosen mucus in cough.",
        "dosage_note": "Taken as syrup.",
        "side_effects": "Mild stomach upset."
    }
}


# 🔥 COMMON FALLBACK (BETTER THAN GENERIC)
FALLBACK_INFO = {
    "ibuprofen": "Pain reliever and anti-inflammatory drug.",
    "omeprazole": "Reduces stomach acid.",
    "pantoprazole": "Reduces stomach acid.",
}


# 🔥 NORMALIZATION (VERY IMPORTANT)
def normalize_name(name: str):
    return name.lower().strip().replace("  ", " ")


# 🔥 FINAL FUNCTION (RAG + GEMINI HYBRID)
def explain_medicine(name: str):
    med = normalize_name(name)

    # ✅ 1. RAG FIRST (FAST + RELIABLE)
    if med in EXPLANATIONS:
        data = EXPLANATIONS[med]

        return (
            f"💊 Use: {data['use']}\n"
            f"📌 Note: {data['dosage_note']}\n"
            f"⚠️ Side Effects: {data['side_effects']}"
        )

    # ✅ 2. SIMPLE FALLBACK (NO API CALL)
    if med in FALLBACK_INFO:
        return f"💊 Use: {FALLBACK_INFO[med]}"

    # 🤖 3. GEMINI (SMART BUT OPTIONAL)
    try:
        return ask_gemini_about_medicine(name)
    except Exception:
        return f"{name} is a commonly prescribed medication."