from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from events.models.news_event import NewsEvent


class AgentOutput(BaseModel):
    agent_name: str
    risk_score: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class Conflict(BaseModel):
    agents_involved: List[str]
    variance: float = Field(ge=0.0)
    description: str


class ChallengeRecord(BaseModel):
    iteration: int = Field(ge=0)
    challenged_agents: List[str]
    responses: Dict[str, AgentOutput] = Field(default_factory=dict)


class RiskState(BaseModel):
    # Raw Input
    company_input: str

    # Structured Context
    business_profile: Dict[str, Any] = Field(default_factory=dict)
    exposures: Dict[str, Any] = Field(default_factory=dict)
    news_events: List[NewsEvent] = Field(default_factory=list)
    market_data: Dict[str, Any] = Field(default_factory=dict)

    # Agent Outputs
    agent_outputs: Dict[str, AgentOutput] = Field(default_factory=dict)

    # Orchestration Metadata
    conflicts: List[Conflict] = Field(default_factory=list)
    challenge_history: List[ChallengeRecord] = Field(default_factory=list)
    iteration_count: int = Field(default=0, ge=0)
    max_iterations: int = Field(default=2, ge=1)

    # Final Output
    final_risk_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    final_confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    final_explanation: Optional[str] = None
    recommendations: List[str] = Field(default_factory=list)

    # Risk Analysis
    risk_contributions: Dict[str, float] = Field(default_factory=dict)
    amplification_signals: List[str] = Field(default_factory=list)
    amplification_boost: float = Field(default=0.0, ge=0.0)
    base_risk_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)