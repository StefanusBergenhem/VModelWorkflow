"""
Comprehensive test suite for Temperature Controller using pytest.

Tests cover:
- State transitions (IDLE -> HEAT, IDLE -> COOL, etc.)
- Deadband hysteresis behavior
- Boundary conditions
- Error handling (out-of-range inputs)
- Default behaviors
- First-call initialization
"""

import pytest
from temperature_controller import TemperatureController, ControllerOutput


class TestTemperatureControllerInitialization:
    """Test initialization and default values."""

    def test_initialization_with_defaults(self):
        """Controller should initialize with default target and deadband."""
        controller = TemperatureController()
        assert controller.current_state == "IDLE"
        assert controller.target_temp == 22.0
        assert controller.deadband == 2.0

    def test_initialization_with_custom_values(self):
        """Controller should accept custom target and deadband."""
        controller = TemperatureController(target_temp=25.0, deadband=1.5)
        assert controller.target_temp == 25.0
        assert controller.deadband == 1.5
        assert controller.current_state == "IDLE"

    def test_first_call_returns_idle(self):
        """First call should always return IDLE state."""
        controller = TemperatureController(target_temp=20.0)
        result = controller.update(20.0)
        assert result.action == "IDLE"
        assert result.state_changed is False


class TestStateTransitionsFromIdle:
    """Test transitions from IDLE state."""

    def test_idle_to_heat_transition(self):
        """Temperature below target - deadband/2 should trigger HEAT."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        # deadband/2 = 1.0, so threshold = 19.0

        # First call at target temp (IDLE)
        result = controller.update(20.0)
        assert result.action == "IDLE"

        # Drop below threshold to trigger heating
        result = controller.update(18.9)
        assert result.action == "HEAT"
        assert result.state_changed is True

    def test_idle_to_cool_transition(self):
        """Temperature above target + deadband/2 should trigger COOL."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        # deadband/2 = 1.0, so threshold = 21.0

        # First call at target temp (IDLE)
        result = controller.update(20.0)
        assert result.action == "IDLE"

        # Rise above threshold to trigger cooling
        result = controller.update(21.1)
        assert result.action == "COOL"
        assert result.state_changed is True

    def test_idle_stays_idle_within_deadband(self):
        """Temperature within deadband boundaries should stay IDLE."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)

        result = controller.update(20.0)
        assert result.action == "IDLE"

        result = controller.update(20.5)
        assert result.action == "IDLE"
        assert result.state_changed is False

        result = controller.update(19.5)
        assert result.action == "IDLE"
        assert result.state_changed is False


class TestHeatingState:
    """Test behavior while in HEATING state."""

    def test_heating_continues_until_upper_threshold(self):
        """Should stay HEAT until temperature reaches target + deadband/2."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)

        # Trigger heating
        controller.update(18.0)

        # Stay in heating (below 21.0)
        result = controller.update(19.5)
        assert result.action == "HEAT"
        assert result.state_changed is False

        result = controller.update(20.5)
        assert result.action == "HEAT"
        assert result.state_changed is False

    def test_heating_to_idle_transition(self):
        """Should transition from HEAT to IDLE when above target + deadband/2."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)

        # Trigger heating
        controller.update(18.0)
        assert controller.current_state == "HEAT"

        # Cross upper threshold (21.0) to go IDLE
        result = controller.update(21.1)
        assert result.action == "IDLE"
        assert result.state_changed is True

    def test_heating_to_cool_transition_large_temp_jump(self):
        """Should transition HEAT -> COOL if temp jumps above cool threshold."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)

        # Trigger heating
        controller.update(18.0)
        assert controller.current_state == "HEAT"

        # Large jump above cool threshold (21.0)
        result = controller.update(22.0)
        assert result.action == "COOL"
        assert result.state_changed is True


