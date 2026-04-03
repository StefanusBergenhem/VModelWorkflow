/**
 * FuelRateResult is the output of FuelRateLimiter.applyLimit().
 * Contains the computed actual rate, clamping status, and reason.
 */
public final class FuelRateResult {
    private final float actualRate;
    private final boolean wasClamped;
    private final ClampingReason clampingReason;

    /**
     * Creates a new FuelRateResult.
     *
     * @param actualRate the fuel rate after applying all limits (liters/hour)
     * @param wasClamped true if actual_rate differs from the requested_rate
     * @param clampingReason why clamping was applied (or NONE)
     */
    public FuelRateResult(float actualRate, boolean wasClamped, ClampingReason clampingReason) {
        this.actualRate = actualRate;
        this.wasClamped = wasClamped;
        this.clampingReason = clampingReason;
    }

    /** Returns the fuel rate after applying all limits (liters/hour). */
    public float getActualRate() {
        return actualRate;
    }

    /** Returns true if actual_rate differs from requested_rate. */
    public boolean wasClampedReason() {
        return wasClamped;
    }

    /** Returns the reason why clamping was applied (or NONE). */
    public ClampingReason getClampingReason() {
        return clampingReason;
    }

    @Override
    public String toString() {
        return "FuelRateResult{" +
                "actualRate=" + actualRate +
                ", wasClamped=" + wasClamped +
                ", clampingReason=" + clampingReason +
                '}';
    }
}
