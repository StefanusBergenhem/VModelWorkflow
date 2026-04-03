package com.fuelcontrol;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.junit.jupiter.params.provider.EnumSource;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Comprehensive test suite for FuelRateLimiter.
 *
 * Derivation strategies employed:
 * 1. Requirement-based: one test per behavior rule (B1-B8) and error condition (E1-E3)
 * 2. Equivalence class partitioning: input classes for operational mode, rate ranges, elapsed time
 * 3. Boundary value analysis: min/max rates, rate-of-change boundaries, elapsed time boundaries
 * 4. Error handling & fault injection: negative inputs, invalid modes, concurrent access
 *
 * Design reference: fuel-rate-limiter-design.md
 */
class FuelRateLimiterTest {

    private FuelRateLimiter limiter;

    @BeforeEach
    void setUp() {
        limiter = new FuelRateLimiter();
    }

    // ============================================================================
    // REQUIREMENT-BASED TESTS: Behavior Rules B1-B8
    // ============================================================================

    @Test
    void testB1_StartupModeUnderMinRateClamps() {
        // B1: operational_mode is startup AND requested_rate < STARTUP_MIN_RATE
        FuelRateResult result = limiter.limitRate(5.0f, OperationalMode.STARTUP, 0);

        assertEquals(10.0f, result.getActualRate(), 0.0001f);
        assertTrue(result.wasClampedResult());
        assertEquals(ClampingReason.MODE_MIN, result.getClampingReason());
    }

    @Test
    void testB2_StartupModeOverMaxRateClamps() {
        // B2: operational_mode is startup AND requested_rate > STARTUP_MAX_RATE
        FuelRateResult result = limiter.limitRate(75.0f, OperationalMode.STARTUP, 0);

        assertEquals(50.0f, result.getActualRate(), 0.0001f);
        assertTrue(result.wasClampedResult());
        assertEquals(ClampingReason.MODE_MAX, result.getClampingReason());
    }

    @Test
    void testB3_StartupModeWithinBoundsPassthrough() {
        // B3: operational_mode is startup AND STARTUP_MIN_RATE <= requested_rate <= STARTUP_MAX_RATE
        FuelRateResult result = limiter.limitRate(30.0f, OperationalMode.STARTUP, 0);

        assertEquals(30.0f, result.getActualRate(), 0.0001f);
        assertFalse(result.wasClampedResult());
        assertEquals(ClampingReason.NONE, result.getClampingReason());
    }

    @Test
    void testB4_CruiseModeExceedsMaxRateClamps() {
        // B4: operational_mode is cruise AND requested_rate > CRUISE_MAX_RATE
        FuelRateResult result = limiter.limitRate(250.0f, OperationalMode.CRUISE, 0);

        assertEquals(200.0f, result.getActualRate(), 0.0001f);
        assertTrue(result.wasClampedResult());
        assertEquals(ClampingReason.MODE_MAX, result.getClampingReason());
    }

    @Test
    void testB5_CruiseModeExceedsRateOfChangeLimit() {
        // B5: rate-of-change exceeds limit
        // Setup: first call establishes previous_rate = 50.0
        limiter.limitRate(50.0f, OperationalMode.STARTUP, 0);

        // Switch to cruise, try to jump to 150.0 in 100ms
        // Max allowed change = 100 L/h/s * 0.1s = 10.0 L/h
        // Actual change = 150 - 50 = 100 > 10, so should clamp to 50 + 10 = 60
        FuelRateResult result = limiter.limitRate(150.0f, OperationalMode.CRUISE, 100);

        assertEquals(60.0f, result.getActualRate(), 0.0001f);
        assertTrue(result.wasClampedResult());
        assertEquals(ClampingReason.RATE_OF_CHANGE, result.getClampingReason());
    }

    @Test
    void testB6_CruiseModeWithinAllLimits() {
        // B6: within bounds and rate-of-change limit
        // Setup: establish previous_rate = 50.0
        limiter.limitRate(50.0f, OperationalMode.STARTUP, 0);

        // Small increase that respects rate-of-change limit
        FuelRateResult result = limiter.limitRate(60.0f, OperationalMode.CRUISE, 100);

        assertEquals(60.0f, result.getActualRate(), 0.0001f);
        assertFalse(result.wasClampedResult());
        assertEquals(ClampingReason.NONE, result.getClampingReason());
    }

