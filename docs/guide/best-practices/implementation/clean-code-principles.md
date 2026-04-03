# Clean Code Principles for V-Model Development

This document covers the core principles for writing maintainable, reliable code. These are not just "nice to have" — they directly support V-model compliance by making code verifiable, traceable, and reviewable.

---

## SOLID Principles

SOLID is the foundation of maintainable object-oriented design. Each principle solves a specific design problem that, left unchecked, makes code brittle, hard to test, and expensive to change.

### Single Responsibility Principle (SRP)

> A class should have one, and only one, reason to change.

Every class handles one specific concern. "Reason to change" means one stakeholder or business rule.

**Practical test:** Can you describe the class's purpose in one sentence without using "and"?

**Why it matters for V-model:** Traceability requires linking design elements to code. A class with three responsibilities creates a many-to-many mapping that's hard to trace and harder to verify. A class with one responsibility traces cleanly to one design element.

**Example violation:**

```java
// BAD: three responsibilities in one class
class ReportGenerator {
    List<Sale> fetchSalesData(DateRange range) { ... }  // data access
    Report applyBusinessRules(List<Sale> sales) { ... }  // domain logic
    void formatAndSendEmail(Report report) { ... }       // presentation + I/O
}
```

**Example fix:**

```java
class SalesRepository {
    List<Sale> fetchByDateRange(DateRange range) { ... }
}

class SalesReportBuilder {
    Report buildFrom(List<Sale> sales) { ... }
}

class ReportEmailSender {
    void send(Report report, EmailAddress recipient) { ... }
}
```

Now each class traces to one design element. Testing each is trivial. Changing the email format doesn't risk breaking the business rules.

### Open/Closed Principle (OCP)

> Software entities should be open for extension but closed for modification.

Add new behavior by adding new code (new classes, new implementations), not by editing existing working code.

**Practical test:** Can you add a new export format / validation rule / calculation strategy without touching existing classes?

**Example:**

```java
// BAD: adding a new format requires editing this method
String export(Report report, String format) {
    if (format.equals("PDF"))      return exportPdf(report);
    else if (format.equals("CSV")) return exportCsv(report);
    else if (format.equals("XML")) return exportXml(report);  // added later
    // ...every new format edits this code
}

// GOOD: new formats are new classes
interface ReportExporter {
    String export(Report report);
}

class PdfExporter implements ReportExporter { ... }
class CsvExporter implements ReportExporter { ... }
class XmlExporter implements ReportExporter { ... }  // added without touching existing code
```

### Liskov Substitution Principle (LSP)

> Subtypes must be substitutable for their base types without altering correctness.

If `S` extends `T`, then objects of type `T` can be replaced with objects of type `S` without breaking behavior.

**Practical test:** Does the subclass honor all contracts (preconditions, postconditions, invariants) of the parent?

**Classic violation:** `Square extends Rectangle` where `setWidth()` silently changes height, breaking the rectangle contract.

**Why it matters:** LSP violations create bugs that are invisible in unit tests but explode in integration. If your design says "any `Sensor` can be used here," but `TemperatureSensor` throws on `calibrate()` while `PressureSensor` doesn't, that's an LSP violation — and a safety issue.

### Interface Segregation Principle (ISP)

> Clients should not be forced to depend upon interfaces they do not use.

Prefer many small, focused interfaces over one large "god interface."

**Practical test:** Does any implementor throw `UnsupportedOperationException` or leave methods empty? That's an ISP violation.

**Example:**

```java
// BAD: one fat interface
interface Vehicle {
    void accelerate();
    void brake();
    void fly();          // cars can't fly
    void submerge();     // planes can't submerge
}

// GOOD: segregated interfaces
interface Driveable { void accelerate(); void brake(); }
interface Flyable   { void takeOff(); void land(); }
interface Submersible { void dive(); void surface(); }
```

### Dependency Inversion Principle (DIP)

> High-level modules should not depend on low-level modules. Both should depend on abstractions.

Business logic depends on interfaces, not concrete implementations. Infrastructure implements those interfaces.

**Practical test:** Can you swap the database from PostgreSQL to SQLite for testing without changing business logic code?

**Example:**

```java
// BAD: business logic depends on infrastructure
class OrderService {
    private PostgresOrderRepository repo = new PostgresOrderRepository();
    // ...
}

// GOOD: business logic depends on abstraction
class OrderService {
    private final OrderRepository repo;

    OrderService(OrderRepository repo) {  // constructor injection
        this.repo = repo;
    }
}

// Production: new OrderService(new PostgresOrderRepository(dataSource))
// Testing:    new OrderService(new InMemoryOrderRepository())
```

---

## DRY, KISS, YAGNI

These three meta-principles form a practical decision framework for everyday coding choices. They sometimes conflict — the skill is in balancing them.

### DRY (Don't Repeat Yourself)

> Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

