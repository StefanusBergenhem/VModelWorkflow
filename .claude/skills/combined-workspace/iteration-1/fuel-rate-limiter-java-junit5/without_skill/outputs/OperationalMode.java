/**
 * OperationalMode enum defines the three engine operating modes.
 * Used by FuelRateLimiter to determine rate bounds and rate-of-change limits.
 */
public enum OperationalMode {
    /** Engine is starting up — requires minimum fuel rate for stable ignition. */
    STARTUP,

    /** Engine is in normal cruise operation — standard rate bounds apply. */
    CRUISE,

    /** Engine is shutting down safely — fuel rate must be zero. */
    EMERGENCY_SHUTDOWN
}
