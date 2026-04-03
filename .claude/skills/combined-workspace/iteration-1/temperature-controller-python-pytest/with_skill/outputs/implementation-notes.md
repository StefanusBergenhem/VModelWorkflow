# Temperature Controller Implementation Notes

## Design Compliance

The implementation faithfully follows the design specification with the following deliberate architectural choices:

### 1. Pure Domain Logic with No Infrastructure Dependencies

**Decision:** Placed all business logic in `TemperatureController` class with zero imports of I/O, database, HTTP, or framework packages.

**Rationale:** Enables isolated testing, deterministic behavior, and clear V-model traceability. The unit can be used in any context (embedded, web, desktop) without modification.

**Trade-off:** Logging is used only for warning messages (invalid sensor readings). The logger is injected from the standard library and can be redirected by the caller without changing domain code.

### 2. State Management

**Decision:** Controller maintains `_current_action` as internal state, updated deterministically after each `decide()` call.

**Rationale:** 
- Hysteresis (deadband) requires history—the next action depends on the previous action, not just the current temperature
- State is encapsulated: only modified internally, only read through `current_action` property
- No race conditions because Python's GIL ensures atomic updates for simple assignments

**Implementation Detail:** State transitions follow explicit rules:
- From IDLE: move to HEAT/COOL only if temperature crosses deadband boundary
- From HEAT: return to IDLE only when upper boundary crossed; cannot jump directly to COOL
- From COOL: return to IDLE only when lower boundary crossed; cannot jump directly to HEAT

### 3. Deadband Hysteresis

**Decision:** Computed dynamically per `decide()` call based on formula:
- Lower boundary = `target - deadband/2`
- Upper boundary = `target + deadband/2`

**Rationale:** 
- Matches the design's explicit behavior rules exactly
- Symmetric around target (standard hysteresis pattern)
- Simple to understand and verify
- No accumulated error or floating-point pitfalls

**Example:** With target=20°C and deadband=4°C:
- Lower = 18°C, Upper = 22°C
- From IDLE: heat if < 18°C, cool if > 22°C, stay if between
- From HEAT: stay if < 22°C, return to IDLE if ≥ 22°C
- From COOL: stay if > 18°C, return to IDLE if ≤ 18°C

### 4. Input Validation and Clamping Strategy

**Decision:** Separate validation into two categories:

**A. Clamping (correctable errors):**
- `targetTemp`: out of [0, 100] → clamped to nearest valid value
- `deadband`: out of [0.5, 10.0] → clamped to nearest valid value
- `deadband` ≤ 0 → use default 2.0

**B. Rejection (non-recoverable errors):**
- `currentTemp`: out of [-50, 150] → return IDLE with stateChanged=false, do NOT update internal state

**Rationale:**
- Configuration errors (target, deadband) are correctable without losing history
- Sensor errors (out-of-range current temp) are transient and should not poison state
- The design requires logging warnings for invalid sensor readings; we do this at the `decide()` boundary
- Rejecting invalid sensor data prevents the system from making decisions on corrupted input

### 5. Result Object Design

**Decision:** Immutable `ControlResult` dataclass with frozen=True.

```python
@dataclass(frozen=True)
class ControlResult:
    action: Action
    state_changed: bool
```

**Rationale:**
- Prevents accidental mutation by caller
- Makes it clear that results are snapshots, not references to mutable state
- `stateChanged` flag is a primary contract: true if action differs from previous call
- No null returns: always returns a valid result (IDLE with state_changed=false for errors)

### 6. Error Handling: No Null Returns

**Decision:** Every code path returns a valid `ControlResult`. No null/None returns.

**Rationale:** 
- Matches the error handling rule: "Never return null"
- Simplifies caller code (no null checks needed)
- Logged warning informs about invalid sensor readings
- Return value semantically encodes the error: action=IDLE, stateChanged=false clearly signals "no action taken"

### 7. Complexity Metrics

**Function Breakdown:**
- `decide()`: 12 lines → straightforward validation, delegation
- `_compute_action()`: 22 lines → state machine with 3 branches (one per action state)
- `_is_valid_sensor_reading()`: 1 line → simple range check
- `_clamp_target()`: 1 line → standard clamp formula
- `_clamp_deadband()`: 3 lines → includes zero/negative check
- Properties (4): trivial getters

**Cyclomatic Complexity:**
- `_compute_action()`: 4 (three if/elif branches for state, each with nested conditions)
- All others: 1-2
- Overall: Straightforward, testable

**Nesting Depth:** Maximum 2 levels (if within if within method) — well under the 3-level limit.

**No Dead Code:** Every function is reachable, every branch is tested. The design specifies all behaviors; no speculative abstractions.

### 8. Naming Conventions

**Python Conventions Applied:**
- Class name: `TemperatureController` (noun, clear intent)
- Public methods: `decide()` (verb, action-oriented)
- Private methods: `_compute_action()`, `_is_valid_sensor_reading()`, etc. (underscore prefix per Python convention)
- Constants: `SENSOR_MIN`, `TARGET_MAX`, etc. (UPPERCASE)
- Enum: `Action` (distinct states: HEAT, COOL, IDLE)
- Properties: `current_action`, `target_temp`, `deadband` (clear getters, no Hungarian notation)
- Data class: `ControlResult` (noun, self-describing)

**Domain Vocabulary:** Uses terms directly from the design: "deadband," "hysteresis," "action," "stateChanged," "target," "sensor," "heating," "cooling," "idle."

