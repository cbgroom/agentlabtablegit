#!/usr/bin/env python3
"""Minimal MCPGit service client used by local tools and GitHub Actions.

The client intentionally exposes only the generic service call. Business semantics,\+revision fences and row-version fences stay in caller scripts.
"""
from __future__ import annotations

import json
import time
import uuid

from websocket import create_connection


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


class Service:
    def __init__(self, url: str, authorization: str, timeout: int = 120):
        self.url = url
        self.authorization = authorization
        self.timeout = timeout

    def call(self, method: str, payload: dict) -> dict:
        request_id = str(uuid.uuid4())
        envelope = {
            "kind": "request",
            "message": {
                "protocol": "mcpgit.service.v2",
                "request_id": request_id,
                "invocation_id": str(uuid.uuid4()),
                "method": method,
                "deadline_unix_ms": int(time.time() * 1000) + self.timeout * 1000,
                "payload": payload,
            },
        }
        connection = create_connection(
            self.url,
            timeout=self.timeout,
            host="gateway",
            subprotocols=["mcpgit.service.ws.v1"],
            header={"Authorization": self.authorization},
        )
        try:
            connection.send_binary(canonical(envelope))
            result = json.loads(connection.recv())
        finally:
            connection.close()
        message = result["message"]
        if message["request_id"] != request_id:
            raise RuntimeError("MCPGit response request_id mismatch")
        if message["outcome"] != "success":
            raise RuntimeError(f"{method} failed: {message.get('error', 'unknown service error')}")
        return message["payload"]
