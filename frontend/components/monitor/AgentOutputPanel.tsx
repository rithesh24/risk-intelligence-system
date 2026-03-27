"use client";

import { useState } from "react";
import { AgentLog, formatAgentName, getRiskLevel } from "@/lib/api";
import clsx from "clsx";

interface AgentOutputPanelProps {
  log: AgentLog;
  index: number;
}

export default function AgentOutputPanel({ log, index }: AgentOutputPanelProps) {
  const [open, setOpen] = useState(false);
  const risk = getRiskLevel(log.risk_score);
  const name = formatAgentName(log.agent);
  const hasMetadata = log.metadata && Object.keys(log.metadata).length > 0;

  const renderMetaValue = (val: unknown): string => {
    if (Array.isArray(val)) return val.join(", ");
    if (typeof val === "boolean") return val ? "Yes" : "No";
    if (val === null || val === undefined) return "—";
    return String(val);
  };

  return (
    <div
      className="card animate-slide-up"
      style={{ animationDelay: `${index * 70}ms`, animationFillMode: "both" }}
    >
      {/* Header row */}
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-center gap-3 min-w-0">
          <div
            className="w-2 h-2 rounded-full flex-shrink-0 mt-1"
            style={{ backgroundColor: risk.color, boxShadow: `0 0 6px ${risk.color}` }}
          />
          <div className="min-w-0">
            <h3 className="font-mono text-sm font-semibold text-white">{name} Agent</h3>
            <p className="font-mono text-xs text-slate-500 truncate mt-0.5">{log.agent}</p>
          </div>
        </div>

        {/* Score pills */}
        <div className="flex items-center gap-3 flex-shrink-0">
          <div className="text-right">
            <p className="label">Risk</p>
            <p className="font-mono text-sm font-semibold" style={{ color: risk.color }}>
              {(log.risk_score * 100).toFixed(0)}%
            </p>
          </div>
          <div className="text-right">
            <p className="label">Conf</p>
            <p className="font-mono text-sm font-semibold text-accent">
              {(log.confidence * 100).toFixed(0)}%
            </p>
          </div>
        </div>
      </div>

      {/* Risk bar */}
      <div className="mt-3 mb-3">
        <div className="w-full h-1 bg-border rounded-full overflow-hidden">
          <div
            className="h-full rounded-full transition-all duration-700"
            style={{
              width: `${log.risk_score * 100}%`,
              backgroundColor: risk.color,
              boxShadow: `0 0 8px ${risk.color}66`,
            }}
          />
        </div>
      </div>

      {/* Reasoning */}
      <p className="text-slate-300 text-sm leading-relaxed font-mono">{log.reasoning}</p>

      {/* Metadata toggle */}
      {hasMetadata && (
        <>
          <button
            onClick={() => setOpen((o) => !o)}
            className="mt-3 flex items-center gap-1.5 font-mono text-xs text-slate-500 hover:text-accent transition-colors"
          >
            <span className={clsx("transition-transform duration-200", open && "rotate-90")}>▶</span>
            Metadata
          </button>

          {open && (
            <div className="mt-2 pt-3 border-t border-border animate-fade-in">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-2">
                {Object.entries(log.metadata).map(([k, v]) => (
                  <div key={k} className="flex justify-between gap-2">
                    <span className="label truncate">{k.replace(/_/g, " ")}</span>
                    <span className="font-mono text-xs text-slate-300 text-right max-w-[60%] truncate">
                      {renderMetaValue(v)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}