### 9. Initialization and Configuration

**Decision:** All configuration happens in `__init__()`. The object is then immutable to its caller.

```python
def __init__(self, target_temp=22.0, deadband=2.0):
    self._target_temp = self._clamp_target(target_temp)
    self._deadband = self._clamp_deadband(deadband)
    self._current_action = Action.IDLE
```

**Rationale:**
- No setters: once created, the controller's configuration is fixed
- Enables clamping and validation once, at initialization
- Simplifies reasoning about state (no surprise parameter changes during operation)
- Properties provide read-only access for inspection

### 10. Temperature Precision and Floating-Point

**Design Requirement:** Temperatures are floats; comparisons are direct (no epsilon tolerance).

**Implementation:** We use direct `<`, `>`, `<=`, `>=` comparisons as specified. The design boundaries are explicit:
- "below" = `<` (strictly less than)
- "above" = `>` (strictly greater than)
- "at" / "reaches" = `>=` or `<=` (inclusive)

**Example from design:**
- "temperature drops below (target - deadband/2)" → `current_temp < lower_bound`
- "temperature reaches (target + deadband/2)" → `current_temp >= upper_bound`

This matches the test derivation (boundary value analysis at exact limits).

## Testing Approach

The test suite uses four derivation strategies:

1. **Requirement-Based (7 tests):** One per behavior rule from the design. Verifies state machine transitions.
2. **Equivalence Class Partitioning (17 tests):** Partitions each input (currentTemp, targetTemp, deadband) into valid/invalid classes. Tests one per class.
3. **Boundary Value Analysis (10 tests):** Tests at min, max, just-below, just-above for all constrained values.
4. **Error Handling & Fault Injection (11+ tests):** Invalid sensor readings, state isolation, extreme values, oscillation near boundaries.

**Key Test Insights:**
- `test_heat_to_cool_transition_requires_crossing_bounds()` verifies that the state machine cannot transition directly HEAT→COOL; it must pass through IDLE. This is the hysteresis guarantee.
- `test_invalid_sensor_does_not_change_state()` verifies that invalid input doesn't corrupt state—a critical robustness property.
- `test_sensor_reading_below_minimum_returns_idle()` and above verify that out-of-range sensor readings are safely ignored.
- Boundary tests at exactly -50°C, 150°C, and deadband boundaries ensure edge-case correctness.

## Design Elements Traced to Code

| Design Element | Implementation |
|---|---|
| "Monitors temperature readings from a sensor" | `decide(current_temp)` method |
| "Compares against target temperature" | `_compute_action()` uses `_target_temp` |
| "Deadband (hysteresis)" | `lower_bound = target - deadband/2`, `upper_bound = target + deadband/2` |
| "Tracks current state" | `_current_action` field |
| "Prevents rapid toggling" | State machine only exits HEAT at upper bound, COOL at lower bound |
| "First call starts from IDLE" | `_current_action = Action.IDLE` in `__init__()` |
| "currentTemp: -50 to 150" | `SENSOR_MIN = -50.0`, `SENSOR_MAX = 150.0`, validated in `_is_valid_sensor_reading()` |
| "targetTemp: 0 to 100" | `TARGET_MIN = 0.0`, `TARGET_MAX = 100.0`, clamped in `_clamp_target()` |
| "deadband: min 0.5, max 10.0" | `DEADBAND_MIN = 0.5`, `DEADBAND_MAX = 10.0`, clamped in `_clamp_deadband()` |
| "Default deadband: 2.0" | `DEFAULT_DEADBAND = 2.0`, used in `_clamp_deadband()` |
| "Default target: 22.0" | `DEFAULT_TARGET_TEMP = 22.0` in `__init__()` |
| "Returns action: HEAT, COOL, or IDLE" | `Action` enum, returned in `ControlResult.action` |
| "Returns stateChanged" | `ControlResult.state_changed` computed as `new_action != self._current_action` |
| "Invalid sensor: log warning, return IDLE with stateChanged=false" | `logger.warning()` and `return ControlResult(IDLE, False)` in `decide()` |
| "targetTemp outside valid range: clamp" | `_clamp_target()` |
| "deadband outside valid range: clamp" | `_clamp_deadband()` |
| "deadband zero or negative: use default" | `if value <= 0: return DEFAULT_DEADBAND` in `_clamp_deadband()` |

## Potential Extensions (Out of Scope)

These are NOT implemented because they're not in the design:
- Thread-safety (no explicit requirement)
- Configuration changes after initialization (immutable by design)
- Persistence or serialization
- Sensor filtering or smoothing (accepts raw readings)
- Integral/derivative control (simple hysteresis only)
- Recovery from permanent sensor failure
- Efficiency optimizations (already O(1) per call)

## Build and Run Instructions

**Prerequisites:**
- Python 3.7+
- pytest

**Run tests:**
```bash
pytest test_temperature_controller.py -v
```

**Run tests with coverage:**
```bash
pytest test_temperature_controller.py --cov=temperature_controller --cov-report=term-missing
```

**Import in your code:**
```python
from temperature_controller import TemperatureController, Action, ControlResult

controller = TemperatureController(target_temp=22.0, deadband=2.0)
result = controller.decide(19.5)
print(result.action)  # Action.HEAT or Action.COOL or Action.IDLE
print(result.state_changed)  # True or False
```
