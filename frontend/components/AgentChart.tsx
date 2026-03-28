"use client";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
  TooltipItem,
} from "chart.js";
import { Bar } from "react-chartjs-2";
import { AgentOutput, formatAgentName, getRiskLevel } from "@/lib/api";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

interface AgentChartProps {
  agentOutputs: Record<string, AgentOutput>;
}

export default function AgentChart({ agentOutputs }: AgentChartProps) {
  const entries = Object.entries(agentOutputs);
  const labels = entries.map(([k]) => formatAgentName(k));
  const scores = entries.map(([, v]) => +(v.risk_score * 100).toFixed(1));
  const confidences = entries.map(([, v]) => +(v.confidence * 100).toFixed(1));

  const barColors = scores.map((s) => getRiskLevel(s / 100).color + "cc");
  const borderColors = scores.map((s) => getRiskLevel(s / 100).color);

  const data = {
    labels,
    datasets: [
      {
        label: "Risk Score",
        data: scores,
        backgroundColor: barColors,
        borderColor: borderColors,
        borderWidth: 1.5,
        borderRadius: 6,
        borderSkipped: false,
      },
      {
        label: "Confidence",
        data: confidences,
        backgroundColor: "#00d4ff22",
        borderColor: "#00d4ff88",
        borderWidth: 1.5,
        borderRadius: 6,
        borderSkipped: false,
      },
    ],
  };

  const options = {
    indexAxis: "y" as const,
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 900,
      easing: "easeOutQuart" as const,
    },
    scales: {
      x: {
        min: 0,
        max: 100,
        grid: { color: "#1e2d4066" },
        ticks: {
          color: "#64748b",
          font: { family: "IBM Plex Mono", size: 11 },
          callback: (v: unknown) => `${v}`,
        },
        border: { color: "#1e2d40" },
      },
      y: {
        grid: { display: false },
        ticks: {
          color: "#94a3b8",
          font: { family: "IBM Plex Mono", size: 12 },
        },
        border: { color: "#1e2d40" },
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
        label: (ctx: TooltipItem<"bar">) =>
          ` ${ctx.dataset.label ?? ""}: ${ctx.raw}%`, 
        },
      },
    },
  };

  const chartHeight = Math.max(200, entries.length * 56 + 40);

  return (
    <div style={{ height: chartHeight }}>
      <Bar data={data} options={options} />
    </div>
  );
}