Duplication means changes require updates in multiple places — a guaranteed source of bugs.

**But beware over-DRYing:** Not all similar-looking code is the same concern. Two functions that happen to have the same implementation today may evolve differently tomorrow. Premature abstraction (DRYing too early) creates worse coupling than the duplication it eliminates.

**The Rule of Three:** Tolerate duplication twice. On the third occurrence, abstract.

**DRY applies to knowledge, not just code.** A business rule expressed in code AND in a comment is a DRY violation — the comment will rot.

### KISS (Keep It Simple, Stupid)

The simplest solution that works is almost always the best.

**Practical test:** Would a new team member understand this code in under 5 minutes?

Over-engineering — adding layers, patterns, abstractions "just in case" — violates KISS. Simple code is easier to read, test, debug, maintain, and for AI agents to understand.

### YAGNI (You Ain't Gonna Need It)

> Always implement things when you actually need them, never when you just foresee that you need them.

Do not build infrastructure for hypothetical future requirements. Every unused abstraction is maintenance cost with zero return.

**This does NOT mean "don't think about architecture."** It means implement the simplest thing that satisfies current, real requirements while keeping the design open for extension (OCP).

### The Tension

DRY, KISS, and YAGNI can conflict:
- Excessive DRY creates complex abstractions (violating KISS)
- YAGNI can lead to duplication (violating DRY)
- The resolution: balance based on **actual, concrete needs** — not hypothetical ones

---

## Function Design

Functions are the fundamental unit of code. Get them right and everything else follows.

### The Rules

1. **Functions should be small.** Target 5-15 lines. Hard max 50 lines. If a function needs a comment explaining what a section does, that section should be a separate function.

2. **Functions should do one thing.** They should do it well. They should do it only. If you can describe the function with "it does X **and** Y", it does too many things.

3. **One level of abstraction per function.** Don't mix high-level policy with low-level detail. If a function calls `authenticateUser()` and also does `socket.getInputStream().read(buffer, 0, len)`, the abstraction levels are mixed.

4. **Minimize arguments.** Zero (niladic) is ideal. One (monadic) is fine. Two (dyadic) are acceptable. Three or more: wrap in a parameter object.

5. **No boolean flag arguments.** A boolean parameter announces the function does more than one thing. Split it: `render(true)` becomes `renderForPrint()` and `renderForScreen()`.

6. **No side effects.** A function that promises to do one thing but secretly modifies shared state is lying. Side effects create temporal couplings.

7. **Command-Query Separation.** A function should either change state (command) or return information (query), not both.

8. **Return early.** Guard clauses at the top reduce nesting.

**Example — before and after:**

```java
// BAD: long, multiple levels of abstraction, side effects
void processOrder(Order order, boolean urgent) {
    if (order != null) {
        if (order.getItems() != null && !order.getItems().isEmpty()) {
            double total = 0;
            for (Item item : order.getItems()) {
                total += item.getPrice() * item.getQuantity();
                if (item.getQuantity() > inventory.getStock(item.getId())) {
                    emailService.sendLowStockAlert(item);  // side effect!
                }
            }
            if (urgent) {
                total *= 1.5;
            }
            order.setTotal(total);
            database.save(order);
            if (urgent) {
                notificationService.sendUrgentConfirmation(order);
            }
        }
    }
}

// GOOD: small functions, one thing each, no side effects in calculation
Money calculateOrderTotal(Order order, ShippingPriority priority) {
    Money subtotal = order.items().stream()
        .map(item -> item.price().multiply(item.quantity()))
        .reduce(Money.ZERO, Money::add);

    return priority.applyMultiplier(subtotal);
}

List<Item> findLowStockItems(Order order, Inventory inventory) {
    return order.items().stream()
        .filter(item -> item.quantity() > inventory.stockOf(item.id()))
        .toList();
}
```

---

## Class Design

### Single Responsibility (Again)

A class should be small enough to describe in one sentence without "and."

**Signals of too-large classes:**
- You can't name it without using a generic word (Manager, Processor, Handler, Utility)
- It has more than ~10 methods
- Its methods naturally cluster into groups that don't interact
- Changes for different reasons require editing the same class

### High Cohesion

All methods should use most of the class's fields. If half the methods use fields A and B, and the other half use fields C and D, you have two classes pretending to be one.

### Prefer Composition Over Inheritance

Inheritance is the strongest form of coupling. Use it only when there's a genuine "is-a" relationship and the Liskov Substitution Principle holds. For "has-a" or "uses-a" relationships, use composition.

```java
// BAD: inheritance for code reuse
class SpecialStack extends ArrayList<Item> {
    // inherits 30+ methods that don't make sense for a stack
}

// GOOD: composition
class SpecialStack {
    private final List<Item> items = new ArrayList<>();

    void push(Item item) { items.add(item); }
    Item pop() { return items.remove(items.size() - 1); }
    boolean isEmpty() { return items.isEmpty(); }
}
```

