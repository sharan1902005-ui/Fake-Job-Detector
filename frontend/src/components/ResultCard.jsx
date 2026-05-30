import FraudMeter from "./FraudMeter";
 
export default function ResultCard({ result }) {
  const isFake = result.prediction === "Fake";
  const cls = isFake ? "fake" : "legit";
  const icon = isFake ? "🚨" : "✅";
  const verdict = isFake ? "FAKE JOB DETECTED" : "LEGITIMATE JOB";
  const rec = isFake
    ? "Do not apply before verifying the company and recruiter identity through official channels."
    : "This posting appears legitimate, but always verify independently before sharing personal data.";
 
  return (
    <div className="result-card">
      <div className={`result-header ${cls}`}>
        <div className={`verdict-icon ${cls}`}>{icon}</div>
        <div>
          <div className={`verdict-label ${cls}`}>{verdict}</div>
          <div className="verdict-sub">
            Confidence: {(result.fraud_probability * 100).toFixed(1)}% fraud probability
          </div>
        </div>
      </div>
 
      <div className="result-body">
        <FraudMeter probability={result.fraud_probability} />
 
        <div className={`rec ${cls}`}>{rec}</div>
 
        {result.reasons?.length > 0 && (
          <div style={{ marginTop: "18px" }}>
            <div className="tags-title">Suspicious Signals</div>
            <div className="tags">
              {result.reasons.map((r) => (
                <span key={r} className="tag">{r}</span>
              ))}
            </div>
          </div>
        )}
 
        {result.preview && (
          <div style={{ marginTop: "16px" }}>
            <div className="tags-title">Extracted Preview</div>
            <div className="preview">{result.preview}</div>
          </div>
        )}
      </div>
    </div>
  );
}