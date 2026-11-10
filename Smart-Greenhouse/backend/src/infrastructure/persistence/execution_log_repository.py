from uuid import UUID
from sqlalchemy.orm import Session
from src.infrastructure.persistence.models import ActuatorExecutionLogRow

class ExecutionLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(
        self,
        device_id: UUID,
        success: bool,
        policy_applied: list[str],
        message: str | None = None,
    ) -> ActuatorExecutionLogRow:
        row = ActuatorExecutionLogRow(
            device_id=device_id,
            success=success,
            policy_applied=policy_applied,
            message=message,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def list_recent(self, limit: int = 20) -> list[ActuatorExecutionLogRow]:
        return (
            self.db.query(ActuatorExecutionLogRow)
            .order_by(ActuatorExecutionLogRow.created_at.desc())
            .limit(limit)
            .all()
        )