"""Comprehensive test suite for TemperatureController.

Test cases derived using four strategies:
1. Requirement-based: one test per behavior rule
2. Equivalence class partitioning: partition each input domain
3. Boundary value analysis: test min/max/edges of constrained values
4. Error handling / fault injection: test invalid inputs and edge cases
"""

import pytest
from temperature_controller import TemperatureController, Action, ControlResult


# ============================================================================
# STRATEGY 1: REQUIREMENT-BASED TESTING
# Tests one per behavior rule from the design
# ============================================================================


class TestRequirementBased:
    """Tests for explicit behavior rules from the design."""

    def test_idle_to_heat_when_temp_drops_below_lower_bound(self):
        """When idle and temp drops below (target - deadband/2), switch to HEAT."""
        controller = TemperatureController(target_temp=20.0, deadband=4.0)
        # Lower bound: 20.0 - 4.0/2 = 18.0
        # Start idle, drop to 17.9 (below bound)
        result = controller.decide(17.9)
        assert result.action == Action.HEAT
        assert result.state_changed is True

    def test_idle_to_cool_when_temp_rises_above_upper_bound(self):
        """When idle and temp rises above (target + deadband/2), switch to COOL."""
        controller = TemperatureController(target_temp=20.0, deadband=4.0)
        # Upper bound: 20.0 + 4.0/2 = 22.0
        # Start idle, rise to 22.1 (above bound)
        result = controller.decide(22.1)
        assert result.action == Action.COOL
        assert result.state_changed is True

    def test_heating_to_idle_when_temp_reaches_upper_bound(self):
        """When heating and temp reaches (target + deadband/2), switch to IDLE."""
        controller = TemperatureController(target_temp=20.0, deadband=4.0)
        # Upper bound: 22.0
        controller.decide(17.9)  # Start heating
        assert controller.current_action == Action.HEAT
        result = controller.decide(22.0)  # Reach upper bound
        assert result.action == Action.IDLE
        assert result.state_changed is True

    def test_cooling_to_idle_when_temp_drops_to_lower_bound(self):
        """When cooling and temp drops to (target - deadband/2), switch to IDLE."""
        controller = TemperatureController(target_temp=20.0, deadband=4.0)
        # Lower bound: 18.0
        controller.decide(22.1)  # Start cooling
        assert controller.current_action == Action.COOL
        result = controller.decide(18.0)  # Drop to lower bound
        assert result.action == Action.IDLE
        assert result.state_changed is True

    def test_heating_stays_heat_below_upper_bound(self):
        """When heating and temp is still below (target + deadband/2), stay HEAT."""
        controller = TemperatureController(target_temp=20.0, deadband=4.0)
        # Upper bound: 22.0
        controller.decide(17.9)  # Start heating
        result = controller.decide(19.5)  # Still below upper bound
        assert result.action == Action.HEAT
        assert result.state_changed is False

    def test_cooling_stays_cool_above_lower_bound(self):
        """When cooling and temp is still above (target - deadband/2), stay COOL."""
        controller = TemperatureController(target_temp=20.0, deadband=4.0)
        # Lower bound: 18.0
        controller.decide(22.1)  # Start cooling
        result = controller.decide(20.5)  # Still above lower bound
        assert result.action == Action.COOL
        assert result.state_changed is False

    def test_first_call_starts_from_idle(self):
        """First call always starts from IDLE state."""
        controller = TemperatureController(target_temp=20.0, deadband=4.0)
        result = controller.decide(19.5)  # Within bounds
        assert controller.current_action == Action.IDLE
        assert result.state_changed is False


# ============================================================================
# STRATEGY 2: EQUIVALENCE CLASS PARTITIONING
# Partition each input by type/constraints; test one per class
# ============================================================================


class TestEquivalenceClassCurrent:
    """Equivalence classes for currentTemp input."""

    def test_current_temp_well_below_sensor_min(self):
        """Test temp far below sensor range."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        result = controller.decide(-60.0)
        assert result.action == Action.IDLE
        assert result.state_changed is False

    def test_current_temp_well_above_sensor_max(self):
        """Test temp far above sensor range."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        result = controller.decide(160.0)
        assert result.action == Action.IDLE
        assert result.state_changed is False

    def test_current_temp_within_valid_range_cold_side(self):
        """Test temp in valid range, cold side."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        result = controller.decide(10.0)
        assert result.action == Action.HEAT
        assert result.state_changed is True

    def test_current_temp_within_valid_range_warm_side(self):
        """Test temp in valid range, warm side."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        result = controller.decide(30.0)
        assert result.action == Action.COOL
        assert result.state_changed is True

    def test_current_temp_within_deadband(self):
        """Test temp within deadband (no action needed)."""
        controller = TemperatureController(target_temp=20.0, deadband=4.0)
        result = controller.decide(20.0)  # At target
        assert result.action == Action.IDLE
        assert result.state_changed is False


