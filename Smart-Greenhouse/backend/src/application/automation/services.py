from uuid import UUID
from sqlalchemy.orm import Session
from src.infrastructure.persistence.automation_repository import AutomationRepository
from src.domain.automation.strategy import get_strategy
from src.application.automation.dto import LocationEvaluationResponseDto, ZoneRecommendationDto


class AutomationService:
    def __init__(self, db: Session):
        self.repo = AutomationRepository(db)

    def save_strategy(self, location_id: UUID, strategy_key: str) -> str:
        get_strategy(strategy_key)
        return self.repo.upsert_strategy_key(location_id, strategy_key)

    def evaluate_location(self, location_id: UUID)-> LocationEvaluationResponseDto:
        strategy_key = self.repo.get_strategy_key(location_id)
        strategy = get_strategy(strategy_key)
        contexts = self.repo.load_location_contexts(location_id)

        recommendations = []
        for ctx in contexts:
            rec = strategy.decide(ctx)
            recommendations.append(
                ZoneRecommendationDto(
                    zone_id=ctx.zone_id,
                    zone_name=ctx.zone_name,
                    action=rec.action,
                    reason=rec.reason,
                    score=rec.score,
                )
            )
            return LocationEvaluationResponseDto (
                location_id=location_id,
                strategy_key=strategy_key,
                recommendations=recommendations,
            )