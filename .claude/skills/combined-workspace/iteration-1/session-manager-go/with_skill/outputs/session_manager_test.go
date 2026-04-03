package session

import (
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

// TestCreateValidSession tests happy path: valid user and roles.
func TestCreateValidSession(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)
	result := store.Create("user123", []string{"admin", "user"})

	if !result.Success {
		t.Errorf("Create should succeed for valid user, got error: %v", result.Error)
	}
	if result.Token == "" {
		t.Errorf("Create should return non-empty token")
	}
}

// TestCreateSessionWithEmptyRoles tests Create with nil roles.
func TestCreateSessionWithEmptyRoles(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)
	result := store.Create("user456", nil)

	if !result.Success {
		t.Errorf("Create should succeed with nil roles, got error: %v", result.Error)
	}
	if result.Token == "" {
		t.Errorf("Create should return non-empty token")
	}

	// Verify roles initialized to empty slice
	validateResult := store.Validate(result.Token)
	if len(validateResult.Info.Roles) != 0 {
		t.Errorf("Roles should be empty slice when nil provided, got %v", validateResult.Info.Roles)
	}
}

// TestCreateRejectsEmptyUserID tests that empty user ID is rejected.
func TestCreateRejectsEmptyUserID(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)
	result := store.Create("", []string{"user"})

	if result.Success {
		t.Errorf("Create should reject empty user ID")
	}
	if result.Error != ErrorInvalidToken {
		t.Errorf("Expected ErrorInvalidToken, got %v", result.Error)
	}
}

// TestCreateWhenNearCapacity tests store at near-max capacity.
func TestCreateWhenNearCapacity(t *testing.T) {
	store := NewSessionStore(3, DefaultTTL)

	// Fill to capacity - 1
	for i := 0; i < 2; i++ {
		result := store.Create("user"+string(rune(i)), []string{})
		if !result.Success {
			t.Fatalf("Create failed when there was capacity: %v", result.Error)
		}
	}

	// One more should succeed
	result := store.Create("user999", []string{})
	if !result.Success {
		t.Errorf("Create should succeed at max capacity, got error: %v", result.Error)
	}
}

// TestCreateWhenStoreFull tests that store rejects when at max capacity.
func TestCreateWhenStoreFull(t *testing.T) {
	store := NewSessionStore(2, DefaultTTL)

	// Fill store
	for i := 0; i < 2; i++ {
		store.Create("user"+string(rune(i)), []string{})
	}

	// Next create should fail
	result := store.Create("userExtra", []string{})
	if result.Success {
		t.Errorf("Create should fail when store is full")
	}
	if result.Error != ErrorStoreFull {
		t.Errorf("Expected ErrorStoreFull, got %v", result.Error)
	}
}

// TestCreateGeneratesUniqueTokens tests that tokens are unique.
func TestCreateGeneratesUniqueTokens(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)

	result1 := store.Create("user1", []string{})
	result2 := store.Create("user2", []string{})
	result3 := store.Create("user3", []string{})

	if result1.Token == result2.Token || result2.Token == result3.Token || result1.Token == result3.Token {
		t.Errorf("Tokens should be unique, got: %s, %s, %s", result1.Token, result2.Token, result3.Token)
	}
}

// TestCreateTokenFormatIs32HexChars tests token format is 32 hex characters.
func TestCreateTokenFormatIs32HexChars(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)
	result := store.Create("user", []string{})

	if len(result.Token) != 32 {
		t.Errorf("Token should be 32 characters, got %d", len(result.Token))
	}

	// Verify all characters are hex
	for i, ch := range result.Token {
		if !((ch >= '0' && ch <= '9') || (ch >= 'a' && ch <= 'f')) {
			t.Errorf("Token character at position %d is not hex: %c", i, ch)
		}
	}
}

// TestCreateSetsExpiryCorrectly tests that expiry is set to now + TTL.
func TestCreateSetsExpiryCorrectly(t *testing.T) {
	ttl := 5 * time.Minute
	store := NewSessionStore(MaxSessions, ttl)

	before := time.Now()
	result := store.Create("user", []string{})
	after := time.Now()

	validateResult := store.Validate(result.Token)
	info := validateResult.Info

	// ExpiresAt should be approximately before/after + TTL
	expectedMin := before.Add(ttl)
	expectedMax := after.Add(ttl)

	if info.ExpiresAt.Before(expectedMin) || info.ExpiresAt.After(expectedMax) {
		t.Errorf("ExpiresAt not set correctly: expected ~%v, got %v", before.Add(ttl), info.ExpiresAt)
	}
}

