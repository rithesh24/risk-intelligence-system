"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import Link from "next/link";
import { analyzeCompany, AnalysisResult, getRiskLevel } from "@/lib/api";
import AgentCard from "@/components/AgentCard";
import RiskGauge from "@/components/RiskGauge";

const AgentChart = dynamic(() => import("@/components/AgentChart"), { ssr: false });

const COMPONENT_INFO: Record<string, { title: string; what: string }> = {
  gauge: {
    title: "Overall Risk Score",
    what: "A composite score from 0–100 combining all agent signals. Higher means greater business risk exposure.",
  },
  risk_score: {
    title: "Risk Score",
    what: "The raw numerical risk value (0–1) aggregated across currency, commodity, demand, policy, and narrative agents.",
  },
  confidence: {
    title: "Confidence",
    what: "How certain the system is about the risk assessment. Low confidence means limited data signals were detected.",
  },
  explanation: {
    title: "AI Explanation",
    what: "A human-readable summary of the primary drivers behind the computed risk level.",
  },
  agent_chart: {
    title: "Agent Risk Contributions",
    what: "Each bar represents one specialized agent's risk score. Longer bars indicate that agent detected higher risk in its domain.",
  },
  recommendations: {
    title: "Recommended Actions",
    what: "Actionable steps to reduce or mitigate the identified risks. Prioritize items marked against high-scoring agents.",
  },
  agent_detail: {
    title: "Agent Detail View",
    what: "Drill down into each agent's individual reasoning, risk score, and confidence. Click any card to expand.",
  },
};

const RISK_PRECAUTIONS: Record<string, { summary: string; actions: string[] }> = {
  Low: {
    summary: "Your business has low overall risk exposure. Continue monitoring key signals.",
    actions: [
      "Maintain quarterly risk reviews",
      "Keep hedging strategies in place for any FX exposure",
      "Monitor supply chain for early disruption signals",
    ],
  },
  Moderate: {
    summary: "Moderate risk detected. Some signals warrant proactive attention.",
    actions: [
      "Review currency hedging — consider forward contracts",
      "Diversify supplier base to reduce single-region dependency",
      "Track regulatory developments in your key markets",
      "Build 2–3 month buffer stock for critical inputs",
    ],
  },
  "Moderate-High": {
    summary: "Elevated risk across multiple dimensions. Immediate review recommended.",
    actions: [
      "Hedge at least 60–70% of FX exposure via forwards or options",
      "Activate alternative supplier protocols",
      "Engage legal/compliance team on regulatory changes",
      "Review pricing strategy to protect margins under cost pressure",
      "Stress-test cash flow under adverse scenarios",
    ],
  },
  High: {
    summary: "High risk exposure detected. Executive-level review and action required.",
    actions: [
      "Convene risk committee — escalate to board if needed",
      "Immediately hedge all major FX and commodity exposures",
      "Evaluate market exit or pause strategy for highest-risk regions",
      "Secure credit lines proactively before liquidity tightens",
      "Engage external risk advisory for independent assessment",
      "Review and update business continuity plan",
    ],
  },
};

function InfoTooltip({ id }: { id: string }) {
  const [visible, setVisible] = useState(false);
  const info = COMPONENT_INFO[id];
  if (!info) return null;
  return (
    <div className="relative inline-block ml-2">
      <button
        onMouseEnter={() => setVisible(true)}
        onMouseLeave={() => setVisible(false)}
        className="w-4 h-4 rounded-full border border-slate-600 text-slate-500 hover:border-accent hover:text-accent transition-colors font-mono text-xs flex items-center justify-center"
      >
        ?
      </button>
      {visible && (
        <div className="absolute z-50 left-6 top-0 w-64 bg-surface border border-border rounded-lg p-3 shadow-xl animate-fade-in">
          <p className="font-mono text-xs text-accent mb-1">{info.title}</p>
          <p className="text-xs text-slate-400 leading-relaxed">{info.what}</p>
        </div>
      )}
    </div>
  );
}

function SectionLabel({ text, tooltipId }: { text: string; tooltipId: string }) {
  return (
    <div className="flex items-center mb-3">
      <span className="label">{text}</span>
      <InfoTooltip id={tooltipId} />
    </div>
  );
}