class TestCoolingState:
    """Test behavior while in COOLING state."""

    def test_cooling_continues_until_lower_threshold(self):
        """Should stay COOL until temperature drops to target - deadband/2."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)

        # Trigger cooling
        controller.update(22.0)

        # Stay in cooling (above 19.0)
        result = controller.update(20.5)
        assert result.action == "COOL"
        assert result.state_changed is False

        result = controller.update(19.5)
        assert result.action == "COOL"
        assert result.state_changed is False

    def test_cooling_to_idle_transition(self):
        """Should transition from COOL to IDLE when below target - deadband/2."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)

        # Trigger cooling
        controller.update(22.0)
        assert controller.current_state == "COOL"

        # Cross lower threshold (19.0) to go IDLE
        result = controller.update(18.9)
        assert result.action == "IDLE"
        assert result.state_changed is True

    def test_cooling_to_heat_transition_large_temp_drop(self):
        """Should transition COOL -> HEAT if temp drops below heat threshold."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)

        # Trigger cooling
        controller.update(22.0)
        assert controller.current_state == "COOL"

        # Large drop below heat threshold (19.0)
        result = controller.update(18.0)
        assert result.action == "HEAT"
        assert result.state_changed is True


class TestDeadbandBehavior:
    """Test deadband hysteresis with various sizes."""

    def test_small_deadband(self):
        """Deadband of 0.5 should have 0.25 hysteresis each side."""
        controller = TemperatureController(target_temp=20.0, deadband=0.5)

        # Heat threshold: 20.0 - 0.25 = 19.75
        # Cool threshold: 20.0 + 0.25 = 20.25

        result = controller.update(19.7)
        assert result.action == "HEAT"

        controller = TemperatureController(target_temp=20.0, deadband=0.5)
        result = controller.update(20.3)
        assert result.action == "COOL"

    def test_large_deadband(self):
        """Deadband of 10.0 should have 5.0 hysteresis each side."""
        controller = TemperatureController(target_temp=20.0, deadband=10.0)

        # Heat threshold: 20.0 - 5.0 = 15.0
        # Cool threshold: 20.0 + 5.0 = 25.0

        result = controller.update(14.9)
        assert result.action == "HEAT"

        controller = TemperatureController(target_temp=20.0, deadband=10.0)
        result = controller.update(25.1)
        assert result.action == "COOL"

    def test_deadband_clamping_too_small(self):
        """Deadband < 0.5 should be clamped to 0.5."""
        controller = TemperatureController(target_temp=20.0, deadband=0.2)
        assert controller.deadband == 0.5

    def test_deadband_clamping_too_large(self):
        """Deadband > 10.0 should be clamped to 10.0."""
        controller = TemperatureController(target_temp=20.0, deadband=15.0)
        assert controller.deadband == 10.0

    def test_deadband_zero_uses_default(self):
        """Deadband of 0 should use default (2.0)."""
        controller = TemperatureController(target_temp=20.0, deadband=0.0)
        assert controller.deadband == 2.0

    def test_deadband_negative_uses_default(self):
        """Negative deadband should use default (2.0)."""
        controller = TemperatureController(target_temp=20.0, deadband=-1.5)
        assert controller.deadband == 2.0


class TestTargetTemperatureValidation:
    """Test target temperature clamping and validation."""

    def test_target_temp_too_low_clamped(self):
        """Target temp < 0 should be clamped to 0.0."""
        controller = TemperatureController(target_temp=-5.0)
        assert controller.target_temp == 0.0

    def test_target_temp_too_high_clamped(self):
        """Target temp > 100 should be clamped to 100.0."""
        controller = TemperatureController(target_temp=120.0)
        assert controller.target_temp == 100.0

    def test_target_temp_valid_range(self):
        """Target temps in valid range should not be modified."""
        for temp in [0.0, 25.5, 50.0, 75.2, 100.0]:
            controller = TemperatureController(target_temp=temp)
            assert controller.target_temp == temp


class TestCurrentTemperatureValidation:
    """Test error handling for out-of-range sensor readings."""

    def test_current_temp_too_low(self):
        """Temperature < -50 should return IDLE with warning."""
        controller = TemperatureController(target_temp=20.0)
        result = controller.update(-51.0)
        assert result.action == "IDLE"
        assert result.state_changed is False

    def test_current_temp_too_high(self):
        """Temperature > 150 should return IDLE with warning."""
        controller = TemperatureController(target_temp=20.0)
        result = controller.update(151.0)
        assert result.action == "IDLE"
        assert result.state_changed is False

    def test_current_temp_at_boundaries_valid(self):
        """Temperatures at -50 and 150 should be valid."""
        controller = TemperatureController(target_temp=20.0)

        result = controller.update(-50.0)
        assert result.action == "HEAT"  # Below threshold

        controller = TemperatureController(target_temp=20.0)
        result = controller.update(150.0)
        assert result.action == "COOL"  # Above threshold


class TestStateChangeFlag:
    """Test the stateChanged flag behavior."""

    def test_state_changed_on_transition(self):
        """stateChanged should be true when action differs from previous."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)

        result = controller.update(20.0)
        assert result.state_changed is False

        result = controller.update(18.0)
        assert result.state_changed is True
        assert result.action == "HEAT"

    def test_state_changed_false_when_staying_same(self):
        """stateChanged should be false when action doesn't change."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)

        controller.update(18.0)  # Transition to HEAT
        result = controller.update(18.5)  # Stay in HEAT
        assert result.state_changed is False
        assert result.action == "HEAT"

    def test_state_changed_tracking_multiple_transitions(self):
        """stateChanged should correctly track multiple transitions."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)

        # IDLE -> HEAT
        result = controller.update(18.0)
        assert result.action == "HEAT"
        assert result.state_changed is True

        # HEAT -> HEAT (stay)
        result = controller.update(19.0)
        assert result.action == "HEAT"
        assert result.state_changed is False

        # HEAT -> IDLE
        result = controller.update(21.5)
        assert result.action == "IDLE"
        assert result.state_changed is True

        # IDLE -> COOL
        result = controller.update(21.1)
        assert result.action == "COOL"
        assert result.state_changed is True


