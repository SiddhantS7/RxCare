import re

# ---------------------------
# 🔥 OCR NORMALIZATION
# ---------------------------
def normalize_ocr_text(text: str) -> str:
    text = text.lower()

    # 🔥 FIX 1: handle OCR symbol noise
    text = text.replace("|", "i")

    replacements = {
        " mo": " mg",
        "m0": "mg",
        " m9": " mg",
        " i50": " 150",
        " i00": " 100",
        "l50": "150",
        "o5": "05",
        " 5 o": " 50",
        " 1o": " 10",
        " s mg": " 5 mg",
        "soo": "500",
        "s00": "500",
    }

    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)

    return text


# ---------------------------
# 🔥 FILTER WORDS
# ---------------------------
STOPWORDS = {
    "once", "twice", "thrice", "daily", "dailyy",
    "before", "after", "food", "meals",
    "needed", "tab", "tablet", "capsule",
    "syrup", "patient", "doctor", "clinic",
    "date", "dr"
}

INVALID_WORDS = {
    "mbbs", "consultant", "clinic",
    "mumbai", "physician", "general",
    "dispense", "solution", "refills",
    "verma", "sharma", "gupta", "kumar", "singh"
}

TIMING_WORDS = {
    "night", "morning", "evening",
    "once", "twice", "thrice", "daily"
}


# ---------------------------
# 🔥 FUZZY MATCHING
# ---------------------------
def correct_medicine_name(name):
    try:
        from rapidfuzz import process

        KNOWN_MEDICINES = [
            "paracetamol", "amoxicillin", "augmentin",
            "montair", "ascoril", "levocetirizine",
            "fexofenadine", "rantac", "azithromycin",
            "ibuprofen", "omeprazole",
            "metformin", "atorvastatin", "cetirizine",
            "ceftum", "fantop", "allegra"
        ]

        match, score, _ = process.extractOne(name, KNOWN_MEDICINES)

        if score > 80:
            return match

    except:
        pass

    return name


# ---------------------------
# 🔥 MAIN FUNCTION
# ---------------------------
def extract_medicine_info(text, known_medicines=None):
    try:
        text = normalize_ocr_text(text)

        # 🔥 FIX 2: DO NOT split on "daily"
        text = re.sub(r'(\d+\s*[_\-\.]?\s*tab)', r'\n\1', text)
        text = re.sub(r'(tab\s+[a-z])', r'\n\1', text)
        text = re.sub(r'(\d+\s*mg)', r'\1\n', text)
        text = re.sub(r'(once|twice|thrice|before|after)', r'\n\1', text)

        medicines = []
        lines = text.split("\n")

        for i, line in enumerate(lines):
            line_clean = re.sub(r'[^a-zA-Z0-9\s]', '', line.strip())
            line_lower = line_clean.lower()

            if any(k in line_lower for k in ["dispense", "refill", "solution"]):
                continue

            if len(line_clean) < 3:
                continue

            if "ors" in line_lower:
                medicines.append({
                    "medicine": "ORS",
                    "dosage": None,
                    "timing": "as needed"
                })
                continue

            context = " ".join(lines[i: min(len(lines), i + 5)]).lower()

            if "patient" in context:
                continue

            if not any(k in context for k in ["tab", "cap", "mg", "ml", "syp", "tsp"]):
                continue

            # ---------------------------
            # NAME DETECTION
            # ---------------------------
            name = None

            match1 = re.search(
                r'(tab|tablet|cap|capsule|syp|syrup)\s+([a-z]{3,})',
                line_lower
            )

            match2 = re.search(
                r'([a-z]{4,})\s*(\d{1,4})',
                context
            )

            if match1:
                name = match1.group(2)

            elif match2:
                candidate = match2.group(1)

                if candidate not in STOPWORDS:
                    name = candidate

            # 🔥 FIX 3: fallback name detection
            if not name:
                for w in context.split():
                    if w.isalpha() and len(w) > 4 and w not in STOPWORDS:
                        name = w
                        break

            if not name:
                continue

            if name in INVALID_WORDS or name in TIMING_WORDS:
                continue

            name = correct_medicine_name(name)

            # ---------------------------
            # DOSAGE
            # ---------------------------
            dosage = None

            match = re.search(r'(\d{1,4})\s*(mg|ml)', context)
            if match:
                dosage = f"{match.group(1)} {match.group(2)}"

            if not dosage:
                tab_match = re.search(r'(\d+)\s*tab', context)
                if tab_match:
                    dosage = f"{tab_match.group(1)} tablet"

            if not dosage:
                tsp_match = re.search(r'(\d+)\s*tsp', context)
                if tsp_match:
                    dosage = f"{tsp_match.group(1)} tsp"

                        # ---------------------------
            # 🔥 TIMING (FINAL FINAL FINAL FIX)
            # ---------------------------
            timing = None

            # use full context instead of broken lines
            full_context = context.lower()

            if "thrice" in full_context:
                timing = "thrice daily"
            elif "twice" in full_context:
                timing = "twice daily"
            elif "once" in full_context:
                timing = "once daily"
            elif "at night" in full_context or "night" in full_context:
                timing = "at night"
            elif "before" in full_context:
                timing = "before food"
            elif "after" in full_context:
                timing = "after food"
            elif "needed" in full_context:
                timing = "as needed"

            medicines.append({
                "medicine": name.capitalize(),
                "dosage": dosage,
                "timing": timing
            })
        # Remove duplicates
        unique = {}
        for med in medicines:
            unique[med["medicine"].lower()] = med

        return {
            "medicines": list(unique.values())
        }

    except Exception as e:
        print("NLP ERROR:", e)
        return {"medicines": []}