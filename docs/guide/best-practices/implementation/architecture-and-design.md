# Architecture and Design at the Code Level

This document covers code-level architectural patterns — how to organize code so that business logic is protected, testable, and maintainable. This is not about system architecture (microservices, deployment) but about the structure within a single application or module.

---

## Separation of Concerns

The foundational principle: each section of a program should address a single concern and not be entangled with unrelated concerns.

This applies at every level:

| Level | Concern Separation |
|-------|-------------------|
| **Function** | Each function does one thing |
| **Class** | Each class encapsulates one concept |
| **Module/Package** | Each module handles one bounded context |
| **Layer** | Each layer addresses one type of responsibility (domain, infrastructure, presentation) |

Without separation of concerns, you get the Big Ball of Mud — code where everything depends on everything, any change risks breaking unrelated features, and testing requires the entire system to be running.

---

## The Core Insight: Business Logic Must Not Depend on Infrastructure

Layered, hexagonal, and clean architectures all share one fundamental insight: **dependency arrows must point toward the business logic, never away from it.**

```
    Infrastructure (HTTP, DB, file system)
         |
         | depends on
         v
    Business Logic (domain rules, use cases)
```

The business logic defines interfaces (ports) that infrastructure implements (adapters). The business logic never imports infrastructure packages.

**Why this matters for V-model:**
- Business logic can be tested in isolation — no database, no HTTP, no filesystem
- Design-to-code traceability is cleaner — domain concepts map directly to domain classes
- Code reviews focus on correctness — reviewers don't need to understand infrastructure to verify business rules
- Compliance evidence is stronger — you can demonstrate that safety-critical logic is isolated from volatile infrastructure

---

## Hexagonal Architecture (Ports and Adapters)

The most practical architectural pattern for most applications.

```
                [REST Controller]
                       |
                    [Input Port]           <-- interface defined by core
                       |
           +-----------+-----------+
           |     APPLICATION       |
           |       CORE            |
           |  (domain + use cases) |
           +-----------+-----------+
                       |
                    [Output Port]          <-- interface defined by core
                       |
                [PostgreSQL Adapter]
```

### Ports

Interfaces defined by the application core:
- **Input ports** (driving): what the application offers to the outside world. Example: `OrderService`, `FuelCalculator`
- **Output ports** (driven): what the application needs from the outside world. Example: `OrderRepository`, `SensorDataProvider`

### Adapters

Concrete implementations of ports:
- **Input adapters**: REST controllers, CLI handlers, message consumers — they translate external input into calls on input ports
- **Output adapters**: database repositories, HTTP clients, file writers — they implement output ports

### The Rule

**The core knows nothing about adapters.** It only knows its own ports (interfaces). Swapping adapters (PostgreSQL to MongoDB, REST to gRPC) requires zero changes to business logic.

### Directory Structure Example

```
src/
  domain/               # Entities, value objects, domain services
    Order.java
    OrderItem.java
    Money.java
  application/          # Use cases (input ports + orchestration)
    ports/
      input/
        CreateOrderUseCase.java     # interface
        GetOrderUseCase.java        # interface
      output/
        OrderRepository.java        # interface
        PaymentGateway.java         # interface
    services/
      OrderService.java             # implements input ports, uses output ports
  infrastructure/       # Adapters (implements output ports)
    persistence/
      PostgresOrderRepository.java
    payment/
      StripePaymentGateway.java
  api/                  # Input adapters
    rest/
      OrderController.java
```

### Testing Benefits

```java
// Unit test: test business logic with fake adapter
class OrderServiceTest {
    private OrderService service;

    @BeforeEach
    void setUp() {
        var fakeRepo = new InMemoryOrderRepository();
        var fakePayment = new FakePaymentGateway();
        service = new OrderService(fakeRepo, fakePayment);
    }

    @Test
    void createOrder_calculatesTotal() {
        // No database, no HTTP, no external services
        // Pure business logic verification
    }
}
```

---

## Clean Architecture (When You Need More Structure)

For large systems with complex domain logic, Robert C. Martin's Clean Architecture adds more explicit layers:

```
    Frameworks & Drivers (outermost)
        Interface Adapters
            Application Business Rules (Use Cases)
                Enterprise Business Rules (Entities) (innermost)
```

**The Dependency Rule:** Source code dependencies must point inward only. Inner layers know nothing about outer layers.

- **Entities** — core business objects and rules, no framework dependencies
- **Use Cases** — application-specific business rules, orchestrate entities
- **Interface Adapters** — convert data between use cases and external formats
- **Frameworks & Drivers** — web framework, database, UI

For most projects, hexagonal architecture provides sufficient structure. Clean Architecture is valuable when you have genuinely complex domain logic that benefits from the entities/use cases distinction.

---

## Testability as a Design Constraint

> If code is hard to test, the design is wrong.

This is the single most actionable heuristic in software design. Hard-to-test code is hard to test because of design problems, not testing problems.

### Testability Signals (Good Design)

- Easy to instantiate in isolation = good cohesion, few dependencies
- Easy to inject test data = proper use of dependency injection
- Deterministic results = no hidden state, no side effects
- Small test surface = small, focused functions