    @Test
    void testB7_EmergencyShutdownAlwaysZero() {
        // B7: operational_mode is emergency_shutdown -> always 0.0
        FuelRateResult result = limiter.limitRate(200.0f, OperationalMode.EMERGENCY_SHUTDOWN, 100);

        assertEquals(0.0f, result.getActualRate(), 0.0001f);
        assertTrue(result.wasClampedResult());
        assertEquals(ClampingReason.EMERGENCY, result.getClampingReason());
    }

    @Test
    void testB8_InternalStateUpdatedAfterEachCall() {
        // B8: previous_rate is updated to actual_rate after each call
        // First call: request 30, should get 30 in startup
        FuelRateResult result1 = limiter.limitRate(30.0f, OperationalMode.STARTUP, 0);
        assertEquals(30.0f, result1.getActualRate(), 0.0001f);

        // Second call: if previous_rate wasn't updated, we'd get different result
        // Request 45 in cruise (200 max) - should succeed because 45 > 30 is within 10L/h change in 100ms
        FuelRateResult result2 = limiter.limitRate(45.0f, OperationalMode.CRUISE, 100);
        assertEquals(45.0f, result2.getActualRate(), 0.0001f);
    }

    // ============================================================================
    // ERROR HANDLING TESTS: E1-E3
    // ============================================================================

    @Test
    void testE1_NegativeRequestedRateTreatedAsZero() {
        // E1: requested_rate is negative -> treat as 0.0
        FuelRateResult result = limiter.limitRate(-5.0f, OperationalMode.STARTUP, 0);

        assertEquals(10.0f, result.getActualRate(), 0.0001f); // Clamped to STARTUP_MIN
        assertTrue(result.wasClampedResult());
        assertEquals(ClampingReason.MODE_MIN, result.getClampingReason());
    }

    @Test
    void testE2_NegativeElapsedTimeSkipsRateOfChangeLimit() {
        // E2: elapsed_time_ms is negative -> treat as 0, skip rate-of-change limiting
        // Setup: establish previous_rate = 50.0
        limiter.limitRate(50.0f, OperationalMode.STARTUP, 0);

        // Request 150 with negative elapsed time - should only apply mode max
        FuelRateResult result = limiter.limitRate(150.0f, OperationalMode.CRUISE, -100);

        assertEquals(200.0f, result.getActualRate(), 0.0001f); // CRUISE_MAX_RATE only
        assertTrue(result.wasClampedResult());
        assertEquals(ClampingReason.MODE_MAX, result.getClampingReason());
    }

    @Test
    void testE3_UnrecognizedOperationalModeTreatedAsEmergency() {
        // E3: unrecognized operational_mode -> treat as emergency_shutdown
        // We test by passing null, which should be converted to emergency mode
        FuelRateResult result = limiter.limitRate(150.0f, null, 0);

        assertEquals(0.0f, result.getActualRate(), 0.0001f);
        assertTrue(result.wasClampedResult());
        assertEquals(ClampingReason.EMERGENCY, result.getClampingReason());
    }

    // ============================================================================
    // EQUIVALENCE CLASS PARTITIONING TESTS
    // ============================================================================

    @ParameterizedTest
    @EnumSource(OperationalMode.class)
    void testAllOperationalModes(OperationalMode mode) {
        // ECP: one test per operational mode enum value
        FuelRateResult result = limiter.limitRate(100.0f, mode, 100);
        assertNotNull(result);
        assertNotNull(result.getClampingReason());
    }

    @Test
    void testRequestedRateEquivalenceClassZero() {
        // ECP: requested_rate = 0.0 (boundary)
        FuelRateResult result = limiter.limitRate(0.0f, OperationalMode.STARTUP, 0);
        assertEquals(10.0f, result.getActualRate(), 0.0001f);
    }

    @Test
    void testRequestedRateEquivalenceClassPositive() {
        // ECP: requested_rate > 0.0 (typical valid class)
        FuelRateResult result = limiter.limitRate(50.0f, OperationalMode.CRUISE, 0);
        assertEquals(50.0f, result.getActualRate(), 0.0001f);
    }

    @Test
    void testElapsedTimeEquivalenceClassZero() {
        // ECP: elapsed_time_ms = 0 (boundary)
        FuelRateResult result = limiter.limitRate(50.0f, OperationalMode.CRUISE, 0);
        assertNotNull(result);
    }

