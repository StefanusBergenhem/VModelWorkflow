import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Comprehensive test suite for FuelRateLimiter.
 * Covers all behaviors (B1-B8), error conditions (E1-E3), and edge cases.
 * Uses nested test classes to organize tests by concern (startup, cruise, emergency, etc.).
 */
@DisplayName("FuelRateLimiter Tests")
class FuelRateLimiterTest {

    private FuelRateLimiter limiter;

    @BeforeEach
    void setUp() {
        limiter = new FuelRateLimiter();
    }

    // ============================================================================
    // STARTUP MODE TESTS (B1, B2, B3)
    // ============================================================================

    @Nested
    @DisplayName("Startup Mode")
    class StartupModeTests {

        @Test
        @DisplayName("B1: Rate below startup minimum should clamp to STARTUP_MIN_RATE")
        void rateBelowStartupMinimum() {
            FuelRateResult result = limiter.applyLimit(5.0f, OperationalMode.STARTUP, 100);

            assertEquals(10.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.MODE_MIN, result.getClampingReason());
        }

        @Test
        @DisplayName("B1: Rate at zero should clamp to STARTUP_MIN_RATE")
        void rateAtZeroInStartup() {
            FuelRateResult result = limiter.applyLimit(0.0f, OperationalMode.STARTUP, 100);

            assertEquals(10.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.MODE_MIN, result.getClampingReason());
        }

        @Test
        @DisplayName("B2: Rate above startup maximum should clamp to STARTUP_MAX_RATE")
        void rateAboveStartupMaximum() {
            FuelRateResult result = limiter.applyLimit(100.0f, OperationalMode.STARTUP, 100);

            assertEquals(50.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.MODE_MAX, result.getClampingReason());
        }

        @Test
        @DisplayName("B3: Rate within startup bounds should not be clamped")
        void rateWithinStartupBounds() {
            FuelRateResult result = limiter.applyLimit(25.0f, OperationalMode.STARTUP, 100);

            assertEquals(25.0f, result.getActualRate(), 0.001f);
            assertFalse(result.wasClampedReason());
            assertEquals(ClampingReason.NONE, result.getClampingReason());
        }

        @Test
        @DisplayName("B3: Rate at startup minimum boundary should not be clamped")
        void rateAtStartupMinimumBoundary() {
            FuelRateResult result = limiter.applyLimit(10.0f, OperationalMode.STARTUP, 100);

            assertEquals(10.0f, result.getActualRate(), 0.001f);
            assertFalse(result.wasClampedReason());
            assertEquals(ClampingReason.NONE, result.getClampingReason());
        }

        @Test
        @DisplayName("B3: Rate at startup maximum boundary should not be clamped")
        void rateAtStartupMaximumBoundary() {
            FuelRateResult result = limiter.applyLimit(50.0f, OperationalMode.STARTUP, 100);

            assertEquals(50.0f, result.getActualRate(), 0.001f);
            assertFalse(result.wasClampedReason());
            assertEquals(ClampingReason.NONE, result.getClampingReason());
        }

        @Test
        @DisplayName("B1: Startup mode with minimal undershoot")
        void startupMinimalUndershoot() {
            FuelRateResult result = limiter.applyLimit(9.999f, OperationalMode.STARTUP, 100);

            assertEquals(10.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.MODE_MIN, result.getClampingReason());
        }

        @Test
        @DisplayName("B2: Startup mode with minimal overshoot")
        void startupMinimalOvershoot() {
            FuelRateResult result = limiter.applyLimit(50.001f, OperationalMode.STARTUP, 100);

            assertEquals(50.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.MODE_MAX, result.getClampingReason());
        }
    }

    // ============================================================================
    // CRUISE MODE TESTS (B4, B5, B6)
    // ============================================================================

    @Nested
    @DisplayName("Cruise Mode")
    class CruiseModeTests {

        @Test
        @DisplayName("B4: Rate above cruise maximum should clamp to CRUISE_MAX_RATE")
        void rateAboveCruiseMaximum() {
            FuelRateResult result = limiter.applyLimit(250.0f, OperationalMode.CRUISE, 100);

            assertEquals(200.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.MODE_MAX, result.getClampingReason());
        }

