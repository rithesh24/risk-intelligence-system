import logging
from datetime import datetime, timezone
from orchestrator.state.state_schema import AgentOutput

logger = logging.getLogger(__name__)


class AgentMonitor:
    def __init__(self):
        self.agent_logs: list[dict] = []
        self.execution_trace: list[dict] = []  

    def log(self, agent_name: str, output: AgentOutput) -> None:
        if output is None:
            return

        errored = output.metadata.get("error", False) if output.metadata else False

        entry = {
            "agent": agent_name,
            "risk_score": output.risk_score,
            "confidence": output.confidence,
            "reasoning": output.reasoning,
            "metadata": output.metadata,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "errored": errored,
        }

        self.agent_logs.append(entry)
        self.execution_trace.append(entry) 
        logger.debug(
            f"[Monitor] {agent_name} — risk={output.risk_score:.2f} "
            f"confidence={output.confidence:.2f}"
        )

    def log_error(self, agent_name: str, error: Exception) -> None:
        """ Logs a hard failure where no AgentOutput was produced."""
        entry = {
            "agent": agent_name,
            "risk_score": None,
            "confidence": None,
            "reasoning": str(error),
            "metadata": {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "errored": True,
        }
        self.agent_logs.append(entry)
        self.execution_trace.append(entry)
        logger.error(f"[Monitor] {agent_name} FAILED — {error}")

    def get_logs(self) -> list[dict]:
        return self.agent_logs

    def get_trace(self) -> list[dict]:
        """ Returns full execution trace including hard failures."""
        return self.execution_trace

    def get_errored_agents(self) -> list[dict]:
        """Returns only logs where agent failed."""
        return [log for log in self.agent_logs if log["errored"]]

    def clear(self) -> None:
        """Reset logs between runs."""
        self.agent_logs = []
        self.execution_trace = []  


monitor = AgentMonitor()