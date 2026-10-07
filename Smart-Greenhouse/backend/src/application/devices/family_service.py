from src.domain.devices.family_factory import get_family_factory
from src.domain.devices.entity import Device
from src.infrastructure.persistence.device_repository import DeviceRepository

class FamilyService:
    def __init__(self, repository: DeviceRepository):
        self.repository= repository

    def provision_family(self, family_key: str) -> list[Device]:
        factory= get_family_factory(family_key)
        devices_to_create = factory.create_device_set()
        return self.repository.save_devices(devices_to_create)

    def list_devices(self, family: str | None = None, role: str | None = None) ->  list[Device]:
        return self.repository.list_devices(family=family, role=role)