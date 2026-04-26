import google.generativeai as genai
import os
import json
import re

# ✅ LOAD API KEY PROPERLY
genai.configure(api_key=os.getenv("AIzaSyB6leUNwkrROfbQAJl0zGnBSroMBamjpLg"))

model = genai.GenerativeModel("gemini-1.5-flash")


# 🔥 BASIC FILTER
INVALID_WORDS = {
    "doctor", "patient", "clinic", "hospital",
    "mbbs", "consultant", "date"
}


# ---------------------------
# 🔧 JSON CLEANER
# ---------------------------
def clean_json_response(text: str):
    text = text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    match = re.search(r'\{.*\}', text, re.DOTALL)
    return match.group(0) if match else None


# ---------------------------
# 🤖 GEMINI EXTRACTION
# ---------------------------
def extract_medicines_with_gemini(text: str):
    try:
        prompt = f"""
You are a medical assistant.

Extract ONLY medicine-related information from this prescription.

Rules:
- Ignore doctor names, patient names, addresses
- Extract only real medicines
- Fix OCR errors if obvious (e.g. 'S mg' → '5 mg')

Return STRICT JSON ONLY:

{{
  "medicines": [
    {{
      "name": "...",
      "dosage": "...",
      "timing": "..."
    }}
  ]
}}

Prescription:
{text}
"""

        response = model.generate_content(prompt)
        raw = response.text

        cleaned = clean_json_response(raw)
        if not cleaned:
            return {"medicines": []}

        data = json.loads(cleaned)

        # 🔥 FILTER
        filtered = []
        for med in data.get("medicines", []):
            name = med.get("name", "").lower()

            if name and name not in INVALID_WORDS:
                filtered.append({
                    "medicine": name.capitalize(),
                    "dosage": med.get("dosage"),
                    "timing": med.get("timing")
                })

        return {"medicines": filtered}

    except Exception as e:
        print("Gemini extraction error:", e)
        return {"medicines": []}


# ---------------------------
# 🤖 GEMINI RAG FALLBACK
# ---------------------------
def ask_gemini_about_medicine(medicine: str) -> str:
    try:
        prompt = f"""
Give a short medical explanation for the medicine: {medicine}

Format:
💊 Use:
📌 Note:
⚠️ Side Effects:

Keep it concise (3-4 lines).
"""

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception:
        return f"{medicine} is a commonly prescribed medication."