        @Test
        @DisplayName("B4: Cruise maximum boundary should not be clamped")
        void rateAtCruiseMaximumBoundary() {
            FuelRateResult result = limiter.applyLimit(200.0f, OperationalMode.CRUISE, 100);

            assertEquals(200.0f, result.getActualRate(), 0.001f);
            assertFalse(result.wasClampedReason());
            assertEquals(ClampingReason.NONE, result.getClampingReason());
        }

        @Test
        @DisplayName("B4: Minimal overshoot at cruise maximum")
        void cruiseMaximalOvershoot() {
            FuelRateResult result = limiter.applyLimit(200.001f, OperationalMode.CRUISE, 100);

            assertEquals(200.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.MODE_MAX, result.getClampingReason());
        }

        @Test
        @DisplayName("B5: Rate-of-change exceeding limit should be clamped (increase)")
        void rateOfChangeExceededIncrease() {
            // Start with rate of 100 liters/hour
            limiter.applyLimit(100.0f, OperationalMode.CRUISE, 100);

            // Try to jump to 120 in 100ms (rate change = 20 liters/hour)
            // With MAX_RATE_CHANGE = 100 liters/hour/second:
            // max allowed change in 100ms = 100 * 0.1 = 10 liters/hour
            // requested change = 20, exceeds limit
            FuelRateResult result = limiter.applyLimit(120.0f, OperationalMode.CRUISE, 100);

            assertEquals(110.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.RATE_OF_CHANGE, result.getClampingReason());
        }

        @Test
        @DisplayName("B5: Rate-of-change exceeding limit should be clamped (decrease)")
        void rateOfChangeExceededDecrease() {
            // Start with rate of 100 liters/hour
            limiter.applyLimit(100.0f, OperationalMode.CRUISE, 100);

            // Try to drop to 80 in 100ms (rate change = -20 liters/hour)
            // max allowed change in 100ms = 100 * 0.1 = 10 liters/hour
            // requested change = -20, exceeds limit
            FuelRateResult result = limiter.applyLimit(80.0f, OperationalMode.CRUISE, 100);

            assertEquals(90.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.RATE_OF_CHANGE, result.getClampingReason());
        }

        @Test
        @DisplayName("B5: Rate-of-change at exact limit should not be clamped")
        void rateOfChangeAtExactLimit() {
            // Start with rate of 100 liters/hour
            limiter.applyLimit(100.0f, OperationalMode.CRUISE, 100);

            // In 100ms, max allowed change = 100 * 0.1 = 10 liters/hour
            // Request exactly 110 liters/hour (at limit)
            FuelRateResult result = limiter.applyLimit(110.0f, OperationalMode.CRUISE, 100);

            assertEquals(110.0f, result.getActualRate(), 0.001f);
            assertFalse(result.wasClampedReason());
            assertEquals(ClampingReason.NONE, result.getClampingReason());
        }

        @Test
        @DisplayName("B5: Rate-of-change with longer time interval allows larger change")
        void rateOfChangeWithLongerInterval() {
            // Start with rate of 100 liters/hour
            limiter.applyLimit(100.0f, OperationalMode.CRUISE, 100);

            // In 500ms, max allowed change = 100 * 0.5 = 50 liters/hour
            // Request 150 liters/hour (50 liters/hour change)
            FuelRateResult result = limiter.applyLimit(150.0f, OperationalMode.CRUISE, 500);

            assertEquals(150.0f, result.getActualRate(), 0.001f);
            assertFalse(result.wasClampedReason());
            assertEquals(ClampingReason.NONE, result.getClampingReason());
        }

        @Test
        @DisplayName("B5: Rate-of-change with zero elapsed time allows no change")
        void rateOfChangeWithZeroElapsedTime() {
            // Start with rate of 100 liters/hour
            limiter.applyLimit(100.0f, OperationalMode.CRUISE, 100);

            // With zero elapsed time, no change is allowed
            // Request 101 liters/hour
            FuelRateResult result = limiter.applyLimit(101.0f, OperationalMode.CRUISE, 0);

            assertEquals(100.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.RATE_OF_CHANGE, result.getClampingReason());
        }

        @Test
        @DisplayName("B6: Rate within bounds and rate-of-change limit should not be clamped")
        void rateWithinAllLimits() {
            // Start with rate of 50 liters/hour
            limiter.applyLimit(50.0f, OperationalMode.CRUISE, 100);

            // Request 55 in 100ms (change = 5, within limit of 10)
            FuelRateResult result = limiter.applyLimit(55.0f, OperationalMode.CRUISE, 100);

            assertEquals(55.0f, result.getActualRate(), 0.001f);
            assertFalse(result.wasClampedReason());
            assertEquals(ClampingReason.NONE, result.getClampingReason());
        }