    @Test
    void testElapsedTimeEquivalenceClassPositive() {
        // ECP: elapsed_time_ms > 0 (typical valid class)
        FuelRateResult result = limiter.limitRate(50.0f, OperationalMode.CRUISE, 500);
        assertNotNull(result);
    }

    // ============================================================================
    // BOUNDARY VALUE ANALYSIS TESTS
    // ============================================================================

    @Test
    void testStartupMinRateBoundary() {
        // BVA: requested_rate at STARTUP_MIN_RATE
        FuelRateResult result = limiter.limitRate(10.0f, OperationalMode.STARTUP, 0);
        assertEquals(10.0f, result.getActualRate(), 0.0001f);
        assertFalse(result.wasClampedResult());
    }

    @Test
    void testStartupMinRateJustBelow() {
        // BVA: requested_rate just below STARTUP_MIN_RATE
        FuelRateResult result = limiter.limitRate(9.999f, OperationalMode.STARTUP, 0);
        assertEquals(10.0f, result.getActualRate(), 0.0001f);
        assertTrue(result.wasClampedResult());
    }

    @Test
    void testStartupMaxRateBoundary() {
        // BVA: requested_rate at STARTUP_MAX_RATE
        FuelRateResult result = limiter.limitRate(50.0f, OperationalMode.STARTUP, 0);
        assertEquals(50.0f, result.getActualRate(), 0.0001f);
        assertFalse(result.wasClampedResult());
    }

    @Test
    void testStartupMaxRateJustAbove() {
        // BVA: requested_rate just above STARTUP_MAX_RATE
        FuelRateResult result = limiter.limitRate(50.001f, OperationalMode.STARTUP, 0);
        assertEquals(50.0f, result.getActualRate(), 0.0001f);
        assertTrue(result.wasClampedResult());
    }

    @Test
    void testCruiseMaxRateBoundary() {
        // BVA: requested_rate at CRUISE_MAX_RATE
        FuelRateResult result = limiter.limitRate(200.0f, OperationalMode.CRUISE, 0);
        assertEquals(200.0f, result.getActualRate(), 0.0001f);
        assertFalse(result.wasClampedResult());
    }

    @Test
    void testCruiseMaxRateJustAbove() {
        // BVA: requested_rate just above CRUISE_MAX_RATE
        FuelRateResult result = limiter.limitRate(200.001f, OperationalMode.CRUISE, 0);
        assertEquals(200.0f, result.getActualRate(), 0.0001f);
        assertTrue(result.wasClampedResult());
    }

    @Test
    void testRateOfChangeAtExactLimit() {
        // BVA: rate change exactly at MAX_RATE_CHANGE limit
        // Setup: previous = 50
        limiter.limitRate(50.0f, OperationalMode.STARTUP, 0);

        // Request 60 in 100ms: change = 10, limit = 100 * 0.1 = 10. Should pass.
        FuelRateResult result = limiter.limitRate(60.0f, OperationalMode.CRUISE, 100);
        assertEquals(60.0f, result.getActualRate(), 0.0001f);
        assertFalse(result.wasClampedResult());
    }

    @Test
    void testRateOfChangeJustAboveLimit() {
        // BVA: rate change just above MAX_RATE_CHANGE limit
        // Setup: previous = 50
        limiter.limitRate(50.0f, OperationalMode.STARTUP, 0);

        // Request 60.001 in 100ms: change = 10.001, limit = 10. Should clamp.
        FuelRateResult result = limiter.limitRate(60.001f, OperationalMode.CRUISE, 100);
        assertEquals(60.0f, result.getActualRate(), 0.0001f);
        assertTrue(result.wasClampedResult());
        assertEquals(ClampingReason.RATE_OF_CHANGE, result.getClampingReason());
    }

    @Test
    void testElapsedTimeZeroBoundary() {
        // BVA: elapsed_time_ms = 0
        limiter.limitRate(50.0f, OperationalMode.STARTUP, 0);
        FuelRateResult result = limiter.limitRate(50.001f, OperationalMode.CRUISE, 0);

        // Any change with 0 elapsed time should be clamped
        assertTrue(result.wasClampedResult());
    }

    // ============================================================================
    // CONCURRENCY & FAULT INJECTION TESTS
    // ============================================================================

