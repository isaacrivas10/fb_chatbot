# ADR-0006: ORM Contract — SQLAlchemy Underneath, Narrow Entity Surface Above

## Status

Accepted.

## Context

Plugins persist entities. The kernel needs an ORM. The question is
which ORM, and how much of it plugins see. This decision shapes plugin
ergonomics, plugin portability, kernel maintenance burden, and the
upper bound on what a malicious or careless plugin can do.

The two-axis trade-off:

- **What ORM does the kernel use internally?** Build something custom,
  use SQLAlchemy, use SQLModel, use Tortoise, use raw SQL with a thin
  wrapper. Each affects what the kernel can offer plugin authors and
  what databases are reachable.
- **How much of that ORM do plugins see?** None (plugins use a kernel-
  defined entity API; ORM is an implementation detail), all (plugins
  use the ORM directly), or some carefully chosen subset.

Two prior-art shapes inform this:

- **Odoo.** Plugins use Odoo's ORM directly. The ORM exposes nearly
  everything (raw SQL through `self.env.cr.execute`, session control,
  model registry manipulation, etc.). This gives plugin authors
  enormous power and produces enormous upgrade pain — every plugin
  reaches into ORM internals somewhere, so any internal change can
  break dozens of plugins. Odoo upgrades are famously expensive.
- **Django.** Plugins ("apps") use Django's ORM directly, but the ORM
  itself is more disciplined than Odoo's. Plugins still couple to ORM
  internals over time, and database-level operations (raw SQL, custom
  expressions) are routine plugin author tools. Manageable, but not
  what we want for a system designed for plugin composition first.

Hearth's vision (ADR-0001) and plugin model (ADR-0003) are demanding:
plugins compose, the kernel is small, and operators are technical but
should not need to be ORM experts to write a plugin. The owner's
explicit guidance was: choose A (kernel exposes an ORM-shaped entity
API to plugins) over B (kernel is storage-agnostic, plugins bring
their own persistence). The cleverness is in *what* we expose, not
*whether* we expose something.

## Decision

The kernel uses **SQLAlchemy 2.x (async-capable)** internally and
exposes a **narrow, opinionated `Entity`-shaped surface** through the
SDK. Plugins do not see SQLAlchemy.

### Internal: SQLAlchemy

The kernel uses SQLAlchemy under the hood for every persistence
operation. Reasons:

- Mature, widely understood, large operator pool.
- Async support is real (SQLAlchemy 2.x with `asyncio` driver).
- Cross-database support that actually works: PostgreSQL is the
  primary target, SQLite is the dev/test target, others are reachable
  if needed.
- The migration story (Alembic) is the de-facto standard.
- The flexibility we need at the kernel level (raw SQL for migrations,
  manual session control for the outbox dispatcher, complex relationship
  management for cross-plugin references) is all available.

### External: the `Entity` surface

Plugins import `Entity` and a small set of field types from the SDK.
That is the contract. Plugins **never**:

- import from `sqlalchemy` directly,
- access the SQLAlchemy `Session` or `engine`,
- execute raw SQL,
- declare relationships using SQLAlchemy `relationship()` / `mapped_column()`,
- use SQLAlchemy events, query API, or expression language.

Plugins **do**:

- subclass `Entity`,
- declare fields using kernel field types: `fields.Text`, `fields.Integer`,
  `fields.Boolean`, `fields.Timestamp`, `fields.Enum`, `fields.Money`,
  `fields.Json`, etc.,
- declare references to other entities using `References`,
- override invariant-protecting methods (e.g., `__post_init__`,
  `validate`, custom narrow methods that protect entity state),
- use the `UnitOfWork` interface (passed into actions) to load and
  save entities — no direct session access.

A plugin's entity declaration looks roughly like:

```python
from hearth import Entity, fields, References, Money

class Order(Entity):
    customer = References("commerce.Customer")
    placed_at = fields.Timestamp(auto_now_add=True)
    total = fields.Money()
    status = fields.Enum(OrderStatus, default=OrderStatus.DRAFT)

    class Meta:
        plugin = "commerce"

    def add_line(self, product, qty):
        if self.status is not OrderStatus.DRAFT:
            raise InvariantError("cannot add lines to a non-draft order")
        ...
```

That's the entire surface a plugin author needs to know.

### Cross-plugin references

References between entities owned by different plugins are **object-
form by default** and **string-form as escape hatch only**.

- Object-form: `References(Order)` — the `Order` class is imported
  from the owning plugin. Typing works, IDE help works, missing-plugin
  errors fire at import time. This is the default and what plugin
  authors use 95% of the time.