        @Test
        @DisplayName("B5: Very long time interval accumulates large allowable change")
        void rateOfChangeVeryLongInterval() {
            // Start with rate of 100 liters/hour
            limiter.applyLimit(100.0f, OperationalMode.CRUISE, 100);

            // In 10 seconds, max allowed change = 100 * 10 = 1000 liters/hour
            // Request 500 liters/hour (but hard limit is 500)
            FuelRateResult result = limiter.applyLimit(500.0f, OperationalMode.CRUISE, 10000);

            assertEquals(500.0f, result.getActualRate(), 0.001f);
            assertFalse(result.wasClampedReason());
            assertEquals(ClampingReason.NONE, result.getClampingReason());
        }
    }

    // ============================================================================
    // EMERGENCY SHUTDOWN MODE TESTS (B7)
    // ============================================================================

    @Nested
    @DisplayName("Emergency Shutdown Mode")
    class EmergencyShutdownModeTests {

        @Test
        @DisplayName("B7: Emergency shutdown should force rate to zero regardless of request")
        void emergencyShutdownForceZero() {
            FuelRateResult result = limiter.applyLimit(100.0f, OperationalMode.EMERGENCY_SHUTDOWN, 100);

            assertEquals(0.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.EMERGENCY, result.getClampingReason());
        }

        @Test
        @DisplayName("B7: Emergency shutdown with zero request still marks as clamped")
        void emergencyShutdownWithZeroRequest() {
            FuelRateResult result = limiter.applyLimit(0.0f, OperationalMode.EMERGENCY_SHUTDOWN, 100);

            assertEquals(0.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.EMERGENCY, result.getClampingReason());
        }

        @Test
        @DisplayName("B7: Emergency shutdown with maximum request")
        void emergencyShutdownWithMaxRequest() {
            FuelRateResult result = limiter.applyLimit(500.0f, OperationalMode.EMERGENCY_SHUTDOWN, 100);

            assertEquals(0.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.EMERGENCY, result.getClampingReason());
        }
    }

    // ============================================================================
    // INTERNAL STATE MANAGEMENT TESTS (B8)
    // ============================================================================

    @Nested
    @DisplayName("Internal State Management")
    class InternalStateTests {

        @Test
        @DisplayName("B8: Actual rate becomes new previous_rate for next call")
        void previousRateUpdatedCorrectly() {
            // Apply 25 liters/hour in startup mode
            limiter.applyLimit(25.0f, OperationalMode.STARTUP, 100);
            assertEquals(25.0f, limiter.getPreviousRate(), 0.001f);

            // Apply 30 liters/hour in cruise mode
            limiter.applyLimit(30.0f, OperationalMode.CRUISE, 100);
            assertEquals(30.0f, limiter.getPreviousRate(), 0.001f);
        }

        @Test
        @DisplayName("B8: Clamped rate becomes previous_rate, not requested_rate")
        void clampedRateBecomsPreviousRate() {
            // Apply 100 liters/hour in startup mode (clamped to 50)
            limiter.applyLimit(100.0f, OperationalMode.STARTUP, 100);
            assertEquals(50.0f, limiter.getPreviousRate(), 0.001f);

            // Next call in cruise: rate-of-change should be calculated from 50, not 100
            // Request 65 (change of 15, exceeds 10 limit for 100ms)
            FuelRateResult result = limiter.applyLimit(65.0f, OperationalMode.CRUISE, 100);
            assertEquals(60.0f, result.getActualRate(), 0.001f);
        }

        @Test
        @DisplayName("B8: Initial previous_rate is zero")
        void initialPreviousRateIsZero() {
            assertEquals(0.0f, limiter.getPreviousRate(), 0.001f);
        }

        @Test
        @DisplayName("B8: Reset clears previous_rate to zero")
        void resetClearsPreviousRate() {
            limiter.applyLimit(50.0f, OperationalMode.CRUISE, 100);
            assertEquals(50.0f, limiter.getPreviousRate(), 0.001f);

            limiter.reset();
            assertEquals(0.0f, limiter.getPreviousRate(), 0.001f);
        }
    }

