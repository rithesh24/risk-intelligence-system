"use client";

import { AgentLog, AGENT_PIPELINE, formatAgentName, getRiskLevel } from "@/lib/api";
import clsx from "clsx";

interface AgentTimelineProps {
  logs: AgentLog[];
}

export default function AgentTimeline({ logs }: AgentTimelineProps) {
  const logMap = new Map(logs.map((l) => [l.agent, l]));

  // Build timeline: known pipeline first, then any extra agents from logs
  const pipelineKeys = AGENT_PIPELINE.map((p) => p.key);
  const extraLogs = logs.filter((l) => !pipelineKeys.includes(l.agent));

  const timelineItems = [
    ...AGENT_PIPELINE.map((p) => ({
      key: p.key,
      label: p.label,
      description: p.description,
      log: logMap.get(p.key) ?? null,
    })),
    ...extraLogs.map((l) => ({
      key: l.agent,
      label: formatAgentName(l.agent),
      description: "",
      log: l,
    })),
  ];

  return (
    <div className="relative">
      {timelineItems.map((item, i) => {
        const ran = !!item.log;
        const risk = item.log ? getRiskLevel(item.log.risk_score) : null;
        const isLast = i === timelineItems.length - 1;

        return (
          <div key={item.key} className="flex gap-4">
            {/* Spine */}
            <div className="flex flex-col items-center">
              {/* Node */}
              <div
                className={clsx(
                  "w-8 h-8 rounded-full border-2 flex items-center justify-center flex-shrink-0 z-10",
                  ran
                    ? "border-accent bg-accent/10"
                    : "border-border bg-surface"
                )}
                style={
                  ran && risk
                    ? { borderColor: risk.color, backgroundColor: risk.color + "18" }
                    : {}
                }
              >
                {ran ? (
                  <div
                    className="w-2.5 h-2.5 rounded-full"
                    style={{ backgroundColor: risk!.color, boxShadow: `0 0 6px ${risk!.color}` }}
                  />
                ) : (
                  <div className="w-2 h-2 rounded-full bg-border" />
                )}
              </div>
              {/* Connector line */}
              {!isLast && (
                <div
                  className={clsx(
                    "w-px flex-1 my-1",
                    ran ? "bg-accent/30" : "bg-border"
                  )}
                  style={{ minHeight: 28 }}
                />
              )}
            </div>

            {/* Content */}
            <div className={clsx("pb-6 flex-1", isLast && "pb-0")}>
              <div className="flex items-center gap-3 mb-0.5">
                <span
                  className={clsx(
                    "font-mono text-sm font-semibold",
                    ran ? "text-white" : "text-slate-600"
                  )}
                >
                  {item.label} Agent
                </span>
                {ran && risk && (
                  <span
                    className="font-mono text-xs px-2 py-0.5 rounded-full border"
                    style={{ color: risk.color, borderColor: risk.color + "44", backgroundColor: risk.color + "11" }}
                  >
                    {risk.label}
                  </span>
                )}
                {!ran && (
                  <span className="font-mono text-xs text-slate-700 border border-border px-2 py-0.5 rounded-full">
                    not run
                  </span>
                )}
              </div>

              {item.description && (
                <p className="font-mono text-xs text-slate-600 mb-1">{item.description}</p>
              )}

              {ran && item.log && (
                <div className="flex gap-4 mt-1">
                  <span className="font-mono text-xs text-slate-400">
                    Risk{" "}
                    <span style={{ color: risk!.color }}>
                      {(item.log.risk_score * 100).toFixed(0)}%
                    </span>
                  </span>
                  <span className="font-mono text-xs text-slate-400">
                    Conf{" "}
                    <span className="text-accent">
                      {(item.log.confidence * 100).toFixed(0)}%
                    </span>
                  </span>
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}