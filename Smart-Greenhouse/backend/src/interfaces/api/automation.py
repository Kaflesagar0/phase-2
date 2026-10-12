from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.infrastructure.db import get_db
from src.application.automation.dto import StrategyUpsertDto, LocationEvaluationResponseDto
from src.application.automation.services import AutomationService
from src.infrastructure.persistence.location_repository import LocationRepository

router = APIRouter(prefix="/api/locations", tags=["Automation"])

def get_automation_service(db: Session = Depends(get_db)) -> AutomationService:
    return AutomationService(db)

@router.put("/{location_id}/automation/strategy", response_model=dict)
def save_location_strategy(
    location_id: UUID,
    payload: StrategyUpsertDto,
    db: Session = Depends(get_db),
    service: AutomationService = Depends(get_automation_service),
):
    loc_repo= LocationRepository(db)
    if not loc_repo.get_by_id(location_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found.")

    try:
        saved_key = service.save_strategy(location_id, payload.strategy_key)
        return {"location_id": location_id, "strategy_key": saved_key}
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_BAD_REQUEST, detail=str(err))


@router.post("/{location_id}/automation/evaluate", response_model=LocationEvaluationResponseDto)
def evaluate_location_automation(
    location_id: UUID,
    db: Session = Depends(get_db),
    service: AutomationService = Depends(get_automation_service),
):
    loc_repo = LocationRepository(db)
    if not loc_repo.get_by_id(location_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found.")

    try: 
        return service.evaluate_location(location_id)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))