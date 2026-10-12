# Strategy Pattern

## Problem
In a smart greenhouse, irrigation and climate control decisions depend on variable algorithms (e.g., conservative watering vs. aggressive threshold tracking). Hardcoding decision logic with conditional statements (`if strategy == "conservative"`) inside API routers or services leads to tightly coupled, rigid code that is difficult to test or extend.

## Solution
The Strategy Pattern defines a common interface (`AutomationStrategy`) with a `decide(context)` method. Concrete strategy classes (`ConservativeMoistureStrategy`, `AggressiveMoistureStrategy`) encapsulate specific algorithms. The application service selects the active strategy based on persisted configuration, keeping business logic pure and polymorphic.

## Code Map
- `src/domain/automation/strategy.py`: Abstract `AutomationStrategy` interface and concrete strategies.
- `src/domain/automation/context.py`: `LocationAutomationContext` value object.
- `src/application/automation/service.py`: Orchestrates loading context, resolving strategy, and returning recommendations.
- `src/interfaces/api/automation.py`: Exposes endpoints for saving strategy preferences and running evaluations.

## Extension Exercise: Adding a Third Strategy
1. Create a new class `TimeBasedStrategy(AutomationStrategy)` in `src/domain/automation/strategy.py` implementing `decide(context)`.
2. Register `"time_based"` in `get_strategy()`.
3. The API and frontend dropdown will instantly support the new strategy without changing evaluation route handlers.