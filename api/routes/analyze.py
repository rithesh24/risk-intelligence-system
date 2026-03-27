from fastapi import APIRouter
from pydantic import BaseModel
from services.risk_engine import RiskEngine
from observability.agent_monitor import monitor

router = APIRouter(prefix="/api", tags=["Analysis"])

engine = RiskEngine()  # single instance


class AnalyzeRequest(BaseModel):
    company_description: str


@router.post("/analyze")
def analyze_company(request: AnalyzeRequest):
    monitor.clear() 
    result = engine.analyze_company(request.company_description)
    return result