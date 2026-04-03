package com.fuelcontrol;

/**
 * Immutable result of fuel rate limiting.
 *
 * Design reference: Outputs O1, O2, O3 in fuel-rate-limiter-design.md
 */
public final class FuelRateResult {
    private final float actualRate;
    private final boolean wasClamped;
    private final ClampingReason clampingReason;

    /**
     * Creates a FuelRateResult.
     *
     * @param actualRate the final rate after clamping (liters/hour)
     * @param wasClamped true if the requested rate was adjusted
     * @param clampingReason why clamping was applied
     */
    public FuelRateResult(float actualRate, boolean wasClamped, ClampingReason clampingReason) {
        this.actualRate = actualRate;
        this.wasClamped = wasClamped;
        this.clampingReason = clampingReason;
    }

    /**
     * Returns the final fuel rate after clamping.
     *
     * @return actual rate in liters/hour (0.0 to 500.0)
     */
    public float getActualRate() {
        return actualRate;
    }

    /**
     * Returns whether the requested rate was clamped.
     *
     * @return true if actual_rate differs from requested_rate
     */
    public boolean wasClampedResult() {
        return wasClamped;
    }

    /**
     * Returns the reason for clamping.
     *
     * @return the clamping reason enum
     */
    public ClampingReason getClampingReason() {
        return clampingReason;
    }

    @Override
    public String toString() {
        return String.format("FuelRateResult{actualRate=%.1f, wasClamped=%s, reason=%s}",
                actualRate, wasClamped, clampingReason);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        FuelRateResult that = (FuelRateResult) o;
        return Float.compare(that.actualRate, actualRate) == 0
                && wasClamped == that.wasClamped
                && clampingReason == that.clampingReason;
    }

    @Override
    public int hashCode() {
        return java.util.Objects.hash(actualRate, wasClamped, clampingReason);
    }
}
