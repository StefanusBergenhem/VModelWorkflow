# Research 5a: System-to-Software Decomposition and Allocation

Research for architecture craft documentation. Covers how to break a system into
software, hardware, and operational parts, and how to make good allocation decisions.

**Sources used:**
- [src-nasa-ld] NASA Systems Engineering Handbook §4.3 — Logical Decomposition. https://www.nasa.gov/reference/4-3-logical-decomposition/
- [src-barr-hwsw] Barr Group — Hardware-Software Partitioning in Embedded Systems. https://barrgroup.com/blog/hardware-software-partitioning-embedded-systems
- [src-hwe-part] HWE Design — Hardware-Software Partitioning. https://www.hwe.design/system-design/what-is-hardware-system-design/hardware-software-partitioning
- [src-mirabilis] Mirabilis Design — Hardware-Software Partitioning in SoC. https://www.mirabilisdesign.com/hardware-software-partitioning-in-system-on-chip-soc/
- [src-sebok-srd] SEBoK Wiki — System Requirements Definition. https://sebokwiki.org/wiki/System_Requirements_Definition
- [src-icd-wiki] Wikipedia — Interface Control Document. https://en.wikipedia.org/wiki/Interface_control_document
- [src-informit-decomp] InformIT — Software System Decomposition (Avoid Functional Decomposition). https://www.informit.com/articles/article.aspx?p=2995357
- [src-volatility] DEV Community — Principles of Volatility-Based Decomposition. https://dev.to/ujjwall-r/principles-of-volatility-based-decomposition-in-system-design-2b62
- [src-state-pat] Game Programming Patterns — State Pattern. https://gameprogrammingpatterns.com/state.html
- [src-4plus1] Visual Paradigm — 4+1 Views in Modeling System Architecture with UML. https://guides.visual-paradigm.com/4-1-views-in-modeling-system-architecture-with-uml/
- [src-conops] Reqi.io — Concept of Operations (CONOPS) for Systems Engineers. https://reqi.io/articles/concept-of-operations-conops
- [src-atam] SEI — Architecture Tradeoff Analysis Method. https://www.sei.cmu.edu/library/file_redirect/1998_005_001_16646.pdf/

---

## 1. What Decomposition Is and Why It Matters

System decomposition is the act of breaking a system into parts that can be designed, built, tested, and integrated separately. It is not just a documentation exercise — it is the primary architectural decision of a project.

NASA's handbook defines the goal precisely: logical decomposition "identifies 'what' the system should achieve at each level" and produces "detailed functional requirements that enable programs and projects to meet stakeholder expectations" [src-nasa-ld]. The key output is not a diagram — it is allocated requirements with clear ownership.

Decomposition must be approached as a creative, engineering-intensive process. NASA explicitly describes it as "creative, recursive, collaborative, and iterative" — not a mechanical procedure [src-nasa-ld]. Good decomposition requires understanding both what the system must do and the means available to do it.

**Why decomposition quality matters:**

- Architecture baselining decisions become exponentially more expensive to change later [src-nasa-ld]
- Partitioning "has dramatic impact on the cost and performance of the whole system" [src-mirabilis]
- Flawed decomposition leads to expensive maintenance and potential system rewrites [src-informit-decomp]

---

## 2. The Decomposition Process: From System to Parts

### 2.1 Start with the complete functional picture

Before allocating anything to hardware, software, or operations, map the full set of functions the system must perform. NASA's functional analysis process works top-down:

1. Translate top-level requirements into performable system functions
2. Decompose each function to lower levels in the product breakdown structure
3. Identify interfaces between functions at each level [src-nasa-ld]

Each function is described by its inputs, outputs, failure modes, consequence of failure, and interface requirements [src-nasa-ld]. This framing forces architects to think about failure behavior during decomposition, not as an afterthought.

### 2.2 Logical vs. physical architecture — keep them separate

A critical discipline: keep the logical architecture (what functions exist and how they relate) separate from the physical architecture (what hardware or software element performs each function).

The SEBoK approach makes this explicit: logical components represent behavioral responsibilities; physical components represent implementation technologies. Allocation is the bridge: "logical components are allocated to the physical components to develop the physical architecture" [src-sebok-srd].

This separation allows:
- Multiple physical alternatives to be evaluated against the same logical design
- Allocation decisions to be made and changed without restructuring the functional model
- Requirements to be traced through both views independently

### 2.3 Allocation is not assignment — it is budgeting

