from orchestrator.state.state_schema import RiskState
from risk.amplification_engine import compute_amplification


def classify_risk(score: float) -> str:
    if score < 0.3:
        return "Low"
    elif score < 0.6:
        return "Moderate"
    elif score < 0.8:
        return "High"
    else:
        return "Critical"


def identify_top_drivers(agent_outputs, top_n: int = 3):
    """
    Identify agents contributing most to risk.
    Excludes failed agents from driver identification.
    """
    healthy_agents = [
        agent for agent in agent_outputs.values()
        if not agent.metadata.get("error", False)
    ]

    sorted_agents = sorted(
        healthy_agents,
        key=lambda x: x.risk_score,
        reverse=True,
    )

    return sorted_agents[:top_n]


def generate_explanation(top_drivers, amplification_signals: list) -> str:
    if not top_drivers:
        return "No driver data available"

    explanations = [
        f"{agent.agent_name}: {agent.reasoning}"
        for agent in top_drivers
    ]

    base = " | ".join(explanations)

    if amplification_signals:
        signals_str = ", ".join(amplification_signals)
        base += f" | Amplification signals detected: {signals_str}"

    return base


def generate_recommendations(risk_score: float) -> list:
    if risk_score > 0.7:
        return [
            "Consider hedging key financial exposures",
            "Monitor macroeconomic signals closely",
            "Evaluate supply chain risk buffers",
        ]
    elif risk_score > 0.4:
        return [
            "Track key market indicators",
            "Review pricing and cost assumptions",
        ]
    else:
        return [
            "Maintain current strategy",
            "Continue monitoring external signals",
        ]


def compute_contributions(agent_outputs) -> dict[str, float]:
    """
    Tracks each agent's risk score contribution.
    Excludes failed agents.
    """
    return {
        agent_name: round(output.risk_score, 4)
        for agent_name, output in agent_outputs.items()
        if not output.metadata.get("error", False)  
    }


def aggregator_node(state: RiskState) -> RiskState:
    base_risk = state.final_risk_score

    if base_risk is None:
        return state

    # Amplification 
    amplification = compute_amplification(state)
    boost = amplification["boost"]
    signals = amplification["signals"]
    final_risk = round(min(base_risk + boost, 1.0), 4)

    # Contributions 
    contributions = compute_contributions(state.agent_outputs)  

    # Explanation & Recommendations 
    risk_level = classify_risk(final_risk)
    top_drivers = identify_top_drivers(state.agent_outputs)
    explanation = generate_explanation(top_drivers, signals)
    recommendations = generate_recommendations(final_risk)

    return state.model_copy(
        update={
            "final_risk_score": final_risk,
            "final_confidence": state.final_confidence,
            "final_explanation": f"Risk Level: {risk_level}. Drivers → {explanation}",
            "recommendations": recommendations,
            "risk_contributions": contributions,  
            "amplification_signals": signals,      
            "amplification_boost": boost,          
            "base_risk_score": base_risk,
        }
    )