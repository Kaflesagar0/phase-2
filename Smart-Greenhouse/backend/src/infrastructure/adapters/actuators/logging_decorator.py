from uuid import UUID
from src.domain.actuators.ports import ActuatorPort
from src.infrastructure.persistence.execution_log_repository import ExecutionLogRepository

class LoggingActuatorDecorator(ActuatorPort):
    def __init__(self, inner: ActuatorPort, exec_repo: ExecutionLogRepository):
        self.inner = inner
        self.exec_repo = exec_repo

    def apply(self, device_id: UUID, command: str, payload: dict) -> None:
        try:
            self.inner.apply(device_id, command, payload)
            # Successful attempt logs "logging" policy
            self.exec_repo.save(
                device_id=device_id,
                success=True,
                policy_applied=["logging"],
                message=None,
            )
        except Exception as err:
            # If blocked by maxRunTime or another policy, log failure with accumulated policies
            error_msg = str(err)
            policies = ["maxRunTime", "logging"] if "Max run time" in error_msg else ["logging"]
            # Avoid duplicate saves if inner decorator already saved
            if "Max run time" not in error_msg:
                self.exec_repo.save(
                    device_id=device_id,
                    success=False,
                    policy_applied=policies,
                    message=error_msg,
                )
            raise