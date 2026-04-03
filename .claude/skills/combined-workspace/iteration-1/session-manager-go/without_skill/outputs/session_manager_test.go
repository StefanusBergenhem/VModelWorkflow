package session

import (
	"testing"
	"time"
)

// TestSessionStoreCreation tests that a session store can be created
func TestSessionStoreCreation(t *testing.T) {
	store := NewSessionStore(100, 30*time.Minute)

	if store == nil {
		t.Fatal("NewSessionStore returned nil")
	}

	if store.maxSessions != 100 {
		t.Errorf("expected maxSessions=100, got %d", store.maxSessions)
	}

	if store.defaultTTL != 30*time.Minute {
		t.Errorf("expected defaultTTL=30m, got %v", store.defaultTTL)
	}

	if store.GetSessionCount() != 0 {
		t.Errorf("expected initial session count=0, got %d", store.GetSessionCount())
	}
}

// TestCreateSession tests basic session creation
func TestCreateSession(t *testing.T) {
	store := NewSessionStore(100, 30*time.Minute)

	result := store.CreateSession("user123", []string{"admin", "user"})

	if !result.Success {
		t.Fatalf("CreateSession failed: %v", result.Error)
	}

	token, ok := result.Data.(SessionToken)
	if !ok {
		t.Fatal("Result data is not a SessionToken")
	}

	if token == "" {
		t.Fatal("SessionToken is empty")
	}

	if store.GetSessionCount() != 1 {
		t.Errorf("expected session count=1, got %d", store.GetSessionCount())
	}
}

// TestSessionTokenFormat tests that tokens are valid hex strings
func TestSessionTokenFormat(t *testing.T) {
	store := NewSessionStore(100, 30*time.Minute)

	result := store.CreateSession("user123", []string{"admin"})
	token := result.Data.(SessionToken)

	// Should be 32 hex characters
	if len(string(token)) != 32 {
		t.Errorf("expected token length=32, got %d", len(string(token)))
	}

	// Should be valid hex
	for _, ch := range string(token) {
		if !((ch >= '0' && ch <= '9') || (ch >= 'a' && ch <= 'f')) {
			t.Errorf("invalid hex character in token: %c", ch)
		}
	}
}

// TestValidateSessionSuccess tests successful session validation
func TestValidateSessionSuccess(t *testing.T) {
	store := NewSessionStore(100, 30*time.Minute)
	validator := NewSessionValidator(store)

	createResult := store.CreateSession("user456", []string{"viewer"})
	token := createResult.Data.(SessionToken)

	validateResult := validator.ValidateSession(token)

	if !validateResult.Success {
		t.Fatalf("ValidateSession failed: %v", validateResult.Error)
	}

	info, ok := validateResult.Data.(SessionInfo)
	if !ok {
		t.Fatal("Result data is not SessionInfo")
	}

	if info.UserID != "user456" {
		t.Errorf("expected UserID=user456, got %s", info.UserID)
	}

	if len(info.Roles) != 1 || info.Roles[0] != "viewer" {
		t.Errorf("expected Roles=[viewer], got %v", info.Roles)
	}

	if info.CreatedAt.IsZero() {
		t.Error("CreatedAt should not be zero")
	}

	if info.ExpiresAt.IsZero() {
		t.Error("ExpiresAt should not be zero")
	}
}

// TestValidateSessionInvalidToken tests validation with non-existent token
func TestValidateSessionInvalidToken(t *testing.T) {
	store := NewSessionStore(100, 30*time.Minute)
	validator := NewSessionValidator(store)

	result := validator.ValidateSession(SessionToken("invalidtoken1234567890abcdef0123"))

	if result.Success {
		t.Fatal("ValidateSession should fail for invalid token")
	}

	if result.Error != ErrorInvalidToken {
		t.Errorf("expected ErrorInvalidToken, got %v", result.Error)
	}
}

// TestValidateSessionExpired tests validation with expired session
func TestValidateSessionExpired(t *testing.T) {
	store := NewSessionStore(100, 1*time.Millisecond) // Very short TTL
	validator := NewSessionValidator(store)

	createResult := store.CreateSession("user789", []string{"admin"})
	token := createResult.Data.(SessionToken)

	// Wait for session to expire
	time.Sleep(10 * time.Millisecond)

	result := validator.ValidateSession(token)

	if result.Success {
		t.Fatal("ValidateSession should fail for expired session")
	}

	if result.Error != ErrorExpired {
		t.Errorf("expected ErrorExpired, got %v", result.Error)
	}
}