### Depend on Abstractions at Boundaries

Within a module, concrete classes are fine. At boundaries between modules, layers, or services — use interfaces. This is where the Dependency Inversion Principle applies.

**When to use interfaces:**
- At architectural boundaries (between layers)
- When there will be multiple implementations
- When you need test doubles
- When crossing team boundaries

**When NOT to use interfaces:**
- For every single class (over-engineering)
- For data/value objects
- When there's exactly one implementation and no testing need

---

## Code Smells: Warning Signs

Code smells are not bugs. The code works. But they indicate structural weaknesses that slow development and increase defect risk.

### The Most Important Smells

| Smell | What It Looks Like | What to Do |
|-------|-------------------|-----------|
| **Long Method** | Function > 20 lines, does multiple things | Extract Method |
| **Large Class** | Class with 15+ methods, generic name | Extract Class |
| **Long Parameter List** | Function with 4+ parameters | Introduce Parameter Object |
| **Feature Envy** | Method uses another class's data more than its own | Move Method |
| **Shotgun Surgery** | One change requires edits in many files | Move related code together |
| **Divergent Change** | One class changed for many different reasons | Split into focused classes |
| **Dead Code** | Unreachable branches, unused methods | Delete (VCS remembers) |
| **Speculative Generality** | Infrastructure for "someday" | Delete (YAGNI) |
| **Primitive Obsession** | `String zipCode` instead of `ZipCode` | Introduce Value Object |
| **Message Chains** | `a.getB().getC().getD()` | Law of Demeter — ask, don't dig |

### Refactoring Patterns for Common Smells

| Refactoring | When to Use |
|-------------|------------|
| Extract Method | Long functions, duplicated blocks |
| Extract Class | Large classes with multiple responsibilities |
| Move Method / Move Field | Put behavior where the data is |
| Rename | Names don't reveal intent |
| Introduce Parameter Object | Long parameter lists, data clumps |
| Replace Conditional with Polymorphism | Switch/if chains on type |
| Replace Magic Number with Named Constant | Unexplained literal values |

---

## Immutability

An immutable object's state cannot be modified after creation. Instead of changing existing data, you create new instances.

### Why It Matters

- **Thread safety:** Immutable objects can be shared across threads without locks.
- **Predictability:** No surprise mutations. What you create is what you get.
- **Debugging:** If a value is wrong, it was wrong at creation time.
- **Safe sharing:** Pass freely without defensive copying.

### In Practice

```java
// Java 17: use records for value objects (immutable by default)
record Coordinate(double latitude, double longitude) {}

// Immutable collections
var points = List.of(new Coordinate(59.3, 18.1), new Coordinate(48.8, 2.3));

// Fields final where possible
class FlightPlan {
    private final String callsign;
    private final List<Waypoint> route;

    FlightPlan(String callsign, List<Waypoint> route) {
        this.callsign = callsign;
        this.route = List.copyOf(route);  // defensive copy to immutable
    }
}
```

### When Not to Use Immutability

- Hot loops where allocation pressure matters (profiler-driven, not premature)
- Frameworks that require mutability (some ORMs, serialization)
- Large data structures without structural sharing

---

## Design Patterns That Actually Help

Not all 23 GoF patterns are equally useful. These consistently solve real problems:

| Pattern | When to Use | Modern Note |
|---------|------------|-------------|
| **Strategy** | Multiple algorithms for the same operation | Often replaced by lambda/function parameters |
| **Factory Method** | Object creation depends on context/configuration | Essential for DI without a framework |
| **Adapter** | Integrating with external APIs or legacy code | Workhorse of hexagonal architecture |
| **Decorator** | Cross-cutting concerns (logging, caching, retry) | Middleware patterns are decorator chains |
| **Builder** | Complex objects with many optional parameters | Ubiquitous in modern Java |
| **Null Object** | Default behavior when no specific implementation exists | Better than null checks |
| **Observer** | Decoupling event producers from consumers | Event buses, reactive streams |

### Patterns to Use Sparingly

- **Singleton** — global state in disguise, makes testing hard
- **Visitor** — powerful but complex, only for stable type hierarchies
- **Abstract Factory** — often over-engineered

### Anti-Patterns to Avoid

- **Service Locator** — hides dependencies, use DI instead
- **God Object** — a single class that knows and does everything
- **Anemic Domain Model** — entities with only data, all behavior in services
- **Golden Hammer** — applying one pattern to every problem

---

## Sources

- Robert C. Martin, *Clean Code* (2008)
- Robert C. Martin, *Clean Architecture* (2017)
- Martin Fowler, *Refactoring* (1999, 2nd ed. 2018)
- Gang of Four, *Design Patterns* (1994)
- Andy Hunt & Dave Thomas, *The Pragmatic Programmer* (1999)
- Alistair Cockburn, Hexagonal Architecture (2005)
