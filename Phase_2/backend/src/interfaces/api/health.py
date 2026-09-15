from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal
from src.infrastructure.db import check_db_connection

router = APIRouter()

class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    db: Literal["ok", "fail"]

@router.get("/health", response_model=HealthResponse)
def get_health():
    is_db_ok = check_db_connection()
    return HealthResponse(
        status="ok" if is_db_ok else "degraded",
        db="ok" if is_db_ok else "fail",
    )
