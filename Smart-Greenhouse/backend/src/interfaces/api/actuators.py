from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.infrastructure.db import get_db
from src.infrastructure.persistence.execution_log_repository import ExecutionLogRepository
from src.infrastructure.persistence.actuator_state_repository import ActuatorStateRepository
from src.infrastructure.adapters.actuators.simulation import SimulationActuatorAdapter
from src.infrastructure.adapters.actuators.max_runtime_decorator import MaxRunTimeActuatorDecorator
from src.infrastructure.adapters.actuators.logging_decorator import LoggingActuatorDecorator

router = APIRouter(prefix="/api/actuators", tags=["Actuators"])

class ExecutionLogDto(BaseModel):
    id: UUID
    device_id: UUID
    success: bool
    policy_applied: list[str]
    message: str | None
    created_at: datetime

class ApplyCommandRequest(BaseModel):
    command: str
    payload: dict = {}

def get_decorated_actuator(db: Session = Depends(get_db)) -> LoggingActuatorDecorator:
    sim_adapter = SimulationActuatorAdapter()
    max_runtime = MaxRunTimeActuatorDecorator(sim_adapter, db)
    exec_repo = ExecutionLogRepository(db)
    return LoggingActuatorDecorator(max_runtime, exec_repo)

@router.get("/executions", response_model=list[ExecutionLogDto])
def list_executions(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    repo = ExecutionLogRepository(db)
    rows = repo.list_recent(limit=limit)
    return [
        ExecutionLogDto(
            id=r.id,
            device_id=r.device_id,
            success=r.success,
            policy_applied=r.policy_applied,
            message=r.message,
            created_at=r.created_at,
        )
        for r in rows
    ]

@router.post("/devices/{device_id}/apply", status_code=status.HTTP_200_OK)
def demo_apply_command(
    device_id: UUID,
    payload: ApplyCommandRequest,
    actuator: LoggingActuatorDecorator = Depends(get_decorated_actuator),
):
    try:
        actuator.apply(device_id, payload.command, payload.payload)
        return {"status": "success", "device_id": device_id, "command": payload.command}
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))