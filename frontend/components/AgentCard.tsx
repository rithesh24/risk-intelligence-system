"use client";

import { useState } from "react";
import { AgentOutput, formatAgentName, getRiskLevel } from "@/lib/api";
import clsx from "clsx";

interface AgentCardProps {
  agentKey: string;
  output: AgentOutput;
  index: number;
}

export default function AgentCard({ agentKey, output, index }: AgentCardProps) {
  const [open, setOpen] = useState(false);
  const risk = getRiskLevel(output.risk_score);
  const name = formatAgentName(agentKey);

  return (
    <div
      className={clsx(
        "card cursor-pointer transition-all duration-200 animate-slide-up",
        open ? "card-active" : "hover:border-slate-600"
      )}
      style={{ animationDelay: `${index * 80}ms`, animationFillMode: "both" }}
      onClick={() => setOpen((o) => !o)}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {/* Risk dot */}
          <div
            className="w-2 h-2 rounded-full flex-shrink-0"
            style={{
              backgroundColor: risk.color,
              boxShadow: `0 0 6px ${risk.color}`,
            }}
          />
          <span className="font-mono text-sm text-slate-300">{name}</span>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right hidden sm:block">
            <p className="label">Risk</p>
            <p className="font-mono text-sm" style={{ color: risk.color }}>
              {(output.risk_score * 100).toFixed(0)}%
            </p>
          </div>
          <div className="text-right hidden sm:block">
            <p className="label">Confidence</p>
            <p className="font-mono text-sm text-accent">
              {(output.confidence * 100).toFixed(0)}%
            </p>
          </div>
          <span
            className={clsx(
              "text-slate-500 text-lg transition-transform duration-200",
              open && "rotate-180"
            )}
          >
            ↓
          </span>
        </div>
      </div>

      {open && (
        <div className="mt-4 pt-4 border-t border-border animate-fade-in">
          {/* Mobile scores */}
          <div className="flex gap-6 sm:hidden mb-3">
            <div>
              <p className="label">Risk Score</p>
              <p className="font-mono text-sm" style={{ color: risk.color }}>
                {(output.risk_score * 100).toFixed(0)}%
              </p>
            </div>
            <div>
              <p className="label">Confidence</p>
              <p className="font-mono text-sm text-accent">
                {(output.confidence * 100).toFixed(0)}%
              </p>
            </div>
          </div>

          {/* Progress bar */}
          <div className="mb-4">
            <div className="flex justify-between mb-1">
              <span className="label">Risk Level</span>
              <span
                className="label"
                style={{ color: risk.color }}
              >
                {risk.label}
              </span>
            </div>
            <div className="w-full h-1.5 bg-border rounded-full overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-700"
                style={{
                  width: `${output.risk_score * 100}%`,
                  backgroundColor: risk.color,
                  boxShadow: `0 0 8px ${risk.color}88`,
                }}
              />
            </div>
          </div>

          <div>
            <p className="label mb-1.5">Reasoning</p>
            <p className="text-slate-300 text-sm leading-relaxed font-mono">
              {output.reasoning}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}