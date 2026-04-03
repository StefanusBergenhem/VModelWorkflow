package com.fuelcontrol;

/**
 * Reason why the requested fuel rate was clamped.
 *
 * Design reference: O3 in fuel-rate-limiter-design.md
 */
public enum ClampingReason {
    NONE,
    MODE_MAX,
    MODE_MIN,
    RATE_OF_CHANGE,
    EMERGENCY
}
