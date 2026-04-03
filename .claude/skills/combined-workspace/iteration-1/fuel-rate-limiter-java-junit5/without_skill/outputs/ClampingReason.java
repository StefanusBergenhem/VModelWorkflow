/**
 * ClampingReason enum indicates why the requested fuel rate was modified.
 * Provides transparency for control loops and diagnostic monitoring.
 */
public enum ClampingReason {
    /** No clamping was applied — actual_rate equals requested_rate. */
    NONE,

    /** Rate was clamped to the mode's maximum limit. */
    MODE_MAX,

    /** Rate was clamped to the mode's minimum limit. */
    MODE_MIN,

    /** Rate was clamped due to exceeding the maximum rate-of-change limit. */
    RATE_OF_CHANGE,

    /** Rate was forced to zero due to emergency shutdown mode. */
    EMERGENCY
}
