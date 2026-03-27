"use client";

import { AgentLog, AGENT_PIPELINE, formatAgentName, getRiskLevel } from "@/lib/api";

interface ExecutionGraphProps {
  logs: AgentLog[];
}

// Layout constants
const NODE_W = 160;
const NODE_H = 64;
const H_GAP = 60;   // horizontal gap between nodes
const V_GAP = 48;   // vertical gap between rows
const PAD = 24;

// Pipeline graph topology — defines connections between agents
// Row 0: business_profile_agent
// Row 1: exposure_mapping_agent
// Row 2: signal agents (currency, commodity, demand, policy, narrative) — side by side
// Row 3: impact_agent
const GRAPH_NODES = [
  { key: "business_profile_agent", col: 0, row: 0 },
  { key: "exposure_mapping_agent", col: 0, row: 1 },
  // Signal agents spread horizontally
  { key: "currency_agent",  col: -2, row: 2 },
  { key: "commodity_agent", col: -1, row: 2 },
  { key: "demand_agent",    col:  0, row: 2 },
  { key: "policy_agent",    col:  1, row: 2 },
  { key: "narrative_sentiment_agent", col:  2, row: 2 },
  { key: "impact_agent",    col:  0, row: 3 },
];

const EDGES = [
  { from: "business_profile_agent", to: "exposure_mapping_agent" },
  { from: "exposure_mapping_agent", to: "currency_agent" },
  { from: "exposure_mapping_agent", to: "commodity_agent" },
  { from: "exposure_mapping_agent", to: "demand_agent" },
  { from: "exposure_mapping_agent", to: "policy_agent" },
  { from: "exposure_mapping_agent", to: "narrative_sentiment_agent" },
  { from: "currency_agent",  to: "impact_agent" },
  { from: "commodity_agent", to: "impact_agent" },
  { from: "demand_agent",    to: "impact_agent" },
  { from: "policy_agent",    to: "impact_agent" },
  { from: "narrative_sentiment_agent", to: "impact_agent" },
];

