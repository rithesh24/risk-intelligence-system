"use client";

import { useState, useCallback } from "react";
import dynamic from "next/dynamic";
import Link from "next/link";
import { fetchAgentLogs, AgentLog, getRiskLevel, formatAgentName } from "@/lib/api";
import AgentOutputPanel from "@/components/monitor/AgentOutputPanel";
import ConflictDetector from "@/components/monitor/ConflictDetector";
import ExecutionGraph from "@/components/monitor/ExecutionGraph";

const RiskRadarChart = dynamic(() => import("@/components/monitor/RiskRadarChart"), { ssr: false });

export default function MonitorPage() {
  const [logs, setLogs] = useState<AgentLog[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fetched, setFetched] = useState(false);
  const [lastRefresh, setLastRefresh] = useState<Date | null>(null);

  const loadLogs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchAgentLogs();
      setLogs(data);
      setFetched(true);
      setLastRefresh(new Date());
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to connect to backend at http://127.0.0.1:8000");
    } finally {
      setLoading(false);
    }
  }, []);

  const avgRisk = logs.length > 0 ? logs.reduce((s, l) => s + l.risk_score, 0) / logs.length : null;
  const avgConf = logs.length > 0 ? logs.reduce((s, l) => s + l.confidence, 0) / logs.length : null;
  const highestRisk = logs.length > 0 ? logs.reduce((a, b) => (a.risk_score > b.risk_score ? a : b)) : null;
  const lowestConf = logs.length > 0 ? logs.reduce((a, b) => (a.confidence < b.confidence ? a : b)) : null;

  return (
    <div className="relative z-10 min-h-screen">
      {/* Header */}
      <header className="border-b border-border bg-surface/60 backdrop-blur-sm sticky top-0 z-20">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-7 h-7 rounded border border-orange-500/40 flex items-center justify-center">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <rect x="2" y="2" width="4" height="4" stroke="#f97316" strokeWidth="1.2" fill="none" />
                <rect x="8" y="2" width="4" height="4" stroke="#f97316" strokeWidth="1.2" fill="none" />
                <rect x="2" y="8" width="4" height="4" stroke="#f97316" strokeWidth="1.2" fill="none" />
                <rect x="8" y="8" width="4" height="4" stroke="#f97316" strokeWidth="1.2" fill="none" opacity="0.4" />
                <line x1="4" y1="6" x2="4" y2="8" stroke="#f97316" strokeWidth="1.2" />
                <line x1="10" y1="6" x2="10" y2="8" stroke="#f97316" strokeWidth="1.2" />
                <line x1="6" y1="4" x2="8" y2="4" stroke="#f97316" strokeWidth="1.2" />
              </svg>
            </div>
            <div>
              <h1 className="font-mono text-sm font-semibold text-white tracking-wide">AGENT MONITOR</h1>
              <p className="font-mono text-xs text-slate-500 tracking-widest">DEVELOPER VIEW</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/" className="font-mono text-xs text-slate-500 hover:text-accent transition-colors">
              ← Business Dashboard
            </Link>
            <button
              onClick={loadLogs}
              disabled={loading}
              className="flex items-center gap-2 border border-orange-500/40 text-orange-400 px-4 py-1.5 rounded-lg font-mono text-xs hover:bg-orange-500/10 transition-all duration-200 disabled:opacity-40"
            >
              {loading ? (
                <><span className="w-3 h-3 border border-orange-400/60 border-t-transparent rounded-full animate-spin" />FETCHING…</>
              ) : <>↻ {fetched ? "REFRESH" : "FETCH LOGS"}</>}
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8 space-y-6">
        {/* Tagline */}
        <div className="animate-fade-in flex items-center justify-between">
          <p className="text-slate-400 text-sm max-w-2xl leading-relaxed">
            Internal view of the multi-agent pipeline — visualizes agent execution flow, risk computations, and inter-agent conflicts.
          </p>
          {lastRefresh && (
            <span className="font-mono text-xs text-slate-600 flex-shrink-0">
              Last refresh: {lastRefresh.toLocaleTimeString()}
            </span>
          )}
        </div>

        {/* Empty state */}
        {!fetched && !loading && !error && (
          <div className="text-center py-24 animate-fade-in">
            <div className="inline-flex flex-col items-center gap-4">
              <svg width="52" height="52" viewBox="0 0 52 52" fill="none" className="opacity-20">
                <rect x="4" y="4" width="20" height="20" stroke="#f97316" strokeWidth="1.5" rx="2" />
                <rect x="28" y="4" width="20" height="20" stroke="#f97316" strokeWidth="1.5" rx="2" />
                <rect x="4" y="28" width="20" height="20" stroke="#f97316" strokeWidth="1.5" rx="2" />
                <rect x="28" y="28" width="20" height="20" stroke="#f97316" strokeWidth="1.5" rx="2" opacity="0.4" />
                <line x1="14" y1="24" x2="14" y2="28" stroke="#f97316" strokeWidth="1.5" />
                <line x1="38" y1="24" x2="38" y2="28" stroke="#f97316" strokeWidth="1.5" />
                <line x1="24" y1="14" x2="28" y2="14" stroke="#f97316" strokeWidth="1.5" />
              </svg>
              <p className="font-mono text-xs text-slate-600 tracking-widest">CLICK FETCH LOGS TO LOAD AGENT EXECUTION DATA</p>
              <p className="font-mono text-xs text-slate-700">Run an analysis first from the Business Dashboard</p>
              <button onClick={loadLogs} className="mt-2 border border-orange-500/30 text-orange-400 px-5 py-2 rounded-lg font-mono text-xs hover:bg-orange-500/10 transition-all">
                ↻ FETCH LOGS
              </button>
            </div>
          </div>
        )}

        {error && (
          <div className="card border-high/40 animate-fade-in">
            <p className="font-mono text-xs text-high">{error}</p>
          </div>
        )}

        {fetched && logs.length === 0 && !loading && (
          <div className="text-center py-16 animate-fade-in">
            <p className="font-mono text-xs text-slate-600">
              No agent logs found. Run an analysis first from the{" "}
              <Link href="/" className="text-accent hover:underline">Business Dashboard</Link>.
            </p>
          </div>
        )}

        {fetched && logs.length > 0 && (
          <>
            {/* Stat cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 animate-slide-up">
              <div className="card">
                <p className="label">Agents Run</p>
                <p className="value-lg text-white mt-1">{logs.length}</p>
              </div>
              <div className="card">
                <p className="label">Avg Risk Score</p>
                {avgRisk !== null && (
                  <>
                    <p className="value-lg mt-1" style={{ color: getRiskLevel(avgRisk).color }}>
                      {(avgRisk * 100).toFixed(0)}<span className="text-lg text-slate-500">%</span>
                    </p>
                    <p className="font-mono text-xs mt-0.5" style={{ color: getRiskLevel(avgRisk).color }}>
                      {getRiskLevel(avgRisk).label}
                    </p>
                  </>
                )}
              </div>
              <div className="card">
                <p className="label">Avg Confidence</p>
                {avgConf !== null && (
                  <p className="value-lg text-accent mt-1">
                    {(avgConf * 100).toFixed(0)}<span className="text-lg text-slate-500">%</span>
                  </p>
                )}
              </div>
              <div className="card">
                <p className="label">Highest Risk Agent</p>
                {highestRisk && (
                  <>
                    <p className="font-mono text-sm font-semibold text-white mt-1">{formatAgentName(highestRisk.agent)}</p>
                    <p className="font-mono text-xs mt-0.5" style={{ color: getRiskLevel(highestRisk.risk_score).color }}>
                      {(highestRisk.risk_score * 100).toFixed(0)}%
                    </p>
                  </>
                )}
              </div>
            </div>

            {/* ── Execution Graph (n8n-style) ──────────────── */}
            <div className="card animate-slide-up">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <p className="label">Agent Execution Flow</p>
                  <p className="font-mono text-xs text-slate-600 mt-0.5">
                    Shows how agents are connected and the order of execution
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-low" />
                  <span className="font-mono text-xs text-slate-500">{logs.length} agents executed</span>
                </div>
              </div>
              <ExecutionGraph logs={logs} />
            </div>

            {/* ── Radar chart ─────────────────────────────── */}
            <div className="card animate-slide-up">
              <p className="label mb-1">Risk vs Confidence Radar</p>
              <p className="font-mono text-xs text-slate-600 mb-4">
                Visualizes each agent&apos;s risk score and confidence across all dimensions simultaneously
              </p>
              <RiskRadarChart logs={logs} />
            </div>

            {/* ── Conflict Detection Panel ─────────────────── */}
            <div className="animate-slide-up">
              <p className="label mb-1">Agent Conflict Analysis</p>
              <p className="font-mono text-xs text-slate-600 mb-3">
                Flags agents with diverging risk assessments — disagreements ≥ 25% signal conflicting data or model uncertainty
              </p>
              <ConflictDetector logs={logs} />
            </div>

            {/* ── Low confidence warning ───────────────────── */}
            {lowestConf && lowestConf.confidence < 0.5 && (
              <div className="card border-yellow-500/20 animate-slide-up">
                <div className="flex items-start gap-3">
                  <span className="text-yellow-400 text-base flex-shrink-0">⚠</span>
                  <div>
                    <p className="font-mono text-xs text-yellow-400 mb-1">LOW CONFIDENCE DETECTED</p>
                    <p className="text-sm text-slate-400">
                      <span className="text-white">{formatAgentName(lowestConf.agent)} Agent</span> reported confidence of{" "}
                      <span className="text-yellow-400">{(lowestConf.confidence * 100).toFixed(0)}%</span>. This means limited signals were detected for this domain. Consider providing more detail about{" "}
                      {lowestConf.agent.replace("_agent", "").replace(/_/g, " ")} exposure in your company description.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* ── Agent Output Panels ──────────────────────── */}
            <div className="animate-slide-up">
              <p className="label mb-1">Agent Output Panels</p>
              <p className="font-mono text-xs text-slate-600 mb-3">
                Detailed output from each agent — click to expand reasoning and metadata
              </p>
              <div className="space-y-3">
                {logs.map((log, i) => (
                  <AgentOutputPanel key={`${log.agent}-${i}`} log={log} index={i} />
                ))}
              </div>
            </div>
          </>
        )}
      </main>

      <footer className="border-t border-border mt-12 py-4">
        <p className="text-center font-mono text-xs text-slate-700">
          AGENT MONITOR · DEVELOPER VIEW · {new Date().getFullYear()}
        </p>
      </footer>
    </div>
  );
}