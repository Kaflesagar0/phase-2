from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.domain.automation.context import LocationAutomationContext

@dataclass(frozen=True)
class Recommendation:
    action: str  
    reason: str
    score: float | None = None

class AutomationStrategy(ABC):
    @abstractmethod
    def decide(self, context: LocationAutomationContext) -> Recommendation:
        pass

class ConservativeMoistureStrategy(AutomationStrategy):
    """Conservative strategy: waits longer before irrigating, cautious of overwatering."""
    def decide(self, context: LocationAutomationContext) -> Recommendation:
        if not context.has_moisture_sensor or context.latest_moisture is None:
            return Recommendation(
                action="wait",
                reason=f"No moisture sensor assigned in zone '{context.zone_name}'."
            )
        
        
        trigger_limit = context.threshold_low * 0.9
        if context.latest_moisture < trigger_limit:
            return Recommendation(
                action="irrigate",
                reason=f"Moisture ({context.latest_moisture}) is below conservative trigger limit ({trigger_limit:.2f}).",
                score=context.latest_moisture
            )
        return Recommendation(
            action="wait",
            reason=f"Moisture ({context.latest_moisture}) is within safe conservative range.",
            score=context.latest_moisture
        )

class AggressiveMoistureStrategy(AutomationStrategy):
    """Aggressive strategy: maintains strict moisture levels close to the low threshold."""
    def decide(self, context: LocationAutomationContext) -> Recommendation:
        if not context.has_moisture_sensor or context.latest_moisture is None:
            return Recommendation(
                action="wait",
                reason=f"No moisture sensor assigned in zone '{context.zone_name}'."
            )
        
        
        if context.latest_moisture <= context.threshold_low:
            return Recommendation(
                action="irrigate",
                reason=f"Moisture ({context.latest_moisture}) is at or below aggressive threshold ({context.threshold_low}).",
                score=context.latest_moisture
            )
        return Recommendation(
            action="wait",
            reason=f"Moisture ({context.latest_moisture}) satisfies aggressive threshold requirements.",
            score=context.latest_moisture
        )

def get_strategy(strategy_key: str) -> AutomationStrategy:
    key = strategy_key.lower().strip()
    if key == "conservative":
        return ConservativeMoistureStrategy()
    elif key == "aggressive":
        return AggressiveMoistureStrategy()
    raise ValueError(f"Unknown strategy key '{strategy_key}'.")