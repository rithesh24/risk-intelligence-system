"use client";

import { useEffect, useState } from "react";
import { getRiskLevel } from "@/lib/api";

interface RiskGaugeProps {
  score: number; // 0–1
}

export default function RiskGauge({ score }: RiskGaugeProps) {
  const [animated, setAnimated] = useState(0);
  const risk = getRiskLevel(score);

  // Animate on mount / score change
  useEffect(() => {
    const t = setTimeout(() => setAnimated(score), 80);
    return () => clearTimeout(t);
  }, [score]);

  const SIZE = 200;
  const STROKE = 14;
  const R = (SIZE - STROKE) / 2;
  const CENTER = SIZE / 2;

  // Semicircle arc: from 180° to 0° (left to right)
  const TOTAL_ANGLE = 180;
  const circumference = Math.PI * R; // half circle
  const offset = circumference * (1 - animated);

  const arcPath = `
    M ${CENTER - R} ${CENTER}
    A ${R} ${R} 0 0 1 ${CENTER + R} ${CENTER}
  `;

  // Needle
  const needleAngle = -180 + animated * 180;
  const needleRad = (needleAngle * Math.PI) / 180;
  const needleLen = R - 20;
  const nx = CENTER + needleLen * Math.cos(needleRad);
  const ny = CENTER + needleLen * Math.sin(needleRad);

  return (
    <div className="flex flex-col items-center">
      <svg
        width={SIZE}
        height={SIZE / 2 + 24}
        viewBox={`0 0 ${SIZE} ${SIZE / 2 + 24}`}
        className="overflow-visible"
      >
        {/* Track */}
        <path
          d={arcPath}
          fill="none"
          stroke="#1e2d40"
          strokeWidth={STROKE}
          strokeLinecap="round"
        />

        {/* Colored fill arc */}
        <path
          d={arcPath}
          fill="none"
          stroke={risk.color}
          strokeWidth={STROKE}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className="gauge-arc"
          style={{
            filter: `drop-shadow(0 0 6px ${risk.color}88)`,
          }}
        />

        {/* Tick marks */}
        {[0, 0.25, 0.5, 0.75, 1].map((t) => {
          const ang = (-180 + t * 180) * (Math.PI / 180);
          const innerR = R - STROKE / 2 - 6;
          const outerR = R + STROKE / 2 + 2;
          return (
            <line
              key={t}
              x1={CENTER + innerR * Math.cos(ang)}
              y1={CENTER + innerR * Math.sin(ang)}
              x2={CENTER + outerR * Math.cos(ang)}
              y2={CENTER + outerR * Math.sin(ang)}
              stroke="#334155"
              strokeWidth={1.5}
            />
          );
        })}

        {/* Needle */}
        <line
          x1={CENTER}
          y1={CENTER}
          x2={nx}
          y2={ny}
          stroke="#e2e8f0"
          strokeWidth={2}
          strokeLinecap="round"
          style={{
            transition: "x2 1.2s cubic-bezier(0.34,1.56,0.64,1), y2 1.2s cubic-bezier(0.34,1.56,0.64,1)",
          }}
        />
        <circle cx={CENTER} cy={CENTER} r={5} fill="#e2e8f0" />

        {/* Score text */}
        <text
          x={CENTER}
          y={CENTER / 2 + 28}
          textAnchor="middle"
          fill="white"
          fontSize="28"
          fontFamily="IBM Plex Mono"
          fontWeight="600"
        >
          {(score * 100).toFixed(0)}
        </text>
        <text
          x={CENTER}
          y={CENTER / 2 + 46}
          textAnchor="middle"
          fill={risk.color}
          fontSize="11"
          fontFamily="IBM Plex Mono"
          letterSpacing="2"
        >
          {risk.label.toUpperCase()}
        </text>

        {/* Min / Max labels */}
        <text x={6} y={CENTER + 20} fill="#475569" fontSize="10" fontFamily="IBM Plex Mono">0</text>
        <text x={SIZE - 14} y={CENTER + 20} fill="#475569" fontSize="10" fontFamily="IBM Plex Mono">100</text>
      </svg>
    </div>
  );
}