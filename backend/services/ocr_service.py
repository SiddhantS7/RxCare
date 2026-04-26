import pytesseract
import cv2
import easyocr

# Mac path
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# initialize once
reader = easyocr.Reader(['en'], gpu=False)


def extract_text(image_path):
    try:
        image = cv2.imread(str(image_path))

        if image is None:
            return {"raw_text": "", "confidence": 0}

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # ---------------------------
        # 🔥 TESSERACT (PRIMARY)
        # ---------------------------
        tess_text = pytesseract.image_to_string(
            gray,
            config="--oem 3 --psm 6"
        )

        # ---------------------------
        # 🔥 DECIDE IF FALLBACK NEEDED
        # ---------------------------
        def is_bad(text):
            if not text or len(text.strip()) < 30:
                return True

            # too many weird chars
            bad_ratio = sum(
                1 for c in text if not (c.isalnum() or c.isspace())
            ) / len(text)

            return bad_ratio > 0.25

        use_easy = is_bad(tess_text)

        # ---------------------------
        # 🔥 EASYOCR (FALLBACK ONLY)
        # ---------------------------
        if use_easy:
            easy_result = reader.readtext(image)
            easy_text = " ".join([res[1] for res in easy_result])

            # choose better one
            if len(easy_text.strip()) > len(tess_text.strip()):
                final_text = easy_text
            else:
                final_text = tess_text
        else:
            final_text = tess_text

        print("\n--- FINAL OCR ---\n", final_text)

        confidence = 80 if final_text.strip() else 0

        return {
            "raw_text": final_text.strip(),
            "confidence": confidence
        }

    except Exception as e:
        print("OCR ERROR:", e)
        return {
            "raw_text": "",
            "confidence": 0
        }