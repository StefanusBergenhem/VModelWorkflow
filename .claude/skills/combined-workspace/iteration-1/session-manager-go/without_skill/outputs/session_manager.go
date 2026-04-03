package session

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"sync"
	"time"
)

// SessionToken is an opaque 32-character hex string representing a session
type SessionToken string

// SessionError represents the type of error that occurred during a session operation
type SessionError string

const (
	ErrorInvalidToken SessionError = "invalid_token"
	ErrorExpired      SessionError = "expired"
	ErrorRevoked      SessionError = "revoked"
	ErrorStoreFull    SessionError = "store_full"
)

// SessionInfo contains user information associated with a session
type SessionInfo struct {
	UserID    string    `json:"user_id"`
	Roles     []string  `json:"roles"`
	CreatedAt time.Time `json:"created_at"`
	ExpiresAt time.Time `json:"expires_at"`
}

// Result represents the outcome of a session operation
type Result struct {
	Success bool
	Error   SessionError
	Data    interface{}
}

// Session represents an internal session record
type session struct {
	token     SessionToken
	userID    string
	roles     []string
	createdAt time.Time
	expiresAt time.Time
	revoked   bool
}

// SessionStore manages in-memory storage of active sessions with thread-safe access
type SessionStore struct {
	mu           sync.RWMutex
	sessions     map[SessionToken]*session
	maxSessions  int
	defaultTTL   time.Duration
}

// SessionValidator checks if a session token is valid, not expired, and not revoked
type SessionValidator struct {
	store *SessionStore
}

// SessionCleaner removes expired sessions on a periodic schedule
type SessionCleaner struct {
	store    *SessionStore
	ticker   *time.Ticker
	stopChan chan struct{}
	done     chan struct{}
}

// NewSessionStore creates a new session store with the given capacity and default TTL
func NewSessionStore(maxSessions int, defaultTTL time.Duration) *SessionStore {
	return &SessionStore{
		sessions:    make(map[SessionToken]*session),
		maxSessions: maxSessions,
		defaultTTL:  defaultTTL,
	}
}

// NewSessionValidator creates a new session validator
func NewSessionValidator(store *SessionStore) *SessionValidator {
	return &SessionValidator{
		store: store,
	}
}

// NewSessionCleaner creates a new session cleaner with the given cleanup interval
func NewSessionCleaner(store *SessionStore, cleanupInterval time.Duration) *SessionCleaner {
	return &SessionCleaner{
		store:    store,
		stopChan: make(chan struct{}),
		done:     make(chan struct{}),
	}
}

// generateToken generates a cryptographically random 32-character hex token
func generateToken() (SessionToken, error) {
	bytes := make([]byte, 16)
	if _, err := rand.Read(bytes); err != nil {
		return "", err
	}
	return SessionToken(hex.EncodeToString(bytes)), nil
}

// CreateSession creates a new session for the given user with the specified roles
// Returns a Result containing the session token or an error
func (s *SessionStore) CreateSession(userID string, roles []string) Result {
	s.mu.Lock()
	defer s.mu.Unlock()

	// Check if store is full
	if len(s.sessions) >= s.maxSessions {
		return Result{
			Success: false,
			Error:   ErrorStoreFull,
		}
	}

	// Generate token
	token, err := generateToken()
	if err != nil {
		return Result{
			Success: false,
			Error:   ErrorInvalidToken,
		}
	}

	// Create session record
	now := time.Now()
	expiresAt := now.Add(s.defaultTTL)

	newSession := &session{
		token:     token,
		userID:    userID,
		roles:     append([]string(nil), roles...), // Copy roles
		createdAt: now,
		expiresAt: expiresAt,
		revoked:   false,
	}

	s.sessions[token] = newSession

	return Result{
		Success: true,
		Data:    token,
	}
}

// ValidateSession checks if a session token is valid, not expired, and not revoked
// Returns a Result containing the SessionInfo or an error
func (sv *SessionValidator) ValidateSession(token SessionToken) Result {
	sv.store.mu.RLock()
	defer sv.store.mu.RUnlock()

	sess, exists := sv.store.sessions[token]
	if !exists {
		return Result{
			Success: false,
			Error:   ErrorInvalidToken,
		}
	}

	if sess.revoked {
		return Result{
			Success: false,
			Error:   ErrorRevoked,
		}
	}

	if time.Now().After(sess.expiresAt) {
		return Result{
			Success: false,
			Error:   ErrorExpired,
		}
	}

	info := SessionInfo{
		UserID:    sess.userID,
		Roles:     sess.roles,
		CreatedAt: sess.createdAt,
		ExpiresAt: sess.expiresAt,
	}

	return Result{
		Success: true,
		Data:    info,
	}
}

// RevokeSession marks a session as revoked
// Returns a Result indicating success or error
func (s *SessionStore) RevokeSession(token SessionToken) Result {
	s.mu.Lock()
	defer s.mu.Unlock()

	sess, exists := s.sessions[token]
	if !exists {
		return Result{
			Success: false,
			Error:   ErrorInvalidToken,
		}
	}

	sess.revoked = true
	return Result{
		Success: true,
	}
}

// Start begins the periodic cleanup process
// The cleaner runs on the given interval and removes expired sessions
// It blocks until Stop() is called
func (sc *SessionCleaner) Start(cleanupInterval time.Duration) {
	sc.ticker = time.NewTicker(cleanupInterval)
	defer sc.ticker.Stop()

	for {
		select {
		case <-sc.stopChan:
			close(sc.done)
			return
		case <-sc.ticker.C:
			sc.cleanExpiredSessions()
		}
	}
}

// Stop signals the cleaner to stop running
func (sc *SessionCleaner) Stop() {
	close(sc.stopChan)
}

// Wait blocks until the cleaner has fully stopped
func (sc *SessionCleaner) Wait() {
	<-sc.done
}

// cleanExpiredSessions removes all expired sessions from the store
// Must complete in under 1ms for concurrent request-handling threads
func (sc *SessionCleaner) cleanExpiredSessions() {
	sc.store.mu.Lock()
	defer sc.store.mu.Unlock()

	now := time.Now()
	for token, sess := range sc.store.sessions {
		if now.After(sess.expiresAt) {
			delete(sc.store.sessions, token)
		}
	}
}

// GetSessionCount returns the current number of sessions in the store
// Useful for testing and monitoring
func (s *SessionStore) GetSessionCount() int {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return len(s.sessions)
}