// TestCreatePreservesRoles tests that roles are stored and retrieved correctly.
func TestCreatePreservesRoles(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)
	roles := []string{"admin", "operator", "viewer"}

	result := store.Create("user", roles)
	validateResult := store.Validate(result.Token)

	if len(validateResult.Info.Roles) != len(roles) {
		t.Errorf("Role count mismatch: expected %d, got %d", len(roles), len(validateResult.Info.Roles))
	}
	for i, role := range roles {
		if validateResult.Info.Roles[i] != role {
			t.Errorf("Role mismatch at index %d: expected %s, got %s", i, role, validateResult.Info.Roles[i])
		}
	}
}

// TestValidateValidSession tests validation of a valid session.
func TestValidateValidSession(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)
	createResult := store.Create("testuser", []string{"admin"})

	validateResult := store.Validate(createResult.Token)

	if !validateResult.Success {
		t.Errorf("Validate should succeed for valid session, got error: %v", validateResult.Error)
	}
	if validateResult.Info.UserID != "testuser" {
		t.Errorf("UserID mismatch: expected testuser, got %s", validateResult.Info.UserID)
	}
}

// TestValidateInvalidToken tests validation of nonexistent token.
func TestValidateInvalidToken(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)

	result := store.Validate("invalidtoken123456789012345678901")

	if result.Success {
		t.Errorf("Validate should fail for nonexistent token")
	}
	if result.Error != ErrorInvalidToken {
		t.Errorf("Expected ErrorInvalidToken, got %v", result.Error)
	}
}

// TestValidateExpiredSession tests that expired sessions are rejected.
func TestValidateExpiredSession(t *testing.T) {
	shortTTL := 100 * time.Millisecond
	store := NewSessionStore(MaxSessions, shortTTL)

	createResult := store.Create("user", []string{})
	time.Sleep(200 * time.Millisecond)

	result := store.Validate(createResult.Token)

	if result.Success {
		t.Errorf("Validate should fail for expired session")
	}
	if result.Error != ErrorExpired {
		t.Errorf("Expected ErrorExpired, got %v", result.Error)
	}
}

// TestValidateRevokedSession tests that revoked sessions are rejected.
func TestValidateRevokedSession(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)

	createResult := store.Create("user", []string{})
	store.Revoke(createResult.Token)

	result := store.Validate(createResult.Token)

	if result.Success {
		t.Errorf("Validate should fail for revoked session")
	}
	if result.Error != ErrorRevoked {
		t.Errorf("Expected ErrorRevoked, got %v", result.Error)
	}
}

// TestValidateEmptyToken tests validation with empty token.
func TestValidateEmptyToken(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)

	result := store.Validate("")

	if result.Success {
		t.Errorf("Validate should fail for empty token")
	}
	if result.Error != ErrorInvalidToken {
		t.Errorf("Expected ErrorInvalidToken, got %v", result.Error)
	}
}

// TestValidateReturnsCorrectInfo tests that Validate returns exact session info.
func TestValidateReturnsCorrectInfo(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)
	userID := "testuser"
	roles := []string{"role1", "role2"}

	createResult := store.Create(userID, roles)
	validateResult := store.Validate(createResult.Token)

	if validateResult.Info.UserID != userID {
		t.Errorf("UserID mismatch: expected %s, got %s", userID, validateResult.Info.UserID)
	}
	if len(validateResult.Info.Roles) != len(roles) {
		t.Errorf("Role count mismatch: expected %d, got %d", len(roles), len(validateResult.Info.Roles))
	}
	if !validateResult.Info.CreatedAt.Before(time.Now().Add(1 * time.Second)) {
		t.Errorf("CreatedAt should be recent")
	}
	if !validateResult.Info.ExpiresAt.After(time.Now()) {
		t.Errorf("ExpiresAt should be in the future")
	}
}

// TestValidateAtExactExpiry tests validation at exact expiry boundary.
func TestValidateAtExactExpiry(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)
	createResult := store.Create("user", []string{})

	// Mock the expiry check by manipulating the internal session's expiry time
	// We'll do this by creating a store with very short TTL and sleeping
	shortStore := NewSessionStore(MaxSessions, 1*time.Millisecond)
	shortCreateResult := shortStore.Create("user", []string{})
	time.Sleep(2 * time.Millisecond)

	result := shortStore.Validate(shortCreateResult.Token)

	if result.Success {
		t.Errorf("Validate should fail at/after expiry boundary")
	}
	if result.Error != ErrorExpired {
		t.Errorf("Expected ErrorExpired, got %v", result.Error)
	}
}

