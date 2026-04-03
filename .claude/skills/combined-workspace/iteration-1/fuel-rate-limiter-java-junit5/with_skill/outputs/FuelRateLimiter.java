package com.fuelcontrol;

import java.util.concurrent.atomic.AtomicReference;

/**
 * Clamps fuel rate to mode-specific bounds and enforces rate-of-change limits.
 *
 * Thread-safe, constant-time, deterministic control component for real-time engine fuel delivery.
 * Design reference: FuelRateLimiter in fuel-rate-limiter-design.md
 */
public class FuelRateLimiter {

    // Configuration constants (Design reference: Configuration section)
    private static final float STARTUP_MIN_RATE = 10.0f;
    private static final float STARTUP_MAX_RATE = 50.0f;
    private static final float CRUISE_MAX_RATE = 200.0f;
    private static final float MAX_RATE_CHANGE = 100.0f; // liters/hour/second
    private static final float ABSOLUTE_MAX_RATE = 500.0f;

    // Internal state (Design reference: Internal State section, B8)
    // AtomicReference for thread-safety without locks
    private final AtomicReference<Float> previousRate;

    /**
     * Creates a new FuelRateLimiter with initial previous rate of 0.
     * Design reference: Internal State initialization
     */
    public FuelRateLimiter() {
        this.previousRate = new AtomicReference<>(0.0f);
    }

    /**
     * Clamps the requested fuel rate according to operational mode and rate-of-change limits.
     *
     * @param requestedRate the desired fuel rate in liters/hour (>= 0)
     * @param operationalMode the current engine operational mode
     * @param elapsedTimeMs time in milliseconds since the last call (>= 0)
     * @return FuelRateResult with the clamped rate and reason
     * @throws NullPointerException if operationalMode is null
     */
    public FuelRateResult limitRate(float requestedRate, OperationalMode operationalMode,
                                     int elapsedTimeMs) {
        if (operationalMode == null) {
            operationalMode = OperationalMode.EMERGENCY_SHUTDOWN;
        }

        // Handle negative requested rate (Design reference: E1)
        float normalizedRate = requestedRate < 0.0f ? 0.0f : requestedRate;
        boolean wasNegative = requestedRate < 0.0f;

        // Get current previous rate
        float prevRate = previousRate.get();

        // Determine actual rate based on operational mode
        FuelRateResult result;
        switch (operationalMode) {
            case STARTUP:
                result = handleStartupMode(normalizedRate, wasNegative);
                break;
            case CRUISE:
                result = handleCruiseMode(normalizedRate, prevRate, elapsedTimeMs);
                break;
            case EMERGENCY_SHUTDOWN:
                result = handleEmergencyShutdown();
                break;
            default:
                // Unrecognized mode treated as emergency_shutdown (Design reference: E3)
                result = handleEmergencyShutdown();
        }

        // Update internal state with the actual rate (Design reference: B8)
        previousRate.set(result.getActualRate());

        return result;
    }

    /**
     * Handles fuel rate limiting in STARTUP mode.
     * Design reference: B1, B2, B3
     */
    private FuelRateResult handleStartupMode(float normalizedRate, boolean wasNegative) {
        if (normalizedRate < STARTUP_MIN_RATE) {
            return new FuelRateResult(STARTUP_MIN_RATE, true, ClampingReason.MODE_MIN);
        } else if (normalizedRate > STARTUP_MAX_RATE) {
            return new FuelRateResult(STARTUP_MAX_RATE, true, ClampingReason.MODE_MAX);
        } else {
            return new FuelRateResult(normalizedRate, wasNegative, ClampingReason.NONE);
        }
    }

    /**
     * Handles fuel rate limiting in CRUISE mode with rate-of-change limits.
     * Design reference: B4, B5, B6
     */
    private FuelRateResult handleCruiseMode(float normalizedRate, float prevRate,
                                             int elapsedTimeMs) {
        // Check mode maximum (Design reference: B4)
        float modeClampedRate = Math.min(normalizedRate, CRUISE_MAX_RATE);
        boolean modeClampApplied = modeClampedRate != normalizedRate;

        // Calculate rate-of-change limit (Design reference: B5)
        // Normalize negative elapsed time to 0 (Design reference: E2)
        int normalizedElapsedMs = Math.max(elapsedTimeMs, 0);
        float maxAllowedChange = MAX_RATE_CHANGE * normalizedElapsedMs / 1000.0f;

        float diff = Math.abs(modeClampedRate - prevRate);
        if (diff > maxAllowedChange) {
            // Rate of change exceeds limit
            float clampedRate = prevRate > modeClampedRate
                    ? prevRate - maxAllowedChange
                    : prevRate + maxAllowedChange;
            return new FuelRateResult(clampedRate, true, ClampingReason.RATE_OF_CHANGE);
        } else if (modeClampApplied) {
            // Only mode maximum was applied
            return new FuelRateResult(modeClampedRate, true, ClampingReason.MODE_MAX);
        } else {
            // No clamping needed (Design reference: B6)
            return new FuelRateResult(modeClampedRate, false, ClampingReason.NONE);
        }
    }

    /**
     * Handles fuel rate limiting in EMERGENCY_SHUTDOWN mode.
     * Design reference: B7
     */
    private FuelRateResult handleEmergencyShutdown() {
        return new FuelRateResult(0.0f, true, ClampingReason.EMERGENCY);
    }
}
