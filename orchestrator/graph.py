from langgraph.graph import StateGraph, START, END

from orchestrator.state.state_schema import RiskState
from orchestrator.nodes.agent_executor import agent_executor_node
from orchestrator.nodes.conflict_detector import conflict_detector_node
from orchestrator.nodes.challenge_phase import challenge_phase_node 
from orchestrator.nodes.tie_breaker import tie_breaker_node
from orchestrator.nodes.aggregator import aggregator_node


def conflict_router(state: RiskState) -> str:
    """
    routes to challenge phase if conflicts exist and iterationremain
    """
    if state.conflicts and state.iteration_count < state.max_iterations:
        return "challenge_phase"
    return "tie_breaker" 


def build_graph():
    graph = StateGraph(RiskState)
    
    #nodes
    graph.add_node("agent_executor",agent_executor_node)
    graph.add_node("conflict_detector",conflict_detector_node)
    graph.add_node("challenge_phase",challenge_phase_node)
    graph.add_node("tie_breaker",tie_breaker_node)
    graph.add_node("aggregator",aggregator_node)
    
    # entry
    graph.add_edge(START, "agent_executor")
    graph.add_edge("agent_executor","conflict_detector")
    
    graph.add_conditional_edges(
        "conflict_detector",
        conflict_router,
        {
            "challenge_phase": "challenge_phase",
            "tie_breaker": "tie_breaker"
        },
    )
    
    graph.add_edge("challenge_phase","conflict_detector")
    graph.add_edge("tie_breaker","aggregator")
    graph.add_edge("aggregator", END)
    
    
    return graph.compile()

    

