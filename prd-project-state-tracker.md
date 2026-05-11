# Project State Tracker — PRD v0.1

> **Working title — rename before first commit.** Throughout this document the
> system is referred to as **PST**. Replace with a real name.

> **Audience:** a coding agent (e.g. Claude Code) implementing the MVP, with the
> primary user reviewing each milestone. This PRD is the single source of truth
> for scope, schema, and acceptance criteria. Where this document is ambiguous,
> stop and ask — do not guess.

---

## 1. Context

PST is a single-user system for keeping track of the state of multiple
parallel industry projects (concretely: component deliveries to vehicle
programs). Inputs arrive as **manually pasted text or dropped PDF files** —
emails, meeting notes, spec excerpts, customer correspondence. The system
extracts structured project state (milestones, commitments, decisions, status
observations, people) into a queryable **spine**, while preserving the raw
source as a **leaf** file.

PST is **not** a notes app, not a Tiago-Forte-style second brain, not a RAG
chatbot, and not a wiki. The primary value is **answering "what's coming up,
what did I commit to, what changed and when"** for several projects at once
without the user having to remember.

**Non-goals are listed explicitly in §2.2 — read them before adding features.**

---

## 2. Goals & non-goals

### 2.1 Goals (MVP)

1. **Capture in under 10 seconds.** Paste or drop → one click → done. If
   capture takes longer, the user will stop using the system.
2. **Never silently lose information.** Raw input is always preserved as a leaf
   file regardless of what extraction does.
3. **Structured state for fast queries.** "What's due in the next two weeks
   across all projects?" must be a SQL query, not a vector search.
4. **Temporality.** "When did this milestone slip, and from what?" must be
   answerable.
5. **Timeline visualization** is a primary surface, not an afterthought (see §9.2).
6. **Human-in-the-loop writes for state changes.** The agent proposes; the user
   approves. See §8 for the per-operation policy.
7. **Per-item approval with edit-then-approve.** A single paste typically
   yields multiple proposed writes; each is approved individually and can be
   edited before approval.
8. **Provider-agnostic LLM.** The system talks to an OpenAI-compatible endpoint
   through a thin abstraction (§11). No vendor lock-in in the code.
9. **Runs locally in WSL.** Localhost only, single user, no auth.

### 2.2 Non-goals (MVP)

These are deliberately out of scope. Do not add them. If they seem necessary,
flag it and ask the user first.

- Auto-ingestion from email, calendar, Teams, etc. (Manual paste only.)
- Embeddings / semantic search. (Plain SQL + grep is the MVP retrieval layer.)
- Multi-user, auth, sharing, permissions.
- Mobile UI / responsive design.
- Knowledge graph features, entity-relationship visualizations beyond timeline.
- Notifications, scheduled reminders, email digests.
- Fancy entity resolution (clustering, fuzzy match, ML). Exact-match +
  user-maintained alias lists only.
- Integration with vmodel or any other tool. PST is standalone.
- A requirements/test schema. Project state only; engineering content stays
  where it lives.
- Free-text tags. If a concept matters, it should be a typed field.
- Anything graph-database shaped.

---

## 3. Tech stack

| Layer        | Choice                                | Notes                          |
|--------------|---------------------------------------|--------------------------------|
| Runtime      | Python 3.11+                          | Always inside a `venv`. Never system Python. |
| Web framework| FastAPI                               | Built-in pydantic = aligns with schema-first approach. |
| ORM / DB     | SQLAlchemy 2.x + Alembic              | Migrations from day one.       |
| Database     | SQLite                                | One file: `~/secondbrain/db.sqlite`. |
| Templating   | Jinja2                                | Server-rendered HTML.          |
| Front-end JS | htmx + Alpine.js                      | No build step.                 |
| Timeline lib | `vis-timeline` (CDN) **or** hand-rolled SVG | Agent's choice based on what works. Justify the call in a comment. |
| PDF reading  | `pypdf` (text extraction)             | Scanned PDFs out of scope for MVP — surface a clear error. |
| LLM client   | `openai` Python SDK against any OpenAI-compatible endpoint | Configurable base URL + key via env. |
| Tests        | `pytest` + `pytest-asyncio`           | TDD non-negotiable (§12).      |
| Lint/format  | `ruff` + `ruff format`                | No suppressions without justification in a comment. |

