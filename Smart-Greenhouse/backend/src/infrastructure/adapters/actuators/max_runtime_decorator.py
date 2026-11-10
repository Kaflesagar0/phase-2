from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.orm import Session
from src.domain.actuators.ports import ActuatorPort
from src.infrastructure.persistence.actuator_state_repository import ActuatorStateRepository
from src.infrastructure.persistence.execution_log_repository import ExecutionLogRepository

class MaxRunTimeActuatorDecorator(ActuatorPort):
    def __init__(
        self,
        inner: ActuatorPort,
        db: Session,
        max_minutes: int = 30,
    ):
        self.inner = inner
        self.db = db
        self.max_minutes = max_minutes
        self.state_repo = ActuatorStateRepository(db)
        self.exec_repo = ExecutionLogRepository(db)

    def apply(self, device_id: UUID, command: str, payload: dict) -> None:
        state_row = self.state_repo.get_or_create(device_id)
        
        # If currently running, check how long it has been running
        if state_row.state == "running":
            now = datetime.now(timezone.utc)
            updated_at = state_row.updated_at
            if updated_at.tzinfo is None:
                updated_at = updated_at.replace(tzinfo=timezone.utc)
            
            elapsed_minutes = (now - updated_at).total_seconds() / 60.0
            if elapsed_minutes >= self.max_minutes:
                # Block execution and record failure with maxRunTime policy
                self.exec_repo.save(
                    device_id=device_id,
                    success=False,
                    policy_applied=["maxRunTime"],
                    message="Max run time exceeded",
                )
                raise ValueError("Max run time exceeded")

        # Delegate to inner adapter if policy passes
        self.inner.apply(device_id, command, payload)