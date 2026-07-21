"use client";

import { useState } from "react";
import { getExample, review } from "../lib/api";
import type { Finding, ReviewResult } from "../lib/types";

function FindingCard({ f }: { f: Finding }) {
  return (
    <div className={`finding ${f.severity}`}>
      <div>
        <span className={`sev ${f.severity}`}>{f.severity.toUpperCase()}</span>
        <span className="ct">{f.clause_type}</span>
      </div>
      <div style={{ marginTop: 4 }}>{f.concern}</div>
      <div className="fix">→ {f.recommendation}</div>
      <div className="quote">“{f.quote}”</div>
    </div>
  );
}

export default function Home() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<ReviewResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function run() {
    if (!text.trim()) return;
    setLoading(true); setError(null); setResult(null);
    try { setResult(await review(text)); }
    catch (e) { setError(e instanceof Error ? e.message : "Something went wrong."); }
    finally { setLoading(false); }
  }

  async function loadExample() {
    try { const { contract } = await getExample(); setText(contract); setResult(null); } catch {}
  }

  const r = result?.review;

  return (
    <div className="container">
      <header>
        <h1>contract-lens</h1>
        <p>Paste a contract or terms-of-service. It flags the clauses worth attention — each with a verbatim quote.</p>
      </header>

      <div className="banner">⚠️ Educational tool, <strong>not legal advice</strong>. It highlights clauses to look at; it doesn&rsquo;t interpret them for your situation.</div>

      <label htmlFor="c">Contract / terms text</label>
      <textarea id="c" value={text} placeholder="Paste the agreement here…" onChange={(e) => setText(e.target.value)} />
      <div className="actions">
        <button onClick={run} disabled={loading}>{loading ? "Reviewing…" : "Review"}</button>
        <button className="ghost" onClick={loadExample} disabled={loading}>Load example</button>
      </div>

      {error && <div className="error">{error}</div>}

      {r && (
        <div className="panel">
          <div><span className={`risk ${r.overall_risk}`}>{r.overall_risk.toUpperCase()} RISK</span></div>
          <p style={{ margin: "10px 0" }}>{r.summary}</p>
          {r.findings.length === 0 ? (
            <p style={{ color: "var(--good)" }}>No notable clauses flagged.</p>
          ) : (
            r.findings.map((f, i) => <FindingCard f={f} key={i} />)
          )}
          <p className="disc">{result!.disclaimer}</p>
        </div>
      )}
    </div>
  );
}