// TestRevokeSession tests session revocation
func TestRevokeSession(t *testing.T) {
	store := NewSessionStore(100, 30*time.Minute)
	validator := NewSessionValidator(store)

	createResult := store.CreateSession("user999", []string{"admin"})
	token := createResult.Data.(SessionToken)

	// Verify session is valid before revocation
	validateResult := validator.ValidateSession(token)
	if !validateResult.Success {
		t.Fatal("ValidateSession should succeed before revocation")
	}

	// Revoke the session
	revokeResult := store.RevokeSession(token)
	if !revokeResult.Success {
		t.Fatalf("RevokeSession failed: %v", revokeResult.Error)
	}

	// Verify session is now invalid
	validateResult = validator.ValidateSession(token)
	if validateResult.Success {
		t.Fatal("ValidateSession should fail after revocation")
	}

	if validateResult.Error != ErrorRevoked {
		t.Errorf("expected ErrorRevoked, got %v", validateResult.Error)
	}
}

// TestRevokeNonExistentSession tests revoking a non-existent session
func TestRevokeNonExistentSession(t *testing.T) {
	store := NewSessionStore(100, 30*time.Minute)

	result := store.RevokeSession(SessionToken("nonexistent123456789abcdef0123456"))

	if result.Success {
		t.Fatal("RevokeSession should fail for non-existent session")
	}

	if result.Error != ErrorInvalidToken {
		t.Errorf("expected ErrorInvalidToken, got %v", result.Error)
	}
}

// TestStoreFullError tests that store respects maximum capacity
func TestStoreFullError(t *testing.T) {
	maxSessions := 5
	store := NewSessionStore(maxSessions, 30*time.Minute)

	// Fill the store
	for i := 0; i < maxSessions; i++ {
		result := store.CreateSession("user"+string(rune(i)), []string{})
		if !result.Success {
			t.Fatalf("CreateSession failed at iteration %d: %v", i, result.Error)
		}
	}

	// Try to exceed capacity
	result := store.CreateSession("overflow_user", []string{})
	if result.Success {
		t.Fatal("CreateSession should fail when store is full")
	}

	if result.Error != ErrorStoreFull {
		t.Errorf("expected ErrorStoreFull, got %v", result.Error)
	}

	if store.GetSessionCount() != maxSessions {
		t.Errorf("expected session count=%d, got %d", maxSessions, store.GetSessionCount())
	}
}

// TestMultipleRoles tests session with multiple roles
func TestMultipleRoles(t *testing.T) {
	store := NewSessionStore(100, 30*time.Minute)
	validator := NewSessionValidator(store)

	roles := []string{"admin", "user", "viewer", "moderator"}
	createResult := store.CreateSession("poweruser", roles)
	token := createResult.Data.(SessionToken)

	validateResult := validator.ValidateSession(token)
	info := validateResult.Data.(SessionInfo)

	if len(info.Roles) != len(roles) {
		t.Errorf("expected %d roles, got %d", len(roles), len(info.Roles))
	}

	for i, role := range roles {
		if i >= len(info.Roles) || info.Roles[i] != role {
			t.Errorf("expected role[%d]=%s, got %s", i, role, info.Roles[i])
		}
	}
}

// TestEmptyRoles tests session with no roles
func TestEmptyRoles(t *testing.T) {
	store := NewSessionStore(100, 30*time.Minute)
	validator := NewSessionValidator(store)

	createResult := store.CreateSession("guest", []string{})
	token := createResult.Data.(SessionToken)

	validateResult := validator.ValidateSession(token)
	info := validateResult.Data.(SessionInfo)

	if len(info.Roles) != 0 {
		t.Errorf("expected 0 roles, got %d", len(info.Roles))
	}
}

