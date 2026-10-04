from abc import ABC, abstractmethod
from src.domain.sensors.reading import Reading

class SensorPort(ABC):
    @abstractmethod
    def read(self, device) -> Reading:
        pass
    