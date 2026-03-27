def _get_agent_risk(outputs, agent_name: str, fallback: float = 0.4) -> float:
    """ safely extract risk score, ignor errored agents """
    agent = outputs.get(agent_name)
    if agent is None:
        return fallback
    if agent.metadata.get("error"):
        return fallback
    return agent.risk_score



def calculate_revenue_impact(demand_risk: float, currency_risk: float) -> float:
    """ revenue impact as a positive percentage """
    demand_impact = demand_risk * 0.08
    currency_impact = currency_risk * 0.05
    return round((demand_impact + currency_impact) * 100,2)


def calculate_cost_impact(commodity_risk: float, policy_risk: float) -> float:
    """ cost impact as a positive percentage """
    commodity_cost = commodity_risk * 0.07
    policy_cost = policy_risk * 0.03
    return round((commodity_cost + policy_cost) * 100, 2)


def run(state) -> dict:
    outputs = state.agent_outputs
    
    currency_risk = _get_agent_risk(outputs, "currency_agent")
    commodity_risk = _get_agent_risk(outputs, "commodity_agent")
    demand_risk = _get_agent_risk(outputs, "demand_agent")
    policy_risk = _get_agent_risk(outputs, "policy_agent")
    
    
    revenue_impact = calculate_revenue_impact(demand_risk, currency_risk)
    cost_impact = calculate_cost_impact(commodity_risk, policy_risk)
    
    margin_impact = round(-(revenue_impact + cost_impact), 2)
    
    avg_risk = round(
        (currency_risk + commodity_risk + demand_risk + policy_risk) / 4, 4
    )
    
    reasoning = (
        f"Revenue ↓{revenue_impact}% driven by demand risk ({demand_risk:.2f}) "
        f"and currency risk ({currency_risk:.2f}). "
        f"Cost ↑{cost_impact}% driven by commodity risk ({commodity_risk:.2f}) "
        f"and policy risk ({policy_risk:.2f}). "
        f"Estimated margin impact: {margin_impact}%."
    )
    
    return {
        "risk_score": avg_risk,
        "confidence": 0.75,
        "reasoning": reasoning,
        "metadata": {
            "revenue_impact_percent": -revenue_impact,   # negative = decline
            "cost_increase_percent": cost_impact,         # positive = increase
            "margin_change_percent": margin_impact,       # negative = compression
        },
    }