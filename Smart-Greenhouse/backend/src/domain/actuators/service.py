from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.domain.actuators.state import validate_transition, get_allowed_commands, IllegalTransitionError
from src.domain.actuators.content import ActuatorContext
from src.infrastructure.persistence.actuator_state_repository import ActuatorStateRepository
from src.infrastructure.persistence.models import DeviceRow

class ActuatorStateService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ActuatorStateRepository(db)

    def get_actuator_context(self, device_id: UUID) -> ActuatorContext:
        device = self.db.query(DeviceRow).filter(DeviceRow.id == device_id).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        if device.role != "actuator":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Device is not an actuator")

        state_row = self.repo.get_or_create(device_id)
        current_state = state_row.state
        allowed_commands = get_allowed_commands(current_state)

        return ActuatorContext(
            device_id=device_id,
            current_state=current_state,
            allowed_commands=allowed_commands,
        )

    def transition_state(self, device_id: UUID, target_state: str) -> ActuatorContext:
        device = self.db.query(DeviceRow).filter(DeviceRow.id == device_id).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        if device.role != "actuator":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Device is not an actuator")

        state_row = self.repo.get_or_create(device_id)
        current_state = state_row.state

        try:
            # Domain guard validation (raises IllegalTransitionError if invalid)
            validate_transition(current_state, target_state)
        except IllegalTransitionError as err:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(err)
            )

        # Persist the new state only if valid
        updated_row = self.repo.update_state(device_id, target_state)
        allowed_commands = get_allowed_commands(updated_row.state)

        return ActuatorContext(
            device_id=device_id,
            current_state=updated_row.state,
            allowed_commands=allowed_commands,
        )