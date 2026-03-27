from typing import List
import statistics

from orchestrator.state.state_schema import RiskState, Conflict

CONFLICT_VARIANCE_THRESHOLD = 0.05
EXTREME_SPREAD_THRESHOLD = 0.4

def detect_variance(scores: List[float]) -> float:
    """ calculate variance in an=gent rish score """
    if len(scores) <= 1:
        return 0.0
    return statistics.variance(scores)



def detect_spread(scores: List[float]) -> float:
    """ difference between highest and lowest risk score """
    return max(scores) - min(scores)



def conflict_detector_node(state: RiskState) -> RiskState:
    """ detects disagreements between agents """
    outputs = state.agent_outputs
    
    if not outputs:
        return state
    
    scores = [agent.risk_score for agent in outputs.values()]
    agent_names = list(outputs.keys())
    
    variance = detect_variance(scores)
    spread = detect_spread(scores)
    
    conflicts = []
    
    #variance based conflict
    
    if variance > CONFLICT_VARIANCE_THRESHOLD:
        conflicts.append(
            Conflict(
                agents_involved=agent_names,
                variance=variance,
                description=f"High Variance ({variance:.4f}) detected between agent risk assesments",
                
            )
        )
        
    #extreme spread conflict
    
    if spread > EXTREME_SPREAD_THRESHOLD:
        conflicts.append(
            Conflict(
                agents_involved=agent_names,
                variance=spread,
                description=f"Extreme Spread ({spread:.4f}) between lowest and highest risk scores",
                
            )
        )
    
    return state.model_copy(update={"conflicts":conflicts})