- String-form: `References("commerce.Order")` — used only for
  forward references within a single module (e.g., self-references,
  circular references between two entities in the same plugin). Both
  Django and SQLAlchemy allow this dual form for the same reason; it's
  cheap.

Cross-plugin references imply hard plugin dependencies: a plugin that
references entities from another plugin declares that other plugin as
a dependency. The kernel refuses to start if dependencies are missing.

### Migrations

Plugins do not write migration files by hand. Each plugin's entity
declarations are the source of truth; the kernel computes a versioned
schema from them. When a plugin's schema changes (a field added, a
field removed, a relationship changed), the kernel generates a
migration and applies it on startup or via an explicit `migrate`
command.

The exact mechanism (Alembic-backed autogenerate vs. a kernel-native
schema journal) is an open decision (see CLAUDE.md). What is settled:

- Plugins declare entities; they do not declare migrations.
- Migration generation, ordering, and application is a kernel
  responsibility.
- Plugin-to-plugin schema dependencies (e.g., `whatsapp` referencing
  `commerce.Order`) follow the plugin dependency graph.

### Read paths

Plugins do not call `Session.query(Entity).filter(...)`. Read access
goes through:

- `UnitOfWork.get(EntityClass, id)` for direct loads inside an action.
- A small finder API (`UnitOfWork.find(EntityClass, **filters)`,
  exact shape TBD) for narrow lookups inside actions.
- **Views** (ADR-0005) for everything else, including reporting,
  presentation, and complex queries. Views are where SQL ergonomics
  live; entities are not the right tool for general querying.

This is intentional. Letting plugins query entities arbitrarily ends
in the same place Odoo did — every plugin reaches into the ORM, and
upgrades break everything. Views give plugin authors a clean read
surface that the kernel can optimize independently (caches, projections,
read replicas) without breaking plugins.

## Consequences

- **Plugin authors learn one small surface and can write a plugin
  without knowing SQLAlchemy exists.** This is a real benefit; not
  every operator who writes a plugin will be a senior database
  engineer.
- **The kernel can change its persistence layer without breaking
  plugins.** If we ever need to swap SQLAlchemy for something else
  (or upgrade SQLAlchemy major versions), the kernel internals change;
  plugin code does not.
- **Plugins cannot accidentally tank performance with bad queries
  buried in entity methods.** General queries go through views, which
  are explicit and reviewable.
- **Plugin authors will occasionally hit a limitation.** Some
  legitimate need will not be expressible through the SDK on day one.
  The right response is to extend the SDK with the smallest addition
  that covers the need, not to add an escape hatch. The walled garden
  is the project's value, not its inconvenience.
- **The SDK has substantial work to do.** Field types, references,
  validation hooks, lifecycle hooks, and the UnitOfWork API are all
  SDK-shaped responsibilities. This is where the project's design
  energy concentrates early.
- **Cross-plugin references couple plugins.** That is intentional:
  hard dependencies, declared explicitly, caught at startup. Plugins
  that genuinely need to be independent of each other communicate by
  events, not by entity references.

## Alternatives considered

- **Plugins use SQLAlchemy directly (Django/Odoo path).** Rejected for
  the upgrade-pain and walled-garden reasons above.
- **Storage-agnostic kernel; plugins choose persistence.** Rejected
  per the owner's guidance and per ADR-0001's principle that plugin
  composition is the project's value. If plugins persist things in
  unrelated stores, references and joins across plugins become
  impossible and the system stops being a kernel.
- **SQLModel as the SDK surface (Pydantic-on-SQLAlchemy).** Considered.
  Rejected because SQLModel is a thin layer that exposes most of
  SQLAlchemy through Pydantic models — it does not constrain the
  surface enough. We want a stricter contract.
- **Custom ORM written from scratch.** Rejected because reinventing
  SQLAlchemy is a multi-year project on its own and the failure modes
  are not interesting. Use a battle-tested ORM internally; constrain
  what plugins see.
- **Soft string-form cross-plugin references everywhere (no hard
  imports).** Rejected per ADR-0003: hard dependencies and typed
  references are the operator's stated preference and the better
  default. String form remains for forward references only.
- **Allow plugins limited query access (`.filter`/`.exclude` chain
  on entities).** Considered. Tentatively rejected: easy to slip
  toward Django-style query methods that couple plugins to ORM
  internals. Views are the cleaner answer. If a real need emerges,
  revisit with an ADR.

## References

- ADR-0001 — vision (kernel + plugins; small kernel).
- ADR-0003 — plugin model (hard dependencies, registration).
- ADR-0004 — SDK-first design (Entity is an SDK surface).
- ADR-0005 — primitives (Entity, Reference, View).
- ADR-0007 — transactional contract (UnitOfWork, outbox).
