import { useEffect, useRef, useState } from "react";
 
export default function FraudMeter({ probability }) {
  const pct = Number(probability || 0) * 100;
  const [width, setWidth] = useState(0);
 
  useEffect(() => {
    const t = setTimeout(() => setWidth(pct), 80);
    return () => clearTimeout(t);
  }, [pct]);
 
  const color =
    pct > 70 ? "#ef4444" : pct > 40 ? "#f59e0b" : "#22c55e";
 
  return (
    <div style={{ marginBottom: "18px" }}>
      <div className="meter-label">
        <span>FRAUD RISK</span>
        <span style={{ color }}>{pct.toFixed(1)}%</span>
      </div>
      <div className="meter-track">
        <div
          className="meter-fill"
          style={{ width: `${width}%`, background: color }}
        />
      </div>
    </div>
  );
}
