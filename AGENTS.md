# AgentLab TableGit maintainer contract

This repository is public. Never add credentials, private task/Works content,
provider-hidden state, live tokens, private source, or non-public evidence.

## Authority

- `schemas/table-definitions.json` defines the public logical tables.
- The configured cbgroom TableGit repository is mutable data authority.
- GitHub stores schema, code, examples, migrations, and deterministic exports only.
- Every write must use revision fencing; updates/deletes must also use row-version
  fencing. Never use last-writer-wins or blind retry.

## Measurement

Preserve behavior, build, scope, lifecycle, timing, model/tool cost, and
infrastructure status as independent observations. Do not collapse them into one
pass bit. Aggregate scores are views, never replacements for raw verdict fields.

## Schema evolution

Prefer additive optional fields. A breaking schema change requires a versioned
migration and a new schema revision. Stable IDs must not be regenerated merely
because a description changes.