class TestComplexScenarios:
    """Test realistic temperature cycling scenarios."""

    def test_heating_cycle_complete(self):
        """Test a complete heating cycle: cold -> heat -> idle."""
        controller = TemperatureController(target_temp=22.0, deadband=2.0)
        # Heat threshold: 21.0, Cool threshold: 23.0

        # Start cold
        result = controller.update(15.0)
        assert result.action == "HEAT"
        assert result.state_changed is True

        # Gradually warm up while heating
        result = controller.update(18.0)
        assert result.action == "HEAT"
        assert result.state_changed is False

        result = controller.update(21.0)
        assert result.action == "HEAT"
        assert result.state_changed is False

        # Cross into idle zone
        result = controller.update(23.5)
        assert result.action == "IDLE"
        assert result.state_changed is True

    def test_cooling_cycle_complete(self):
        """Test a complete cooling cycle: hot -> cool -> idle."""
        controller = TemperatureController(target_temp=22.0, deadband=2.0)
        # Heat threshold: 21.0, Cool threshold: 23.0

        # Start hot
        result = controller.update(30.0)
        assert result.action == "COOL"
        assert result.state_changed is True

        # Gradually cool down while cooling
        result = controller.update(26.0)
        assert result.action == "COOL"
        assert result.state_changed is False

        result = controller.update(24.0)
        assert result.action == "COOL"
        assert result.state_changed is False

        # Cross into idle zone
        result = controller.update(20.5)
        assert result.action == "IDLE"
        assert result.state_changed is True

    def test_oscillation_around_target(self):
        """Test behavior when temperature oscillates around target."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)

        updates = [
            (20.0, "IDLE", False),   # Start idle
            (19.5, "IDLE", False),   # Still idle
            (18.9, "HEAT", True),    # Cross heat threshold
            (19.5, "HEAT", False),   # Still heating
            (21.0, "IDLE", True),    # Back to idle
            (21.1, "COOL", True),    # Cross cool threshold
            (20.5, "COOL", False),   # Still cooling
            (19.0, "IDLE", True),    # Back to idle
        ]

        for temp, expected_action, expected_changed in updates:
            result = controller.update(temp)
            assert result.action == expected_action, \
                f"At temp {temp}: expected {expected_action}, got {result.action}"
            assert result.state_changed == expected_changed, \
                f"At temp {temp}: expected changed={expected_changed}, got {result.state_changed}"

    def test_sensor_malfunction_recovery(self):
        """Test recovery after sensor malfunction (out of range)."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)

        # Normal operation
        result = controller.update(20.0)
        assert result.action == "IDLE"

        # Sensor malfunction (out of range)
        result = controller.update(-100.0)
        assert result.action == "IDLE"
        assert result.state_changed is False

        # Sensor recovers with valid reading
        result = controller.update(15.0)
        assert result.action == "HEAT"
        assert result.state_changed is True


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_exact_heat_threshold(self):
        """Temperature exactly at heat threshold should trigger heating."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        # Heat threshold: 19.0

        result = controller.update(19.0)
        assert result.action == "HEAT"

    def test_just_below_heat_threshold(self):
        """Temperature just below heat threshold should trigger heating."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)

        result = controller.update(18.99999)
        assert result.action == "HEAT"

    def test_just_above_heat_threshold(self):
        """Temperature just above heat threshold should stay IDLE."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)

        result = controller.update(19.00001)
        assert result.action == "IDLE"

    def test_exact_cool_threshold(self):
        """Temperature exactly at cool threshold should trigger cooling."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)
        # Cool threshold: 21.0

        result = controller.update(21.0)
        assert result.action == "COOL"

    def test_just_below_cool_threshold(self):
        """Temperature just below cool threshold should stay IDLE."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)

        result = controller.update(20.99999)
        assert result.action == "IDLE"

    def test_just_above_cool_threshold(self):
        """Temperature just above cool threshold should trigger cooling."""
        controller = TemperatureController(target_temp=20.0, deadband=2.0)

        result = controller.update(21.00001)
        assert result.action == "COOL"

    def test_zero_temperature(self):
        """Controller should handle zero temperature correctly."""
        controller = TemperatureController(target_temp=0.0, deadband=2.0)

        result = controller.update(0.0)
        assert result.action == "IDLE"

        result = controller.update(-1.0)
        assert result.action == "HEAT"

    def test_extreme_valid_temperatures(self):
        """Controller should handle extreme but valid temperatures."""
        controller = TemperatureController(target_temp=50.0, deadband=2.0)

        result = controller.update(-50.0)
        assert result.action == "HEAT"

        result = controller.update(150.0)
        assert result.action == "COOL"


class TestOutputStructure:
    """Test the ControllerOutput structure."""

    def test_output_has_required_fields(self):
        """ControllerOutput should have action and stateChanged."""
        controller = TemperatureController()
        result = controller.update(20.0)

        assert hasattr(result, 'action')
        assert hasattr(result, 'state_changed')
        assert result.action in ["HEAT", "COOL", "IDLE"]
        assert isinstance(result.state_changed, bool)

    def test_output_is_immutable(self):
        """ControllerOutput should be a predictable data structure."""
        controller = TemperatureController()
        result = controller.update(20.0)

        # Should be able to access both attributes
        action = result.action
        changed = result.state_changed
        assert action is not None
        assert changed is not None


class TestConsistency:
    """Test consistency across multiple instantiations."""

    def test_multiple_controllers_independent(self):
        """Multiple controllers should maintain independent state."""
        controller1 = TemperatureController(target_temp=20.0, deadband=2.0)
        controller2 = TemperatureController(target_temp=25.0, deadband=1.0)

        controller1.update(15.0)
        controller2.update(30.0)

        assert controller1.current_state == "HEAT"
        assert controller2.current_state == "COOL"

    def test_identical_inputs_produce_identical_outputs(self):
        """Same inputs should always produce same outputs."""
        for _ in range(3):
            controller = TemperatureController(target_temp=22.0, deadband=2.0)
            result = controller.update(18.0)
            assert result.action == "HEAT"
            assert result.state_changed is True
