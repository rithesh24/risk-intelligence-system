const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

// Backend pipeline runs 3 sequential LLM calls (15s timeout, 1 retry each)
// plus RSS/market-data fetches — bound the UI wait so it fails instead of
// spinning forever if the backend hangs.
const ANALYZE_TIMEOUT_MS = 90_000;
export interface AgentOutput {
  risk_score: number;
  confidence: number;
  reasoning: string;
}

export interface AnalysisResult {
  risk_score: number;
  confidence: number;
  explanation: string;
  recommendations: string[];
  agent_outputs: Record<string, AgentOutput>;
}

export interface AgentLog {
  agent: string;
  risk_score: number;
  confidence: number;
  reasoning: string;
  metadata: Record<string, unknown>;
  timestamp: string;        
  errored: boolean;
}

export async function analyzeCompany(
  description: string
): Promise<AnalysisResult> {
  let res: Response;
  try {
    res = await fetch(`${BASE_URL}/api/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ company_description: description }),
      signal: AbortSignal.timeout(ANALYZE_TIMEOUT_MS),
    });
  } catch (e) {
    if (e instanceof DOMException && e.name === "TimeoutError") {
      throw new Error("Analysis timed out — the backend may be overloaded. Please try again.");
    }
    throw e;
  }

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`API error ${res.status}: ${errorText}`);
  }

  return res.json();
}

export async function fetchAgentLogs(): Promise<AgentLog[]> {
  const res = await fetch(`${BASE_URL}/observability/agent-logs`, {
    cache: "no-store",
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`API error ${res.status}: ${errorText}`);
  }

  return res.json();
}

// Agent execution order for timeline
export const AGENT_PIPELINE: { key: string; label: string; description: string }[] = [
  { key: "business_profile_agent", label: "Business Profile", description: "Extracts industry, markets, dependencies" },
  { key: "exposure_mapping_agent", label: "Exposure Mapping", description: "Maps currency, commodity & demand exposure" },
  { key: "currency_agent",         label: "Currency",         description: "Evaluates FX & USD exposure risk" },
  { key: "commodity_agent",        label: "Commodity",        description: "Assesses commodity price volatility" },
  { key: "demand_agent",           label: "Demand",           description: "Measures export demand risk" },
  { key: "policy_agent",           label: "Policy",           description: "Monitors regulatory & policy signals" },
  { key: "narrative_agent",        label: "Narrative",        description: "Analyses news & sentiment signals" },
  { key: "impact_agent",           label: "Impact",           description: "Computes final revenue & margin impact" },
];

export function getRiskLevel(score: number): {
  label: string;
  color: string;
  tailwind: string;
} {
  if (score < 0.35)
    return { label: "Low", color: "#22c55e", tailwind: "text-low" };
  if (score < 0.65)
    return { label: "Moderate", color: "#f59e0b", tailwind: "text-medium" };
  if (score < 0.8)
    return {
      label: "Moderate-High",
      color: "#f97316",
      tailwind: "text-orange-400",
    };
  return { label: "High", color: "#ef4444", tailwind: "text-high" };
}

export function formatAgentName(key: string): string {
  return key
    .replace(/_agent$/, "")
    .split("_")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}