Requirements do not simply move from system level to subsystem level unchanged. Allocation involves decomposing budgeted quantities. The SEBoK framework identifies examples of decomposable parameters: mass, power usage, bandwidth, time, and quality attributes [src-sebok-srd]. Changes cascade — if a timing budget is tightened at the system level, every allocated timing budget below it is affected.

This means every allocation decision must carry:
- The parent requirement it derives from
- The portion of the parent budget assigned
- The rationale for that split
- What other allocations would need to change if this one changes [src-sebok-srd]

---

## 3. What Drives Allocation to Hardware, Software, or Operations

### 3.1 The candidate allocation domains

A system function can be allocated to:
- **Custom hardware** (dedicated circuits, FPGAs, ASICs)
- **Software on general-purpose processor** (application software, firmware)
- **RTOS / middleware** (scheduling, communication, resource management)
- **External hardware** (sensors, actuators, infrastructure not built by the team)
- **Human operators** (procedures, manual steps, judgment calls)
- **A combination** (software controlling hardware under operator supervision)

At the lowest level, "a subset of the requirements are assigned to a particular hardware or software item, skilled staff, procedures, facilities, interfaces, services, or other individual elements of the final system" [src-sebok-srd].

### 3.2 Primary allocation criteria

These criteria are the practical decision drivers:

**Timing and determinism**

Hardware delivers deterministic sub-microsecond timing. When a function requires response times under 100 nanoseconds, hardware is almost always necessary [src-barr-hwsw]. Software on a general-purpose OS introduces jitter that cannot be designed away — the non-determinism is structural.

Corollary: slow interfaces (anything that can tolerate millisecond response) belong in software by default. "Slow speed interfaces should absolutely be done in software" [src-barr-hwsw].

**Performance throughput**

For functions that require massively parallel computation — signal processing, encryption at high data rates, video codec — dedicated hardware is often necessary. Software running on a single core simply cannot match the throughput. Modern FPGAs with embedded processors allow a hybrid: offload the high-throughput function to the FPGA fabric while keeping control logic in software [src-barr-hwsw].

**Flexibility and maintainability**

Software can be updated after deployment; hardware (especially ASIC) cannot. Functions that are likely to change — business logic, protocol handling, user-visible behavior — should be in software. "Design requires future modifications or maintenance" is a decisive argument for software [src-barr-hwsw].

A smart home system example: control algorithms in software for flexibility, "always-on" voice detection on a dedicated low-power microcontroller [src-hwe-part]. The always-on detection function has fixed behavior and tight power constraints — hardware. The control algorithm changes with product updates — software.

**Cost structure**

Two cost dimensions move in opposite directions:
- *NRE (non-recurring engineering)*: Hardware typically costs 2-3x more in development effort. Hardware synthesis tools alone cost $5-10K vs. software tool costs [src-barr-hwsw].
- *Recurring (per unit)*: If software requires a more powerful processor or more memory, per-unit BOM cost increases. In high-volume products, a $0.50 difference per unit matters.

This creates a volume threshold: for low volumes, software wins on NRE. For very high volumes, hardware acceleration may win on per-unit cost despite higher NRE.

**Power consumption**

Dedicated hardware can achieve far better energy efficiency for specific workloads than a general-purpose processor running equivalent software [src-hwe-part]. For battery-powered or thermally constrained products, this may be decisive.

**Testability**

Software is cheaper to test and easier to instrument than hardware. Functions with complex test requirements (boundary conditions, fault injection, coverage measurement) are easier to verify in software [src-atam]. Hardware faults during integration are expensive to diagnose and fix.

**Development risk and timeline**

FPGA development time grows nonlinearly with complexity; software compilation remains fast regardless [src-barr-hwsw]. Synthesis, place-and-route, and timing closure are engineering work that does not parallelise well. Teams routinely underestimate hardware development schedules.

### 3.3 The default rule and its exceptions

The practical default: **if a function can be done in software, do it in software** [src-barr-hwsw]. Override this default only when a measurable constraint forces the alternative:
- A timing requirement that software cannot meet
- A throughput requirement that software cannot sustain
- A power budget that software cannot fit
- A cost-per-unit target that software cannot achieve

Documenting which constraint drove the hardware allocation is important — it enables future re-evaluation as technology changes.

### 3.4 Allocation to human operations

