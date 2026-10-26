from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.db import get_db
from src.application.overview.facade import LocationOverviewFacade
from src.application.overview.dto import LocationOverviewDto

router = APIRouter(prefix="/api/locations", tags=["Overview"])

@router.get("/{location_id}/overview", response_model=LocationOverviewDto)
def get_location_overview(location_id: UUID, db: Session = Depends(get_db)):
    facade = LocationOverviewFacade(db)
    try:
        return facade.get_overview(location_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")