### Testability Anti-Signals (Design Smells)

| Anti-Signal | Design Problem |
|-------------|---------------|
| Excessive setup / mocking in tests | Too many dependencies (SRP violation) |
| Tests break when internal details change | Testing implementation, not behavior |
| Can't test without a database / network | Missing abstraction boundary |
| Slow tests | Coupling to I/O that should be behind an interface |
| Flaky tests | Hidden shared state, temporal coupling, non-determinism |
| Test requires complex object graph | Over-coupled classes, missing factories/builders |

### The Functional Core, Imperative Shell Pattern

Separate pure computation from I/O:

```
Imperative Shell (reads input, calls core, writes output)
    |
    v
Functional Core (pure functions, no I/O, all logic)
```

The core is trivially testable — pass in data, check output. The shell is thin and mostly calls the core. Most bugs live in logic, not in I/O plumbing.

```java
// Functional core: pure, testable, no I/O
record FuelEstimate(double requiredKg, double reserveKg, boolean sufficient) {}

FuelEstimate calculateFuel(FlightPlan plan, WeatherData weather, AircraftPerformance perf) {
    double required = plan.legs().stream()
        .mapToDouble(leg -> perf.fuelBurnRate(leg, weather))
        .sum();
    double reserve = required * perf.reserveFactor();
    return new FuelEstimate(required, reserve, required + reserve <= perf.maxFuelKg());
}

// Imperative shell: I/O, no logic
void handleFuelCheck(String flightPlanId) {
    var plan = flightPlanRepo.findById(flightPlanId);
    var weather = weatherService.getCurrentForRoute(plan.route());
    var perf = aircraftRepo.getPerformanceData(plan.aircraftType());

    var estimate = calculateFuel(plan, weather, perf);  // pure call

    fuelReportRepo.save(estimate);
    if (!estimate.sufficient()) {
        alertService.sendInsufficientFuelAlert(flightPlanId, estimate);
    }
}
```

---

## Cohesion and Coupling

The two most fundamental metrics of module quality.

### Cohesion (Internal)

How closely related are the elements within a module?

**Spectrum (worst to best):**

1. **Coincidental** — elements are in the same module by accident
2. **Logical** — grouped by type (all validators, all parsers) not by feature
3. **Temporal** — grouped because they run at the same time
4. **Communicational** — elements operate on the same data
5. **Sequential** — output of one element is input to the next
6. **Functional** (best) — every element contributes to a single, well-defined task

**Practical test:** If you had to split the class, would there be a natural seam? If yes, the class has mixed responsibilities.

### Coupling (External)

How much does one module depend on another?

**Spectrum (worst to best):**

1. **Content** — one module modifies another's internal data directly
2. **Common** — modules share global data
3. **Control** — one module controls another's logic via flags
4. **Stamp** — modules share a data structure but each uses only part of it
5. **Data** (best) — modules communicate only through simple parameters

### The Goal

**HIGH cohesion within modules, LOW coupling between them.**

A module with high cohesion and low coupling is:
- Easy to understand (one focused concept)
- Easy to test (few external dependencies)
- Easy to change (changes are localized)
- Easy to trace (maps cleanly to one design element)

---

## Interface-Driven Design

Interfaces (or abstract types / protocols / traits) are the primary tool for achieving loose coupling.

### Principles

- **Program to an interface, not an implementation** (GoF, 1994)
- **Define interfaces from the consumer's perspective.** What does the caller need? Not: what does the provider offer?
- **Keep interfaces small and focused** (ISP)
- **Use interfaces to define boundaries between layers** (ports in hexagonal architecture)

### When to Use Interfaces

- At architectural boundaries (between layers, between modules)
- When there will be multiple implementations (now or plausibly)
- When you need test doubles
- When crossing team boundaries

### When NOT to Use Interfaces

- For every single class — if a class has exactly one implementation and no testing need, an interface adds ceremony without value
- For data/value objects — these are concrete by nature
- Premature abstraction — extract an interface when you have a second consumer or implementation, not before (YAGNI)

---

## Practical Architecture Checklist

For code reviews and self-assessment:

- [ ] Business logic has zero `import` statements for infrastructure packages
- [ ] All external dependencies are accessed through interfaces defined by the core
- [ ] Each layer only calls the layer directly below/inside it
- [ ] No circular dependencies between packages/modules
- [ ] Domain objects have no framework annotations (or minimal, justified ones)
- [ ] Test doubles can replace all external dependencies
- [ ] Adding a new input channel (REST, CLI, message queue) requires no changes to business logic
- [ ] Adding a new data store requires no changes to business logic
- [ ] Each class can be described in one sentence without "and"
- [ ] Functions are under 20 lines with cyclomatic complexity under 10

---

## Sources

- Robert C. Martin, *Clean Architecture* (2017)
- Alistair Cockburn, Hexagonal Architecture / Ports and Adapters (2005)
- Martin Fowler, *Patterns of Enterprise Application Architecture* (2002)
- Gary Bernhardt, "Functional Core, Imperative Shell" (2012)
- Meilir Page-Jones, *Fundamentals of Object-Oriented Design in UML* (1999)