class TestEquivalenceClassTarget:
    """Equivalence classes for targetTemp input."""

    def test_target_temp_at_minimum(self):
        """Test target at 0.0 (clamped minimum)."""
        controller = TemperatureController(target_temp=0.0, deadband=2.0)
        assert controller.target_temp == 0.0
        result = controller.decide(-1.0)
        assert result.action == Action.HEAT

    def test_target_temp_at_maximum(self):
        """Test target at 100.0 (clamped maximum)."""
        controller = TemperatureController(target_temp=100.0, deadband=2.0)
        assert controller.target_temp == 100.0
        result = controller.decide(101.0)
        assert result.action == Action.COOL

    def test_target_temp_below_valid_range(self):
        """Test target below 0.0 (clamped to 0.0)."""
        controller = TemperatureController(target_temp=-10.0, deadband=2.0)
        assert controller.target_temp == 0.0

    def test_target_temp_above_valid_range(self):
        """Test target above 100.0 (clamped to 100.0)."""
        controller = TemperatureController(target_temp=110.0, deadband=2.0)
        assert controller.target_temp == 100.0

    def test_target_temp_nominal(self):
        """Test target in typical range."""
        controller = TemperatureController(target_temp=22.0, deadband=2.0)
        assert controller.target_temp == 22.0