// TestSessionCleanerCreation tests that a cleaner can be created
func TestSessionCleanerCreation(t *testing.T) {
	store := NewSessionStore(100, 30*time.Minute)
	cleaner := NewSessionCleaner(store, 100*time.Millisecond)

	if cleaner == nil {
		t.Fatal("NewSessionCleaner returned nil")
	}
}

// TestSessionCleanerRemovesExpiredSessions tests that the cleaner removes expired sessions
func TestSessionCleanerRemovesExpiredSessions(t *testing.T) {
	store := NewSessionStore(100, 50*time.Millisecond) // Short TTL
	cleaner := NewSessionCleaner(store, 100*time.Millisecond)

	// Create a session
	createResult := store.CreateSession("cleanuptest", []string{})
	if !createResult.Success {
		t.Fatal("CreateSession failed")
	}

	if store.GetSessionCount() != 1 {
		t.Errorf("expected session count=1, got %d", store.GetSessionCount())
	}

	// Wait for session to expire and run cleaner
	time.Sleep(150 * time.Millisecond)

	// Manually clean (no goroutine version)
	cleaner.cleanExpiredSessions()

	// Session should be removed
	if store.GetSessionCount() != 0 {
		t.Errorf("expected session count=0 after cleanup, got %d", store.GetSessionCount())
	}
}

// TestConcurrentCreateAndValidate tests thread-safe concurrent access
func TestConcurrentCreateAndValidate(t *testing.T) {
	store := NewSessionStore(1000, 30*time.Minute)
	validator := NewSessionValidator(store)

	numGoroutines := 10
	sessionsPerGoroutine := 50
	done := make(chan bool, numGoroutines)

	// Create sessions concurrently
	for i := 0; i < numGoroutines; i++ {
		go func(id int) {
			tokens := []SessionToken{}
			for j := 0; j < sessionsPerGoroutine; j++ {
				result := store.CreateSession("user"+string(rune(id))+string(rune(j)), []string{"user"})
				if result.Success {
					tokens = append(tokens, result.Data.(SessionToken))
				}
			}

			// Validate concurrently
			for _, token := range tokens {
				validateResult := validator.ValidateSession(token)
				if !validateResult.Success {
					t.Errorf("ValidateSession failed for token: %v", validateResult.Error)
				}
			}
			done <- true
		}(i)
	}

	// Wait for all goroutines to complete
	for i := 0; i < numGoroutines; i++ {
		<-done
	}

	expectedCount := numGoroutines * sessionsPerGoroutine
	if store.GetSessionCount() != expectedCount {
		t.Errorf("expected %d sessions, got %d", expectedCount, store.GetSessionCount())
	}
}

// TestTokenUniqueness tests that generated tokens are unique
func TestTokenUniqueness(t *testing.T) {
	store := NewSessionStore(1000, 30*time.Minute)

	tokens := make(map[SessionToken]bool)
	numTokens := 100

	for i := 0; i < numTokens; i++ {
		result := store.CreateSession("user"+string(rune(i)), []string{})
		token := result.Data.(SessionToken)

		if tokens[token] {
			t.Fatalf("Duplicate token generated: %s", token)
		}
		tokens[token] = true
	}

	if len(tokens) != numTokens {
		t.Errorf("expected %d unique tokens, got %d", numTokens, len(tokens))
	}
}

// TestExpiryTimestamp tests that expiry time is set correctly
func TestExpiryTimestamp(t *testing.T) {
	ttl := 5 * time.Minute
	store := NewSessionStore(100, ttl)
	validator := NewSessionValidator(store)

	beforeCreate := time.Now()
	createResult := store.CreateSession("expirytest", []string{})
	afterCreate := time.Now()
	token := createResult.Data.(SessionToken)

	validateResult := validator.ValidateSession(token)
	info := validateResult.Data.(SessionInfo)

	expectedExpiryMin := beforeCreate.Add(ttl)
	expectedExpiryMax := afterCreate.Add(ttl)

	if info.ExpiresAt.Before(expectedExpiryMin) || info.ExpiresAt.After(expectedExpiryMax) {
		t.Errorf("expiry time out of expected range: expected [%v, %v], got %v",
			expectedExpiryMin, expectedExpiryMax, info.ExpiresAt)
	}
}

