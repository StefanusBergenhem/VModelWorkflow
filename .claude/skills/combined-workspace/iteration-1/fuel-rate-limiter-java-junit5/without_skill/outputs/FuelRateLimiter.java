/**
 * FuelRateLimiter clamps the requested fuel rate to mode-specific bounds
 * and enforces rate-of-change limits to prevent sudden fuel delivery changes
 * that could damage the engine or cause unstable combustion.
 *
 * Thread-safe: each instance manages its own internal state independently.
 * Constant-time execution: no allocations, no unbounded loops.
 * Deterministic: same inputs and state always produce same outputs.
 */
public final class FuelRateLimiter {

    // Configuration constants
    private static final float STARTUP_MIN_RATE = 10.0f;      // liters/hour
    private static final float STARTUP_MAX_RATE = 50.0f;      // liters/hour
    private static final float CRUISE_MAX_RATE = 200.0f;      // liters/hour
    private static final float MAX_RATE_CHANGE = 100.0f;      // liters/hour/second
    private static final float ABSOLUTE_MAX_RATE = 500.0f;    // liters/hour (hard limit)

    // Internal state
    private float previousRate;

    /**
     * Creates a new FuelRateLimiter with initial previous_rate of 0.0.
     */
    public FuelRateLimiter() {
        this.previousRate = 0.0f;
    }

    /**
     * Applies fuel rate limiting based on operational mode and rate-of-change constraints.
     *
     * @param requestedRate desired fuel rate (liters/hour); negative values treated as 0.0
     * @param operationalMode current engine mode (null/unrecognized treated as EMERGENCY_SHUTDOWN)
     * @param elapsedTimeMs time since last call in milliseconds; negative values treated as 0
     * @return FuelRateResult containing actual rate, clamping status, and reason
     */
    public synchronized FuelRateResult applyLimit(
            float requestedRate,
            OperationalMode operationalMode,
            int elapsedTimeMs) {

        // E1: Handle negative requested_rate
        float workingRate = requestedRate;
        if (requestedRate < 0.0f) {
            workingRate = 0.0f;
        }

        // E2: Handle negative elapsed_time_ms (treat as 0)
        int safeElapsedTimeMs = Math.max(elapsedTimeMs, 0);

        // E3: Treat null or unrecognized mode as emergency_shutdown
        OperationalMode safeMode = (operationalMode != null) ? operationalMode : OperationalMode.EMERGENCY_SHUTDOWN;

        // Apply mode-specific bounds and rate-of-change limits
        float actualRate;
        ClampingReason reason;

        switch (safeMode) {
            case STARTUP:
                // B1: below startup minimum
                if (workingRate < STARTUP_MIN_RATE) {
                    actualRate = STARTUP_MIN_RATE;
                    reason = ClampingReason.MODE_MIN;
                }
                // B2: above startup maximum
                else if (workingRate > STARTUP_MAX_RATE) {
                    actualRate = STARTUP_MAX_RATE;
                    reason = ClampingReason.MODE_MAX;
                }
                // B3: within startup bounds
                else {
                    actualRate = workingRate;
                    reason = ClampingReason.NONE;
                }
                break;

            case CRUISE:
                // B4: above cruise maximum
                if (workingRate > CRUISE_MAX_RATE) {
                    actualRate = CRUISE_MAX_RATE;
                    reason = ClampingReason.MODE_MAX;
                }
                // B5: check rate-of-change limit
                else {
                    float maxAllowedChange = MAX_RATE_CHANGE * safeElapsedTimeMs / 1000.0f;
                    float maxAllowedRate = previousRate + maxAllowedChange;
                    float minAllowedRate = previousRate - maxAllowedChange;

                    if (workingRate > maxAllowedRate) {
                        actualRate = maxAllowedRate;
                        reason = ClampingReason.RATE_OF_CHANGE;
                    } else if (workingRate < minAllowedRate) {
                        actualRate = minAllowedRate;
                        reason = ClampingReason.RATE_OF_CHANGE;
                    }
                    // B6: within bounds and rate-of-change limit
                    else {
                        actualRate = workingRate;
                        reason = ClampingReason.NONE;
                    }
                }
                break;

            case EMERGENCY_SHUTDOWN:
                // B7: emergency shutdown — force zero rate
                actualRate = 0.0f;
                reason = ClampingReason.EMERGENCY;
                break;

            default:
                // Fallback: treat as emergency (fail-safe)
                actualRate = 0.0f;
                reason = ClampingReason.EMERGENCY;
        }

        // Hard limit: never exceed absolute maximum
        if (actualRate > ABSOLUTE_MAX_RATE) {
            actualRate = ABSOLUTE_MAX_RATE;
        }

        // Ensure non-negative
        if (actualRate < 0.0f) {
            actualRate = 0.0f;
        }

        // B8: Update internal state
        this.previousRate = actualRate;

        // Determine if clamping occurred
        boolean wasClamped = !requestedRate < 0.0f && (actualRate != requestedRate || reason != ClampingReason.NONE);

        return new FuelRateResult(actualRate, wasClamped, reason);
    }

    /**
     * Returns the current internal state (previous_rate) for testing purposes.
     */
    float getPreviousRate() {
        return previousRate;
    }

    /**
     * Resets the internal state to initial conditions (previous_rate = 0.0).
     * Useful for testing and system resets.
     */
    void reset() {
        this.previousRate = 0.0f;
    }
}
