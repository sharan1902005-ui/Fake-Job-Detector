import { useState } from "react";

export default function JobInput({ onAnalyze, loading }) {
  const [text, setText] = useState("");

  return (
    <div className="mt-8">
      <textarea
        className="w-full h-72 p-4 rounded-xl bg-slate-900 border border-slate-700"
        placeholder="Paste job posting..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <div style={{ marginTop: "10px" }}>
        <button
          onClick={() =>
            setText(
              "Earn money from home immediately. No experience needed. Unlimited income. Apply now."
            )
          }
        >
          Scam Example
        </button>

        <button
          onClick={() =>
            setText(
              "Software Engineer. Work with our development team to build scalable web applications using React and Python."
            )
          }
          style={{ marginLeft: "10px" }}
        >
          Legit Example
        </button>
      </div>

      <button
        onClick={() => onAnalyze(text)}
        className="mt-4 bg-blue-600 px-6 py-3 rounded-xl hover:bg-blue-700"
      >
        {loading ? "Analyzing..." : "Analyze Job"}
      </button>
    </div>
  );
}