Not all functions belong in software or hardware. Some are allocated to operating procedures:
- Functions that require judgment or contextual knowledge that cannot be formalized
- Functions that are too infrequent to justify automation
- Calibration and maintenance functions performed by skilled technicians
- Emergency overrides that must be human-supervised

The engineering decision: if a function is automated, the system must handle all its failure modes. If it is procedural (human-performed), the design must include the human in the reliability model and ensure the interface supports correct human performance.

---

## 4. Hardware/Software Interface Contracts

### 4.1 What an interface contract specifies

The hardware-software interface is a contract that defines what the software sees when it accesses hardware, and what the hardware guarantees about its behavior. It specifies:

- **Signal/data definitions**: data types, number of bytes, units, minimum and maximum values [src-icd-wiki]
- **Protocol**: sequence of operations, timing relationships, valid state transitions
- **Error conditions**: what errors the hardware can signal, what the software must do in response
- **Performance guarantees**: latency, throughput, jitter bounds hardware will deliver
- **Constraints on the caller**: ordering requirements, setup/hold times, forbidden operation sequences

The ICD (Interface Control Document) is the standard form of this contract: "provides a record of all interface information...generated for a project" and functions as "an umbrella document over the system interfaces" [src-icd-wiki].

### 4.2 Logical vs. physical interface specification

A mature interface specification exists at two levels:

**Logical interface**: captures the essential information exchange and protocol without committing to physical implementation. What data flows. What acknowledgments are required. What error modes exist. This can be written before hardware exists, and is what software architects need to proceed.

**Physical interface**: provides the precise definitions required for integration — connector pin assignments, voltage levels, bit encoding, register addresses, interrupt vectors. This is what the board-support-package author needs.

Separating these allows software design to proceed against the logical contract while hardware design firms up the physical details. The logical contract must remain stable once the software design begins; the physical contract can evolve independently as long as it implements the same logical behavior.

### 4.3 What makes a good interface contract

**Testability at the boundary**: "Adequately defined interfaces allow teams to test its implementation of the interface by simulating the opposing side with a simple communications simulator" [src-icd-wiki]. If you cannot write a simulator for one side of the interface using only the contract, the contract is underspecified.

**Scope discipline**: An ICD "should only describe the detailed interface documentation itself, and not the characteristics of the systems which use it." It should not include anything about the meaning or intended use of the data [src-icd-wiki]. The interface contract is not the place to explain what the system does with the data.

**Error control explicitly specified**: "Specify the sequence numbering, legality checks, error control and recovery procedures that will be used to manage the interface. Include any acknowledgment messages related to these procedures" [src-icd-wiki]. Omitting error handling from the contract leaves it undefined, which means each side will assume the other handles it.

**Version management**: Interfaces change. The ICD approach specifies "a set of interface versions that work together," which allows hardware and software to evolve at different rates [src-icd-wiki]. Without explicit versioning, an interface change is invisible until integration fails.

### 4.4 What software receives as constraints from the physical world

When hardware is designed first (or constrained by physical reality), software inherits constraints it cannot negotiate:

- **Sensor resolution and range**: the physical transducer determines what precision is achievable. Software cannot recover precision that the sensor does not provide.
- **Timing windows**: hardware may require the software to respond within a specific time window (interrupt latency, bus transaction timeout). Miss the window and behavior is undefined.
- **Noise and error characteristics**: sensors produce noise; signals degrade; bits get corrupted. The software architecture must account for the statistical error model, not treat inputs as perfect.
- **Power sequencing**: hardware components have required startup sequences. Software must not attempt to use a peripheral before it is powered and initialized.
- **Memory-mapped registers**: register access may have side effects (read-to-clear, write-to-trigger). Software must know which registers are safe to read repeatedly and which trigger hardware state changes.

These constraints flow into derived software requirements that are not visible in the system requirements — they emerge from the hardware design and must be captured in the interface contract or the software design will make incorrect assumptions.

---

## 5. Allocation Strategies and Their Trade-offs

### 5.1 Functional decomposition: the anti-pattern to avoid

The most common decomposition mistake is organizing the system by what it does. This creates services or subsystems like "InvoicingService", "BillingService", "ShippingService" that directly mirror the requirement list [src-informit-decomp].

The problems are structural:
- Any requirement change forces architectural restructuring, because the structure *is* the requirements
- Components become aware of each other's sequencing — "built into the fabric of B is the notion that it was called after A and before C"
- Reuse becomes impossible because each component assumes a specific call context
- Business logic migrates to the caller because the components cannot compose properly [src-informit-decomp]