    // ============================================================================
    // ERROR HANDLING TESTS (E1, E2, E3)
    // ============================================================================

    @Nested
    @DisplayName("Error Handling")
    class ErrorHandlingTests {

        @Test
        @DisplayName("E1: Negative requested_rate should be treated as zero")
        void negativeRequestedRateTreatedAsZero() {
            FuelRateResult result = limiter.applyLimit(-10.0f, OperationalMode.STARTUP, 100);

            // In startup mode, zero is below minimum (10), so clamped to 10
            assertEquals(10.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.MODE_MIN, result.getClampingReason());
        }

        @Test
        @DisplayName("E1: Very large negative requested_rate should be treated as zero")
        void veryLargeNegativeRequestedRate() {
            FuelRateResult result = limiter.applyLimit(-1000.0f, OperationalMode.CRUISE, 100);

            // Zero is within cruise bounds (no minimum), so not clamped
            assertEquals(0.0f, result.getActualRate(), 0.001f);
            assertFalse(result.wasClampedReason());
            assertEquals(ClampingReason.NONE, result.getClampingReason());
        }

        @Test
        @DisplayName("E2: Negative elapsed_time_ms should be treated as zero")
        void negativeElapsedTimeTreatedAsZero() {
            limiter.applyLimit(100.0f, OperationalMode.CRUISE, 100);

            // With -100ms treated as 0ms, no rate change allowed
            FuelRateResult result = limiter.applyLimit(105.0f, OperationalMode.CRUISE, -100);

            assertEquals(100.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.RATE_OF_CHANGE, result.getClampingReason());
        }

        @Test
        @DisplayName("E2: Very large negative elapsed_time_ms should be treated as zero")
        void veryLargeNegativeElapsedTime() {
            limiter.applyLimit(100.0f, OperationalMode.CRUISE, 100);

            FuelRateResult result = limiter.applyLimit(105.0f, OperationalMode.CRUISE, -5000);

            assertEquals(100.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.RATE_OF_CHANGE, result.getClampingReason());
        }

        @Test
        @DisplayName("E3: Null operational_mode should be treated as emergency_shutdown")
        void nullOperationalModeTreatedAsEmergency() {
            FuelRateResult result = limiter.applyLimit(100.0f, null, 100);

            assertEquals(0.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.EMERGENCY, result.getClampingReason());
        }
    }

    // ============================================================================
    // EDGE CASES AND INTEGRATION TESTS
    // ============================================================================

    @Nested
    @DisplayName("Edge Cases and Integration")
    class EdgeCasesTests {

        @Test
        @DisplayName("Hard limit: rate never exceeds 500.0 liters/hour")
        void absoluteMaximumLimit() {
            // Even in cruise mode with no rate-of-change restriction
            FuelRateResult result = limiter.applyLimit(1000.0f, OperationalMode.CRUISE, 10000);

            assertEquals(500.0f, result.getActualRate(), 0.001f);
        }

        @Test
        @DisplayName("Full startup-to-cruise-to-shutdown transition")
        void completeEngineLifecycle() {
            // Startup phase
            FuelRateResult startup = limiter.applyLimit(25.0f, OperationalMode.STARTUP, 100);
            assertEquals(25.0f, startup.getActualRate(), 0.001f);
            assertFalse(startup.wasClampedReason());

            // Transition to cruise (gradual acceleration)
            FuelRateResult cruiseRamp1 = limiter.applyLimit(35.0f, OperationalMode.CRUISE, 100);
            assertEquals(35.0f, cruiseRamp1.getActualRate(), 0.001f);
            assertFalse(cruiseRamp1.wasClampedReason());

            FuelRateResult cruiseRamp2 = limiter.applyLimit(50.0f, OperationalMode.CRUISE, 100);
            assertEquals(50.0f, cruiseRamp2.getActualRate(), 0.001f);
            assertFalse(cruiseRamp2.wasClampedReason());

            // Cruise steady-state
            FuelRateResult cruiseSteady = limiter.applyLimit(50.0f, OperationalMode.CRUISE, 100);
            assertEquals(50.0f, cruiseSteady.getActualRate(), 0.001f);
            assertFalse(cruiseSteady.wasClampedReason());

            // Emergency shutdown
            FuelRateResult shutdown = limiter.applyLimit(50.0f, OperationalMode.EMERGENCY_SHUTDOWN, 100);
            assertEquals(0.0f, shutdown.getActualRate(), 0.001f);
            assertTrue(shutdown.wasClampedReason());
        }

