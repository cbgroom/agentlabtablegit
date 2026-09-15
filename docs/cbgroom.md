# cbgroom hosting contract

The target runtime authority is the public cbgroom TableGit instance.

## Roles

- **cbgroom TableGit repository `agentlabtablegit`**: mutable row/history authority.
- **GitHub `yxsicd/agentlabtablegit`**: public schema/client/migration/export mirror.
- **Local AgentLab / GitHub Actions**: producers. They do not edit repository storage
  directly; they submit revision-fenced TableGit transactions.

## Transport

The currently qualified AgentLab client uses the MCPGit service protocol over a
WebSocket transport with subprotocol `mcpgit.service.ws.v1`. The logical operations
are `table.worktree.open`, `table.create`, `table.query`, and
`table.transact_many`.

Do not invent an HTTP write route. If cbgroom exposes an HTTP transport, record the
exact discovered endpoint and request contract here before enabling CI writes.
MCP and HTTP transports must drive the same TableGit transaction semantics.

## CI authorization

Use a repository-scoped cbgroom credential provided as a GitHub Actions secret.
Never commit it or print it. CI writes must carry:

1. exact repository id `agentlabtablegit`;
2. current expected repository revision;
3. a unique transaction/idempotency id;
4. expected row version for update/delete;
5. evidence digests/URIs, not private raw payloads.

On a revision or row-version conflict, re-read the current row and reconcile. Never
blindly retry a stale mutation.

## Bootstrap status

The public Git repository can be prepared independently. Runtime bootstrap is only
complete after cbgroom is reachable, the repository exists there, all seven table
definitions are initialized, and a read-after-write/read-at-revision probe passes.
