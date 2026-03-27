from typing import Dict, List

from orchestrator.state.state_schema import RiskState, AgentOutput, ChallengeRecord
from agents.signal_agents.currency_agent import run as currency_agent
from agents.signal_agents.commodity_agent import run as commodity_agent
from agents.signal_agents.demand_sector_agent import run as demand_agent
from agents.signal_agents.policy_agent import run as policy_agent
from agents.llm_agents.narrative_sentiment_agent import run as narrative_agent
from orchestrator.nodes.agent_executor import execute_agent


CHALLENGE_REGISTRY = {
    "currency_agent": currency_agent,
    "commodity_agent": commodity_agent,
    "demand_agent": demand_agent,
    "policy_agent": policy_agent,
    "narrative_sentiment_agent": narrative_agent,
}

def challenge_phase_node(state: RiskState) -> RiskState:
    """ re-evaluates agents involved in conflicts """
    
    if not state.conflicts:
        return state
    
    if state.iteration_count >= state.max_iterations:
        return state
    
    # collect all agents involved in conflict
    
    challenged_agents: set = {
        agent
        for conflict in state.conflicts
        for agent in conflict.agents_involved
        if agent in CHALLENGE_REGISTRY
    }
    
    responses: Dict[str, AgentOutput] = {}
    
    for agent_name in challenged_agents:
        agents_fn = CHALLENGE_REGISTRY[agent_name]
        output, state = execute_agent(agent_name, agents_fn, state)
        responses[agent_name] =  output
        
        
    challenge_record = ChallengeRecord(
        iteration=state.iteration_count + 1,
        challenged_agents=list(challenged_agents),
        responses=responses,
    )
    
    # build all updates as new objects
    
    updated_agent_outputs = {**state.agent_outputs, **responses}
    updated_challenge_history = [*state.challenge_history, challenge_record]
    
    return state.model_copy(
        update={
            "agent_outputs":updated_agent_outputs,
            "challenge_history":updated_challenge_history,
            "iteration_count":state.iteration_count + 1,
        }
    )