**No frameworks beyond these without asking.** Specifically: no LangChain,
LangGraph, CrewAI, AutoGen, Pydantic AI, Agno, LlamaIndex.

---

## 4. System architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     BROWSER (localhost)                     │
│  Log │ Timeline │ Queue │ Browse │ Ask                      │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP (htmx)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                       FastAPI app                           │
│                                                             │
│  /api/ingest      ──► extraction agent ──► proposal queue   │
│  /api/proposals/* ──► approve/edit/reject ──► spine writes  │
│  /api/timeline    ──► SQL on spine                          │
│  /api/ask         ──► query router (spine vs leaves)        │
│  /api/leaves/*    ──► read leaf files                       │
│                                                             │
└──┬──────────────────────────┬───────────────────────────────┘
   │                          │
   ▼                          ▼
┌──────────────┐        ┌──────────────────────┐
│ SQLite       │        │ Filesystem           │
│ (the spine)  │        │ ~/secondbrain/       │
│ db.sqlite    │        │   leaves/*.md        │
│              │        │   attachments/*.pdf  │
└──────────────┘        └──────────────────────┘
        │                          │
        └──────────┬───────────────┘
                   ▼
              ┌─────────┐
              │   git   │  whole dir is one repo
              └─────────┘
```

### Components

- **FastAPI app** — single Python process. No background workers in MVP.
  Extraction runs synchronously in the request handler (acceptable for manual
  paste volume).
- **SQLite spine** — authoritative for project state.
- **Filesystem leaves** — authoritative for raw source content. Each leaf is
  one markdown file with YAML frontmatter + the original pasted text (or
  extracted PDF text).
- **Git repo** — entire `~/secondbrain/` is one repo. `db.sqlite` is committed.
  The user commits manually for MVP; no auto-commit yet.

### Data flow: a paste

```
1. User pastes / drops in Log view
2. Backend creates a leaf file with raw content + initial frontmatter
3. Backend calls extraction agent → JSON (§7 schema)
4. Each extracted item becomes a row in `proposals` table (status=pending)
5. User sees proposals in Queue view, approves/edits/rejects one by one
6. Approve → write row to corresponding spine table + event log entry
7. Reject → mark proposal rejected; do not re-propose for this leaf
```

---

## 5. Data model

All tables use UUID primary keys (string, `uuid4`). All timestamps are
timezone-aware UTC ISO 8601. Dates (no time) are ISO 8601 dates.

### 5.1 Spine tables

```
projects
  id              uuid pk
  name            text not null
  customer        text null
  status          enum: active | on_hold | completed | cancelled
  created_at      timestamp not null
  archived_at     timestamp null

people
  id              uuid pk
  canonical_name  text not null
  aliases         json (list of strings)
  org             text null
  role            text null
  created_at      timestamp not null

milestones
  id              uuid pk
  project_id      uuid fk -> projects
  title           text not null
  planned_date    date not null      -- IMMUTABLE after creation
  current_date    date not null      -- updated on slip; = planned_date initially
  actual_date     date null          -- set on completion
  status          enum: planned | slipped | completed | cancelled
  source_leaf_id  uuid fk -> leaves (null)
  created_at      timestamp not null

commitments
  id              uuid pk
  project_id      uuid fk -> projects
  direction       enum: i_owe | owed_to_me | between_others
  who_owes        text not null      -- free text; may match a person but not enforced
  who_to          text not null
  what            text not null
  due             date null
  status          enum: open | completed | cancelled | lapsed
  source_leaf_id  uuid fk -> leaves (null)
  created_at      timestamp not null

decisions
  id              uuid pk
  project_id      uuid fk -> projects (null — decisions can be cross-project)
  title           text not null
  rationale       text null
  decided_by      text null
  decided_at      date not null
  source_leaf_id  uuid fk -> leaves (null)
  created_at      timestamp not null

status_observations
  id              uuid pk
  project_id      uuid fk -> projects
  about           text not null      -- "what is being statused"
  observation     text not null
  confidence      enum: high | medium | low
  observed_at     timestamp not null -- when the observation was made (usually pasted_at of leaf)
  source_leaf_id  uuid fk -> leaves (null)

leaves
  id              uuid pk
  path            text not null      -- relative to ~/secondbrain/leaves/
  project_ids     json (list of uuid)
  source_type     enum: email | meeting_notes | spec_excerpt | chat | other
  pasted_at       timestamp not null
  summary         text null          -- 1-2 sentences from extraction
  raw_text_sha    text not null      -- sha256 of normalised raw text, for dedup
```

### 5.2 Event log (temporality)

```
events
  id              uuid pk
  table_name      text not null      -- 'milestones', 'commitments', etc.
  row_id          uuid not null
  op              enum: insert | update | delete
  before          json null
  after           json null
  occurred_at     timestamp not null
  actor           enum: agent | human
  source_leaf_id  uuid null
```

**Every mutation to a spine table writes an event row in the same transaction.**
No exceptions. Implement this once, in the persistence layer, not at call sites.

### 5.3 Proposals (approval queue)

```
proposals
  id              uuid pk
  leaf_id         uuid fk -> leaves
  target_table    text not null      -- which spine table this would insert into
  payload         json not null      -- the proposed row, pre-validation
  evidence        text not null      -- quoted span from leaf
  confidence      enum: high | medium | low
  status          enum: pending | approved | rejected | edited_approved
  resolution_note text null          -- optional human note on approval/rejection
  created_at      timestamp not null
  resolved_at     timestamp null
```

### 5.4 Indexes

At minimum:
- `milestones (project_id, current_date)`
- `milestones (current_date)` — for cross-project agenda queries
- `commitments (project_id, due)`
- `commitments (due, status)` — for "what's coming up"
- `leaves (pasted_at)`
- `events (table_name, row_id, occurred_at)`
- `proposals (status, created_at)`

### 5.5 Slip semantics

A "slip" is any mutation of `milestones.current_date` to a value different from
the previous `current_date`. The event log captures this automatically. The
timeline UI surfaces slips as a hover/click expansion showing the chain of
dates over time.

`planned_date` is **immutable after first commit** — enforce in the persistence
layer, not just by convention. If a milestone was wrongly planned, the user
deletes it and creates a new one; no in-place editing of `planned_date`.

---

## 6. Storage layout

```
~/secondbrain/                  <-- git repo root
├── .git/
├── db.sqlite                   <-- committed
├── alembic/                    <-- migrations
├── leaves/
│   ├── 2026-05-11T142312-a1b2.md
│   ├── 2026-05-11T154508-c3d4.md
│   └── ...
├── attachments/
│   ├── 2026-05-11T142312-a1b2/
│   │   └── original.pdf
│   └── ...
└── config.toml                 <-- LLM endpoint, base URL, etc. (no secrets)
```

Secrets (API keys) live in `.env` at the repo root and are **gitignored**.
Provide a `.env.example`.

### Leaf file format

```markdown
---
id: a1b2c3d4-...
pasted_at: 2026-05-11T14:23:12Z
source_type: email
project_ids:
  - 11111111-...
summary: |
  Customer requesting earlier A-sample delivery and proposing a new review
  cadence.
raw_text_sha: 5f2a...
---

[Original pasted text, verbatim. If from PDF, this is the extracted text
followed by a note: "<extracted from attachments/<leaf-id>/original.pdf>"]
```

The leaf file is **enough on its own** to reconstruct its row in the `leaves`
table. This is a deliberate invariant: a future reindex script can rebuild
the `leaves` table from disk. Do not put information in the table that isn't
also in the file.

---

## 7. Extraction JSON schema

The extraction agent is called once per leaf. It receives the raw text and
returns the following JSON. **Validate strictly** with pydantic; if the model
returns malformed JSON or missing required fields, retry once with the
validation error in the prompt, then surface the failure to the user.

```json
{
  "summary": "1-2 sentence what-is-this",
  "source_type": "email | meeting_notes | spec_excerpt | chat | other",
  "source_metadata": {
    "from": "string | null",
    "to": ["string"],
    "sent_at": "ISO8601 | null",
    "subject": "string | null"
  },
  "project_refs": [
    {
      "project_hint": "string",
      "confidence": "high | medium | low",
      "evidence": "quoted span from source"
    }
  ],
  "people": [
    {
      "name": "string",
      "org": "string | null",
      "role_in_context": "sender | recipient | mentioned | decision_maker",
      "confidence": "high | medium | low"
    }
  ],
  "dates": [
    {
      "date": "ISO8601",
      "kind": "deadline | milestone | meeting | mentioned | sent",
      "what": "string describing what the date refers to",
      "confidence": "high | medium | low"
    }
  ],
  "commitments": [
    {
      "direction": "i_owe | owed_to_me | between_others",
      "who_owes": "string",
      "who_to": "string",
      "what": "string",
      "due": "ISO8601 | null",
      "evidence": "quoted span",
      "confidence": "high | medium | low"
    }
  ],
  "decisions": [
    {
      "title": "string",
      "decided_by": "string | null",
      "rationale": "string | null",
      "evidence": "quoted span",
      "confidence": "high | medium | low"
    }
  ],
  "status_observations": [
    {
      "about": "string",
      "observation": "string",
      "evidence": "quoted span",
      "confidence": "high | medium | low"
    }
  ],
  "open_questions": ["string"],
  "ambiguities": ["string"]
}
```

### Extraction → proposals mapping

| Extraction field        | Becomes proposal targeting           |
|-------------------------|--------------------------------------|
| `project_refs[]`        | `projects` (only if no existing match by name or alias) |
| `people[]`              | `people` (only if no existing match by canonical_name or alias) |
| `dates[].kind=deadline` | `commitments` proposal (direction inferred from context, low confidence if unclear) |
| `dates[].kind=milestone`| `milestones` proposal                |
| `commitments[]`         | `commitments` proposal               |
| `decisions[]`           | `decisions` proposal                 |
| `status_observations[]` | `status_observations` proposal       |
| `open_questions` / `ambiguities` | Surfaced in the Queue view as flags, not as proposals |

`source_type`, `source_metadata`, and `summary` are written directly into the
leaf row and frontmatter — they do not go through the proposal queue (these
are leaf metadata, not spine state; write policy A per §8).

### Evidence is non-negotiable

Every proposal must carry a verbatim `evidence` span from the leaf. The
approval UI shows the evidence beside the proposed write. If a coding agent
ever finds itself omitting `evidence` "because the field was obvious from
context," that is a bug — refuse the temptation.

---

## 8. Write policies

Recap (already discussed and decided):

| Operation                                | Policy | Why                            |
|------------------------------------------|--------|--------------------------------|
| Create leaf file + metadata              | A      | Cheap, reversible              |
| Classify source_type, summary on leaf    | A      | Pure metadata                  |
| Tag leaf with existing project ids       | A → B  | A if confidence=high and exact name match; B otherwise |
| Resolve person to existing record        | A → B  | A if exact alias match; B otherwise |
| Create new project                       | B      | Forces deliberate creation     |
| Create new person                        | B      | Same                           |
| Create / update milestone                | B      | Dates matter                   |
| Update milestone.current_date (slip)     | B      | Drift is real                  |
| Record commitment                        | B      | Agent drafts, human ratifies   |
| Record decision                          | C      | Decisions deserve the human's own words |
| Record status_observation                | B      | Auto-proposed                  |

A = autonomous, B = proposal queue, C = suggestion only (surfaced in Queue as
"you may want to record this decision" but no auto-draft).

---

## 9. UI surfaces

Five views. No more. Top nav: **Log · Timeline · Queue · Browse · Ask**.

### 9.1 Log

```
┌─────────────────────────────────────────────────────────┐
│  Drop files here, or paste text                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │            (drop zone)                            │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  [ Paste textarea                                    ]  │
│  [                                                   ]  │
│                                                         │
│  Project hint (optional): [ free text or pick ▼ ]       │
│  Source type (optional):  [ auto ▼ ]                    │
│                                                         │
│                                          [ Log it ]     │
└─────────────────────────────────────────────────────────┘
```

Behaviour:
- Drop zone accepts PDF and plain text files. Multiple files = multiple leaves.
- "Log it" disabled if textarea empty **and** no files dropped.
- On submit: backend creates leaves, runs extraction synchronously, redirects
  to Queue with the new proposals at top.
- PDF text extraction: `pypdf`. If extraction yields < 50 chars, surface a
  clear error ("Looks like a scanned PDF — OCR not supported in MVP") and
  still create the leaf with the raw PDF preserved.
- Dedup: if `raw_text_sha` matches an existing leaf, show a warning and link to
  the existing leaf rather than creating a duplicate. Allow override.

### 9.2 Timeline

Two sub-views, switchable with a toggle: **Agenda** (short term, list) and
**Gantt** (long term, visual).

#### Agenda (default, "what's coming up")

```
┌───────────── Horizon: [ 4 weeks ▼ ]    Project: [ all ▼ ] ─┐
│                                                            │
│  THIS WEEK                                                 │
│  ─ Tue 12 May   Send DV plan          (Volvo XC60)         │
│  ─ Thu 14 May   A-sample delivery  ●  (Volvo XC60) slipped │
│  ─ Fri 15 May   Review w/ Mike        (Scania R)           │
│                                                            │
│  NEXT WEEK                                                 │
│  ─ Mon 18 May   ...                                        │
│                                                            │
│  LATER (in horizon)                                        │
│  ─ ...                                                     │
└────────────────────────────────────────────────────────────┘
```

Default horizon: 4 weeks. Configurable: 1 week, 4 weeks, 12 weeks.

Sources:
- `milestones` where `current_date ≤ horizon_end` and `status` in (planned, slipped).
- `commitments` where `due ≤ horizon_end` and `status = open`.

Sort by date, then by project name. The `●` slip marker links to slip history.

#### Gantt (long term, "where is each project")

```
┌──────── Range: [ 6 months ▼ ]    Project: [ all ▼ ] ────────┐
│                                                             │
│  Volvo XC60                                                 │
│  ├─ A-sample delivery     ●──                               │
│  ├─ DV plan to customer        ●                            │
│  └─ B-sample                ──────●                         │
│                                                             │
│  Scania R                                                   │
│  ├─ Spec review w/ Mike   ●                                 │
│  └─ ...                                                     │
│                                                             │
│       May      Jun      Jul      Aug      Sep      Oct      │
└─────────────────────────────────────────────────────────────┘
```

Default range: 6 months. Configurable: 3, 6, 12 months.

One row per milestone, grouped by project. Each milestone shows a marker at
`current_date`. If `planned_date != current_date`, show a faint marker at
`planned_date` connected by a line — this is the visual slip indicator.
Completed milestones (`actual_date` set) shown in a different colour.

Commitments are **not** shown on the gantt (would clutter it). Agenda is for
commitments.

### 9.3 Queue

List of pending proposals, grouped by leaf, most recent first.

```
┌─────────────────────────────────────────────────────────┐
│  Leaf: email from Mike, 2026-05-11 14:23                │
│  Summary: Customer requesting earlier A-sample...       │
│  [open leaf]                                            │
│                                                         │
│  ► Proposed milestone (high confidence)                 │
│    Title:        A-sample delivery to customer          │
│    Project:      Volvo XC60                             │
│    Planned date: 2026-06-15                             │
│    Evidence: "...we'd like the A-samples by mid-June..."│
│    [ approve ] [ edit ] [ reject ]                      │
│                                                         │
│  ► Proposed commitment (medium confidence)              │
│    ...                                                  │
│    [ approve ] [ edit ] [ reject ]                      │
│                                                         │
│  Ambiguity flag:                                        │
│    "Mike mentions 'the usual review cadence' — unclear  │
│     if weekly or biweekly."                             │
│    [ dismiss ]                                          │
└─────────────────────────────────────────────────────────┘
```

- One proposal = one approve/edit/reject decision.
- Edit shows a typed form (per target table) pre-filled with the proposed
  payload. User edits, hits "approve edited." Stored as `status=edited_approved`.
- Reject prompts for optional note ("not actually a commitment" etc.). Stored
  for the future auto-classifier dataset.
- Approval is **idempotent at the proposal level** but **not at the row level** —
  approving the same proposal twice is a no-op (status check); approving two
  similar proposals creates two rows.

### 9.4 Browse

CRUD reader. Tabs: **Projects · People · Milestones · Commitments · Decisions
· Leaves**. Plain table view with filter + sort. Click a row to see details
and history (from events log). Direct edit is allowed for typos but every edit
goes through the events log as `actor=human`.

### 9.5 Ask

Single input box. Backend routes:

```
def route(question):
    classification = llm_classify(question)
    if classification == "structured":
        return spine_query(question)  # NL → SQL via LLM, validated
    elif classification == "context":
        return leaf_search(question)  # grep-based for MVP
    else:  # "hybrid"
        spine_result = spine_query(question)
        leaf_result = leaf_search(question)
        return synthesize(question, spine_result, leaf_result)
```

For MVP:
- NL→SQL: use the LLM with the schema in the prompt. Run query against a
  **read-only** SQLAlchemy session. Refuse any DDL.
- Leaf search: plain substring + filename match (grep). No embeddings yet.
- Always show: the actual SQL run, the leaf paths consulted, and the answer.
  Citations are non-negotiable.

---

## 10. Approval flow — concrete spec

For each pending proposal:

1. **Show:** target table, proposed payload (typed fields), evidence span,
   confidence, link to source leaf.
2. **Actions:** approve, edit, reject.
3. **Approve:**
   - Validate payload against the spine table schema.
   - Begin transaction:
     - Insert into target table.
     - Insert into events (`actor=agent` if direct approve, `actor=human` if
       `edited_approved` — capture human edit as actor=human).
     - Update proposals.status.
   - Commit.
4. **Edit:**
   - Present typed form pre-filled with payload.
   - On submit, treat as approve with `status=edited_approved` and
     `actor=human` on the event row.
5. **Reject:**
   - Optional note.
   - Update proposals.status. No row written to spine.

If approval would create a row that exact-matches an existing row (same
project, same title, same date for milestones; same project + who_owes +
who_to + what + due for commitments), show a "this looks like a duplicate of
X" confirmation before writing. The user can override.

---

## 11. LLM client abstraction

```python
# llm/client.py
class LLMClient(Protocol):
    def extract(self, text: str, hint: str | None) -> dict: ...
    def answer(self, question: str, context: dict) -> str: ...
    def classify_question(self, question: str) -> Literal["structured", "context", "hybrid"]: ...
    def nl_to_sql(self, question: str, schema: str) -> str: ...
```

Implementation: `OpenAICompatibleClient` using the `openai` SDK with
configurable `base_url` and `api_key` from env vars:

```
LLM_BASE_URL=https://...
LLM_API_KEY=...
LLM_MODEL=...
```

Every prompt template lives in `llm/prompts/` as a `.txt` or `.jinja` file —
never inlined in Python. This is a hard rule. Prompts must be diffable and
testable independently.

Retries: one retry on JSON validation failure, with the validation error
appended to the prompt. No further retries. Surface failures to the user.

---

## 12. Testing requirements

TDD is non-negotiable. Red → green → refactor for all logic.

### 12.1 Required test layers

1. **Unit tests** — pure functions, schema validation, slip detection, event
   log generation, dedup hash, etc. Fast, no I/O.
2. **Integration tests** — full request handlers with a temp SQLite DB and a
   stubbed LLM client. Cover: ingest → propose → approve → row in spine →
   event row written.
3. **E2E tests** — `httpx` or `playwright` against the running app. At
   minimum: paste a fixture email, walk through the queue, verify the timeline
   shows the resulting milestone.
4. **Extraction golden tests** — corpus of fixture pastes under
   `tests/fixtures/extraction/`, each with a paired expected JSON. Run against
   a stubbed LLM client returning canned responses. Verify the pipeline turns
   that JSON into the expected set of proposals. **The LLM itself is not under
   test here — the deterministic glue around it is.**

### 12.2 Forbidden patterns

- "Test by running the app and checking manually." Every behaviour gets a test.
- Hitting the real LLM in tests. Use a stub or recorded responses.
- Tests that depend on each other's ordering.
- `# noqa`, `# type: ignore`, lint suppressions without a justification comment
  on the same line.

### 12.3 Coverage target

No coverage number — coverage is a poor proxy. Instead: **every public
function on the persistence layer, every API route, and every prompt
template's parsing logic has at least one test.** If something is hard to
test, that's a design signal; refactor it.

---

## 13. Build order & milestones

Build in this order. Each milestone has a green-light criterion. Do not
proceed to the next until the criterion is met and tests are green.

### M1 — Skeleton + schema (½ day)

- Repo, venv, `ruff`, `pytest` configured.
- FastAPI app boots. Health check `/healthz` returns 200.
- Alembic migrations create all spine + proposals + events tables.
- Persistence layer wraps SQLAlchemy and **automatically writes event rows on
  spine mutations**. This is the foundation — get it right.

**Green-light:** unit + integration tests pass. Inserting a milestone via the
persistence layer produces both the row and a matching event row in the same
transaction. Updating it produces a second event row with `before`/`after`
populated.

### M2 — Log + extraction + proposals (1 day)

- `/log` page (htmx).
- File drop + paste handling.
- `pypdf` text extraction.
- LLM client + prompt template for extraction.
- Extraction JSON → proposals rows.
- Leaf file written to disk with frontmatter.
- Dedup by `raw_text_sha`.

**Green-light:** paste a fixture email → leaf file appears on disk with
correct frontmatter → proposals visible in DB. Golden tests for extraction
pipeline pass.

### M3 — Queue + approval flow (1 day)

- `/queue` page.
- Approve / edit / reject actions.
- Per-target-table edit forms.
- Duplicate-detection warning.

**Green-light:** end-to-end test: paste fixture → walk queue → approve all →
verify rows in spine and events. Edit-then-approve writes the edited values
and tags the event `actor=human`.

### M4 — Timeline (1 day)

- `/timeline` page.
- Agenda sub-view (default).
- Gantt sub-view with slip indicators.
- Horizon + project filters.

**Green-light:** seed DB with 3 projects × ~10 milestones (some slipped,
some completed). Both sub-views render correctly. Slipping a milestone in
Browse updates the gantt immediately.

### M5 — Browse (½ day)

- `/browse` tabs.
- Table per entity with filter + sort.
- Detail panel with event history.
- Direct edit with event-log integration.

**Green-light:** every entity is viewable, filterable, editable. Edits show
up in the entity's history panel.

### M6 — Ask (1 day)

- `/ask` page.
- Question classifier (LLM).
- NL→SQL path with read-only session.
- Leaf grep path.
- Synthesis path.
- Always-cite output.

**Green-light:** fixture questions cover all three routing paths. Each answer
includes the SQL run and/or leaves consulted. No question writes to the DB.

### M7 — Polish & ship-to-self (½ day)

- README with WSL setup instructions.
- `.env.example`.
- A `make seed` for a tiny demo dataset.
- A `make run` that activates the venv and starts uvicorn.
- Manual smoke test: log 5 real items, walk through the flow.

**Green-light:** the user can do their actual work using PST for one week
without falling back to old habits. If they fall back, capture why and revise.

---

## 14. Explicit deferrals (YAGNI list)

These are real things the system will likely want eventually, but not now.
Listed here so the implementer doesn't pre-build hooks for them.

- Auto-ingestion from email/calendar/Teams
- Embeddings on leaves; semantic search
- Multi-user / auth
- Background jobs / scheduled extraction
- Mobile UI
- Notifications / reminders
- Export / reporting (PDF status reports, etc.)
- Project templates
- Cross-project dependency modelling
- Fuzzy entity resolution
- Auto-commit to git
- Optimistic locking / multi-tab editing

Do not add infrastructure (queues, workers, plugin systems, abstract base
classes) "in case we need it later" for any of these.

---

## 15. Open questions for the implementer

Where this PRD is ambiguous, prefer to ask rather than guess. Specific known
ambiguities the implementer should surface decisions on, *before* coding the
relevant area:

1. **Timeline library** — `vis-timeline` (CDN, JS-heavy but ready) vs.
   hand-rolled SVG (lighter, more control, more code). The PRD does not pick.
   Implementer should propose, justify, and confirm.
2. **htmx vs. Alpine.js boundaries** — both are listed. Where each is used
   should be a deliberate call, documented in a short `docs/frontend.md`.
3. **Gantt density** — when a project has 20+ milestones in the visible range,
   should rows wrap, scroll, or collapse? Propose a behaviour, ask.
4. **PDF extraction edge cases** — multi-column layouts, embedded tables.
   `pypdf` handles these poorly. Surface examples that fail and propose either
   "fail loudly" or "best-effort with warning."
5. **NL→SQL safety** — even with a read-only session, a poorly-formed query
   can be expensive or wrong. What guardrails? At minimum, statement timeout
   and result row cap. Propose specifics, ask.
6. **Confidence thresholds for write policy A→B promotion** — the PRD says
   "confidence=high and exact match" triggers A. Is that the right threshold
   in practice? Add a setting; revisit after first week of real use.

---

## 16. Style & engineering rules (binding)

- Python: always `venv`, never system. Activate in every dev command.
- TDD: red-green-refactor for all logic. No "verify manually" tests.
- DRY, YAGNI. No suppressions without a same-line justification.
- Prompts live in files, never inline.
- Every spine mutation writes an event in the same transaction.
- Every proposal carries verbatim evidence.
- No vendor lock-in: LLM access goes through the abstraction (§11).
- Never fabricate citations, sources, or rationale in any generated content.
- When unsure, surface the ambiguity. Do not guess silently.

---

*End of PRD v0.1. Revise rather than extend — this document should stay under
1000 lines.*
