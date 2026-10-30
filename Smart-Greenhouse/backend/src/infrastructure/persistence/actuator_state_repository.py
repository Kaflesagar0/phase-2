from uuid import UUID
from sqlalchemy.orm import Session
from src.infrastructure.persistence.models import ActuatorStateRow

class ActuatorStateRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create(self, device_id: UUID) -> ActuatorStateRow:
        row = self.db.query(ActuatorStateRow).filter(ActuatorStateRow.device_id == device_id).first()
        if not row:
            row = ActuatorStateRow(device_id=device_id, state="idle")
            self.db.add(row)
            self.db.commit()
            self.db.refresh(row)
        return row

    def update_state(self, device_id: UUID, new_state: str) -> ActuatorStateRow:
        row = self.get_or_create(device_id)
        row.state = new_state
        self.db.commit()
        self.db.refresh(row)
        return row