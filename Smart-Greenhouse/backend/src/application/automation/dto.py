from uuid import UUID
from pydantic import BaseModel, Field

class StrategyUpsertDto(BaseModel):
    strategy_key: str = Field(..., min_length=1)

class ZoneRecommendationDto(BaseModel):
    zone_id: UUID
    zone_name: str
    action: str
    reason: str
    score: float | None = None

class LocationEvaluationResponseDto(BaseModel):
    location_id: UUID
    strategy_key: str
    recommendations: list[ZoneRecommendationDto]