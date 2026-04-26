from fastapi import APIRouter, UploadFile, File
import shutil
from pathlib import Path

from backend.services.ocr_service import extract_text
from backend.services.nlp_service import extract_medicine_info
from backend.services.rag_service import explain_medicine

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])

UPLOAD_DIR = Path("data/uploads")


@router.post("/upload")
async def upload_prescription(file: UploadFile = File(...)):
    try:
        # ✅ Ensure folder exists
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        # ✅ Read file properly
        contents = await file.read()

        print("FILE RECEIVED:", file.filename)
        print("FILE SIZE:", len(contents))

        if len(contents) == 0:
            return {
                "error": "Empty file received",
                "confidence": 0,
                "raw_text": "",
                "structured_data": {"medicines": []}
            }

        # ✅ Save file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            f.write(contents)

        # ---------------------------
        # 🧠 OCR
        # ---------------------------
        ocr_result = extract_text(file_path)

        text = ocr_result.get("raw_text", "")
        print("OCR RAW:", text)

        # ---------------------------
        # 🧠 NLP
        # ---------------------------
        structured_data = extract_medicine_info(text)
        medicines = structured_data.get("medicines", [])

        print("DEBUG medicines:", medicines)

        # ---------------------------
        # 📘 RAG
        # ---------------------------
        explanations = {}

        for med in medicines:
            name = med.get("medicine")
            if name:
                explanations[name] = explain_medicine(name)

        return {
            "raw_text": text,
            "confidence": ocr_result.get("confidence", 0),
            "structured_data": structured_data,
            "alerts": [],
            "rag_explanations": explanations
        }

    except Exception as e:
        print("ERROR:", e)
        return {
            "error": str(e),
            "confidence": 0,
            "raw_text": "",
            "structured_data": {"medicines": []}
        }