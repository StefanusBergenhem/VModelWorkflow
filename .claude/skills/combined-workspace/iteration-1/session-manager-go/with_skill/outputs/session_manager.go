package session

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"sync"
	"time"
)

// SessionToken is an opaque 32-character hex string.
type SessionToken string

// SessionInfo contains user identity and session metadata.
type SessionInfo struct {
	UserID    string
	Roles     []string
	CreatedAt time.Time
	ExpiresAt time.Time
}

// SessionError describes what went wrong with a session operation.
type SessionError string

const (
	ErrorInvalidToken SessionError = "invalid_token"
	ErrorExpired      SessionError = "expired"
	ErrorRevoked      SessionError = "revoked"
	ErrorStoreFull    SessionError = "store_full"
)

// Result is a discriminated union for session operations.
type Result struct {
	Success bool
	Error   SessionError
	Token   SessionToken
	Info    SessionInfo
}

// MaxSessions is the hard limit on concurrent sessions.
const MaxSessions = 10000

// DefaultTTL is the default session lifetime.
const DefaultTTL = 30 * time.Minute

// session is the internal representation stored in SessionStore.
type session struct {
	info      SessionInfo
	revokedAt *time.Time // nil if not revoked
}

// SessionStore manages active sessions with thread-safe access.
type SessionStore struct {
	mu          sync.RWMutex
	sessions    map[SessionToken]*session
	maxSessions int
	ttl         time.Duration
}

// NewSessionStore creates a thread-safe session store.
func NewSessionStore(maxSessions int, ttl time.Duration) *SessionStore {
	return &SessionStore{
		sessions:    make(map[SessionToken]*session),
		maxSessions: maxSessions,
		ttl:         ttl,
	}
}

// Create adds a new session for the given user and roles.
// Returns an opaque session token or an error if the store is full.
func (s *SessionStore) Create(userID string, roles []string) Result {
	if userID == "" {
		return Result{Success: false, Error: ErrorInvalidToken}
	}
	if roles == nil {
		roles = []string{}
	}

	s.mu.Lock()
	defer s.mu.Unlock()

	if len(s.sessions) >= s.maxSessions {
		return Result{Success: false, Error: ErrorStoreFull}
	}

	token, err := generateToken()
	if err != nil {
		return Result{Success: false, Error: ErrorInvalidToken}
	}

	now := time.Now()
	info := SessionInfo{
		UserID:    userID,
		Roles:     roles,
		CreatedAt: now,
		ExpiresAt: now.Add(s.ttl),
	}

	s.sessions[token] = &session{info: info}

	return Result{Success: true, Token: token}
}

// Validate checks if a token is valid, not expired, and not revoked.
// Returns SessionInfo on success or an error.
func (s *SessionStore) Validate(token SessionToken) Result {
	s.mu.RLock()
	defer s.mu.RUnlock()

	sess, found := s.sessions[token]
	if !found {
		return Result{Success: false, Error: ErrorInvalidToken}
	}

	if sess.revokedAt != nil {
		return Result{Success: false, Error: ErrorRevoked}
	}

	if time.Now().After(sess.info.ExpiresAt) {
		return Result{Success: false, Error: ErrorExpired}
	}

	return Result{Success: true, Info: sess.info}
}

// Revoke marks a session as revoked.
// Returns success or invalid_token if the token does not exist.
func (s *SessionStore) Revoke(token SessionToken) Result {
	s.mu.Lock()
	defer s.mu.Unlock()

	sess, found := s.sessions[token]
	if !found {
		return Result{Success: false, Error: ErrorInvalidToken}
	}

	now := time.Now()
	sess.revokedAt = &now

	return Result{Success: true}
}

// CleanExpired removes all expired and revoked sessions.
// Returns the count of sessions removed.
func (s *SessionStore) CleanExpired() int {
	s.mu.Lock()
	defer s.mu.Unlock()

	now := time.Now()
	removedCount := 0

	for token, sess := range s.sessions {
		if sess.revokedAt != nil || now.After(sess.info.ExpiresAt) {
			delete(s.sessions, token)
			removedCount++
		}
	}

	return removedCount
}

// ActiveCount returns the current number of active (non-expired, non-revoked) sessions.
func (s *SessionStore) ActiveCount() int {
	s.mu.RLock()
	defer s.mu.RUnlock()

	now := time.Now()
	activeCount := 0

	for _, sess := range s.sessions {
		if sess.revokedAt == nil && now.Before(sess.info.ExpiresAt) {
			activeCount++
		}
	}

	return activeCount
}

// generateToken creates a cryptographically random 32-character hex token.
func generateToken() (SessionToken, error) {
	bytes := make([]byte, 16)
	if _, err := rand.Read(bytes); err != nil {
		return "", err
	}
	return SessionToken(hex.EncodeToString(bytes)), nil
}

// SessionCleaner periodically removes expired sessions.
type SessionCleaner struct {
	store    *SessionStore
	ticker   *time.Ticker
	stopChan chan struct{}
}

// NewSessionCleaner creates a cleaner that runs periodically.
func NewSessionCleaner(store *SessionStore, interval time.Duration) *SessionCleaner {
	return &SessionCleaner{
		store:    store,
		ticker:   time.NewTicker(interval),
		stopChan: make(chan struct{}),
	}
}

// Start begins the periodic cleanup loop. Must be called in a goroutine.
func (c *SessionCleaner) Start() {
	for {
		select {
		case <-c.ticker.C:
			c.store.CleanExpired()
		case <-c.stopChan:
			c.ticker.Stop()
			return
		}
	}
}

// Stop signals the cleaner to stop. Non-blocking.
func (c *SessionCleaner) Stop() {
	select {
	case c.stopChan <- struct{}{}:
	default:
		// Stop already called or channel closed
	}
}