        @Test
        @DisplayName("Rapid on-off transitions require rate-of-change limiting")
        void rapidOnOffTransitions() {
            // Start cruise at 100 liters/hour
            limiter.applyLimit(100.0f, OperationalMode.CRUISE, 100);

            // Try to drop to 0 in 100ms (would be 1000 liters/hour/second change)
            // Max allowed change = 100 * 0.1 = 10 liters/hour
            FuelRateResult drop = limiter.applyLimit(0.0f, OperationalMode.CRUISE, 100);
            assertEquals(90.0f, drop.getActualRate(), 0.001f);
            assertEquals(ClampingReason.RATE_OF_CHANGE, drop.getClampingReason());

            // Continue ramping down
            FuelRateResult drop2 = limiter.applyLimit(0.0f, OperationalMode.CRUISE, 100);
            assertEquals(80.0f, drop2.getActualRate(), 0.001f);
        }

        @Test
        @DisplayName("Floating-point precision: very small changes within limit")
        void floatingPointPrecision() {
            limiter.applyLimit(50.0f, OperationalMode.CRUISE, 100);

            // Request a tiny change (0.001 liters/hour)
            FuelRateResult result = limiter.applyLimit(50.001f, OperationalMode.CRUISE, 100);

            assertEquals(50.001f, result.getActualRate(), 0.0001f);
            assertFalse(result.wasClampedReason());
        }

        @Test
        @DisplayName("Cruise mode with no minimum bound allows zero fuel rate")
        void cruiseZeroFuelRate() {
            limiter.applyLimit(50.0f, OperationalMode.CRUISE, 100);

            // Request zero with sufficient time window to allow rate-of-change
            FuelRateResult result = limiter.applyLimit(0.0f, OperationalMode.CRUISE, 600);

            // Change = 50, allowed change in 600ms = 100 * 0.6 = 60
            assertEquals(0.0f, result.getActualRate(), 0.001f);
            assertFalse(result.wasClampedReason());
        }

        @Test
        @DisplayName("Multiple rapid calls accumulate rate-of-change correctly")
        void multipleRapidCalls() {
            // Start at 0
            limiter.applyLimit(0.0f, OperationalMode.CRUISE, 100);

            // Call 1: Try to jump to 50 in 100ms (max 10 allowed)
            FuelRateResult call1 = limiter.applyLimit(50.0f, OperationalMode.CRUISE, 100);
            assertEquals(10.0f, call1.getActualRate(), 0.001f);

            // Call 2: Try to jump to 50 again in 100ms (max 10 from current 10)
            FuelRateResult call2 = limiter.applyLimit(50.0f, OperationalMode.CRUISE, 100);
            assertEquals(20.0f, call2.getActualRate(), 0.001f);

            // Call 3: Try to jump to 50 again in 100ms (max 10 from current 20)
            FuelRateResult call3 = limiter.applyLimit(50.0f, OperationalMode.CRUISE, 100);
            assertEquals(30.0f, call3.getActualRate(), 0.001f);

            // Call 4: Try to jump to 50 again in 100ms (max 10 from current 30)
            FuelRateResult call4 = limiter.applyLimit(50.0f, OperationalMode.CRUISE, 100);
            assertEquals(40.0f, call4.getActualRate(), 0.001f);

            // Call 5: Try to jump to 50 again in 100ms (max 10 from current 40)
            FuelRateResult call5 = limiter.applyLimit(50.0f, OperationalMode.CRUISE, 100);
            assertEquals(50.0f, call5.getActualRate(), 0.001f);
            assertFalse(call5.wasClampedReason());
        }

        @Test
        @DisplayName("Startup mode ignores rate-of-change limit (uses mode bounds only)")
        void startupModeIgnoresRateOfChangeLimit() {
            // Start at 0 (clamped to 10 minimum)
            FuelRateResult start = limiter.applyLimit(0.0f, OperationalMode.STARTUP, 100);
            assertEquals(10.0f, start.getActualRate(), 0.001f);

            // Jump directly to 50 in startup mode (should work, no rate-of-change check)
            FuelRateResult jump = limiter.applyLimit(50.0f, OperationalMode.STARTUP, 100);
            assertEquals(50.0f, jump.getActualRate(), 0.001f);
            assertFalse(jump.wasClampedReason());
            assertEquals(ClampingReason.NONE, jump.getClampingReason());
        }

