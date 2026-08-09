import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.risk_engine import RiskEngine
from observability.agent_monitor import monitor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Analysis"])

engine = RiskEngine()  # single instance


class AnalyzeRequest(BaseModel):
    company_description: str


@router.post("/analyze")
def analyze_company(request: AnalyzeRequest):
    monitor.clear()
    try:
        return engine.analyze_company(request.company_description)
    except Exception:
        # Caught here (inside CORSMiddleware) rather than left to bubble up —
        # an exception that escapes the route entirely skips CORS header
        # injection, so the frontend just sees an opaque "Failed to fetch"
        # instead of a real error.
        logger.exception("Pipeline failed for /api/analyze")
        raise HTTPException(
            status_code=500,
            detail="Risk analysis failed. Please try again.",
        )