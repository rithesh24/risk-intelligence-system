"use client";

import { useCallback, useState } from "react";
import { AgentLog, fetchAgentLogs } from "@/lib/api";
import clsx from "clsx";

export default function AgentLogsPanel() {
  const [logs, setLogs] = useState<AgentLog[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [open, setOpen] = useState(false);

  const loadLogs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchAgentLogs();
      console.log("LOGS RESPONSE:", data);
      setLogs(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load logs");
    } finally {
      setLoading(false);
    }
  }, []);

  // ✅ open panel triggers fetch automatically
  const handleToggle = () => {
    if (!open) loadLogs();
    setOpen((o) => !o);
  };

  return (
    <div className="card mt-4">
      <button
        onClick={handleToggle}
        className="w-full flex items-center justify-between text-left"
      >
        <div className="flex items-center gap-2">
          <span className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse-slow" />
          <span className="label text-slate-400">Agent Execution Logs</span>
        </div>
        <span
          className={clsx(
            "font-mono text-xs text-slate-500 transition-transform duration-200",
            open && "rotate-180"
          )}
        >
          ↓
        </span>
      </button>

      {open && (
        <div className="mt-4 animate-fade-in">
          <div className="flex items-center justify-between mb-3">
            <span className="label">{logs.length} entries</span>
            <button
              onClick={loadLogs}
              className="label text-accent hover:text-white transition-colors"
            >
              ↻ Refresh
            </button>
          </div>

          {loading && (
            <div className="text-center py-8">
              <span className="font-mono text-xs text-slate-500 animate-pulse">
                Loading logs...
              </span>
            </div>
          )}

          {error && (
            <p className="font-mono text-xs text-high py-4 text-center">
              {error}
            </p>
          )}

          {!loading && !error && logs.length === 0 && (
            <p className="font-mono text-xs text-slate-500 py-4 text-center">
              No logs available — run an analysis first
            </p>
          )}

          {!loading && logs.length > 0 && (
            <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
              {logs.map((log, i) => (
                <div
                  key={i}
                  className="flex gap-3 text-xs font-mono border-b border-border pb-2 last:border-0"
                >
                  {/* Timestamp */}
                  <span className="text-slate-600 flex-shrink-0 w-20 truncate">
                    {log.timestamp
                      ? new Date(log.timestamp).toLocaleTimeString()
                      : "—"}
                  </span>

                  {/* Agent name */}
                  <span className="text-slate-400 flex-shrink-0 w-28 truncate">
                    {log.agent}
                  </span>

                  {/* Status — derived from errored field */}
                  <span
                    className={clsx(
                      "flex-shrink-0 w-16",
                      log.errored ? "text-high" : "text-low"
                    )}
                  >
                    {log.errored ? "FAILED" : "OK"}
                  </span>

                  {/* Reasoning */}
                  <span className="text-slate-300 flex-1 truncate">
                    {log.reasoning}
                  </span>

                  {/* Risk score */}
                  <span className="text-slate-500 flex-shrink-0">
                    {(log.risk_score * 100).toFixed(0)}%
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}