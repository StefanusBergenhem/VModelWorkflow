# Session Manager Test Coverage Matrix

## Design Elements to Test

### SessionStore.Create(userID, roles)

| Design Element | Derivation Strategy | Test Name | Expected Behavior |
|---|---|---|---|
| Happy path: valid user, roles provided | Requirement-Based | TestCreateValidSession | Returns success with non-empty token |
| Happy path: valid user, empty roles | Requirement-Based | TestCreateSessionWithEmptyRoles | Token created, Roles set to empty slice |
| User ID validation: empty string | Error Handling | TestCreateRejectsEmptyUserID | Returns ErrorInvalidToken |
| Store capacity: at max (9999 sessions) | Boundary Value | TestCreateWhenNearCapacity | Returns success |
| Store capacity: exceeds max (10000 sessions) | Boundary Value | TestCreateWhenStoreFull | Returns ErrorStoreFull |
| Token generation: cryptographic randomness | Error Handling | TestCreateGeneratesUniqueTokens | Multiple calls produce different tokens |
| Token format: hex string | Equivalence Class | TestCreateTokenFormatIs32HexChars | Token length is 32, all hex characters |
| Session metadata: TTL applied | Requirement-Based | TestCreateSetsExpiryCorrectly | ExpiresAt = CreatedAt + TTL |
| Session metadata: roles preserved | Requirement-Based | TestCreatePreservesRoles | Returned token validates with correct roles |

### SessionStore.Validate(token)

| Design Element | Derivation Strategy | Test Name | Expected Behavior |
|---|---|---|---|
| Valid, non-expired session | Requirement-Based | TestValidateValidSession | Returns success with SessionInfo |
| Invalid token (not found) | Error Handling | TestValidateInvalidToken | Returns ErrorInvalidToken |
| Expired session | Error Handling | TestValidateExpiredSession | Returns ErrorExpired |
| Revoked session | Error Handling | TestValidateRevokedSession | Returns ErrorRevoked |
| Empty token string | Equivalence Class | TestValidateEmptyToken | Returns ErrorInvalidToken |
| Session info accuracy | Requirement-Based | TestValidateReturnsCorrectInfo | Info matches created session (userID, roles, timestamps) |
| Boundary: exactly at expiry time | Boundary Value | TestValidateAtExactExpiry | Returns ErrorExpired (not before expiry) |
| Boundary: just before expiry | Boundary Value | TestValidateJustBeforeExpiry | Returns success |

### SessionStore.Revoke(token)

| Design Element | Derivation Strategy | Test Name | Expected Behavior |
|---|---|---|---|
| Revoke valid session | Requirement-Based | TestRevokeValidSession | Returns success |
| After revoke, validate fails | Requirement-Based | TestValidateAfterRevoke | Subsequent Validate returns ErrorRevoked |
| Revoke invalid token | Error Handling | TestRevokeInvalidToken | Returns ErrorInvalidToken |
| Double revoke | Error Handling | TestRevokeAlreadyRevoked | Second revoke returns success (idempotent) |

### SessionStore.CleanExpired()

| Design Element | Derivation Strategy | Test Name | Expected Behavior |
|---|---|---|---|
| Remove expired sessions | Requirement-Based | TestCleanExpiredRemovesExpiredSessions | Expired sessions deleted, valid ones remain |
| Remove revoked sessions | Requirement-Based | TestCleanExpiredRemovesRevokedSessions | Revoked sessions deleted |
| Return count of removed | Requirement-Based | TestCleanExpiredReturnsCorrectCount | Returns number of sessions removed |
| No sessions to clean | Equivalence Class | TestCleanExpiredWhenEmpty | Returns 0 on empty store |
| Mixed valid/expired/revoked | Requirement-Based | TestCleanExpiredMixed | Only expired and revoked removed |

### SessionStore.ActiveCount()

| Design Element | Derivation Strategy | Test Name | Expected Behavior |
|---|---|---|---|
| Count active sessions | Requirement-Based | TestActiveCountAfterCreation | Reflects non-expired, non-revoked sessions |
| Exclude expired from count | Requirement-Based | TestActiveCountExcludesExpired | Expired sessions not counted |
| Exclude revoked from count | Requirement-Based | TestActiveCountExcludesRevoked | Revoked sessions not counted |
| Empty store count | Equivalence Class | TestActiveCountEmptyStore | Returns 0 |

### Concurrency and Thread-Safety

| Design Element | Derivation Strategy | Test Name | Expected Behavior |
|---|---|---|---|
| Concurrent Create calls | Error Handling / Concurrency | TestConcurrentCreate | Multiple goroutines creating sessions simultaneously succeed |
| Concurrent Create and Validate | Error Handling / Concurrency | TestConcurrentCreateAndValidate | Operations do not race or deadlock |
| Concurrent Create and Clean | Error Handling / Concurrency | TestConcurrentCreateAndClean | Clean does not block Create beyond 1ms (design requirement) |
| Validate during Clean | Error Handling / Concurrency | TestValidateDuringClean | Validate does not block during cleanup |

### SessionCleaner

| Design Element | Derivation Strategy | Test Name | Expected Behavior |
|---|---|---|---|
| Periodic cleanup execution | Requirement-Based | TestSessionCleanerRunsPeriodically | Cleaner removes expired sessions on schedule |
| Stop signal | Requirement-Based | TestSessionCleanerStopsOnSignal | Stop() halts the cleanup loop |

---

## Summary

- **Total Test Cases:** 31
- **Coverage by Strategy:**
  - Requirement-Based: 16 tests
  - Equivalence Class: 5 tests
  - Boundary Value: 4 tests
  - Error Handling / Fault Injection: 6 tests

- **Coverage by Component:**
  - SessionStore.Create: 9 tests
  - SessionStore.Validate: 8 tests
  - SessionStore.Revoke: 4 tests
  - SessionStore.CleanExpired: 5 tests
  - SessionStore.ActiveCount: 4 tests
  - Concurrency: 4 tests
  - SessionCleaner: 2 tests

All design requirements are covered:
- All interfaces tested (Create, Validate, Revoke, Clean, ActiveCount)
- All error conditions tested (invalid token, expired, revoked, store full)
- Boundary conditions tested (at max capacity, exact expiry time)
- Thread-safety verified with concurrent tests
- Performance-relevant operations (Clean, Validate) included in concurrency tests
