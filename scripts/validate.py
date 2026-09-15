#!/usr/bin/env python3
"""Validate public definitions and example referential integrity without a server."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    definitions = json.loads((ROOT / "schemas/table-definitions.json").read_text())
    sample = json.loads((ROOT / "examples/first-calibrated-sample.json").read_text())
    tables = definitions["tables"]
    assert definitions["schema"] == "agentlab.tablegit.definitions.v1"
    assert set(sample["rows"]) == set(tables)
    ids: dict[str, set[str]] = {}
    for name, definition in tables.items():
        rows = sample["rows"][name]
        required = set(definition["required_fields"])
        ids[name] = set()
        for row in rows:
            missing = required - row.keys()
            assert not missing, (name, row.get("id"), sorted(missing))
            assert row["id"] not in ids[name], (name, row["id"])
            ids[name].add(row["id"])
    for row in sample["rows"]["interventions"]:
        assert row["difficultyId"] in ids["difficulty_points"]
        assert row["checkpointId"] in ids["checkpoints"]
    for row in sample["rows"]["crossings"]:
        assert row["interventionId"] in ids["interventions"]
    for row in sample["rows"]["decisions"]:
        assert row["interventionId"] in ids["interventions"]
    print(json.dumps({"ok": True, "tables": len(tables), "sampleRows": sum(len(v) for v in sample["rows"].values())}))


if __name__ == "__main__":
    main()
