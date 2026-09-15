# AgentLab TableGit

Public structured research authority for AgentLab Code Agent difficulty evaluation.

This repository defines the durable TableGit model used to store reusable facts from
AgentLab experiments without coupling the data model to one Harness, Agent, model,
language, or CI provider.

The causal unit is:

`Task -> Difficulty Point -> Checkpoint -> Intervention -> Crossing -> Decision`

Capability profiles are derived from Crossing rows; raw evidence remains in external
artifacts and is referenced by immutable URI/digest rows.

## Tables

| Table | Purpose |
| --- | --- |
| `difficulty_points` | Evidence-linked failure mechanisms and maturity |
| `checkpoints` | Exact admitted state used for controlled forks |
| `interventions` | One-variable controlled experiments |
| `crossings` | Per-arm behavior/build/scope/cost outcomes |
| `decisions` | Agent adopt/reject/repeat/next-experiment decisions |
| `capability_profiles` | Derived capability matrix by difficulty mechanism |
| `evidence_refs` | Immutable references to public/raw evidence |

`schemas/table-definitions.json` is the public schema authority. TableGit history is
the data authority once the repository is bootstrapped on the serving instance.

## Hosting

The intended serving authority is the public `cbgroom` TableGit instance. Local tools
and GitHub Actions must write through cbgroom MCP/TableGit service operations (or an
explicitly documented HTTP transport exposed by that instance), using revision and
row-version fences. GitHub is the public source/mirror for schema, clients, examples,
and deterministic exports; it is not a second mutable database authority.

See `docs/cbgroom.md` and `examples/first-calibrated-sample.json`.

## Safety / reproducibility rules

- No credentials, private Works data, provider secrets, or hidden model state.
- Infrastructure failures are not Agent failures.
- Unknown gates remain unknown; never impute pass.
- Updates require the current repository revision and row version.
- Raw evidence is content-addressed and referenced rather than copied into rows.
- A formal checkpoint and a reproduced difficulty are separate facts.

Licensed under Apache-2.0.