Domain decomposition (organizing by business area) has the same problem. It is "functional decomposition in disguise" [src-informit-decomp].

### 5.2 Volatility-based decomposition: the principle

The alternative: decompose around *areas of change*, not around *operations* [src-volatility].

The key insight: volatility and variability are different.
- **Variability** is handled by an `if-else`. It belongs inside a component.
- **Volatility** requires changing the component itself. It should define the component boundary.

To find volatility, analyze two independent axes:
- **Temporal**: what can change for existing users over time? (algorithm upgrades, new protocols, regulatory changes)
- **Customer/use-case**: what differs across different users or deployment contexts at the same point in time?

These axes must be independent. If they overlap, you have found a functional grouping, not a volatility grouping [src-volatility].

### 5.3 The Stable Dependencies Principle

When allocating requirements across components, the direction of dependency matters. Robert Martin's Stable Dependencies Principle: "dependencies between packages should be in the direction of the stability of the packages. A package should only depend upon packages that are more stable than it is" [src-volatility].

Applied to system decomposition:
- Hardware interfaces are relatively stable — the physical layer does not change often
- Protocols are moderately stable — change during system evolution
- Application logic is volatile — changes most frequently with requirements

Architecture should be structured so application logic depends on stable abstractions (interfaces to hardware, service contracts), not on other volatile modules. A module that is likely to change should not be depended on by many other modules.

### 5.4 Budgeting as strategy

When a system requirement is budgeted across subsystems, the allocation strategy itself is a design choice. Consider a 100ms end-to-end response time:

| Allocation | HW sensing | SW processing | HW actuation |
|---|---|---|---|
| Conservative SW | 10ms | 70ms | 20ms |
| Aggressive SW | 10ms | 85ms | 5ms |
| Balanced | 15ms | 60ms | 25ms |

Each allocation produces different design constraints on each subsystem. The conservative allocation gives the software more budget but demands faster actuation. The aggressive allocation gives software maximum budget but leaves little margin for hardware variation.

Good allocation strategy builds in margin at known-risk elements, is explicit about what happens when a sub-budget is exceeded, and makes it possible to re-allocate as component designs mature.

---

## 6. System Modes and Their Architectural Implications

### 6.1 Why modes matter for decomposition

A system that operates in multiple modes is not a single system architecture — it is multiple behavioral configurations of the same physical elements. If the decomposition does not account for modes, the resulting architecture will have incorrect module boundaries and scattered mode-handling logic throughout the codebase.

Every real system has at least these mode categories:
- **Startup**: hardware power-on sequence, self-test, initialization, transition to operational
- **Normal operation**: the primary functional mode
- **Degraded operation**: reduced capability when components fail or resources are constrained
- **Maintenance / calibration**: special access modes for testing and adjustment
- **Diagnostic**: extended observability, may disable production optimizations
- **Shutdown**: ordered de-energization, state preservation, hardware protection

Each mode has different:
- Active functions (some functions only run in specific modes)
- Permitted transitions (not all mode-to-mode transitions are valid)
- Performance requirements (diagnostic mode may be slower; startup mode has strict timing)
- Interface contracts (some hardware interfaces may be unavailable in degraded mode)

### 6.2 Static and dynamic architectural views — why both are required

A static architecture diagram shows what components exist and how they are connected. It does not show which components are active in each mode, how mode transitions occur, or what happens at transitions.

A dynamic view (state machines, sequence diagrams, activity flows) shows behavior over time. The 4+1 view model captures this: the **Process View** shows "the flow of control between various activities or processes" and how components collaborate to accomplish tasks; the **Logical View** shows the static structure. Neither alone is sufficient [src-4plus1].

For modes specifically, the essential dynamic artifact is a mode state machine that specifies:
- All valid modes (the states)
- All valid transitions (including what events trigger them)
- Entry and exit actions for each mode
- Invariants that must hold in each mode

This state machine is an architectural document, not an implementation detail. It drives requirements allocation — requirements may only apply in specific modes, and that scope must be captured.

### 6.3 Mode-driven decomposition: the State pattern at system scale

The software State pattern applies at the architectural level, not just the object level. The key insight from the pattern: "all of the behavior and data for one state in a single class" [src-state-pat]. Boolean flags (`isJumping_`, `isDucking_`) are the software equivalent of undocumented system modes — scattered mode-handling logic that creates impossible state combinations.

