#!/usr/bin/env python3
"""Insert the public calibrated sample using one revision-fenced transaction."""
from __future__ import annotations

import argparse
import json
import os
import uuid
from pathlib import Path

from clients.tablegit_service import Service

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=os.getenv("CBGROOM_WS_URL"))
    parser.add_argument("--authorization", default=os.getenv("CBGROOM_AUTHORIZATION"))
    parser.add_argument("--repo", default=os.getenv("CBGROOM_REPO", "agentlabtablegit"))
    parser.add_argument("--topic", default=os.getenv("CBGROOM_TOPIC_ID", "main"))
    args = parser.parse_args()
    if not args.url or not args.authorization:
        parser.error("cbgroom URL and authorization are required")

    package = json.loads((ROOT / "examples/first-calibrated-sample.json").read_text())
    service = Service(args.url, args.authorization)
    worktree = {"topic_id": args.topic}
    revision = service.call("table.worktree.open", {"repo": args.repo, "worktree": worktree})["revision"]
    transaction_id = str(uuid.uuid4())
    tables = []
    row_count = 0
    for path, rows in package["rows"].items():
        if not rows:
            continue
        operations = []
        for row in rows:
            operations.append({
                "op": "insert",
                "operation_id": str(uuid.uuid4()),
                "key": row["id"],
                "row": row,
            })
            row_count += 1
        tables.append({"path": path, "operations": operations})
    result = service.call(
        "table.transact_many",
        {
            "repo": args.repo,
            "worktree": worktree,
            "expected_revision": revision,
            "transaction_id": transaction_id,
            "idempotency_key": transaction_id,
            "actor": None,
            "tables": tables,
            "message": "Import first public AgentLab calibrated difficulty sample",
        },
    )
    if not result.get("applied") or result.get("conflicts"):
        raise RuntimeError("sample transaction did not apply; re-read and reconcile")
    print(json.dumps({"ok": True, "repo": args.repo, "revision": result["revision"], "rows": row_count}))


if __name__ == "__main__":
    main()
