from fastapi import APIRouter
from orchestrator.nodes.agent_executor import (
    business_profile_agent,
    exposure_mapping_agent,
    currency_agent,
    commodity_agent,
    demand_agent,
    policy_agent,
    narrative_agent,
    impact_agent,
)

router = APIRouter(prefix="/observability", tags=["Observability"])

LOADED_AGENTS = [
    "business_profile_agent",
    "exposure_mapping_agent",
    "currency_agent",
    "commodity_agent",
    "demand_agent",
    "policy_agent",
    "narrative_sentiment_agent",
    "impact_agent",
]

@router.get("/system-state")
def system_state():
    return {
        "status": "running",
        "agents_loaded": LOADED_AGENTS,
        "agent_count": len(LOADED_AGENTS),
    }