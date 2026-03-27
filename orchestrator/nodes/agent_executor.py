from typing import Dict

from orchestrator.state.state_schema import RiskState, AgentOutput
from observability.agent_monitor import monitor
from ingestion.sources.rss_feed import fetch_and_filter_news        
from ingestion.pipeline.event_builder import build_news_events

# agents
from agents.llm_agents.business_profile_agent import run as business_profile_agent
from agents.llm_agents.exposure_mapping_agent import run as exposure_mapping_agent
from agents.llm_agents.narrative_sentiment_agent import run as narrative_agent
from agents.signal_agents.currency_agent import run as currency_agent
from agents.signal_agents.commodity_agent import run as commodity_agent
from agents.signal_agents.demand_sector_agent import run as demand_agent
from agents.signal_agents.policy_agent import run as policy_agent
from agents.impact.impact_translation_agent import run as impact_agent


def execute_agent(
    agent_name: str, agent_fn, state: RiskState
) -> tuple[AgentOutput, RiskState]:
    """
    Executes a single agent safely.
    Logs success via monitor.log and hard failures via monitor.log_error.
    """
    try:
        result = agent_fn(state)
        output = AgentOutput(
            agent_name=agent_name,
            risk_score=result.get("risk_score", 0.0),
            confidence=result.get("confidence", 0.0),
            reasoning=result.get("reasoning", ""),
            metadata=result.get("metadata", {}),
        )
        monitor.log(agent_name, output)

    except Exception as e:
        output = AgentOutput(
            agent_name=agent_name,
            risk_score=0.0,
            confidence=0.0,
            reasoning=f"Agent failed: {str(e)}",
            metadata={"error": True},
        )
        monitor.log_error(agent_name, e)

    updated_outputs = {**state.agent_outputs, agent_name: output}
    state = state.model_copy(update={"agent_outputs": updated_outputs})

    return output, state


def agent_executor_node(state: RiskState) -> RiskState:
    """
    Staged sequential execution:
    Stage 1 → business profile
    Stage 2 → exposure mapping (depends on profile)
    Stage 2.5 → fetch and filter news (needs exposures for context)
    Stage 3 → signal agents (depend on exposures + news)
    Stage 4 → impact agent (depends on all signal agents)
    """

    # Stage 1: Business Profile 
    _, state = execute_agent("business_profile_agent", business_profile_agent, state)
    profile = state.agent_outputs["business_profile_agent"].metadata
    state = state.model_copy(update={"business_profile": profile})

    # Stage 2: Exposure Mapping 
    _, state = execute_agent("exposure_mapping_agent", exposure_mapping_agent, state)
    exposures = state.agent_outputs["exposure_mapping_agent"].metadata
    state = state.model_copy(update={"exposures": exposures})

    # Stage 2.5: Fetch & Filter News 
    # Run after exposures are known so keyword context is richer
    try:
        articles = fetch_and_filter_news()
        news_events = build_news_events(articles)
        state = state.model_copy(update={"news_events": news_events})
        print(f"[Pipeline] {len(news_events)} news events loaded into state")
    except Exception as e:
        
        print(f"[Pipeline] News fetch failed, continuing without news: {e}")

    # Stage 3: Signal Agents 
    signal_agents = [
        ("currency_agent", currency_agent),
        ("commodity_agent", commodity_agent),
        ("demand_agent", demand_agent),
        ("policy_agent", policy_agent),
        ("narrative_sentiment_agent", narrative_agent),
    ]

    for name, fn in signal_agents:
        _, state = execute_agent(name, fn, state)

    # Stage 4: Impact Agent 
    _, state = execute_agent("impact_agent", impact_agent, state)

    return state