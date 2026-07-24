# Compass Semantic Object Model — Architectural Contract

## Principle: "One semantic object, many representations."

Every Compass workspace is a **different view of the same underlying meaning structure — not a copy of it.**

A learner's ideas exist once, as canonical semantic objects. The Meaning Workspace,
Writing Plan, Draft Workspace, Revision Workspace, Teacher tools, and analytics are all
*representations* (views/overlays) over those same objects. No workspace ever duplicates,
forks, or re-creates a semantic object.

---

## Canonical store

The **Meaning Workspace** holds the canonical semantic objects for a session:

- `meaning_maps.objects[]`     — meaning objects (the ideas themselves)
- `meaning_maps.groups[]`      — spatial clusters
- `meaning_maps.connections[]` — relationships between objects
- `meaning_maps.events[]`      — append-only trace of every learner action

Each is addressed by a stable `id`. Relationships are stored **by reference**:
- `connection.from_id` / `connection.to_id` → object ids
- `object.group_id`                          → group id
- `event.data.id`                            → the object/group/connection acted on
- `event.session_id`                         → the owning session

The map has its own `id` and `session_id`. All map ids default to `uuid.uuid4()` server-side.

---

## ID rules

1. **Globally unique.** New object/group/connection ids are `prefix + crypto.randomUUID()`
   (`obj_…`, `grp_…`, `edge_…`). The prefix is for human legibility only; the UUID body
   guarantees global uniqueness across sessions, maps, and workspaces.
2. **Immutable for life.** An id, once assigned, is NEVER regenerated or migrated. Objects
   are updated in place; edits/moves/reloads preserve the id. Deletion removes the object; it
   does not recycle the id.
3. **Backward compatible.** Legacy ids created before the UUID change (older
   `obj_<base36>_<counter>` form) are preserved on load and never rewritten. They remain
   valid, stable references. Only *newly created* objects receive UUID-based ids.
4. **Server trusts client ids.** `PUT /api/meaning-maps/{id}` overwrites the arrays with the
   client payload; the client always round-trips the same ids, so identity survives autosave.

---

## Contract for downstream / future workspaces

Future workspaces (Meaning Map, Writing Plan, Draft, Revision, Teacher tools, analytics)
**MUST**:

- Reference semantic objects, groups, and connections by their immutable `id`.
- Store only **workspace-specific metadata** as an overlay keyed by that id — e.g.
  `{ meaning_object_id, x, y, formatting, paragraph_assignment, visibility, comments, order }`.

Future workspaces **MUST NOT**:

- Duplicate or embed a semantic object's content (text/notes) into their own store.
- Fork an object (create a second id representing the same idea).
- Rewrite or migrate existing ids.

### Example (illustrative — not yet built)

```jsonc
// Canonical (Meaning Workspace):
{ "id": "obj_9f1c…", "text": "Homework harms rest", "notes": "…", "group_id": "grp_2a…" }

// Writing Plan overlay — a VIEW, references by id, adds plan-specific metadata only:
{ "meaning_object_id": "obj_9f1c…", "paragraph": 2, "order": 1, "role": "topic_claim" }

// Draft overlay — another VIEW of the same object:
{ "meaning_object_id": "obj_9f1c…", "included": true, "char_range": [340, 512] }
```

Editing the idea's text happens in exactly one place (the canonical object); every view
reflects it automatically because they all point at the same id.

---

_Last updated: 2026-06 — introduced with Meaning Workspace V1 UUID hardening._
