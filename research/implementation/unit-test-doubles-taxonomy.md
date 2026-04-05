# Research: Test Doubles — Taxonomy, Usage Patterns, and Pitfalls

**Date:** 2026-04-05
**Purpose:** Foundation research for VModelWorkflow documentation on test doubles in unit testing
**Target audience:** Professional engineers in safety-critical domains (DO-178C, ISO 26262/ASPICE, IEC 62304)

---

## 1. Test Double Taxonomy (Meszaros Classification)

Gerard Meszaros introduced the term "test double" in his book *xUnit Test Patterns: Refactoring Test Code* (2007) as a generic term for any object that stands in for a real dependency during testing — analogous to a stunt double in film. Martin Fowler popularized and summarized this taxonomy in his *TestDouble* bliki entry.

The taxonomy defines five distinct types, each serving a different purpose:

### 1.1 Dummy

A dummy is passed around but never actually used. It exists solely to satisfy a parameter list or constructor requirement.

```java
// The emailService is required by the constructor but irrelevant to this test
public class OrderProcessorTest {
    @Test
    void calculatesOrderTotal() {
        EmailService dummyEmail = null; // or a no-op implementation
        OrderProcessor processor = new OrderProcessor(dummyEmail);
        
        Order order = new Order();
        order.addItem(new Item("Widget", 10.00));
        order.addItem(new Item("Gadget", 25.00));
        
        assertEquals(35.00, processor.calculateTotal(order));
    }
}
```

**When to use:** When a collaborator is required by the API but plays no role in the specific behavior being tested.

### 1.2 Stub

A stub provides canned answers to calls made during the test. It does not respond to anything outside what was explicitly programmed for the test. Stubs are used to control **indirect inputs** — data the system under test receives from its collaborators.

```java
public class StubPriceService implements PriceService {
    @Override
    public BigDecimal getPrice(String productId) {
        // Always returns the same canned price
        return new BigDecimal("99.95");
    }
}

@Test
void appliesDiscountToPrice() {
    PriceService stubPrices = new StubPriceService();
    DiscountCalculator calculator = new DiscountCalculator(stubPrices);
    
    BigDecimal discounted = calculator.applyDiscount("PROD-1", 10); // 10% off
    
    assertEquals(new BigDecimal("89.955"), discounted);
}
```

**When to use:** When you need to control what data flows into the system under test, without caring about how the dependency was called.

### 1.3 Spy

A spy is a stub that also records information about how it was called. It captures **indirect outputs** — calls the system under test makes to its collaborators — for later verification in the test. Meszaros calls this a "Test Spy."

```java
public class SpyAuditLog implements AuditLog {
    private final List<String> loggedMessages = new ArrayList<>();
    
    @Override
    public void log(String message) {
        loggedMessages.add(message);
    }
    
    // Inspection method for test assertions
    public List<String> getLoggedMessages() {
        return Collections.unmodifiableList(loggedMessages);
    }
}

@Test
void logsOrderCompletion() {
    SpyAuditLog spyLog = new SpyAuditLog();
    OrderService service = new OrderService(spyLog);
    
    service.completeOrder(new Order("ORD-42"));
    
    assertEquals(1, spyLog.getLoggedMessages().size());
    assertTrue(spyLog.getLoggedMessages().get(0).contains("ORD-42"));
}
```

**When to use:** When you need to verify that the system under test sent the right messages to a collaborator, but you want to make the assertion after the fact (state-style verification of interactions).

### 1.4 Mock

A mock is pre-programmed with **expectations** about calls it should receive. Unlike a spy, a mock verifies interactions as they happen (or at verify-time) and will fail the test if unexpected calls occur or expected calls are missing. Of all test doubles, **only mocks insist upon behavior verification** (Fowler, "Mocks Aren't Stubs").

```java
@Test
void sendsConfirmationEmail() {
    // Using Mockito as a mocking framework
    EmailService mockEmail = mock(EmailService.class);
    OrderService service = new OrderService(mockEmail);
    
    service.completeOrder(new Order("ORD-42", "customer@example.com"));
    
    // Behavior verification: did the SUT call the right method with the right args?
    verify(mockEmail).sendConfirmation(
        eq("customer@example.com"),
        contains("ORD-42")
    );
}
```

**When to use:** When the key behavior you are testing is that the system under test correctly communicates with a collaborator — the interaction *is* the observable behavior.

### 1.5 Fake

A fake has a working implementation but takes shortcuts that make it unsuitable for production. The canonical example is an in-memory database replacing a real database.

```java
public class InMemoryUserRepository implements UserRepository {
    private final Map<String, User> store = new HashMap<>();
    
    @Override
    public void save(User user) {
        store.put(user.getId(), user);
    }
    
    @Override
    public Optional<User> findById(String id) {
        return Optional.ofNullable(store.get(id));
    }
    
    @Override
    public List<User> findByRole(String role) {
        return store.values().stream()
            .filter(u -> u.getRole().equals(role))
            .collect(Collectors.toList());
    }
}
```

**When to use:** When you need realistic behavior from a dependency (not just canned responses), but the real implementation is too slow, requires infrastructure, or has side effects. Fakes shine when the dependency has complex query/filter logic that stubs cannot reasonably replicate.

