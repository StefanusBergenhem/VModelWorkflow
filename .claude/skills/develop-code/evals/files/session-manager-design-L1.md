---
artifact_id: CD-003
artifact_type: detailed-design
version: 1.0.0
status: approved
component: session-management
layer: 1
trace_from: [ARCH-021, ARCH-022]
---

# Session Management

## Purpose

Manages user sessions for an HTTP API server. Handles session creation on login, validation on each request, and cleanup of expired sessions. Without this component, the API server would have no way to track authenticated users between requests, forcing re-authentication on every call.

## External Interfaces

| Direction | Partner Component | Mechanism | Data | Description |
|-----------|-------------------|-----------|------|-------------|
| Receives | auth-controller | function call | Credentials | Login request with username and token |
| Provides | auth-controller | return value | SessionToken | Opaque session token string |
| Receives | request-router | function call | SessionToken | Token from request header for validation |
| Provides | request-router | return value | SessionInfo | User id, roles, expiry time — or rejection |
| Receives | scheduler | function call | — | Periodic trigger to clean expired sessions |

## Unit Inventory

| Unit ID | Layer | Brief Description |
|---------|-------|-------------------|
| SessionStore | 1 | In-memory storage of active sessions with thread-safe access |
| SessionValidator | 1 | Checks if a session token is valid, not expired, and not revoked |
| SessionCleaner | 1 | Removes expired sessions on a periodic schedule |

## Shared Patterns

### Error Strategy

All units return result objects rather than throwing exceptions. Callers check the result type (success or specific error variant). No session operation should ever crash the server — all failures are contained and reported through return values.

### Threading Model

The session store is accessed from multiple request-handling threads concurrently. All access must be thread-safe. The cleaner runs on a separate timer thread and must not block request-handling threads for more than 1ms.

### Common Data Types

- `SessionToken`: opaque string, 32 hex characters
- `SessionInfo`: contains user_id (string), roles (list of strings), created_at (timestamp), expires_at (timestamp)
- `SessionError`: enum with values invalid_token, expired, revoked, store_full

## Constraints

- Maximum 10,000 concurrent sessions
- Session creation must complete in under 5ms
- Session validation must complete in under 1ms
- Default session TTL: 30 minutes
- Token generation must be cryptographically random
