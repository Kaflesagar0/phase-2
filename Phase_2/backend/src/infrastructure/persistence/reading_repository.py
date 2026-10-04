from uuid import UUID
from sqlalchemy.orm import Session
from src.domain.sensors.reading import Reading
from src.infrastructure.persistence.models import ReadingRow

class ReadingRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, reading: Reading) -> ReadingRow:
        row = ReadingRow(
            device_id=reading.device_id,
            value=reading.value,
            unit=reading.unit,
            source=reading.source,
            recorded_at=reading.recorded_at,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def list_recent(self, device_id: UUID, limit: int = 10) -> list[ReadingRow]:
        return (
            self.db.query(ReadingRow)
            .filter(ReadingRow.device_id == device_id)
            .order_by(ReadingRow.recorded_at.desc())
            .limit(limit)
            .all()
        )

    def get_latest(self, device_id: UUID) -> ReadingRow | None:
        return (
            self.db.query(ReadingRow)
            .filter(ReadingRow.device_id == device_id)
            .order_by(ReadingRow.recorded_at.desc())
            .first()
        )