### 1.6 Key Differences Summary

| Type  | Has behavior? | Records calls? | Verifies expectations? | Use case |
|-------|:---:|:---:|:---:|---|
| Dummy | No  | No  | No  | Fill parameter lists |
| Stub  | Canned only | No  | No  | Control indirect inputs |
| Spy   | Canned only | Yes | No (test asserts after) | Capture indirect outputs |
| Mock  | Canned only | Yes | Yes (expectations set up front) | Verify interactions |
| Fake  | Yes (simplified) | No  | No  | Realistic lightweight substitute |

### 1.7 The "Mock" Terminology Problem

In practice, the word "mock" is routinely used as a generic term for all test doubles. Developers say "I'll mock that dependency" when they mean "I'll replace that dependency with a test double" — which might actually be a stub, fake, or spy. Mocking frameworks like Mockito compound this: `mock(SomeClass.class)` creates an object that can function as a stub, spy, or mock depending on how it's configured.

This terminological confusion matters because the choice of test double type has real consequences for test quality, and the imprecise language masks those consequences. As Fowler notes: "The term 'mock' is commonly used as a synonym for any test double, but it's worth being more precise" (Fowler, "TestDouble").

**Sources:**
- Meszaros, Gerard. *xUnit Test Patterns: Refactoring Test Code*. Addison-Wesley, 2007.
  - [Amazon](https://www.amazon.com/xUnit-Test-Patterns-Refactoring-Code/dp/0131495054)
  - [Martin Fowler's book page](https://martinfowler.com/books/meszaros.html)
- [Fowler, Martin. "TestDouble." martinfowler.com](https://martinfowler.com/bliki/TestDouble.html)
- [xUnit Patterns — Test Double](http://xunitpatterns.com/Test%20Double.html)

---

## 2. Mocks Aren't Stubs (Fowler's Distinction)

Martin Fowler's 2007 article "Mocks Aren't Stubs" is the definitive treatment of two interrelated distinctions: (1) state vs. behavior verification, and (2) classical vs. mockist TDD.

### 2.1 State Verification vs. Behavior Verification

**State verification** determines test success by examining the state of the system under test and its collaborators *after* exercising the behavior:

```java
// State verification: check the warehouse state after the order is filled
@Test
void orderIsFilledFromWarehouse_stateVerification() {
    Warehouse warehouse = new Warehouse();
    warehouse.add("Widget", 50);
    Order order = new Order("Widget", 10);
    
    order.fill(warehouse);
    
    assertTrue(order.isFilled());
    assertEquals(40, warehouse.getInventory("Widget")); // State check
}
```

**Behavior verification** determines test success by checking that the system under test made the correct calls to its collaborators:

```java
// Behavior verification: check the warehouse received the right method call
@Test
void orderIsFilledFromWarehouse_behaviorVerification() {
    Warehouse mockWarehouse = mock(Warehouse.class);
    when(mockWarehouse.hasInventory("Widget", 10)).thenReturn(true);
    Order order = new Order("Widget", 10);
    
    order.fill(mockWarehouse);
    
    assertTrue(order.isFilled());
    verify(mockWarehouse).remove("Widget", 10); // Behavior check
}
```

Fowler's key insight: **Stubs support state verification. Mocks enforce behavior verification.** A stub *can* be used for behavior verification (Meszaros calls this a spy), but only mocks *require* it.

### 2.2 Classical (Detroit/Chicago) vs. Mockist (London) TDD

These two schools represent fundamentally different philosophies about what "unit testing" means:

**Classical TDD (Detroit School)**
- Originated with Kent Beck at Chrysler in the late 1990s
- Prominent practitioners: Kent Beck, Martin Fowler, Robert C. Martin, Ron Jeffries
- A "unit" is a unit of behavior, which may span multiple classes
- Uses real objects wherever practical; test doubles only at system boundaries
- Prefers state verification
- The SUT grows with the application — tests operate on expanding context
- Tests break only when behavior changes, not when implementation is refactored

**Mockist TDD (London School)**
- Originated with Steve Freeman, Nat Pryce, and the London XP community
- Codified in *Growing Object-Oriented Software, Guided by Tests* (2009)
- A "unit" is a single class; all collaborators are replaced with mocks
- Uses behavior verification to specify how objects communicate
- Tests are focused and small — limited context per test
- Design emerges from specifying object interactions top-down
- Tests drive interface discovery: "Tell, Don't Ask"

### 2.3 Trade-offs

| Dimension | Classical (Detroit) | Mockist (London) |
|---|---|---|
| **Test granularity** | Coarser — tests may span multiple classes | Finer — one class per test |
| **Coupling to implementation** | Low — tests coupled to behavior, not structure | High — tests coupled to interaction patterns |
| **Refactoring resilience** | High — internal restructuring rarely breaks tests | Low — changing how classes communicate breaks tests |
| **Failure localization** | Lower — failures may trace to multiple classes | Higher — failures pinpoint one class |
| **Setup complexity** | Can be higher (constructing real object graphs) | Can be higher (configuring mock expectations) |
| **Design feedback** | Tests reveal when classes are hard to construct | Tests reveal when classes have too many collaborators |
| **Risk of false positives** | Lower — tests exercise real interactions | Higher — mocks may not match real behavior |

### 2.4 Which Approach Is More Maintainable Long-Term?

The industry consensus, as reflected in Google's testing practices and Fowler's writings, tilts toward the classical approach for long-term maintainability:

- **State-based tests survive refactoring.** If you restructure internal collaborations without changing external behavior, classical tests remain green. Mockist tests break because the interaction choreography changed.
- **Behavior verification creates invisible coupling.** Mockist tests encode *how* the SUT achieves its result, not just *what* result it achieves. This makes every refactoring a test-rewriting exercise.
- **The London school's strength is design discovery.** When building new systems top-down, mock-driven TDD can help discover interfaces. But once interfaces stabilize, the ongoing cost of interaction-based tests exceeds their value.

The pragmatic recommendation from multiple sources: **default to classical testing; use behavior verification only when the interaction itself is the observable behavior** (e.g., "the system must send a notification," "the system must publish an event").

**Sources:**
- [Fowler, Martin. "Mocks Aren't Stubs." martinfowler.com, 2007](https://martinfowler.com/articles/mocksArentStubs.html)
- Freeman, Steve and Nat Pryce. *Growing Object-Oriented Software, Guided by Tests*. Addison-Wesley, 2009. [Publisher](https://www.pearson.com/en-us/subject-catalog/p/growing-object-oriented-software-guided-by-tests/P200000009298/9780321503626)
- Beck, Kent. *Test Driven Development: By Example*. Addison-Wesley, 2002. [Amazon](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
- [Falski, Maciej. "Detroit and London Schools of Test-Driven Development." Dev Genius](https://blog.devgenius.io/detroit-and-london-schools-of-test-driven-development-3d2f8dca71e5)

---

## 3. When to Use Test Doubles

Test doubles exist to solve real problems. The legitimate use cases share a common theme: the real dependency introduces some property that is incompatible with fast, deterministic, isolated testing.

### 3.1 External System Dependencies

Dependencies that cross process or network boundaries:
- **Network services** (HTTP APIs, gRPC, message brokers)
- **Databases** (SQL, NoSQL, search indices)
- **File systems** (especially shared or remote)
- **Hardware** (sensors, actuators, embedded peripherals)

These cannot be reliably present in a unit test environment and introduce latency, flakiness, and side effects.

### 3.2 Non-Deterministic Dependencies

Dependencies that produce different results on each invocation:
- **System clock** (`LocalDateTime.now()`, `System.currentTimeMillis()`)
- **Random number generators** (`Random`, `UUID.randomUUID()`)
- **System environment** (environment variables, hostname, available memory)

Non-determinism is the enemy of reproducible tests. Replace these with injectable abstractions:

```java
// Instead of calling LocalDateTime.now() directly
public interface Clock {
    LocalDateTime now();
}

// In production
public class SystemClock implements Clock {
    public LocalDateTime now() { return LocalDateTime.now(); }
}

// In tests — deterministic
public class FixedClock implements Clock {
    private final LocalDateTime fixed;
    public FixedClock(LocalDateTime fixed) { this.fixed = fixed; }
    public LocalDateTime now() { return fixed; }
}
```

### 3.3 Slow Dependencies

Dependencies that make individual tests take hundreds of milliseconds or more:
- Database queries requiring schema setup and teardown
- Service calls with network latency
- File I/O with large datasets
- Computationally expensive algorithms used as collaborators

A unit test suite must complete in seconds, not minutes. If a real dependency prevents this, a test double is justified.

### 3.4 Difficult-to-Configure Dependencies

Dependencies that require significant infrastructure or setup:
- Services requiring authentication tokens or certificates
- Systems needing specific data states (e.g., a pre-populated database)
- Third-party services with rate limits or costs per call

### 3.5 The Guiding Principle: Mock at the Boundary

The principle "Don't Mock What You Don't Own" (Freeman & Pryce, also elaborated by Hynek Schlawack) captures the right instinct:

1. **Wrap third-party dependencies** in your own thin adapter/port
2. **Mock your own adapter interface**, not the third-party API directly
3. **Test the adapter itself** with integration tests against the real dependency

This keeps mocks at the architectural boundary — the ports in a hexagonal architecture — and avoids coupling tests to the internal APIs of libraries you don't control.

```java
// BAD: Mocking a third-party class directly
@Test
void bad_mockingThirdPartyDirectly() {
    HttpClient mockClient = mock(HttpClient.class); // Don't mock what you don't own
    when(mockClient.send(any(), any())).thenReturn(someResponse);
    // If HttpClient's API changes in a library upgrade, this breaks
}

// GOOD: Mock your own port
public interface PaymentGateway {
    PaymentResult charge(Money amount, CardToken token);
}

@Test
void good_mockingOwnPort() {
    PaymentGateway stubGateway = mock(PaymentGateway.class);
    when(stubGateway.charge(any(), any()))
        .thenReturn(PaymentResult.success("TXN-123"));
    // Your interface, your control
}
```

**Sources:**
- [Schlawack, Hynek. "'Don't Mock What You Don't Own' in 5 Minutes." hynek.me](https://hynek.me/articles/what-to-mock-in-5-mins/)
- [testdouble. "Don't mock what you don't own." GitHub Wiki](https://github.com/testdouble/contributing-tests/wiki/Don't-mock-what-you-don't-own)
- [Khorikov, Vladimir. "When to Mock." Enterprise Craftsmanship](https://enterprisecraftsmanship.com/posts/when-to-mock/)

---

## 4. When NOT to Use Test Doubles (Over-Mocking)

Over-mocking is one of the most common testing anti-patterns. It produces tests that are expensive to maintain, provide false confidence, and resist refactoring.

### 4.1 Don't Mock Internals of the System Under Test

If two classes collaborate within the same module/component to deliver a single behavior, do not mock one to test the other. They are implementation details of the same unit of behavior.

```java
// BAD: Mocking an internal collaborator
@Test
void bad_mockingInternalHelper() {
    TaxCalculator mockTax = mock(TaxCalculator.class);
    when(mockTax.calculate(any())).thenReturn(new BigDecimal("8.00"));
    
    InvoiceGenerator generator = new InvoiceGenerator(mockTax);
    Invoice invoice = generator.generate(order);
    
    // This test will break if we refactor how InvoiceGenerator and
    // TaxCalculator collaborate, even if the invoice is still correct.
    verify(mockTax).calculate(any());
}

// GOOD: Test the behavior through the public API
@Test
void good_testBehaviorNotInteraction() {
    // Use the real TaxCalculator — it's an internal detail
    InvoiceGenerator generator = new InvoiceGenerator(new TaxCalculator());
    Invoice invoice = generator.generate(order);
    
    // Assert on the outcome, not the internal interaction
    assertEquals(new BigDecimal("108.00"), invoice.getTotal());
}
```

As Vladimir Khorikov (Enterprise Craftsmanship) puts it: "Intra-system communications are implementation details; inter-system communications form the observable behavior." Mock the latter, not the former.

### 4.2 Don't Mock Value Objects or Simple Data Structures

Value objects are immutable, have no side effects, and are trivial to construct. Mocking them adds complexity for zero benefit:

```java
// BAD: Mocking a value object
Money mockMoney = mock(Money.class);
when(mockMoney.getAmount()).thenReturn(new BigDecimal("100"));
when(mockMoney.getCurrency()).thenReturn(Currency.USD);

// GOOD: Just create the value object
Money money = Money.of(100, Currency.USD);
```

### 4.3 The "Mockery" Anti-Pattern

The mockery (named in various anti-pattern catalogs) occurs when a unit test contains so many mocks, stubs, and fakes that the system under test is no longer being meaningfully tested. Instead, the test verifies that mocked data flows through mocked interactions — a self-referential exercise.

Symptoms:
- Test setup is longer than the test itself
- More `when(...).thenReturn(...)` lines than assertions
- Changing any internal method signature breaks dozens of tests
- Tests pass but the production system fails
- You can delete the implementation and the tests still compile (they test the mocks, not the code)

```java
// THE MOCKERY: What are we even testing here?
@Test
void the_mockery() {
    UserRepository mockRepo = mock(UserRepository.class);
    EmailService mockEmail = mock(EmailService.class);
    AuditLogger mockAudit = mock(AuditLogger.class);
    PermissionChecker mockPerms = mock(PermissionChecker.class);
    ConfigService mockConfig = mock(ConfigService.class);
    
    when(mockPerms.canRegister(any())).thenReturn(true);
    when(mockConfig.get("max.users")).thenReturn("1000");
    when(mockRepo.count()).thenReturn(500L);
    when(mockRepo.save(any())).thenReturn(new User("id-1", "test@test.com"));
    
    RegistrationService service = new RegistrationService(
        mockRepo, mockEmail, mockAudit, mockPerms, mockConfig);
    
    service.register(new RegistrationRequest("test@test.com", "password"));
    
    verify(mockRepo).save(any());
    verify(mockEmail).sendWelcome(any());
    verify(mockAudit).log(any());
    // We've just verified that our mocks were called. 
    // We have not tested that registration actually works.
}
```

### 4.4 Tests That Pass Against Mocks but Fail Against Real Implementations

This is the most dangerous consequence of over-mocking. When stubs and mocks don't accurately reflect the behavior of real dependencies, tests provide **false confidence**:

- A stub returns `Optional.of(user)` but the real repository returns `Optional.empty()` for that query
- A mock accepts any argument order but the real API is order-sensitive
- A stub always succeeds but the real service sometimes throws exceptions
- A fake uses case-sensitive comparison but the real database is case-insensitive

This is not a theoretical risk. It is the primary argument for preferring real implementations and verified fakes over mocks.

### 4.5 The Maintenance Burden

Heavily mocked test suites create a **tax on every refactoring**:

- Renaming a method → update every mock that references it
- Changing a method signature → update every `when()` and `verify()` call
- Extracting a class → reconfigure mock wiring in every test
- Reordering operations → fix verification order in every mock-based test

This maintenance burden often exceeds the cost of maintaining the production code itself, turning the test suite from an asset into a liability. When engineers avoid refactoring because "it will break too many tests," the test suite has failed its purpose.

**Sources:**
- [Codurance. "TDD Anti-Patterns — Chapter 2"](https://www.codurance.com/publications/tdd-anti-patterns-chapter-2)
- [Vinted Engineering. "The Downsides of Excessive Mocks and Stubs in Unit Testing." 2023](https://vinted.engineering/2023/10/02/mocking-framework-downside/)
- [Codepipes Blog. "Software Testing Anti-patterns"](https://blog.codepipes.com/testing/software-testing-antipatterns.html)
- [Microsoft Engineering Playbook. "Mocking in Unit Tests"](https://microsoft.github.io/code-with-engineering-playbook/automated-testing/unit-testing/mocking/)
- [AmazingCTO. "Mocking is an Anti-Pattern"](https://www.amazingcto.com/mocking-is-an-antipattern-how-to-test-without-mocking/)

---

## 5. Contract Testing and Verified Fakes

### 5.1 The Problem: Fake Drift

When you write a fake implementation of a dependency, you create a second implementation that must remain behaviorally consistent with the first. Over time, the real implementation evolves — new edge cases are handled, error conditions change, behavior is refined — and the fake falls behind. This is **fake drift**.

The consequence is the same as over-mocking: tests pass against the fake but fail against the real implementation. The test suite provides false confidence.

### 5.2 What Contract Tests Are

A contract test is a test suite that codifies the expected behavior of an interface and runs against **both** the real implementation and the fake. If both pass the same tests, you have reasonable confidence that the fake accurately represents the real thing.

```java
// Contract test: defines what ANY UserRepository must do
public abstract class UserRepositoryContractTest {
    
    protected abstract UserRepository createRepository();
    
    @Test
    void savedUserCanBeRetrievedById() {
        UserRepository repo = createRepository();
        User user = new User("u1", "Alice", "alice@example.com");
        
        repo.save(user);
        Optional<User> found = repo.findById("u1");
        
        assertTrue(found.isPresent());
        assertEquals("Alice", found.get().getName());
    }
    
    @Test
    void findByIdReturnsEmptyForUnknownId() {
        UserRepository repo = createRepository();
        
        Optional<User> found = repo.findById("nonexistent");
        
        assertTrue(found.isEmpty());
    }
    
    @Test
    void saveOverwritesExistingUser() {
        UserRepository repo = createRepository();
        repo.save(new User("u1", "Alice", "alice@example.com"));
        repo.save(new User("u1", "Alice Updated", "alice2@example.com"));
        
        Optional<User> found = repo.findById("u1");
        assertEquals("Alice Updated", found.get().getName());
    }
}

// Run the contract against the fake
public class InMemoryUserRepositoryTest extends UserRepositoryContractTest {
    @Override
    protected UserRepository createRepository() {
        return new InMemoryUserRepository();
    }
}

// Run the same contract against the real implementation (integration test)
@Tag("integration")
public class PostgresUserRepositoryTest extends UserRepositoryContractTest {
    @Override
    protected UserRepository createRepository() {
        return new PostgresUserRepository(testDataSource);
    }
}
```

### 5.3 Verified Fakes

A **verified fake** is a fake whose behavior has been verified to match the real implementation through shared contract tests. The term comes from Google's testing practices (described in *Software Engineering at Google*, Chapter 13).

Google's recommendation hierarchy:
1. **Prefer real implementations** when they are fast, deterministic, and have no problematic side effects
2. **Use verified fakes** when real implementations are too slow or require infrastructure
3. **Use stubs/mocks as a last resort** when neither real implementations nor fakes are practical

A verified fake gives higher confidence than mocks because it has actual behavior that has been tested against the same contract as the real implementation.

### 5.4 Who Maintains the Fake?

Google's practice: **the team that owns the real implementation should also own and maintain the fake.** This ensures the fake is updated whenever the real implementation changes. When a fake is maintained by consumers instead of producers, drift is almost guaranteed.

**Sources:**
- [Google. *Software Engineering at Google*, Chapter 13: Test Doubles. abseil.io](https://abseil.io/resources/swe-book/html/ch13.html)
- [Itamar Turner-Trauring. "Fast tests for slow services: why you should use verified fakes." pythonspeed.com](https://pythonspeed.com/articles/verified-fakes/)
- [Adam Wathan. "Preventing API Drift with Contract Tests"](https://adamwathan.me/2016/02/01/preventing-api-drift-with-contract-tests/)

---

## 6. Test Double Patterns in Practice

### 6.1 Dependency Injection as the Enabler

Test doubles are only possible when the system under test does not create its own dependencies. Dependency injection (DI) — whether constructor injection, method injection, or framework-managed — is the fundamental enabler.

```java
// UNTESTABLE: Creates its own dependency
public class OrderService {
    public void placeOrder(Order order) {
        PaymentGateway gateway = new StripePaymentGateway(); // Hard-coded
        gateway.charge(order.getTotal(), order.getPaymentToken());
    }
}

// TESTABLE: Dependency is injected
public class OrderService {
    private final PaymentGateway gateway;
    
    public OrderService(PaymentGateway gateway) { // Injected
        this.gateway = gateway;
    }
    
    public void placeOrder(Order order) {
        gateway.charge(order.getTotal(), order.getPaymentToken());
    }
}
```

Constructor injection is the preferred form because:
- Dependencies are explicit and visible
- Objects are fully initialized after construction
- It's impossible to use the object in an invalid state (missing dependency)
- No framework required — works with plain `new`

### 6.2 Hexagonal Architecture and Testability

Hexagonal architecture (ports and adapters, Alistair Cockburn, 2005) creates a natural structure for test doubles:

```
                    +------------------+
   Driving Adapter  |                  |  Driven Adapter
   (Controller) --->|   Domain Logic   |---> (Database Adapter)
                    |   (Application)  |
   Driving Adapter  |                  |  Driven Adapter
   (CLI) ---------->|   Uses PORTS     |---> (Email Adapter)
                    |   (interfaces)   |
                    +------------------+
```

- **Ports** are interfaces defined by the domain. They express what the domain needs from the outside world.
- **Adapters** implement ports using specific technologies (PostgreSQL, SMTP, HTTP).
- **Test doubles replace adapters, not ports.** The port interface is your mock/fake contract.

This architecture makes test doubles trivial: the domain is already decoupled from infrastructure through ports. Testing the domain means plugging in fake adapters.

```java
// Port (interface defined by the domain)
public interface NotificationPort {
    void notify(UserId user, Message message);
}

// Production adapter
public class SmtpNotificationAdapter implements NotificationPort {
    public void notify(UserId user, Message message) {
        // Real SMTP logic
    }
}

// Test fake
public class InMemoryNotificationAdapter implements NotificationPort {
    private final List<Notification> sent = new ArrayList<>();
    
    public void notify(UserId user, Message message) {
        sent.add(new Notification(user, message));
    }
    
    public List<Notification> getSentNotifications() {
        return Collections.unmodifiableList(sent);
    }
}
```

### 6.3 Hand-Written Fakes vs. Mocking Frameworks

| Dimension | Hand-Written Fakes | Mocking Frameworks (Mockito, etc.) |
|---|---|---|
| **Initial effort** | Higher — must implement the interface | Lower — one-liner to create |
| **Reusability** | High — shared across all tests | Low — configured per test |
| **Behavior richness** | Full — can implement real logic | Limited — canned responses only |
| **Coupling to implementation** | Low — tests assert on state | High — tests verify method calls |
| **Maintenance** | Ongoing — must keep in sync with interface | Per-test — each test maintains its own setup |
| **Readability** | Higher — fake is a real class you can read | Lower — mock configuration is test noise |
| **Framework dependency** | None | Tied to a specific framework |
| **Supports contract testing** | Yes — naturally | No — mocks are per-test disposable |

**The practical recommendation:** Use hand-written fakes for core domain ports that appear in many tests. Use mocking frameworks for one-off situations and for verifying specific interactions at system boundaries. As Google recommends: "A real implementation should be preferred over a test double. A fake is often the ideal solution if a real implementation can't be used in a test" (*Software Engineering at Google*, Ch. 13).

### 6.4 Mockito: Practical Java Reference

Mockito is the dominant mocking framework in the Java ecosystem. Key patterns:

```java
// Creating a stub
UserRepository stubRepo = mock(UserRepository.class);
when(stubRepo.findById("u1")).thenReturn(Optional.of(testUser));

// Creating a spy (wrapping a real object)
UserRepository realRepo = new InMemoryUserRepository();
UserRepository spyRepo = spy(realRepo);
// Real behavior, but calls are recorded
verify(spyRepo).findById("u1"); // After the test exercises it

// Argument matchers
verify(mockEmail).send(eq("to@example.com"), anyString(), contains("Welcome"));

// Verifying no unwanted interactions
verifyNoMoreInteractions(mockEmail);

// Argument captor (spy-like pattern within Mockito)
ArgumentCaptor<Email> captor = ArgumentCaptor.forClass(Email.class);
verify(mockEmail).send(captor.capture());
assertEquals("Welcome!", captor.getValue().getSubject());
```

**Mockito best practices (from Mockito documentation and community):**
1. Prefer `when().thenReturn()` over `doReturn().when()` (type-safe)
2. Use `@Mock` annotation with `MockitoExtension` for cleaner setup
3. Avoid `verify()` unless the interaction is the point of the test
4. Never mock value objects, collections, or final classes you own
5. Use `@InjectMocks` sparingly — explicit constructor calls are clearer
6. If your mock setup is longer than 5 lines, consider a hand-written fake

**Sources:**
- [Holub, Oleksii. "Prefer Fakes Over Mocks." tyrrrz.me](https://tyrrrz.me/blog/fakes-over-mocks)
- [Dawson, Andrew. "Fakes are Better than Mocks." Medium](https://andrewjdawson2016.medium.com/fakes-are-better-than-mocks-e11ae17539fb)
- [Rasmussen, Peter Daugaard. "Writing test implementations vs mocking frameworks, pros and cons"](https://peterdaugaardrasmussen.com/2018/12/03/mocks-vs-stubs-the-pros-and-cons-of-frameworks-vs-implementations/)
- [Diffblue. "Mockito Tutorial: Complete Java Unit Testing Guide"](https://www.diffblue.com/resources/mocking-best-practices/)
- [Java Code Geeks. "Hexagonal Architecture: Ports, Adapters, and Real Use Cases"](https://www.javacodegeeks.com/2025/06/hexagonal-architecture-in-practice-ports-adapters-and-real-use-cases.html)

---

## 7. Test Doubles in Safety-Critical Context

Safety-critical standards (DO-178C, ISO 26262/ASPICE, IEC 62304) add specific constraints to how test doubles may be used. The core concern: **test doubles introduce an abstraction gap between what was tested and what runs in production.** Standards auditors need to understand and accept that gap.

### 7.1 Traceability Requirements

All three major standards require bidirectional traceability between requirements, design, code, and tests. When a test uses a test double, the traceability chain must account for it:

- **What was replaced:** The specific real dependency that the test double substitutes
- **Why it was replaced:** Justification (e.g., "external hardware interface not available in unit test environment")
- **What was not tested as a result:** The interaction between the SUT and the real dependency
- **Where that interaction is tested:** Reference to the integration test that exercises the real dependency

In V-model terms: test doubles are acceptable at the unit test level (bottom of the V), but the gaps they create must be closed at the integration test level (moving up the right side of the V).

### 7.2 DO-178C Perspective

DO-178C (RTCA, 2012) does not use the term "unit test" — it refers to low-level requirements-based testing. The standard requires:

- Tests must verify that software satisfies its requirements
- Test cases must be traceable to requirements
- Structural coverage analysis (MC/DC for Level A) must be achieved

Test doubles (stubs) are an accepted practice for isolating units during low-level testing. Tool qualification (DO-330) may apply if test doubles are generated by a tool that could fail to detect errors. Key documentation requirements:
- The test procedure must describe the test environment, including any stubs or simulated components
- Stub behavior must be documented sufficiently for an auditor to understand what was replaced and how

Rapita Systems and Parasoft (both major DO-178C tooling vendors) explicitly support stub/mock frameworks in their unit testing tools, confirming industry acceptance.

### 7.3 ASPICE SWE.4 Perspective

ASPICE process area SWE.4 (Software Unit Verification) requires:
- Unit verification criteria derived from the software detailed design
- Evidence that each unit meets its design specification
- Methods may include code review, static analysis, and unit testing

ASPICE does not prescribe specific test double strategies, but the process assessment model expects:
- Verification methods are appropriate for the unit's complexity and safety classification
- Test environments are documented
- Deviations from real environment behavior are identified and justified

### 7.4 IEC 62304 Perspective

IEC 62304 (Medical Device Software) scales requirements by safety class:
- **Class A** (no injury possible): Verification can be limited to review
- **Class B** (non-serious injury possible): Static analysis or code review sufficient
- **Class C** (death or serious injury possible): Full unit testing required

For Class C software, test stubs must be documented, and the manufacturer must demonstrate that stubbed-out behavior is verified elsewhere (typically integration testing).

### 7.5 The Risk of Masking Integration Issues

The most significant risk of test doubles in safety-critical software is that they can mask integration defects:

1. **Interface mismatches:** A stub returns data in a format the SUT expects, but the real component returns it differently (endianness, null handling, error codes)
2. **Timing issues:** A stub responds instantly, but the real component has latency that causes race conditions
3. **Resource constraints:** A stub uses unbounded memory, but the real component operates under tight constraints
4. **Error behavior:** A stub only simulates the happy path, but the real component has failure modes that the SUT must handle

Mitigation strategies:
- **Contract tests** between fakes and real implementations (Section 5)
- **Integration tests** that exercise real dependencies for every path tested with doubles
- **Environmental qualification** — documenting the differences between test and target environments
- **Traceability matrix** — explicit mapping showing which unit test gaps are covered by which integration tests

### 7.6 Documentation Requirements for Auditable Environments

For any test that uses a test double, the following should be documented (or derivable from the test artifacts):

| Item | Description |
|---|---|
| **Test Double Identity** | Which dependency is being replaced |
| **Type** | Dummy, stub, spy, mock, or fake (using Meszaros taxonomy) |
| **Justification** | Why the real dependency cannot be used |
| **Behavior Specification** | What the test double does (for stubs and fakes) |
| **Limitations** | What behaviors are NOT simulated |
| **Coverage Gap** | What cannot be verified with this test double in place |
| **Closure Reference** | Which integration/system test verifies the real interaction |

In practice, much of this can be captured through:
- Naming conventions (e.g., `InMemoryUserRepository` clearly identifies the fake)
- Test organization (unit tests and integration tests grouped by component)
- Traceability tools linking unit tests to integration tests

**Sources:**
- [Rapita Systems. "DO-178C Testing"](https://www.rapitasystems.com/do178c-testing)
- [Parasoft. "Unit Testing in Safety-Critical Software for Aerospace & Defense"](https://www.parasoft.com/learning-center/do-178c/unit-testing/)
- [Johner Institute. "Unit testing and IEC 62304"](https://blog.johner-institute.com/iec-62304-medical-software/unit-testing-iec-62304/)
- [Kugler Maag. "SWE.4 Software Unit Verification." ASPICE Whitepaper](https://www.kuglermaagcie.cn/fileadmin/whitepapers/ASPICE/whitepaper_automotive-spice_en_swe4_software-unit-verification.pdf)
- RTCA. *DO-178C: Software Considerations in Airborne Systems and Equipment Certification.* 2012.
- IEC. *IEC 62304:2006 — Medical device software — Software life cycle processes.*
- [Vector. "Complete Verification and Validation for DO-178C." Whitepaper](https://cdn.vector.com/cms/content/know-how/aerospace/Documents/Complete_Verification_and_Validation_for_DO-178C.pdf)

---

## 8. Summary of Key Findings

### 8.1 Taxonomy Matters

The five types of test doubles (dummy, stub, spy, mock, fake) serve different purposes. Using precise terminology prevents the common mistake of applying mock-style behavior verification when state verification would be more appropriate and maintainable.

### 8.2 Default to State Verification

The classical/Detroit approach — using real objects and verifying state — produces tests that are more resilient to refactoring and provide higher fidelity. Use behavior verification (mocks) only when the interaction itself is the observable behavior being tested.

### 8.3 The Preference Hierarchy

Following Google's recommendation:
1. **Real implementations** — highest fidelity, no abstraction gap
2. **Verified fakes** — realistic behavior, fast execution, contract-tested
3. **Stubs** — control inputs when needed
4. **Mocks** — verify interactions when the interaction is the behavior
5. **Dummies** — fill parameter lists

### 8.4 Mock at Boundaries, Not Internals

Test doubles belong at architectural boundaries (ports in hexagonal architecture). Never mock internal collaborators within the same module. Intra-system communication is an implementation detail; inter-system communication is observable behavior.

### 8.5 Contract Tests Close the Fake Drift Gap

Any hand-written fake should be accompanied by a contract test suite that runs against both the fake and the real implementation. This catches drift before it causes false confidence.

### 8.6 Over-Mocking Is a Design Smell

If a class requires many mocks to test, the class likely has too many dependencies. The need for excessive mocking is feedback about the design — listen to it. Refactor the design rather than papering over it with mocks.

### 8.7 Safety-Critical Domains Add Documentation Requirements

In auditable environments, every test double must be justified, its limitations documented, and the resulting test coverage gaps explicitly closed by higher-level tests. The V-model's right side (integration, system tests) must verify what the left side's unit tests could not due to test doubles. This is not optional — it is a regulatory requirement.

### 8.8 Architecture Determines Testability

Good architecture (hexagonal/ports-and-adapters, dependency injection, clear boundaries) makes test doubles natural and minimal. Poor architecture (hidden dependencies, static calls, god classes) makes test doubles necessary in excess. Invest in architecture to reduce the need for test doubles, rather than investing in elaborate mocking to compensate for poor architecture.

---

## Appendix: Key References

### Books
1. Meszaros, Gerard. *xUnit Test Patterns: Refactoring Test Code*. Addison-Wesley, 2007.
2. Freeman, Steve and Nat Pryce. *Growing Object-Oriented Software, Guided by Tests*. Addison-Wesley, 2009.
3. Beck, Kent. *Test Driven Development: By Example*. Addison-Wesley, 2002.
4. Winters, Titus, Tom Manshreck, and Hyrum Wright. *Software Engineering at Google*. O'Reilly, 2020. [Chapter 13: Test Doubles](https://abseil.io/resources/swe-book/html/ch13.html)

### Articles
5. [Fowler, Martin. "Mocks Aren't Stubs." 2007](https://martinfowler.com/articles/mocksArentStubs.html)
6. [Fowler, Martin. "TestDouble." martinfowler.com](https://martinfowler.com/bliki/TestDouble.html)
7. [Google Testing Blog. "Increase Test Fidelity By Avoiding Mocks." 2024](https://testing.googleblog.com/2024/02/increase-test-fidelity-by-avoiding-mocks.html)
8. [Schlawack, Hynek. "'Don't Mock What You Don't Own' in 5 Minutes"](https://hynek.me/articles/what-to-mock-in-5-mins/)
9. [Holub, Oleksii. "Prefer Fakes Over Mocks"](https://tyrrrz.me/blog/fakes-over-mocks)
10. [Khorikov, Vladimir. "When to Mock." Enterprise Craftsmanship](https://enterprisecraftsmanship.com/posts/when-to-mock/)

### Standards
11. RTCA. *DO-178C: Software Considerations in Airborne Systems and Equipment Certification.* 2012.
12. ISO. *ISO 26262: Road vehicles — Functional safety.* 2018.
13. Automotive SIG. *Automotive SPICE Process Assessment / Reference Model.* v3.1+.
14. IEC. *IEC 62304:2006+A1:2015 — Medical device software — Software life cycle processes.*
