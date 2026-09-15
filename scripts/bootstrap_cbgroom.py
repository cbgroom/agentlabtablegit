#!/usr/bin/env python3
"""Create the seven public AgentLab tables on a cbgroom MCPGit repository."""
from __future__ import annotations

import argparse
import json
import os
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

    definitions = json.loads((ROOT / "schemas/table-definitions.json").read_text())["tables"]
    service = Service(args.url, args.authorization)
    worktree = {"topic_id": args.topic}
    opened = service.call("table.worktree.open", {"repo": args.repo, "worktree": worktree})
    revision = opened["revision"]
    created = []
    for name, definition in definitions.items():
        result = service.call(
            "table.create",
            {
                "repo": args.repo,
                "worktree": worktree,
                "path": name,
                "expected_revision": revision,
                "definition": definition,
                "message": f"Initialize AgentLab public table {name}",
            },
        )
        revision = result["revision"]
        created.append(name)
    print(json.dumps({"ok": True, "repo": args.repo, "revision": revision, "created": created}))


if __name__ == "__main__":
    main()
