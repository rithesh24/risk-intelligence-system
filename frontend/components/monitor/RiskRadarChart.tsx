"use client";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  RadialLinearScale,
  Filler,
  TooltipItem,  
} from "chart.js";
import { Radar } from "react-chartjs-2";
import { AgentLog, formatAgentName, getRiskLevel } from "@/lib/api";

ChartJS.register(
  CategoryScale, LinearScale, BarElement, Tooltip, Legend,
  LineElement, PointElement, RadialLinearScale, Filler
);

interface RiskRadarChartProps {
  logs: AgentLog[];
}

export default function RiskRadarChart({ logs }: RiskRadarChartProps) {
  if (logs.length === 0) return null;

  const labels = logs.map((l) => formatAgentName(l.agent));
  const riskScores = logs.map((l) => +(l.risk_score * 100).toFixed(1));
  const confidences = logs.map((l) => +(l.confidence * 100).toFixed(1));

  const data = {
    labels,
    datasets: [
      {
        label: "Risk Score",
        data: riskScores,
        backgroundColor: "#ef444422",
        borderColor: "#ef4444",
        borderWidth: 1.5,
        pointBackgroundColor: riskScores.map((s) => getRiskLevel(s / 100).color),
        pointBorderColor: "#0a0e1a",
        pointRadius: 4,
        pointHoverRadius: 6,
      },
      {
        label: "Confidence",
        data: confidences,
        backgroundColor: "#00d4ff11",
        borderColor: "#00d4ff66",
        borderWidth: 1.5,
        pointBackgroundColor: "#00d4ff",
        pointBorderColor: "#0a0e1a",
        pointRadius: 3,
        pointHoverRadius: 5,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 900 },
    scales: {
      r: {
        min: 0,
        max: 100,
        angleLines: { color: "#1e2d40" },
        grid: { color: "#1e2d4055" },
        pointLabels: {
          color: "#94a3b8",
          font: { family: "IBM Plex Mono", size: 11 },
        },
        ticks: {
          color: "#475569",
          backdropColor: "transparent",
          font: { family: "IBM Plex Mono", size: 9 },
          stepSize: 25,
        },
      },
    },
    plugins: {
      legend: {
        labels: {
          color: "#94a3b8",
          font: { family: "IBM Plex Mono", size: 11 },
          boxWidth: 12,
          padding: 16,
        },
      },
      tooltip: {
        backgroundColor: "#111827",
        borderColor: "#1e2d40",
        borderWidth: 1,
        titleFont: { family: "IBM Plex Mono", size: 12 },
        bodyFont: { family: "IBM Plex Mono", size: 11 },
        callbacks: {
          label: (ctx: TooltipItem<"radar">) =>
          ` ${ctx.dataset.label ?? ""}: ${ctx.raw}%`,
        },
      },
    },
  };

  return (
    <div style={{ height: 320 }}>
      <Radar data={data} options={options} />
    </div>
  );
}