// TestCreatedAtTimestamp tests that creation time is set correctly
func TestCreatedAtTimestamp(t *testing.T) {
	store := NewSessionStore(100, 30*time.Minute)
	validator := NewSessionValidator(store)

	beforeCreate := time.Now()
	createResult := store.CreateSession("createdattest", []string{})
	afterCreate := time.Now()
	token := createResult.Data.(SessionToken)

	validateResult := validator.ValidateSession(token)
	info := validateResult.Data.(SessionInfo)

	if info.CreatedAt.Before(beforeCreate) || info.CreatedAt.After(afterCreate) {
		t.Errorf("created time out of expected range: expected [%v, %v], got %v",
			beforeCreate, afterCreate, info.CreatedAt)
	}
}

// TestRolesMutationIsolation tests that modifying original roles doesn't affect stored roles
func TestRolesMutationIsolation(t *testing.T) {
	store := NewSessionStore(100, 30*time.Minute)
	validator := NewSessionValidator(store)

	roles := []string{"admin", "user"}
	createResult := store.CreateSession("mutationtest", roles)
	token := createResult.Data.(SessionToken)

	// Mutate the original roles slice
	roles[0] = "hacker"
	roles = append(roles, "attacker")

	// Validate and check that stored roles are unchanged
	validateResult := validator.ValidateSession(token)
	info := validateResult.Data.(SessionInfo)

	if len(info.Roles) != 2 {
		t.Errorf("expected 2 roles, got %d", len(info.Roles))
	}

	if info.Roles[0] != "admin" || info.Roles[1] != "user" {
		t.Errorf("expected [admin, user], got %v", info.Roles)
	}
}

// TestValidatorWithNilStore tests validator behavior with nil operations
func TestValidatorWithNilStore(t *testing.T) {
	store := NewSessionStore(100, 30*time.Minute)
	validator := NewSessionValidator(store)

	// Test with empty UserID
	createResult := store.CreateSession("", []string{})
	if !createResult.Success {
		t.Fatal("CreateSession should succeed with empty UserID")
	}

	token := createResult.Data.(SessionToken)
	validateResult := validator.ValidateSession(token)
	info := validateResult.Data.(SessionInfo)

	if info.UserID != "" {
		t.Errorf("expected empty UserID, got %s", info.UserID)
	}
}

// TestSessionCleanerGoroutine tests the cleaner in a background goroutine
func TestSessionCleanerGoroutine(t *testing.T) {
	store := NewSessionStore(100, 50*time.Millisecond)
	cleaner := NewSessionCleaner(store, 75*time.Millisecond)

	// Create a session
	createResult := store.CreateSession("goroutinetest", []string{})
	token := createResult.Data.(SessionToken)

	if store.GetSessionCount() != 1 {
		t.Errorf("expected 1 session, got %d", store.GetSessionCount())
	}

	// Start cleaner in background
	go cleaner.Start(75 * time.Millisecond)

	// Wait for expiry and cleanup
	time.Sleep(250 * time.Millisecond)

	// Stop cleaner
	cleaner.Stop()
	cleaner.Wait()

	// Session should be cleaned up
	if store.GetSessionCount() != 0 {
		t.Errorf("expected 0 sessions after background cleanup, got %d", store.GetSessionCount())
	}
}

// BenchmarkCreateSession benchmarks session creation
func BenchmarkCreateSession(b *testing.B) {
	store := NewSessionStore(100000, 30*time.Minute)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		store.CreateSession("user", []string{"admin"})
	}
}

// BenchmarkValidateSession benchmarks session validation
func BenchmarkValidateSession(b *testing.B) {
	store := NewSessionStore(100000, 30*time.Minute)
	validator := NewSessionValidator(store)

	createResult := store.CreateSession("user", []string{"admin"})
	token := createResult.Data.(SessionToken)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		validator.ValidateSession(token)
	}
}

// BenchmarkRevokeSession benchmarks session revocation
func BenchmarkRevokeSession(b *testing.B) {
	store := NewSessionStore(100000, 30*time.Minute)

	tokens := make([]SessionToken, b.N)
	for i := 0; i < b.N; i++ {
		result := store.CreateSession("user", []string{})
		tokens[i] = result.Data.(SessionToken)
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		store.RevokeSession(tokens[i])
	}
}