export default function DashboardPage() {
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!description.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await analyzeCompany(description.trim());
      setResult(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to connect to backend.");
    } finally {
      setLoading(false);
    }
  };

  const risk = result ? getRiskLevel(result.risk_score) : null;
  const precautions = risk ? RISK_PRECAUTIONS[risk.label] : null;

  return (
    <div className="relative z-10 min-h-screen">
      <header className="border-b border-border bg-surface/60 backdrop-blur-sm sticky top-0 z-20">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-7 h-7 rounded border border-accent/40 flex items-center justify-center">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <path d="M7 1L13 4V10L7 13L1 10V4L7 1Z" stroke="#00d4ff" strokeWidth="1.2" fill="none" />
                <circle cx="7" cy="7" r="2" fill="#00d4ff" opacity="0.7" />
              </svg>
            </div>
            <div>
              <h1 className="font-mono text-sm font-semibold text-white tracking-wide">RISK INTELLIGENCE</h1>
              <p className="font-mono text-xs text-slate-500 tracking-widest">MULTI-AGENT SYSTEM</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/monitor" className="font-mono text-xs text-slate-500 hover:text-orange-400 transition-colors border border-border hover:border-orange-500/40 px-3 py-1.5 rounded-lg">
              ⬡ Agent Monitor →
            </Link>
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-low animate-pulse-slow" />
              <span className="font-mono text-xs text-slate-500">LIVE</span>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8 space-y-6">
        <div className="animate-fade-in">
          <p className="text-slate-400 text-sm max-w-2xl leading-relaxed">
            AI system that monitors economic signals — currency volatility, commodity prices, demand shifts, policy changes, and narrative sentiment — to evaluate business risk exposure.
          </p>
        </div>

        {/* Input */}
        <div className="card animate-slide-up">
          <label className="label block mb-1">Describe Your Organisation</label>
          <p className="text-xs text-slate-500 mb-3 leading-relaxed">
            Include your industry, key import &amp; export markets, supply chain dependencies, currencies used, major commodities, and any known regulatory exposure. The more detail you provide, the more accurate the risk assessment.
          </p>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder={`e.g. "We are a mid-sized pharmaceutical manufacturer based in India. We import active pharmaceutical ingredients (APIs) from China and export finished medicines to the US, EU, and Middle East. Our revenue is primarily in USD and EUR. We depend on chemical inputs and are subject to FDA and EMA compliance. We have significant INR/USD FX exposure and rising logistics costs."`}
            rows={5}
            className="w-full bg-bg border border-border rounded-lg px-4 py-3 text-sm text-slate-200 font-sans placeholder:text-slate-600 focus:outline-none focus:border-accent transition-colors resize-none leading-relaxed"
          />
          <div className="flex items-center justify-end mt-3">
            <button
              onClick={handleAnalyze}
              disabled={loading || !description.trim()}
              className="flex items-center gap-2 bg-accent text-bg px-5 py-2 rounded-lg font-mono text-xs font-semibold tracking-wider hover:bg-accent-dim transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed active:scale-95"
            >
              {loading ? (
                <><span className="w-3 h-3 border border-bg/60 border-t-transparent rounded-full animate-spin" />ANALYZING…</>
              ) : <>▶ ANALYZE RISK</>}
            </button>
          </div>
        </div>

        {error && (
          <div className="card border-high/40 animate-fade-in">
            <p className="font-mono text-xs text-high">{error}</p>
          </div>
        )}

        {result && risk && (
          <>
            {/* Risk Summary Banner */}
            <div className="rounded-xl border px-5 py-4 animate-fade-in" style={{ borderColor: risk.color + "44", backgroundColor: risk.color + "0d" }}>
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="font-mono text-xs tracking-widest mb-1" style={{ color: risk.color }}>RISK ASSESSMENT SUMMARY</p>
                  <p className="text-white text-sm leading-relaxed max-w-2xl">{precautions?.summary}</p>
                </div>
                <span className="font-mono text-xs px-3 py-1.5 rounded-full border flex-shrink-0" style={{ color: risk.color, borderColor: risk.color + "60", backgroundColor: risk.color + "18" }}>
                  {risk.label.toUpperCase()}
                </span>
              </div>
            </div>

            {/* Gauge + Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 animate-slide-up">
              <div className="card flex flex-col items-center justify-center md:col-span-1">
                <SectionLabel text="Overall Risk Score" tooltipId="gauge" />
                <RiskGauge score={result.risk_score} />
              </div>
              <div className="md:col-span-2 grid grid-cols-2 gap-4">
                <div className="card flex flex-col justify-between">
                  <SectionLabel text="Risk Score" tooltipId="risk_score" />
                  <div>
                    <p className="value-lg" style={{ color: risk.color }}>{(result.risk_score * 100).toFixed(0)}<span className="text-lg text-slate-500">%</span></p>
                    <p className="font-mono text-xs mt-1" style={{ color: risk.color }}>{risk.label}</p>
                  </div>
                </div>
                <div className="card flex flex-col justify-between">
                  <SectionLabel text="Confidence" tooltipId="confidence" />
                  <div>
                    <p className="value-lg text-accent">{(result.confidence * 100).toFixed(0)}<span className="text-lg text-slate-500">%</span></p>
                    <div className="w-full h-1 bg-border rounded-full mt-2 overflow-hidden">
                      <div className="h-full bg-accent rounded-full transition-all duration-1000" style={{ width: `${result.confidence * 100}%` }} />
                    </div>
                  </div>
                </div>
                <div className="card col-span-2">
                  <SectionLabel text="AI Explanation" tooltipId="explanation" />
                  <p className="text-slate-300 text-sm leading-relaxed">{result.explanation}</p>
                </div>
              </div>
            </div>

            {/* Agent Chart */}
            {Object.keys(result.agent_outputs).length > 0 && (
              <div className="card animate-slide-up">
                <SectionLabel text="Agent Risk Contributions" tooltipId="agent_chart" />
                <AgentChart agentOutputs={result.agent_outputs} />
              </div>
            )}

            {/* Precautions */}
            {precautions && (
              <div className="card animate-slide-up border-slate-700">
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-base">🛡</span>
                  <span className="label">Precautions &amp; Mitigation Actions</span>
                  <span className="font-mono text-xs px-2 py-0.5 rounded-full border ml-1" style={{ color: risk.color, borderColor: risk.color + "44", backgroundColor: risk.color + "11" }}>
                    {risk.label}
                  </span>
                </div>
                <div className="space-y-2">
                  {precautions.actions.map((action, i) => (
                    <div key={i} className="flex items-start gap-3" style={{ animation: `slideUp 0.3s ease ${i * 50}ms forwards`, opacity: 0 }}>
                      <span className="font-mono text-xs text-slate-600 mt-0.5 flex-shrink-0 w-5">{String(i + 1).padStart(2, "0")}</span>
                      <span className="w-1.5 h-1.5 rounded-full flex-shrink-0 mt-1.5" style={{ backgroundColor: risk.color }} />
                      <p className="text-sm text-slate-300 leading-relaxed">{action}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Recommendations */}
            {result.recommendations.length > 0 && (
              <div className="card animate-slide-up">
                <SectionLabel text="Recommended Actions" tooltipId="recommendations" />
                <ul className="space-y-2">
                  {result.recommendations.map((rec, i) => (
                    <li key={i} className="flex items-start gap-3 text-sm text-slate-300" style={{ animation: `slideUp 0.35s ease ${i * 60}ms forwards`, opacity: 0 }}>
                      <span className="text-accent font-mono mt-0.5 flex-shrink-0">{String(i + 1).padStart(2, "0")}</span>
                      {rec}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Agent Detail */}
            {Object.keys(result.agent_outputs).length > 0 && (
              <div className="animate-slide-up">
                <SectionLabel text="Agent Detail View" tooltipId="agent_detail" />
                <div className="space-y-2">
                  {Object.entries(result.agent_outputs).map(([key, output], i) => (
                    <AgentCard key={key} agentKey={key} output={output} index={i} />
                  ))}
                </div>
              </div>
            )}
          </>
        )}

        {!result && !loading && !error && (
          <div className="text-center py-20 animate-fade-in">
            <div className="inline-flex flex-col items-center gap-3">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none" className="opacity-20">
                <path d="M24 4L44 14V34L24 44L4 34V14L24 4Z" stroke="#00d4ff" strokeWidth="1.5" />
                <path d="M24 14V24M24 24L30 30" stroke="#00d4ff" strokeWidth="1.5" strokeLinecap="round" />
                <circle cx="24" cy="24" r="3" fill="#00d4ff" opacity="0.5" />
              </svg>
              <p className="font-mono text-xs text-slate-600 tracking-widest">DESCRIBE YOUR ORGANISATION TO BEGIN ANALYSIS</p>
              <p className="font-mono text-xs text-slate-700 max-w-sm text-center leading-relaxed">Include industry, markets, supply chain, currencies, and dependencies for the most accurate assessment.</p>
            </div>
          </div>
        )}
      </main>

      <footer className="border-t border-border mt-12 py-4">
        <p className="text-center font-mono text-xs text-slate-700">RISK INTELLIGENCE SYSTEM · MULTI-AGENT · {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}