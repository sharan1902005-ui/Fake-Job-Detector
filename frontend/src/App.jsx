import { useState } from "react";
import axios from "axios";
import IntroPage from "./components/IntroPage";
import ResultCard from "./components/ResultCard";

export default function App() {
  const [screen, setScreen] = useState("intro"); // "intro" | "app"
  const [mode, setMode] = useState("text");
  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const clearOut = () => { setResult(null); setError(""); };

  const analyzeText = async () => {
    if (!text.trim() || loading) return;
    clearOut(); setLoading(true);
    try {
      const { data } = await axios.post("http://127.0.0.1:8000/predict", { text });
      setResult(data);
    } catch { setError("Unable to connect to API. Make sure the FastAPI server is running on port 8000."); }
    setLoading(false);
  };

  const analyzeUrl = async () => {
    if (!url.trim() || loading) return;
    clearOut(); setLoading(true);
    try {
      const { data } = await axios.post("http://127.0.0.1:8000/predict-url", { url });
      setResult(data);
    } catch { setError("Unable to connect to API. Make sure the FastAPI server is running on port 8000."); }
    setLoading(false);
  };

  const fillExample = (type) => {
    const examples = {
      scam: "Earn $5000/week from home. No experience needed. Unlimited income potential. Work only 2 hours per day. Send your bank details to apply now.",
      legit: "Software Engineer — Join our team to build scalable web applications using React and FastAPI. Requirements: 3+ years experience, CS degree preferred. Competitive salary and remote-friendly.",
    };
    setText(examples[type]);
  };

  if (screen === "intro") {
    return <IntroPage onEnter={() => setScreen("app")} />;
  }

  return (
    <div className="app-page">
      <div className="grid-bg" />

      <div className="inner">
        <button className="back-btn" onClick={() => { setScreen("intro"); clearOut(); }}>
          ← Back to intro
        </button>

        <div className="app-header">
          <div className="app-badge">
            <div className="pulse-dot" /> Live Detection
          </div>
          <h1 className="app-title">Fake Job Detector</h1>
          <p className="app-sub">Paste a job posting or URL to analyze it instantly.</p>
        </div>

        <div className="stats">
          <div className="stat"><div className="stat-num">17,880</div><div className="stat-lbl">Jobs Analyzed</div></div>
          <div className="stat"><div className="stat-num">98.5%</div><div className="stat-lbl">ROC-AUC</div></div>
          <div className="stat"><div className="stat-num">90%</div><div className="stat-lbl">Fraud Recall</div></div>
        </div>

        <div className="tabs">
          <button className={`tab${mode === "text" ? " active" : ""}`} onClick={() => { setMode("text"); clearOut(); }}>Text Analysis</button>
          <button className={`tab${mode === "url" ? " active" : ""}`} onClick={() => { setMode("url"); clearOut(); }}>URL Analysis</button>
        </div>

        {mode === "text" && (
          <>
            <div className="examples">
              <button className="ex-btn" onClick={() => fillExample("scam")}>
                <span className="ex-icon">🚨</span>SCAM EXAMPLE
              </button>
              <button className="ex-btn" onClick={() => fillExample("legit")}>
                <span className="ex-icon">✅</span>LEGIT EXAMPLE
              </button>
            </div>
            <div className="input-wrap">
              <textarea
                className="textarea"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste job posting here..."
              />
              <span className="char-count">{text.length} chars</span>
            </div>
            <button
              className={`analyze-btn${loading ? " loading-state" : " ready"}`}
              onClick={analyzeText}
              disabled={loading}
            >
              {loading ? <><div className="loader" /> Analyzing...</> : "Analyze Job Posting"}
            </button>
          </>
        )}

        {mode === "url" && (
          <>
            <div className="input-wrap">
              <input
                className="urlinput"
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://linkedin.com/jobs/view/..."
              />
            </div>
            <button
              className={`analyze-btn${loading ? " loading-state" : " ready"}`}
              onClick={analyzeUrl}
              disabled={loading}
            >
              {loading ? <><div className="loader" /> Analyzing...</> : "Analyze URL"}
            </button>
          </>
        )}

        {error && <div className="error-msg">⚠ {error}</div>}
        {result?.prediction && <ResultCard result={result} />}

        <div className="footer">
          Built by Sharan<span>·</span>Machine Learning<span>·</span>FastAPI<span>·</span>React<span>·</span>SHAP
        </div>
      </div>
    </div>
  );
}
