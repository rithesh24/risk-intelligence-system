from orchestrator.graph import build_graph
from orchestrator.state.state_schema import RiskState
from data.market_data_service import get_market_data


class RiskEngine:
    def __init__(self):
        self.graph = build_graph()

    def analyze_company(self, company_description: str) -> dict:

        initial_state = RiskState(company_input=company_description)

        result = self.graph.invoke(initial_state)

        final_state = RiskState(**result)

        # Fetch live market data based on this company's commodities
        commodity_dependencies = final_state.exposures.get("commodity_dependencies", [])
        market_data = get_market_data(commodity_dependencies)
        final_state = final_state.model_copy(update={"market_data": market_data})

        return {
            "risk_score": final_state.final_risk_score,
            "confidence": final_state.final_confidence,
            "explanation": final_state.final_explanation,
            "recommendations": final_state.recommendations,
            "market_data": final_state.market_data,

            # Risk analysis fields
            "risk_contributions": final_state.risk_contributions,
            "amplification_boost": final_state.amplification_boost,
            "amplification_signals": final_state.amplification_signals,
            "base_risk_score": final_state.base_risk_score,

            "agent_outputs": {
                name: {
                    "risk_score": agent.risk_score,
                    "confidence": agent.confidence,
                    "reasoning": agent.reasoning,
                    "metadata": agent.metadata,  
                }
                for name, agent in final_state.agent_outputs.items()
            },
        }