export default function ExecutionGraph({ logs }: ExecutionGraphProps) {
  const logMap = new Map(logs.map((l) => [l.agent, l]));

  // Compute pixel positions
  // Row 2 has 5 nodes spread across columns -2..2
  const signalCount = 5;
  const totalSignalWidth = signalCount * NODE_W + (signalCount - 1) * H_GAP;
  const centerX = PAD + totalSignalWidth / 2;

  function nodePos(col: number, row: number) {
    const x = centerX + col * (NODE_W + H_GAP) - NODE_W / 2;
    const y = PAD + row * (NODE_H + V_GAP);
    return { x, y };
  }

  const nodePosMap: Record<string, { x: number; y: number }> = {};
  GRAPH_NODES.forEach((n) => {
    nodePosMap[n.key] = nodePos(n.col, n.row);
  });

  const svgWidth = PAD * 2 + totalSignalWidth;
  const svgHeight = PAD * 2 + 4 * (NODE_H + V_GAP) - V_GAP;

  // Add extra nodes from logs not in pipeline
  const pipelineKeys = new Set(GRAPH_NODES.map((n) => n.key));
  const extraLogs = logs.filter((l) => !pipelineKeys.has(l.agent));

  return (
    <div className="w-full overflow-x-auto">
      <svg
        width={svgWidth}
        height={svgHeight}
        viewBox={`0 0 ${svgWidth} ${svgHeight}`}
        className="block mx-auto"
        style={{ minWidth: 600 }}
      >
        <defs>
          {/* Arrowhead marker */}
          <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
            <path d="M0,0 L0,6 L8,3 z" fill="#334155" />
          </marker>
          <marker id="arrow-active" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
            <path d="M0,0 L0,6 L8,3 z" fill="#00d4ff66" />
          </marker>

          {/* Glow filters */}
          <filter id="glow-green">
            <feGaussianBlur stdDeviation="3" result="coloredBlur" />
            <feMerge><feMergeNode in="coloredBlur" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
          <filter id="glow-accent">
            <feGaussianBlur stdDeviation="2" result="coloredBlur" />
            <feMerge><feMergeNode in="coloredBlur" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
        </defs>

        {/* ── Edges ─────────────────────────────────────────── */}
        {EDGES.map((edge, i) => {
          const from = nodePosMap[edge.from];
          const to = nodePosMap[edge.to];
          if (!from || !to) return null;

          const fromRan = logMap.has(edge.from);
          const toRan = logMap.has(edge.to);
          const bothRan = fromRan && toRan;

          // Edge from bottom-center of source to top-center of target
          const x1 = from.x + NODE_W / 2;
          const y1 = from.y + NODE_H;
          const x2 = to.x + NODE_W / 2;
          const y2 = to.y;

          // Bezier control points
          const cy1 = y1 + (y2 - y1) * 0.4;
          const cy2 = y2 - (y2 - y1) * 0.4;

          return (
            <path
              key={`edge-${i}`}
              d={`M${x1},${y1} C${x1},${cy1} ${x2},${cy2} ${x2},${y2}`}
              fill="none"
              stroke={bothRan ? "#00d4ff44" : "#1e2d40"}
              strokeWidth={bothRan ? 1.5 : 1}
              strokeDasharray={bothRan ? "none" : "4,4"}
              markerEnd={bothRan ? "url(#arrow-active)" : "url(#arrow)"}
            />
          );
        })}

        {/* ── Pipeline Nodes ────────────────────────────────── */}
        {GRAPH_NODES.map((n) => {
          const pos = nodePosMap[n.key];
          const log = logMap.get(n.key);
          const ran = !!log;
          const risk = log ? getRiskLevel(log.risk_score) : null;
          const label = formatAgentName(n.key);

          return (
            <g key={`node-${n.key}`} transform={`translate(${pos.x}, ${pos.y})`}>
              {/* Node shadow/glow when active */}
              {ran && (
                <rect
                  x={-2} y={-2} width={NODE_W + 4} height={NODE_H + 4}
                  rx={10} ry={10}
                  fill="none"
                  stroke={risk!.color}
                  strokeWidth={1}
                  opacity={0.3}
                  filter="url(#glow-accent)"
                />
              )}

              {/* Node body */}
              <rect
                x={0} y={0} width={NODE_W} height={NODE_H}
                rx={8} ry={8}
                fill={ran ? "#111827" : "#0d1424"}
                stroke={ran ? risk!.color + "88" : "#1e2d40"}
                strokeWidth={ran ? 1.5 : 1}
              />

              {/* Left accent bar */}
              <rect
                x={0} y={0} width={4} height={NODE_H}
                rx={8} ry={8}
                fill={ran ? risk!.color : "#1e2d40"}
              />
              <rect x={0} y={8} width={4} height={NODE_H - 16} fill={ran ? risk!.color : "#1e2d40"} />

              {/* Status dot */}
              <circle
                cx={NODE_W - 12} cy={12}
                r={4}
                fill={ran ? risk!.color : "#1e2d40"}
                filter={ran ? "url(#glow-green)" : "none"}
              />

              {/* Agent name */}
              <text
                x={14} y={26}
                fill={ran ? "#e2e8f0" : "#475569"}
                fontSize="11"
                fontFamily="IBM Plex Mono"
                fontWeight="600"
              >
                {label}
              </text>
              <text
                x={14} y={38}
                fill="#475569"
                fontSize="9"
                fontFamily="IBM Plex Mono"
              >
                Agent
              </text>

              {/* Risk + confidence when ran */}
              {ran && log && (
                <>
                  <text
                    x={14} y={54}
                    fill={risk!.color}
                    fontSize="9"
                    fontFamily="IBM Plex Mono"
                  >
                    {`Risk ${(log.risk_score * 100).toFixed(0)}%`}
                  </text>
                  <text
                    x={70} y={54}
                    fill="#00d4ff"
                    fontSize="9"
                    fontFamily="IBM Plex Mono"
                  >
                    {`Conf ${(log.confidence * 100).toFixed(0)}%`}
                  </text>
                </>
              )}

              {/* Not run label */}
              {!ran && (
                <text
                  x={14} y={54}
                  fill="#334155"
                  fontSize="9"
                  fontFamily="IBM Plex Mono"
                >
                  not run
                </text>
              )}
            </g>
          );
        })}

        {/* ── Extra agents not in pipeline ──────────────────── */}
        {extraLogs.map((log, i) => {
          const ex = PAD + i * (NODE_W + H_GAP);
          const ey = svgHeight - NODE_H - PAD + 10;
          const risk = getRiskLevel(log.risk_score);
          const label = formatAgentName(log.agent);
          return (
            <g key={`extra-${log.agent}-${i}`} transform={`translate(${ex}, ${ey})`}>
              <rect x={0} y={0} width={NODE_W} height={NODE_H} rx={8} fill="#111827" stroke={risk.color + "88"} strokeWidth={1.5} />
              <rect x={0} y={0} width={4} height={NODE_H} rx={8} fill={risk.color} />
              <rect x={0} y={8} width={4} height={NODE_H - 16} fill={risk.color} />
              <text x={14} y={26} fill="#e2e8f0" fontSize="11" fontFamily="IBM Plex Mono" fontWeight="600">{label}</text>
              <text x={14} y={38} fill="#475569" fontSize="9" fontFamily="IBM Plex Mono">Agent</text>
              <text x={14} y={54} fill={risk.color} fontSize="9" fontFamily="IBM Plex Mono">
                {`Risk ${(log.risk_score * 100).toFixed(0)}%  Conf ${(log.confidence * 100).toFixed(0)}%`}
              </text>
            </g>
          );
        })}
      </svg>

      {/* Legend */}
      <div className="flex items-center gap-6 mt-3 px-2">
        <div className="flex items-center gap-2">
          <div className="w-6 h-px bg-accent/40" />
          <span className="font-mono text-xs text-slate-600">Executed</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-px border-t border-dashed border-border" />
          <span className="font-mono text-xs text-slate-600">Not run</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-low" />
          <span className="font-mono text-xs text-slate-600">Low risk</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-medium" />
          <span className="font-mono text-xs text-slate-600">Moderate</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-high" />
          <span className="font-mono text-xs text-slate-600">High</span>
        </div>
      </div>
    </div>
  );
}