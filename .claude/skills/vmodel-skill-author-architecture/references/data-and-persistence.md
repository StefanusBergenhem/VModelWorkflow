# Data and persistence

Data topology is where most post-launch regret accumulates. An Architecture that decomposes beautifully at the component level and punts persistence to "we'll use a Postgres" is a ticking liability — by the time the topology becomes a problem, it is expensive to change.

## Database-per-service vs shared

| | Database-per-service | Shared database (per-module schemas) |
|---|---|---|
| Schema evolution | Per-service, independent | Coupled — one migration affects every service |
| Cross-service joins | Become cross-service calls | Trivial |
| Blast-radius isolation | Strong | Weak |
| Operational cost | Higher (N databases) | Lower (1 database) |
| Fits | Microservices with independent teams | Modular monolith; small teams; one deploy cadence |

**Rule of attribution:** a microservices system that *shares* a database has imported the operational cost of microservices without the independence benefit. A modular monolith can legitimately share a database. The Architecture entry names the choice and rationale.

## Consistency model — choose per data path

Strong consistency (every read sees every prior write, globally) costs availability or latency under partitions. CAP (Brewer) and PACELC (Abadi) state the trade-off formally.

The useful question is not "strong or eventual?" but:

1. **What is the maximum staleness window the user can tolerate** for this read path?
2. **What is the reconciliation story** when two writes collide?

*Eventual consistency without a reconciliation story is a bug factory.*

Consistency vocabulary worth naming explicitly:

- **Strong** — linearisable; every read sees the latest committed write.
- **Read-your-writes** — a session sees its own writes; other sessions may not yet.
- **Bounded staleness** — reads are at most N seconds / N versions behind.
- **Eventual** — convergence guaranteed; window unbounded unless stated.

Slot-fill per data path:

```yaml
consistency_model:
  read_path: "<<strong | read-your-writes | bounded-staleness | eventual>>"
  staleness_window: "<<≤Ns | n/a if strong>>"
  reconciliation_on_conflict: "<<last-writer-wins | CRDT-merge | manual-review-queue | n/a if single-writer>>"
```

Cross-link: Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017) — standard reference; Architecture cites it rather than re-teaches.

## Read replicas and CQRS

Read traffic often dominates write in transactional systems.

- **Read replica** — same schema, asynchronous copy, absorbs read load with bounded staleness. Cheap, low ceremony.
- **CQRS (Command-Query Responsibility Segregation)** — separate read model optimised for query shape (denormalised, indexed for read patterns, fed by events). Powerful when read and write shapes diverge sharply; overkill when they don't.

Decision rule: if your reads and writes have similar shape (same entity, same projection), a read replica suffices. If reads need different denormalisation or indexes than writes, CQRS earns its keep.

## Event sourcing as persistence

When event sourcing is the composition pattern (see `composition-patterns.md`), persistence *is* the event log plus projections. The Architecture entry for the log is the central data decision:

- **Retention** — forever (audit) or windowed (operational).
- **Partitioning** — by aggregate id (preserves ordering per aggregate).
- **Schema evolution** — upcasters / lazy migration / read-time projection rebuild. Pick one and state it.

## Multi-tenancy isolation tiers

Four tiers, increasing in cost and isolation:

| Tier | Mechanism | Cost | Isolation strength |
|---|---|---|---|
| **Row-level** | `tenant_id` column on every table | Cheapest | Weakest — query bug = cross-tenant leak |
| **Schema-level** | Schema per tenant in shared DB | Moderate | Moderate — schema mistakes still possible |
| **Database-level** | Database per tenant on shared infra | Higher | Strong — connection-string boundary |
| **Deployment-level** | Separate deployment per tenant | Highest | Strongest — process / network boundary |

**Tier mixing is legitimate and normal.** A high-isolation tier for audit data (database-level) can coexist with row-level for most operational tables. Defaulting to row-level for everything is cheap until the first compliance audit; defaulting to deployment-level for everything is expensive forever.

Slot-fill per data category:

```yaml
multi_tenancy:
  category: "<<operational | audit | secrets | analytics>>"
  isolation_tier: "<<row | schema | database | deployment>>"
  rationale: "<<compliance / blast-radius / cost trade-off>>"
```

## Data-decision checklist before declaring this section complete

- [ ] DB-per-service vs shared decision made and rationale stated
- [ ] Consistency model named per read path (strong / read-your-writes / bounded / eventual)
- [ ] Reconciliation story explicit for any non-strong path
- [ ] Read-replica or CQRS choice made where read traffic is dominant
- [ ] Event log discipline (retention / partition / schema evo) stated if event-sourcing
- [ ] Multi-tenancy tier chosen per data category
- [ ] Cross-service transaction smell audited (a checkout that requires two-phase commit across services is a redecomposition signal)
