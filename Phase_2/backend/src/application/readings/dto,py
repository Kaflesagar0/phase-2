from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class ReadingDto(BaseModel):
    id: UUID
    device_id: UUID
    value: float
    unit: str
    source: str
    recorded_at: datetime

    