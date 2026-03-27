"use client";

import { AgentLog, formatAgentName, getRiskLevel } from "@/lib/api";

interface ConflictDetectorProps {
  logs: AgentLog[];
}

interface Conflict {
  agentA: string;
  agentB: string;
  scoreA: number;
  scoreB: number;
  delta: number;
}

const CONFLICT_THRESHOLD = 0.25;

export default function ConflictDetector({ logs }: ConflictDetectorProps) {
  const conflicts: Conflict[] = [];

  for (let i = 0; i < logs.length; i++) {
    for (let j = i + 1; j < logs.length; j++) {
      const delta = Math.abs(logs[i].risk_score - logs[j].risk_score);
      if (delta >= CONFLICT_THRESHOLD) {
        conflicts.push({
          agentA: logs[i].agent,
          agentB: logs[j].agent,
          scoreA: logs[i].risk_score,
          scoreB: logs[j].risk_score,
          delta,
        });
      }
    }
  }

  if (conflicts.length === 0) {
    return (
      <div className="card">
        <div className="flex items-center gap-2 mb-1">
          <p className="label">Conflict Detection</p>
        </div>
        <div className="flex items-center gap-2 mt-2">
          <span className="w-1.5 h-1.5 rounded-full bg-low" />
          <span className="font-mono text-xs text-low">No conflicts detected — agents are in agreement</span>
        </div>
      </div>
    );
  }

  return (
    <div className="card border-orange-500/20">
      <div className="flex items-center justify-between mb-3">
        <p className="label">Conflict Detection</p>
        <span className="font-mono text-xs text-orange-400 border border-orange-500/30 px-2 py-0.5 rounded-full">
          {conflicts.length} conflict{conflicts.length > 1 ? "s" : ""}
        </span>
      </div>

      <div className="space-y-3">
        {conflicts.map((c, i) => {
          const riskA = getRiskLevel(c.scoreA);
          const riskB = getRiskLevel(c.scoreB);
          return (
            <div
              key={i}
              className="flex items-start gap-3 p-3 rounded-lg bg-orange-500/5 border border-orange-500/15 animate-fade-in"
            >
              <span className="text-orange-400 text-base mt-0.5 flex-shrink-0">⚠</span>
              <div className="flex-1 min-w-0">
                <p className="font-mono text-xs text-slate-300">
                  <span className="font-semibold text-white">{formatAgentName(c.agentA)} Agent</span>
                  <span className="text-slate-500"> vs </span>
                  <span className="font-semibold text-white">{formatAgentName(c.agentB)} Agent</span>
                </p>
                <div className="flex gap-4 mt-1.5">
                  <span className="font-mono text-xs" style={{ color: riskA.color }}>
                    {formatAgentName(c.agentA)}: {(c.scoreA * 100).toFixed(0)}%
                  </span>
                  <span className="font-mono text-xs" style={{ color: riskB.color }}>
                    {formatAgentName(c.agentB)}: {(c.scoreB * 100).toFixed(0)}%
                  </span>
                  <span className="font-mono text-xs text-orange-400">
                    Δ {(c.delta * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <p className="font-mono text-xs text-slate-600 mt-3">
        Conflict threshold: ≥{CONFLICT_THRESHOLD * 100}% divergence between agent risk scores
      </p>
    </div>
  );
}