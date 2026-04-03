"""Temperature Controller: monitors sensor readings and controls heating/cooling via hysteresis."""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class Action(Enum):
    """Possible states of the temperature controller."""
    HEAT = "HEAT"
    COOL = "COOL"
    IDLE = "IDLE"


@dataclass(frozen=True)
class ControlResult:
    """Immutable result from a control decision."""
    action: Action
    state_changed: bool


class TemperatureController:
    """
    Monitors temperature and decides heating/cooling via deadband hysteresis.

    Uses deadband (hysteresis) to prevent rapid toggling between states.
    Transitions only occur when temperature crosses a deadband boundary.
    """

    # Configuration defaults
    DEFAULT_TARGET_TEMP = 22.0
    DEFAULT_DEADBAND = 2.0

    # Constraints
    SENSOR_MIN = -50.0
    SENSOR_MAX = 150.0
    TARGET_MIN = 0.0
    TARGET_MAX = 100.0
    DEADBAND_MIN = 0.5
    DEADBAND_MAX = 10.0

    def __init__(
        self,
        target_temp: float = DEFAULT_TARGET_TEMP,
        deadband: float = DEFAULT_DEADBAND,
    ):
        """
        Initialize the controller.

        Args:
            target_temp: Desired temperature in Celsius. Clamped to [0, 100].
            deadband: Hysteresis band width in degrees. Clamped to [0.5, 10.0].
                If <= 0, uses default (2.0).
        """
        self._target_temp = self._clamp_target(target_temp)
        self._deadband = self._clamp_deadband(deadband)
        self._current_action = Action.IDLE

    def decide(self, current_temp: float) -> ControlResult:
        """
        Decide heating/cooling action based on current temperature.

        Args:
            current_temp: Current temperature in Celsius.

        Returns:
            ControlResult with action and state_changed flag.
        """
        # Validate sensor reading
        if not self._is_valid_sensor_reading(current_temp):
            logger.warning(
                f"Invalid sensor reading: {current_temp}C (outside range "
                f"{self.SENSOR_MIN} to {self.SENSOR_MAX})"
            )
            return ControlResult(action=Action.IDLE, state_changed=False)

        # Compute state transition
        new_action = self._compute_action(current_temp)
        state_changed = new_action != self._current_action
        self._current_action = new_action

        return ControlResult(action=new_action, state_changed=state_changed)

    def _compute_action(self, current_temp: float) -> Action:
        """
        Compute the next action based on current temperature and state.

        Deadband boundaries:
        - Lower boundary: target - deadband/2
        - Upper boundary: target + deadband/2
        """
        lower_bound = self._target_temp - self._deadband / 2
        upper_bound = self._target_temp + self._deadband / 2

        if self._current_action == Action.IDLE:
            # From idle: transition to heat or cool if out of bounds
            if current_temp < lower_bound:
                return Action.HEAT
            elif current_temp > upper_bound:
                return Action.COOL
            else:
                return Action.IDLE

        elif self._current_action == Action.HEAT:
            # From heating: stay heat until upper boundary reached
            if current_temp >= upper_bound:
                return Action.IDLE
            else:
                return Action.HEAT

        elif self._current_action == Action.COOL:
            # From cooling: stay cool until lower boundary reached
            if current_temp <= lower_bound:
                return Action.IDLE
            else:
                return Action.COOL

        # Should not reach here
        return Action.IDLE

    def _is_valid_sensor_reading(self, temp: float) -> bool:
        """Check if temperature is within valid sensor range."""
        return self.SENSOR_MIN <= temp <= self.SENSOR_MAX

    def _clamp_target(self, value: float) -> float:
        """Clamp target temperature to valid range."""
        return max(self.TARGET_MIN, min(self.TARGET_MAX, value))

    def _clamp_deadband(self, value: float) -> float:
        """Clamp deadband to valid range. Zero or negative uses default."""
        if value <= 0:
            return self.DEFAULT_DEADBAND
        return max(self.DEADBAND_MIN, min(self.DEADBAND_MAX, value))

    @property
    def current_action(self) -> Action:
        """Get the current action (for testing/inspection)."""
        return self._current_action

    @property
    def target_temp(self) -> float:
        """Get the effective target temperature."""
        return self._target_temp

    @property
    def deadband(self) -> float:
        """Get the effective deadband."""
        return self._deadband