// TestValidateJustBeforeExpiry tests validation just before expiry.
func TestValidateJustBeforeExpiry(t *testing.T) {
	ttl := 500 * time.Millisecond
	store := NewSessionStore(MaxSessions, ttl)

	createResult := store.Create("user", []string{})
	time.Sleep(400 * time.Millisecond) // Just before expiry

	result := store.Validate(createResult.Token)

	if !result.Success {
		t.Errorf("Validate should succeed before expiry, got error: %v", result.Error)
	}
}

// TestRevokeValidSession tests revoking a valid session.
func TestRevokeValidSession(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)

	createResult := store.Create("user", []string{})
	revokeResult := store.Revoke(createResult.Token)

	if !revokeResult.Success {
		t.Errorf("Revoke should succeed for valid session, got error: %v", revokeResult.Error)
	}
}

// TestValidateAfterRevoke tests that validation fails after revocation.
func TestValidateAfterRevoke(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)

	createResult := store.Create("user", []string{})
	store.Revoke(createResult.Token)

	validateResult := store.Validate(createResult.Token)

	if validateResult.Success {
		t.Errorf("Validate should fail after revoke")
	}
	if validateResult.Error != ErrorRevoked {
		t.Errorf("Expected ErrorRevoked after revoke, got %v", validateResult.Error)
	}
}

// TestRevokeInvalidToken tests revoking a nonexistent token.
func TestRevokeInvalidToken(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)

	result := store.Revoke("invalidtoken123456789012345678901")

	if result.Success {
		t.Errorf("Revoke should fail for invalid token")
	}
	if result.Error != ErrorInvalidToken {
		t.Errorf("Expected ErrorInvalidToken, got %v", result.Error)
	}
}

// TestRevokeAlreadyRevoked tests that revoking twice is idempotent.
func TestRevokeAlreadyRevoked(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)

	createResult := store.Create("user", []string{})
	store.Revoke(createResult.Token)

	// Second revoke should succeed (idempotent)
	result := store.Revoke(createResult.Token)

	if !result.Success {
		t.Errorf("Second revoke should succeed (idempotent), got error: %v", result.Error)
	}
}

// TestCleanExpiredRemovesExpiredSessions tests that cleanup removes expired sessions.
func TestCleanExpiredRemovesExpiredSessions(t *testing.T) {
	shortTTL := 100 * time.Millisecond
	store := NewSessionStore(MaxSessions, shortTTL)

	// Create and let expire
	result1 := store.Create("user1", []string{})
	time.Sleep(200 * time.Millisecond)

	// Create fresh session
	result2 := store.Create("user2", []string{})

	removedCount := store.CleanExpired()

	if removedCount != 1 {
		t.Errorf("CleanExpired should remove 1 expired session, removed %d", removedCount)
	}

	// Verify expired session is gone
	validateExpired := store.Validate(result1.Token)
	if validateExpired.Error != ErrorInvalidToken {
		t.Errorf("Expired session should be gone, got error: %v", validateExpired.Error)
	}

	// Verify fresh session still exists
	validateFresh := store.Validate(result2.Token)
	if !validateFresh.Success {
		t.Errorf("Fresh session should still exist, got error: %v", validateFresh.Error)
	}
}

// TestCleanExpiredRemovesRevokedSessions tests that cleanup removes revoked sessions.
func TestCleanExpiredRemovesRevokedSessions(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)

	result1 := store.Create("user1", []string{})
	result2 := store.Create("user2", []string{})

	store.Revoke(result1.Token)

	removedCount := store.CleanExpired()

	if removedCount != 1 {
		t.Errorf("CleanExpired should remove 1 revoked session, removed %d", removedCount)
	}

	// Verify revoked session is gone
	validateRevoked := store.Validate(result1.Token)
	if validateRevoked.Error != ErrorInvalidToken {
		t.Errorf("Revoked session should be gone, got error: %v", validateRevoked.Error)
	}

	// Verify other session still exists
	validateOther := store.Validate(result2.Token)
	if !validateOther.Success {
		t.Errorf("Other session should still exist, got error: %v", validateOther.Error)
	}
}