Applied architecturally:
- Each system mode has a defined set of active functions, resource allocations, and interface behaviors
- Mode transitions are explicit events, not implicit consequences of state accumulation
- Mode-specific data (resources allocated to a mode that are irrelevant in others) belongs with the mode, not in a global context
- Entry and exit actions (hardware initialization sequences, state preservation) are defined as part of the mode, not scattered through callers

### 6.4 Degraded operation: design it, do not discover it

Graceful degradation is an architectural decision that must be made during decomposition, not patched in after integration. The principle: when faults occur, shed lower-priority functions to preserve higher-priority ones. This requires:

1. **Criticality assignment**: each function must have a declared criticality level
2. **Independence between criticality tiers**: high-criticality functions must not depend on the availability of low-criticality components
3. **Explicit degraded-mode contracts**: each component must specify what it can deliver in degraded mode, not just nominal mode
4. **Monitoring architecture**: the system must be able to detect that degradation has occurred

The design test: if any single component fails, can the system continue operating with reduced capability? If the answer is "it depends," the degraded-mode behavior is not designed — it is accidental.

### 6.5 Modes create derived requirements

A mode analysis is a requirements-generating activity, not just a documentation one. From a mode state machine, derived requirements include:

- Maximum time allowed for startup sequence
- State preservation requirements during mode transitions (what must not be lost)
- Watchdog and health monitoring requirements (how the system detects mode transition failures)
- Recovery requirements (what happens if a mode transition cannot complete)
- Restricted access requirements for maintenance and diagnostic modes

These requirements are not typically stated in system requirements documents — they emerge from the decision to have those modes. They must be captured and allocated to specific components.

---

## 7. Synthesis: A Decomposition Process That Avoids Common Failures

Combining the sources, a decomposition process with lower risk of structural failure:

**Step 1: Capture the operational concept first**

Before decomposing, document the CONOPS — what the system does in each mode from the operator's perspective. "Operational scenarios translate into specific system requirements, ensuring every system requirement can be traced back to a real operational need" [src-conops]. A mode state machine is the core artifact.

**Step 2: Build a logical functional model, not a physical one**

Map functions to a logical architecture. Do not assign technologies at this step. Resist the impulse to draw boxes labeled "database" or "microcontroller" — those are physical choices that should come after the functional structure is clear.

**Step 3: Identify volatility, not operations**

Find the boundaries where change is likely to occur. The two-axis analysis (temporal and customer/use-case) from volatility-based decomposition gives a structured way to find real module boundaries [src-volatility]. Operations (what functions do) make poor boundaries. Areas of likely change make good boundaries.

**Step 4: Allocate using measurable criteria**

For each function, apply the allocation criteria from section 3.2: timing, throughput, flexibility, cost structure, power, testability, development risk. Allocate to hardware only when a measurable constraint forces it; otherwise default to software. Document the forcing constraint — it enables re-evaluation when technology changes.

**Step 5: Define interface contracts before implementation begins**

For every allocated boundary, write the interface contract before any implementation. A contract is underspecified if you cannot write a test harness from it alone. Include: data types and ranges, protocol and sequencing, error conditions and recovery, performance bounds, version identifier [src-icd-wiki].

**Step 6: Propagate derived requirements**

Allocation produces derived requirements that were not in the input. Hardware constraints generate software requirements (timing budgets, error handling, initialization sequences). Mode analysis generates lifecycle requirements (startup time, state preservation, monitoring). These must be captured and allocated before the implementation is considered specified.

---

## 8. What the Sources Are Silent On

- **Mixed-criticality allocation**: how to handle a system where one software component has high-criticality requirements and another has low-criticality requirements, and they share a processor. The sources touch on degraded modes but not the allocation discipline for mixed-criticality systems.
- **Legacy retrofit**: all sources assume greenfield decomposition. Decomposing an existing system to understand its allocation (reverse decomposition) is a different problem — none of the sources address it directly.
- **Automated decomposition tools**: the sources mention that automated partitioning algorithms exist for SoC design, but do not give practical guidance on using them.
- **Team organization effects on decomposition**: Conway's Law (system structure mirrors team communication structure) is not discussed by any source, though it is a significant practical constraint on real decomposition decisions.
- **Incremental decomposition of large systems**: all sources treat decomposition as a single-pass activity. How to decompose incrementally (module by module, layer by layer) in a large system is not addressed.
