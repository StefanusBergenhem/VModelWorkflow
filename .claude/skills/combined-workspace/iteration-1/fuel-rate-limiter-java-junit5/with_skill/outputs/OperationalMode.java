package com.fuelcontrol;

/**
 * Operational mode of the engine.
 *
 * Design reference: I2 in fuel-rate-limiter-design.md
 */
public enum OperationalMode {
    STARTUP,
    CRUISE,
    EMERGENCY_SHUTDOWN
}