// TestCleanExpiredReturnsCorrectCount tests that CleanExpired returns accurate count.
func TestCleanExpiredReturnsCorrectCount(t *testing.T) {
	shortTTL := 100 * time.Millisecond
	store := NewSessionStore(MaxSessions, shortTTL)

	// Create 3 sessions and let expire
	store.Create("user1", []string{})
	store.Create("user2", []string{})
	store.Create("user3", []string{})
	time.Sleep(200 * time.Millisecond)

	// Create 2 fresh sessions
	store.Create("user4", []string{})
	store.Create("user5", []string{})

	removedCount := store.CleanExpired()

	if removedCount != 3 {
		t.Errorf("CleanExpired should remove 3 expired sessions, removed %d", removedCount)
	}
}

// TestCleanExpiredWhenEmpty tests cleanup on empty store.
func TestCleanExpiredWhenEmpty(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)

	removedCount := store.CleanExpired()

	if removedCount != 0 {
		t.Errorf("CleanExpired on empty store should remove 0, removed %d", removedCount)
	}
}

// TestCleanExpiredMixed tests cleanup with mixed valid/expired/revoked sessions.
func TestCleanExpiredMixed(t *testing.T) {
	shortTTL := 100 * time.Millisecond
	store := NewSessionStore(MaxSessions, shortTTL)

	// Create 5 sessions
	token1 := store.Create("user1", []string{}).Token
	token2 := store.Create("user2", []string{}).Token
	token3 := store.Create("user3", []string{}).Token
	token4 := store.Create("user4", []string{}).Token
	token5 := store.Create("user5", []string{}).Token

	store.Revoke(token1) // Revoke 1
	time.Sleep(200 * time.Millisecond)
	store.Create("user6", []string{}) // Create fresh after expiry

	// Expected to clean: token1 (revoked), token2-5 (expired)
	removedCount := store.CleanExpired()

	if removedCount != 5 {
		t.Errorf("CleanExpired should remove 5 sessions, removed %d", removedCount)
	}
}

// TestActiveCountAfterCreation tests ActiveCount reflects created sessions.
func TestActiveCountAfterCreation(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)

	store.Create("user1", []string{})
	store.Create("user2", []string{})
	store.Create("user3", []string{})

	count := store.ActiveCount()

	if count != 3 {
		t.Errorf("ActiveCount should be 3, got %d", count)
	}
}

// TestActiveCountExcludesExpired tests that ActiveCount excludes expired sessions.
func TestActiveCountExcludesExpired(t *testing.T) {
	shortTTL := 100 * time.Millisecond
	store := NewSessionStore(MaxSessions, shortTTL)

	store.Create("user1", []string{})
	time.Sleep(200 * time.Millisecond)
	store.Create("user2", []string{})

	count := store.ActiveCount()

	if count != 1 {
		t.Errorf("ActiveCount should exclude expired, expected 1, got %d", count)
	}
}

// TestActiveCountExcludesRevoked tests that ActiveCount excludes revoked sessions.
func TestActiveCountExcludesRevoked(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)

	token1 := store.Create("user1", []string{}).Token
	store.Create("user2", []string{})
	store.Create("user3", []string{})

	store.Revoke(token1)

	count := store.ActiveCount()

	if count != 2 {
		t.Errorf("ActiveCount should exclude revoked, expected 2, got %d", count)
	}
}

// TestActiveCountEmptyStore tests ActiveCount on empty store.
func TestActiveCountEmptyStore(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)

	count := store.ActiveCount()

	if count != 0 {
		t.Errorf("ActiveCount on empty store should be 0, got %d", count)
	}
}

// TestConcurrentCreate tests that concurrent Create calls succeed without races.
func TestConcurrentCreate(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)
	var wg sync.WaitGroup
	errorCount := atomic.Int32{}

	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func(userNum int) {
			defer wg.Done()
			result := store.Create("user"+string(rune(userNum)), []string{})
			if !result.Success {
				errorCount.Add(1)
			}
		}(i)
	}

	wg.Wait()

	if errorCount.Load() > 0 {
		t.Errorf("Concurrent Create had %d errors", errorCount.Load())
	}

	if store.ActiveCount() != 100 {
		t.Errorf("Expected 100 active sessions, got %d", store.ActiveCount())
	}
}

