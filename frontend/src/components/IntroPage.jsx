export default function IntroPage({ onEnter }) {
  return (
    <div className="intro-page">
      <div className="glow-ring">
        <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
          <path
            d="M32 6L8 16v18c0 13 10.5 22 24 24 13.5-2 24-11 24-24V16L32 6z"
            fill="rgba(59,130,246,0.15)"
            stroke="#3b82f6"
            strokeWidth="1.5"
            strokeLinejoin="round"
          />
          <path
            d="M23 32l6 6 12-12"
            stroke="#60a5fa"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>

      <div className="intro-badge">
        <div className="pulse-dot" />
        ML-Powered · Explainable AI
      </div>

      <h1 className="intro-title">Fake Job Detector</h1>

      <p className="intro-sub">
        Protect yourself from fraudulent job postings. Our ML model analyzes
        job descriptions in seconds — with full explainability.
      </p>

      <div className="features">
        <div className="feat"><div className="feat-dot blue" />FastAPI Backend</div>
        <div className="feat"><div className="feat-dot green" />98.5% ROC-AUC</div>
        <div className="feat"><div className="feat-dot amber" />SHAP Explainability</div>
        <div className="feat"><div className="feat-dot purple" />URL + Text Analysis</div>
      </div>

      <div className="cta-row">
        <button className="btn-primary" onClick={onEnter}>
          Get Started <span className="arrow-anim">→</span>
        </button>
        <button className="btn-secondary" onClick={onEnter}>
          Continue to App
        </button>
      </div>
    </div>
  );
}
