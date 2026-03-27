from orchestrator.state.state_schema import RiskState

TIEBREAKER_AGENT_WEIGHT_MULTIPLIER = {
    "impact_agent": 2.0,  
}


def compute_weighted_risk(agent_outputs) -> float:
    """
    Compute weighted risk score based on agent confidence.
    Impact agent gets elevated weight as the designated tie-breaker.
    """
    weighted_sum = 0.0
    confidence_sum = 0.0

    for agent in agent_outputs.values():
        trust_multiplier = TIEBREAKER_AGENT_WEIGHT_MULTIPLIER.get(agent.agent_name, 1.0)
        effective_weight = agent.confidence * trust_multiplier
        weighted_sum += agent.risk_score * effective_weight
        confidence_sum += effective_weight

    if confidence_sum == 0:
        return 0.0

    return weighted_sum / confidence_sum


def compute_system_confidence(agent_outputs) -> float:
    """
    Aggregate confidence of the system as a simple mean.
    """
    if not agent_outputs:
        return 0.0

    total = sum(agent.confidence for agent in agent_outputs.values())
    return total / len(agent_outputs)


def tie_breaker_node(state: RiskState) -> RiskState:
    """
    Resolves remaining disagreement between agents
    """
    outputs = state.agent_outputs

    if not outputs:
        return state

    final_risk = compute_weighted_risk(outputs)
    final_confidence = compute_system_confidence(outputs)

  
    return state.model_copy(
        update={
            "final_risk_score": final_risk,
            "final_confidence": final_confidence,
        }
    )