class TestEquivalenceClassDeadband:
    """Equivalence classes for deadband input."""

    def test_deadband_at_minimum(self):
        """Test deadband at 0.5 (minimum valid)."""
        controller = TemperatureController(target_temp=20.0, deadband=0.5)
        assert controller.deadband == 0.5

    def test_deadband_at_maximum(self):
        """Test deadband at 10.0 (maximum valid)."""
        controller = TemperatureController(target_temp=20.0, deadband=10.0)
        assert controller.deadband == 10.0

    def test_deadband_below_minimum(self):
        """Test deadband below 0.5 (clamped to minimum)."""
        controller = TemperatureController(target_temp=20.0, deadband=0.3)
        assert controller.deadband == 0.5

    def test_deadband_above_maximum(self):
        """Test deadband above 10.0 (clamped to maximum)."""
        controller = TemperatureController(target_temp=20.0, deadband=15.0)
        assert controller.deadband == 10.0

    def test_deadband_zero_uses_default(self):
        """Test deadband of 0 uses default (2.0)."""
        controller = TemperatureController(target_temp=20.0, deadband=0.0)
        assert controller.deadband == 2.0

    def test_deadband_negative_uses_default(self):
        """Test negative deadband uses default (2.0)."""
        controller = TemperatureController(target_temp=20.0, deadband=-5.0)
        assert controller.deadband == 2.0

    def test_deadband_nominal(self):
        """Test deadband at typical value (2.0)."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        assert controller.deadband == 2.0


# ============================================================================
# STRATEGY 3: BOUNDARY VALUE ANALYSIS
# Test at min, max, just-below, just-above for constrained values
# ============================================================================


class TestBoundaryValueAnalysis:
    """Boundary tests for all constrained inputs."""

    def test_current_temp_at_sensor_minimum(self):
        """Test currentTemp at -50.0 (sensor minimum)."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        result = controller.decide(-50.0)
        assert result.action == Action.HEAT

    def test_current_temp_just_above_sensor_minimum(self):
        """Test currentTemp at -49.9 (just above sensor minimum)."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        result = controller.decide(-49.9)
        assert result.action == Action.HEAT

    def test_current_temp_just_below_sensor_maximum(self):
        """Test currentTemp at 149.9 (just below sensor maximum)."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        result = controller.decide(149.9)
        assert result.action == Action.COOL

    def test_current_temp_at_sensor_maximum(self):
        """Test currentTemp at 150.0 (sensor maximum)."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        result = controller.decide(150.0)
        assert result.action == Action.COOL

    def test_current_temp_just_below_lower_deadband_boundary(self):
        """Test temp just below lower boundary (triggers heat)."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        # Lower bound = 20.0 - 1.0 = 19.0
        result = controller.decide(18.99)
        assert result.action == Action.HEAT

    def test_current_temp_at_lower_deadband_boundary(self):
        """Test temp at exact lower boundary (no change from idle)."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        # Lower bound = 19.0
        result = controller.decide(19.0)
        assert result.action == Action.IDLE

    def test_current_temp_at_upper_deadband_boundary(self):
        """Test temp at exact upper boundary (no change from idle)."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        # Upper bound = 20.0 + 1.0 = 21.0
        result = controller.decide(21.0)
        assert result.action == Action.IDLE

    def test_current_temp_just_above_upper_deadband_boundary(self):
        """Test temp just above upper boundary (triggers cool)."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        # Upper bound = 21.0
        result = controller.decide(21.01)
        assert result.action == Action.COOL

    def test_target_temp_boundary_minimum(self):
        """Test target at minimum (0.0)."""
        controller = TemperatureController(target_temp=0.0, deadband=2.0)
        result = controller.decide(-1.0)
        assert result.action == Action.HEAT

    def test_target_temp_boundary_maximum(self):
        """Test target at maximum (100.0)."""
        controller = TemperatureController(target_temp=100.0, deadband=2.0)
        result = controller.decide(101.0)
        assert result.action == Action.COOL

    def test_deadband_boundary_minimum(self):
        """Test deadband at minimum (0.5)."""
        controller = TemperatureController(target_temp=20.0, deadband=0.5)
        # Bounds: 19.75 and 20.25
        result = controller.decide(19.74)
        assert result.action == Action.HEAT

    def test_deadband_boundary_maximum(self):
        """Test deadband at maximum (10.0)."""
        controller = TemperatureController(target_temp=20.0, deadband=10.0)
        # Bounds: 15.0 and 25.0
        result = controller.decide(14.9)
        assert result.action == Action.HEAT


# ============================================================================
# STRATEGY 4: ERROR HANDLING AND FAULT INJECTION
# Test explicit error conditions and implicit faults
# ============================================================================


class TestErrorHandlingInvalidSensor:
    """Error handling for out-of-range sensor readings."""

    def test_sensor_reading_below_minimum_returns_idle(self):
        """Out-of-range sensor reading returns IDLE, stateChanged=false."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        result = controller.decide(-51.0)  # Below minimum -50.0
        assert result.action == Action.IDLE
        assert result.state_changed is False

    def test_sensor_reading_above_maximum_returns_idle(self):
        """Out-of-range sensor reading returns IDLE, stateChanged=false."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        result = controller.decide(151.0)  # Above maximum 150.0
        assert result.action == Action.IDLE
        assert result.state_changed is False

    def test_invalid_sensor_does_not_change_state(self):
        """Invalid sensor reading does not change internal state."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        controller.decide(15.0)  # Valid, triggers heat
        assert controller.current_action == Action.HEAT
        controller.decide(-51.0)  # Invalid reading
        assert controller.current_action == Action.HEAT  # State unchanged

    def test_multiple_invalid_readings_before_valid(self):
        """Multiple invalid readings don't affect state or cause transitions."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        controller.decide(15.0)  # Valid, triggers heat
        result1 = controller.decide(-60.0)  # Invalid
        result2 = controller.decide(160.0)  # Invalid
        result3 = controller.decide(19.5)  # Valid, within bounds
        assert result1.action == Action.IDLE
        assert result2.action == Action.IDLE
        assert result3.action == Action.HEAT  # Still heating
        assert result3.state_changed is False


class TestStateTransitions:
    """State machine transition tests."""

    def test_heat_to_cool_transition_requires_crossing_bounds(self):
        """Cannot transition directly HEAT -> COOL without crossing boundaries."""
        controller = TemperatureController(target_temp=20.0, deadband=4.0)
        # Lower: 18.0, Upper: 22.0
        controller.decide(17.9)  # Enter HEAT
        assert controller.current_action == Action.HEAT
        # Try to jump to cool territory (above 22.0)
        result = controller.decide(22.1)
        # From HEAT, we only exit to IDLE (at 22.0), not directly to COOL
        assert result.action == Action.IDLE

    def test_cool_to_heat_transition_requires_crossing_bounds(self):
        """Cannot transition directly COOL -> HEAT without crossing boundaries."""
        controller = TemperatureController(target_temp=20.0, deadband=4.0)
        # Lower: 18.0, Upper: 22.0
        controller.decide(22.1)  # Enter COOL
        assert controller.current_action == Action.COOL
        # Try to jump to heat territory (below 18.0)
        result = controller.decide(17.9)
        # From COOL, we only exit to IDLE (at 18.0), not directly to HEAT
        assert result.action == Action.IDLE

    def test_heat_to_idle_to_cool_sequence(self):
        """Full cycle: IDLE -> HEAT -> IDLE -> COOL."""
        controller = TemperatureController(target_temp=20.0, deadband=4.0)
        # Lower: 18.0, Upper: 22.0

        # 1. Idle -> Heat
        r1 = controller.decide(17.9)
        assert r1.action == Action.HEAT and r1.state_changed

        # 2. Heat -> Idle
        r2 = controller.decide(22.0)
        assert r2.action == Action.IDLE and r2.state_changed

        # 3. Idle -> Cool
        r3 = controller.decide(22.1)
        assert r3.action == Action.COOL and r3.state_changed

        # 4. Cool -> Idle
        r4 = controller.decide(18.0)
        assert r4.action == Action.IDLE and r4.state_changed


class TestStateChangeFlag:
    """Tests for stateChanged flag accuracy."""

    def test_state_changed_true_on_transition(self):
        """stateChanged=true when action changes."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        result = controller.decide(15.0)
        assert result.state_changed is True
        assert controller.current_action == Action.HEAT

    def test_state_changed_false_on_no_transition(self):
        """stateChanged=false when action remains the same."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        controller.decide(15.0)  # Transition to HEAT
        result = controller.decide(14.0)  # Remain HEAT
        assert result.state_changed is False
        assert result.action == Action.HEAT

    def test_state_changed_false_idle_remains_idle(self):
        """stateChanged=false when staying IDLE."""
        controller = TemperatureController(target_temp=20.0, deadband=4.0)
        result = controller.decide(20.0)
        assert result.action == Action.IDLE
        assert result.state_changed is False


class TestEdgeCasesAndRobustness:
    """Additional edge cases for robustness."""

    def test_very_small_deadband(self):
        """Controller works with minimal deadband (0.5)."""
        controller = TemperatureController(target_temp=20.0, deadband=0.5)
        # Lower: 19.75, Upper: 20.25
        result = controller.decide(19.74)
        assert result.action == Action.HEAT

    def test_very_large_deadband(self):
        """Controller works with maximal deadband (10.0)."""
        controller = TemperatureController(target_temp=20.0, deadband=10.0)
        # Lower: 15.0, Upper: 25.0
        result = controller.decide(14.99)
        assert result.action == Action.HEAT

    def test_extreme_target_with_deadband(self):
        """Controller works at temperature range extremes."""
        # Cold extreme
        controller_cold = TemperatureController(target_temp=0.0, deadband=2.0)
        result = controller_cold.decide(-1.1)
        assert result.action == Action.HEAT

        # Hot extreme
        controller_hot = TemperatureController(target_temp=100.0, deadband=2.0)
        result = controller_hot.decide(101.1)
        assert result.action == Action.COOL

    def test_repeated_calls_same_temperature(self):
        """Repeated calls with same temperature maintain state."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        controller.decide(15.0)  # Transition to HEAT
        for _ in range(5):
            result = controller.decide(15.0)
            assert result.action == Action.HEAT
            assert result.state_changed is False

    def test_temperature_oscillation_near_boundary(self):
        """Temperature oscillating near boundary creates state changes."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        # Lower: 19.0, Upper: 21.0
        controller.decide(15.0)  # Enter HEAT
        assert controller.current_action == Action.HEAT

        # Oscillate around upper boundary
        r1 = controller.decide(21.1)  # Cross upper, go IDLE
        assert r1.action == Action.IDLE and r1.state_changed

        r2 = controller.decide(20.9)  # Back below upper, stay IDLE
        assert r2.action == Action.IDLE and not r2.state_changed


class TestResultImmutability:
    """ControlResult is immutable (dataclass frozen)."""

    def test_result_object_is_frozen(self):
        """ControlResult is immutable."""
        result = ControlResult(action=Action.IDLE, state_changed=False)
        with pytest.raises(AttributeError):
            result.action = Action.HEAT


class TestControllerPreservesState:
    """Controller maintains and correctly updates internal state."""

    def test_controller_preserves_action_across_calls(self):
        """Controller remembers its current action."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        controller.decide(15.0)
        assert controller.current_action == Action.HEAT
        controller.decide(14.0)
        assert controller.current_action == Action.HEAT

    def test_controller_target_and_deadband_fixed_after_init(self):
        """Target and deadband don't change after initialization."""
        controller = TemperatureController(target_temp=22.0, deadband=3.0)
        for _ in range(10):
            controller.decide(20.0)
        assert controller.target_temp == 22.0
        assert controller.deadband == 3.0


class TestDefaultValues:
    """Test default configuration values."""

    def test_default_target_is_22_celsius(self):
        """Default target temperature is 22.0."""
        controller = TemperatureController()
        assert controller.target_temp == 22.0

    def test_default_deadband_is_2_degrees(self):
        """Default deadband is 2.0."""
        controller = TemperatureController()
        assert controller.deadband == 2.0

    def test_default_action_is_idle(self):
        """Controller starts in IDLE state."""
        controller = TemperatureController()
        assert controller.current_action == Action.IDLE