    @Test
    void testThreadSafetyMultipleConcurrentCalls() throws InterruptedException {
        // Fault injection: concurrent calls should not corrupt state
        int threadCount = 5;
        int callsPerThread = 100;
        CountDownLatch latch = new CountDownLatch(threadCount);
        AtomicReference<Exception> exceptionHolder = new AtomicReference<>();

        for (int t = 0; t < threadCount; t++) {
            new Thread(() -> {
                try {
                    for (int i = 0; i < callsPerThread; i++) {
                        float rate = (i % 20) * 10.0f;
                        limiter.limitRate(rate, OperationalMode.CRUISE, 100);
                    }
                } catch (Exception e) {
                    exceptionHolder.set(e);
                } finally {
                    latch.countDown();
                }
            }).start();
        }

        latch.await();
        assertNull(exceptionHolder.get(), "Concurrent calls should not throw exceptions");
    }

    @Test
    void testRateOfChangeDownwardClamp() {
        // Fault injection: test clamping when rate decreases
        // Setup: previous = 100
        limiter.limitRate(50.0f, OperationalMode.STARTUP, 0);
        limiter.limitRate(100.0f, OperationalMode.CRUISE, 1000);

        // Try to drop to 50 in 100ms: change = 50, limit = 10. Should clamp to 90.
        FuelRateResult result = limiter.limitRate(50.0f, OperationalMode.CRUISE, 100);
        assertEquals(90.0f, result.getActualRate(), 0.0001f);
        assertTrue(result.wasClampedResult());
        assertEquals(ClampingReason.RATE_OF_CHANGE, result.getClampingReason());
    }

    @Test
    void testStatePreservationAcrossMultipleCalls() {
        // Requirement B8: internal state must be preserved correctly
        limiter.limitRate(20.0f, OperationalMode.STARTUP, 0);
        limiter.limitRate(100.0f, OperationalMode.CRUISE, 1000);

        // After a long elapsed time, large jump should be allowed
        FuelRateResult result = limiter.limitRate(150.0f, OperationalMode.CRUISE, 1000);
        // Change = 50, limit = 100 * 1 = 100. Should pass.
        assertEquals(150.0f, result.getActualRate(), 0.0001f);
        assertFalse(result.wasClampedResult());
    }

    @Test
    void testEmergencyShutdownStopsAnyRate() {
        // Emergency shutdown should always result in 0, regardless of previous state
        limiter.limitRate(200.0f, OperationalMode.CRUISE, 1000);
        FuelRateResult result = limiter.limitRate(250.0f, OperationalMode.EMERGENCY_SHUTDOWN, 0);

        assertEquals(0.0f, result.getActualRate(), 0.0001f);
        assertTrue(result.wasClampedResult());
        assertEquals(ClampingReason.EMERGENCY, result.getClampingReason());
    }

    @Test
    void testRecoveryAfterEmergencyShutdown() {
        // After emergency shutdown, recovery to normal operation should work
        limiter.limitRate(200.0f, OperationalMode.CRUISE, 1000);
        limiter.limitRate(250.0f, OperationalMode.EMERGENCY_SHUTDOWN, 0);

        // Now try to start up again - should enforce startup limits
        FuelRateResult result = limiter.limitRate(30.0f, OperationalMode.STARTUP, 0);
        assertEquals(30.0f, result.getActualRate(), 0.0001f);
        assertFalse(result.wasClampedResult());
    }

    @Test
    void testVeryLargeElapsedTime() {
        // BVA: large elapsed_time_ms allows large rate changes
        limiter.limitRate(50.0f, OperationalMode.STARTUP, 0);

        // 10 seconds elapsed: limit = 100 * 10 = 1000 L/h
        FuelRateResult result = limiter.limitRate(200.0f, OperationalMode.CRUISE, 10000);
        assertEquals(200.0f, result.getActualRate(), 0.0001f);
        assertFalse(result.wasClampedResult());
    }

    @Test
    void testSequentialRateIncreases() {
        // Multiple sequential increases that respect rate limits
        limiter.limitRate(10.0f, OperationalMode.STARTUP, 0);

        // 100ms at 100 L/h/s = 10 L/h per step
        FuelRateResult r1 = limiter.limitRate(20.0f, OperationalMode.CRUISE, 100);
        assertEquals(20.0f, r1.getActualRate(), 0.0001f);

        FuelRateResult r2 = limiter.limitRate(30.0f, OperationalMode.CRUISE, 100);
        assertEquals(30.0f, r2.getActualRate(), 0.0001f);

        FuelRateResult r3 = limiter.limitRate(40.0f, OperationalMode.CRUISE, 100);
        assertEquals(40.0f, r3.getActualRate(), 0.0001f);
    }
}
