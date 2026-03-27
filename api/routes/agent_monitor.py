from fastapi import APIRouter
from observability.agent_monitor import monitor

router = APIRouter(prefix="/observability", tags=["Observability"])


@router.get("/agent-logs")
def get_agent_logs():
    return monitor.get_logs()


@router.get("/agent-logs/errors")
def get_errored_agents():
    return monitor.get_errored_agents()


@router.get("/execution-trace")
def get_execution_trace():
    """Returns full execution trace including hard failures."""
    return {"execution_trace": monitor.get_trace()}


@router.delete("/agent-logs")
def clear_agent_logs():
    monitor.clear()
    return {"message": "Agent logs cleared"}