// TestConcurrentCreateAndValidate tests concurrent Create and Validate operations.
func TestConcurrentCreateAndValidate(t *testing.T) {
	store := NewSessionStore(MaxSessions, DefaultTTL)
	tokens := make([]SessionToken, 50)

	// Pre-create tokens
	for i := 0; i < 50; i++ {
		result := store.Create("user"+string(rune(i)), []string{})
		tokens[i] = result.Token
	}

	var wg sync.WaitGroup
	errorCount := atomic.Int32{}

	// Concurrent validates
	for i := 0; i < 50; i++ {
		wg.Add(1)
		go func(idx int) {
			defer wg.Done()
			result := store.Validate(tokens[idx])
			if !result.Success {
				errorCount.Add(1)
			}
		}(i)
	}

	wg.Wait()

	if errorCount.Load() > 0 {
		t.Errorf("Concurrent Validate had %d errors", errorCount.Load())
	}
}

// TestConcurrentCreateAndClean tests that Create and Clean don't race.
func TestConcurrentCreateAndClean(t *testing.T) {
	shortTTL := 50 * time.Millisecond
	store := NewSessionStore(MaxSessions, shortTTL)

	var wg sync.WaitGroup

	// Creator goroutines
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(creatorNum int) {
			defer wg.Done()
			for j := 0; j < 10; j++ {
				store.Create("user"+string(rune(creatorNum*10+j)), []string{})
				time.Sleep(5 * time.Millisecond)
			}
		}(i)
	}

	// Cleaner goroutines
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := 0; j < 20; j++ {
				store.CleanExpired()
				time.Sleep(10 * time.Millisecond)
			}
		}()
	}

	wg.Wait()

	// Test should complete without deadlock or panic
	if store.ActiveCount() < 0 {
		t.Errorf("ActiveCount should be non-negative")
	}
}

// TestValidateDuringClean tests that Validate doesn't block during cleanup.
func TestValidateDuringClean(t *testing.T) {
	shortTTL := 50 * time.Millisecond
	store := NewSessionStore(MaxSessions, shortTTL)

	// Create many sessions
	tokens := make([]SessionToken, 100)
	for i := 0; i < 100; i++ {
		result := store.Create("user"+string(rune(i)), []string{})
		tokens[i] = result.Token
	}

	var wg sync.WaitGroup

	// Cleaner
	wg.Add(1)
	go func() {
		defer wg.Done()
		for i := 0; i < 10; i++ {
			store.CleanExpired()
			time.Sleep(15 * time.Millisecond)
		}
	}()

	// Validators
	validationErrors := atomic.Int32{}
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func(idx int) {
			defer wg.Done()
			result := store.Validate(tokens[idx])
			// Session might be expired, but operation should not hang
			_ = result
		}(i)
	}

	wg.Wait()

	// Test should complete without deadlock
	if validationErrors.Load() > 0 {
		t.Logf("Some validations failed, but that's OK for expired sessions")
	}
}

// TestSessionCleanerRunsPeriodically tests that SessionCleaner executes cleanup on schedule.
func TestSessionCleanerRunsPeriodically(t *testing.T) {
	interval := 100 * time.Millisecond
	shortTTL := 50 * time.Millisecond
	store := NewSessionStore(MaxSessions, shortTTL)

	// Create sessions that will expire
	store.Create("user1", []string{})
	store.Create("user2", []string{})

	cleaner := NewSessionCleaner(store, interval)
	go cleaner.Start()

	// Wait for cleanup to run
	time.Sleep(250 * time.Millisecond)
	cleaner.Stop()

	// Sessions should have been cleaned
	activeCount := store.ActiveCount()
	if activeCount > 0 {
		t.Errorf("SessionCleaner should have removed expired sessions, got %d active", activeCount)
	}
}

// TestSessionCleanerStopsOnSignal tests that Stop() halts the cleaner.
func TestSessionCleanerStopsOnSignal(t *testing.T) {
	interval := 100 * time.Millisecond
	store := NewSessionStore(MaxSessions, DefaultTTL)

	cleaner := NewSessionCleaner(store, interval)
	stopChan := make(chan struct{})

	go func() {
		cleaner.Start()
		stopChan <- struct{}{}
	}()

	cleaner.Stop()

	// Wait for cleaner to actually stop
	select {
	case <-stopChan:
		// Expected
	case <-time.After(500 * time.Millisecond):
		t.Errorf("SessionCleaner.Stop() did not halt the loop in time")
	}
}
