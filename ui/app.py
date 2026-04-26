import streamlit as st
import requests

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="RxCare – AI Prescription Reader",
    page_icon="💊",
    layout="wide"
)

BACKEND_URL = "http://127.0.0.1:8000/prescriptions/upload"

# ---------------- STYLES ----------------
st.markdown("""
<style>

/* HEADER */
.title {
    font-size: 42px;
    font-weight: 700;
    color: #2E86C1;
    margin-bottom: 0;
}

.subtitle {
    font-size: 18px;
    color: #555;
    margin-bottom: 10px;
}

/* CARD */
.card {
    background-color: #f9fafb;
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border-left: 6px solid #2E86C1;
    color: #111;
}

/* MEDICINE */
.medicine {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 6px;
}

/* OCR BOX */
.ocr-box {
    background-color: #0f172a;
    color: #22c55e;
    padding: 14px;
    border-radius: 10px;
    font-family: monospace;
    font-size: 14px;
    overflow-x: auto;
}

/* BADGE */
.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    background: #e3f2fd;
    color: #1e88e5;
    margin-bottom: 6px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">💊 RxCare</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered Prescription Reader</div>', unsafe_allow_html=True)
st.divider()

# ---------------- INFO NOTE ----------------
st.info("⚠️ Handles noisy handwritten prescriptions (e.g., 'S mg' → '5 mg') using OCR normalization.")

# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader(
    "📤 Upload Prescription Image",
    type=["png", "jpg", "jpeg"]
)

# ---------------- PROCESS ----------------
if uploaded_file:

    st.success("📤 Prescription uploaded successfully")
    st.caption("🔒 Uploaded prescriptions are processed securely and not displayed.")

    if st.button("🔍 Analyze Prescription"):

        with st.spinner("Analyzing prescription... ⏳"):
            files = {"file": uploaded_file.getvalue()}

            try:
                response = requests.post(BACKEND_URL, files=files)
                data = response.json()
            except Exception as e:
                st.error(f"Backend error: {e}")
                st.stop()

        st.success("✅ Analysis Complete!")

        # ---------------- CONFIDENCE ----------------
        st.metric(
            "📊 OCR Confidence",
            f"{data.get('confidence', 0)}%",
            help="Confidence of extracted text quality"
        )

        st.warning("⚠️ This is an AI-assisted interpretation. Always verify with a doctor.")

        # ---------------- RAW OCR TEXT ----------------
        st.subheader("🧾 Raw OCR Output")
        st.markdown(
            f"<div class='ocr-box'>{data.get('raw_text', '')}</div>",
            unsafe_allow_html=True
        )

        st.divider()

        # ---------------- MEDICINES ----------------
        st.subheader("💊 Extracted Medicines")

        medicines = data.get("structured_data", {}).get("medicines", [])

        if medicines:
            cols = st.columns(2)

            for idx, med in enumerate(medicines):
                with cols[idx % 2]:
                    st.markdown(f"""
                        <div class="card">
                            <div class="badge">Medicine</div>
                            <div class="medicine">💊 {med.get("medicine", "")}</div>
                            <div>💉 Dosage: <b>{med.get("dosage", "N/A")}</b></div>
                            <div>⏰ Timing: <b>{med.get("timing", "N/A")}</b></div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No medicines detected.")

        # ---------------- EXPLANATIONS ----------------
        st.subheader("📘 Medicine Information")

        explanations = data.get("rag_explanations", {})

        if explanations:
            for med, exp in explanations.items():
                st.markdown(f"""
                    <div class="card">
                        <div class="badge">Info</div>
                        <div class="medicine">📘 {med}</div>
                        <div>{exp}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No explanations available.")
            st.info("⚠️ Results may vary for extremely handwritten or unclear prescriptions.")

        # ---------------- AI UNDERSTANDING ----------------
        st.subheader("🧠 AI Understanding")

        st.markdown("""
        <div class="card">
        ✔ OCR noise corrected automatically (e.g., 'S mg' → '5 mg')<br>
        ✔ Medicines identified using pattern recognition + fuzzy matching<br>
        ✔ Dosage inferred even when units are missing<br>
        ✔ Context-based timing extraction (e.g., 'night' → 'at night')<br>
        </div>
        """, unsafe_allow_html=True)