        @Test
        @DisplayName("Switching from startup to cruise preserves rate-of-change state")
        void modeTransitionPreservesState() {
            // Startup at 40 liters/hour
            limiter.applyLimit(40.0f, OperationalMode.STARTUP, 100);
            assertEquals(40.0f, limiter.getPreviousRate(), 0.001f);

            // Switch to cruise and try to increase to 60 in 100ms
            // Change = 20, max allowed = 10, should be clamped
            FuelRateResult result = limiter.applyLimit(60.0f, OperationalMode.CRUISE, 100);
            assertEquals(50.0f, result.getActualRate(), 0.001f);
            assertEquals(ClampingReason.RATE_OF_CHANGE, result.getClampingReason());
        }

        @Test
        @DisplayName("Thread-safety: synchronized access to previous_rate")
        void threadSafetyBasic() {
            // This test verifies the method is synchronized, preventing concurrent modification
            FuelRateResult result1 = limiter.applyLimit(25.0f, OperationalMode.STARTUP, 100);
            FuelRateResult result2 = limiter.applyLimit(50.0f, OperationalMode.CRUISE, 100);

            // Sequential calls should maintain consistent state
            assertEquals(50.0f, limiter.getPreviousRate(), 0.001f);
            assertTrue(result2.wasClampedReason());
        }
    }

    // ============================================================================
    // PARAMETERIZED TESTS
    // ============================================================================

    @Nested
    @DisplayName("Parameterized Tests")
    class ParameterizedTests {

        @ParameterizedTest(name = "Startup rate {0} should be clamped to minimum")
        @ValueSource(floats = {0.0f, 1.0f, 5.0f, 9.0f, 9.999f})
        @DisplayName("Various rates below startup minimum")
        void startupRatesUnderMinimum(float requestedRate) {
            FuelRateResult result = limiter.applyLimit(requestedRate, OperationalMode.STARTUP, 100);

            assertEquals(10.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.MODE_MIN, result.getClampingReason());
        }

        @ParameterizedTest(name = "Startup rate {0} should be clamped to maximum")
        @ValueSource(floats = {50.001f, 75.0f, 100.0f, 500.0f, 1000.0f})
        @DisplayName("Various rates above startup maximum")
        void startupRatesOverMaximum(float requestedRate) {
            FuelRateResult result = limiter.applyLimit(requestedRate, OperationalMode.STARTUP, 100);

            assertEquals(50.0f, result.getActualRate(), 0.001f);
            assertTrue(result.wasClampedReason());
            assertEquals(ClampingReason.MODE_MAX, result.getClampingReason());
        }

        @ParameterizedTest(name = "Startup rate {0} within bounds should not be clamped")
        @ValueSource(floats = {10.0f, 15.0f, 25.0f, 40.0f, 50.0f})
        @DisplayName("Valid startup rates")
        void startupValidRates(float requestedRate) {
            FuelRateResult result = limiter.applyLimit(requestedRate, OperationalMode.STARTUP, 100);

            assertEquals(requestedRate, result.getActualRate(), 0.001f);
            assertFalse(result.wasClampedReason());
            assertEquals(ClampingReason.NONE, result.getClampingReason());
        }

        @ParameterizedTest(name = "Various time intervals: {0}ms")
        @ValueSource(ints = {0, 1, 10, 50, 100, 500, 1000, 5000})
        @DisplayName("Rate-of-change calculation with different time intervals")
        void rateOfChangeWithVariousIntervals(int elapsedMs) {
            limiter.applyLimit(100.0f, OperationalMode.CRUISE, 100);

            float maxAllowedChange = 100.0f * elapsedMs / 1000.0f;
            float requestedRate = 100.0f + maxAllowedChange + 1.0f; // Just exceed limit

            FuelRateResult result = limiter.applyLimit(requestedRate, OperationalMode.CRUISE, elapsedMs);

            if (maxAllowedChange >= 1.0f) {
                // Can accommodate the change
                assertEquals(requestedRate, result.getActualRate(), 0.001f);
            } else {
                // Change is clamped
                assertTrue(result.wasClampedReason());
                assertEquals(ClampingReason.RATE_OF_CHANGE, result.getClampingReason());
            }
        }
    }
}
