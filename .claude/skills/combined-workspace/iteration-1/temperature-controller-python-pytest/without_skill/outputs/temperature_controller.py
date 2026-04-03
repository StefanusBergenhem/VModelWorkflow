"""
Temperature Controller Implementation

Monitors temperature readings from a sensor and decides whether to activate
heating, cooling, or neither using deadband (hysteresis) to prevent rapid
toggling between states.

Usage:
    controller = TemperatureController(target_temp=22.0, deadband=2.0)
    result = controller.update(current_temperature)
    print(f"Action: {result.action}, State Changed: {result.state_changed}")
"""

from dataclasses import dataclass
from typing import Literal
import logging

# Configure logging for warnings
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


@dataclass
class ControllerOutput:
    """Output from a temperature controller update.

    Attributes:
        action: One of "HEAT", "COOL", or "IDLE"
        state_changed: True if action differs from previous call
    """
    action: Literal["HEAT", "COOL", "IDLE"]
    state_changed: bool


class TemperatureController:
    """Temperature controller with deadband hysteresis.

    Controls heating and cooling based on temperature readings relative to
    a target, using a deadband to prevent rapid state toggling.

    Attributes:
        target_temp: Target temperature in Celsius (0-100)
        deadband: Hysteresis band width in degrees (0.5-10.0)
        current_state: Current action state (HEAT, COOL, or IDLE)
    """

    # Sensor range constraints
    SENSOR_MIN = -50.0
    SENSOR_MAX = 150.0

    # Target temperature constraints
    TARGET_MIN = 0.0
    TARGET_MAX = 100.0

    # Deadband constraints
    DEADBAND_MIN = 0.5
    DEADBAND_MAX = 10.0
    DEADBAND_DEFAULT = 2.0

    # Default target temperature
    TARGET_DEFAULT = 22.0

    def __init__(
        self,
        target_temp: float = TARGET_DEFAULT,
        deadband: float = DEADBAND_DEFAULT
    ):
        """Initialize the temperature controller.

        Args:
            target_temp: Target temperature in Celsius. Will be clamped to
                        [0.0, 100.0]. Defaults to 22.0.
            deadband: Hysteresis band width in degrees. Will be clamped to
                     [0.5, 10.0] or set to default if <= 0. Defaults to 2.0.
        """
        self.target_temp = self._clamp_target(target_temp)
        self.deadband = self._clamp_deadband(deadband)
        self.current_state: Literal["HEAT", "COOL", "IDLE"] = "IDLE"

    def update(self, current_temp: float) -> ControllerOutput:
        """Update controller with current temperature reading.

        Evaluates the current temperature against the target and deadband,
        determines the appropriate action, and tracks state changes.

        Args:
            current_temp: Current temperature in Celsius. Should be in range
                         [-50, 150]. Out-of-range values return IDLE.

        Returns:
            ControllerOutput with action and stateChanged flag.
        """
        # Validate sensor reading
        if not self._is_valid_sensor_reading(current_temp):
            logger.warning(
                f"Invalid sensor reading: {current_temp}. "
                f"Valid range is [{self.SENSOR_MIN}, {self.SENSOR_MAX}]"
            )
            old_state = self.current_state
            return ControllerOutput(
                action="IDLE",
                state_changed=(old_state != "IDLE")
            )

        # Calculate thresholds
        half_deadband = self.deadband / 2.0
        heat_threshold = self.target_temp - half_deadband
        cool_threshold = self.target_temp + half_deadband

        # Determine next state based on current state and temperature
        new_state = self._calculate_next_state(
            current_temp,
            heat_threshold,
            cool_threshold
        )

        # Determine if state changed
        state_changed = (new_state != self.current_state)

        # Update current state
        self.current_state = new_state

        return ControllerOutput(
            action=new_state,
            state_changed=state_changed
        )

    def _calculate_next_state(
        self,
        current_temp: float,
        heat_threshold: float,
        cool_threshold: float
    ) -> Literal["HEAT", "COOL", "IDLE"]:
        """Calculate the next state based on current state and temperature.

        Implements hysteresis logic:
        - From IDLE: transition if temp crosses deadband boundary
        - From HEAT: continue until temp reaches cool threshold
        - From COOL: continue until temp reaches heat threshold

        Args:
            current_temp: Current temperature reading
            heat_threshold: Temperature below which heating should activate
            cool_threshold: Temperature above which cooling should activate

        Returns:
            The next state to transition to
        """
        if self.current_state == "IDLE":
            if current_temp <= heat_threshold:
                return "HEAT"
            elif current_temp >= cool_threshold:
                return "COOL"
            else:
                return "IDLE"

        elif self.current_state == "HEAT":
            if current_temp >= cool_threshold:
                return "COOL"
            elif current_temp >= heat_threshold:
                return "IDLE"
            else:
                return "HEAT"

        elif self.current_state == "COOL":
            if current_temp <= heat_threshold:
                return "HEAT"
            elif current_temp <= cool_threshold:
                return "IDLE"
            else:
                return "COOL"

        # Fallback (should never reach)
        return "IDLE"

    @staticmethod
    def _clamp_target(temp: float) -> float:
        """Clamp target temperature to valid range.

        Args:
            temp: Target temperature to clamp

        Returns:
            Clamped temperature in [0.0, 100.0]
        """
        return max(TemperatureController.TARGET_MIN,
                   min(temp, TemperatureController.TARGET_MAX))

    @staticmethod
    def _clamp_deadband(deadband: float) -> float:
        """Clamp deadband to valid range or use default if invalid.

        Args:
            deadband: Deadband width to process

        Returns:
            Valid deadband in [0.5, 10.0] or default if <= 0
        """
        if deadband <= 0:
            return TemperatureController.DEADBAND_DEFAULT

        return max(TemperatureController.DEADBAND_MIN,
                   min(deadband, TemperatureController.DEADBAND_MAX))

    @staticmethod
    def _is_valid_sensor_reading(temp: float) -> bool:
        """Check if temperature reading is within sensor range.

        Args:
            temp: Temperature to validate

        Returns:
            True if temperature is in valid sensor range
        """
        return (TemperatureController.SENSOR_MIN <= temp <=
                TemperatureController.SENSOR_MAX)
