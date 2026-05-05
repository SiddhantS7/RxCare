import { useState } from "react";
import "./App.css";

export default function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Upload a prescription");

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setData(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/prescriptions/upload", {
        method: "POST",
        body: formData,
      });

      const result = await res.json();
      setData(result);
    } catch {
      alert("Backend error");
    }

    setLoading(false);
  };

  return (
    <div className="app">

      {/* HEADER */}
      <div className="header">
        <h1>💊 RxCare</h1>
        <p>AI-powered Prescription Intelligence</p>
      </div>

      {/* UPLOAD */}
      <div className="upload-card">
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload}>
          {loading ? "Analyzing..." : "Analyze Prescription"}
        </button>
      </div>

      {/* RESULTS */}
      {data && (
        <div className="results">

          {/* STEP 1 */}
          <div className="ai-block">
            <h2>🧠 Step 1: OCR Extraction</h2>
            <p className="confidence">Confidence: {data.confidence}%</p>

            <div className="raw-box">
              {data.raw_text}
            </div>
          </div>

          {/* STEP 2 */}
          <div className="ai-block">
            <h2>⚙️ Step 2: AI Parsing</h2>

            {data.structured_data?.medicines?.length > 0 ? (
              data.structured_data.medicines.map((med, i) => (
                <div key={i} className="medicine-card">
                  <h3>{med.medicine}</h3>

                  <div className="meta">
                    <span>💉 {med.dosage || "N/A"}</span>
                    <span>⏰ {med.timing || "N/A"}</span>
                  </div>
                </div>
              ))
            ) : (
              <p>No medicines detected</p>
            )}
          </div>

          {/* STEP 3 */}
          <div className="ai-block">
            <h2>📘 Step 3: Medical Intelligence</h2>

            {data.rag_explanations &&
            Object.keys(data.rag_explanations).length > 0 ? (
              Object.entries(data.rag_explanations).map(([med, info]) => (
                <div key={med} className="medicine-card">
                  <h3>{med}</h3>
                  <p>{info}</p>
                </div>
              ))
            ) : (
              <p>No insights available</p>
            )}
          </div>

        </div>
      )}
    </div>
  );
}