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

    def get_newest_readings_for_devices(self, device_ids: list[UUID]) -> dict[UUID, ReadingRow]:
        if not device_ids:
            return {}
        
        subq = (
            self.db.query(ReadingRow)
            .filter(ReadingRow.device_id.in_(device_ids))
            .order_by(ReadingRow.device_id, ReadingRow.recorded_at.desc())
            .distinct(ReadingRow.device_id)
            .subquery()
        )
        reading_rows = self.db.query(ReadingRow).join(
            subq,
            (ReadingRow.device_id == subq.c.device_id) & (ReadingRow.recorded_at == subq.c.recorded_at)
        ).all()

        return {r.device_id: r for r in reading_rows}