import re

# ---------------------------
# 🔥 OCR NORMALIZATION
# ---------------------------
def normalize_ocr_text(text: str) -> str:
    text = text.lower()

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
    "dispense", "solution", "refills"
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

        # Restore structure
        text = re.sub(r'(\d+\s*[_\-\.]?\s*tab)', r'\n\1', text)
        text = re.sub(r'(tab\s+[a-z])', r'\n\1', text)
        text = re.sub(r'(\d+\s*mg)', r'\1\n', text)
        text = re.sub(r'(once|twice|thrice|daily|before|after)', r'\n\1', text)

        medicines = []
        lines = text.split("\n")

        for i, line in enumerate(lines):
            line_clean = re.sub(r'[^a-zA-Z0-9\s]', '', line.strip())
            line_lower = line_clean.lower()

            if any(k in line_lower for k in ["dispense", "refill", "solution"]):
                continue

            if len(line_clean) < 3:
                continue

            # ORS special case
            if "ors" in line_lower:
                medicines.append({
                    "medicine": "ORS",
                    "dosage": None,
                    "timing": "as needed"
                })
                continue

            # Context
            context = line_lower
            if i + 1 < len(lines):
                context += " " + lines[i + 1].lower()
            if i + 2 < len(lines):
                context += " " + lines[i + 2].lower()

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
                r'([a-z]{4,})\s+\d{1,4}',
                context
            )

            if match1:
                name = match1.group(2)

            elif match2:
                candidate = match2.group(1)

                if candidate in TIMING_WORDS:
                    continue

                if candidate not in STOPWORDS:
                    name = candidate

            if not name:
                continue

            if (
                name in STOPWORDS
                or name in INVALID_WORDS
                or name in TIMING_WORDS
            ):
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
            # 🔥 TIMING (FINAL FIX)
            # ---------------------------
            timing = None

            # LOCAL window per medicine
            local_window = " ".join(lines[max(0, i-2): min(len(lines), i + 6)])

            # 🔥 ADD THIS (IMPORTANT)
            if i + 1 < len(lines):
               local_window += " " + lines[i + 1].lower()

            clean_text = re.sub(r'[^a-zA-Z]', ' ', local_window.lower())
            words = clean_text.split()
            joined = " ".join(words)

            if "once" in words:
                timing = "once daily"
            elif "twice" in words:
                timing = "twice daily"
            elif "thrice" in words:
                timing = "thrice daily"
            elif "daily" in words:
                timing = "once daily"
            elif "before breakfast" in joined:
                timing = "before breakfast"
            elif "before" in words:
                timing = "before food"
            elif "after" in words:
                timing = "after food"
            elif "night" in words:
                timing = "at night"
            elif "morning" in words:
                timing = "in morning"
            elif "needed" in words:
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