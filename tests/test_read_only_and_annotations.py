"""MCP-SERVER-STANDARDS section 7: annotation, naming and read-only checks.

Run in a subprocess so each case gets a fresh import of the server module
(it builds the FastMCP instance from the environment at import time).
"""

import json
import os
import subprocess
import sys

from mcp_server_snipeit.http_auth import WRITE_ACTIONS

_LIST = """
import asyncio, json
from mcp_server_snipeit.mcp_server import mcp
out = []
for t in asyncio.run(mcp.list_tools()):
    a = t.annotations
    out.append([t.name, t.title, a and [a.read_only_hint, a.destructive_hint,
                                         a.idempotent_hint, a.open_world_hint]])
print(json.dumps(out))
"""

_CALL = """
import asyncio
from mcp_server_snipeit.mcp_server import mcp
try:
    asyncio.run(mcp.call_tool("manage_assets", {"action": "delete", "asset_id": 1}))
except Exception as exc:
    print("ERR:", exc)
"""


def _run(code, read_only):
    env = dict(os.environ, SNIPEIT_URL="http://snipe.invalid", SNIPEIT_TOKEN="x")
    env.pop("SNIPEIT_READ_ONLY", None)
    if read_only:
        env["SNIPEIT_READ_ONLY"] = "true"
    return subprocess.run([sys.executable, "-W", "ignore", "-c", code], env=env,
                          capture_output=True, text=True, check=True).stdout


def test_every_tool_has_title_and_all_hints():
    tools = json.loads(_run(_LIST, False).splitlines()[-1])
    assert tools
    for name, title, hints in tools:
        assert title and title != name, name
        assert hints is not None and all(h is not None for h in hints), name
        read_only, destructive = hints[0], hints[1]
        assert not (read_only and destructive), name
        if name.startswith(("get_", "list_", "search_")):
            assert read_only, name


def test_read_only_mode_blocks_write_actions():
    assert "read-only" in _run(_CALL, True)


def test_write_actions_include_core_mutations():
    assert {"create", "update", "delete", "checkout", "checkin"} <= WRITE_ACTIONS


_CALL_OAUTH = """
import asyncio
from mcp_server_snipeit.mcp_server import mcp, _auth_provider
assert _auth_provider is not None, "OAuth provider must be active in this test"
try:
    asyncio.run(mcp.call_tool("manage_assets", {"action": "delete", "asset_id": 1}))
except Exception as exc:
    print("ERR:", exc)
"""


def test_read_only_mode_is_enforced_with_oauth():
    """Read-only must not be silently dropped when the OAuth branch is active."""
    env = dict(
        os.environ,
        SNIPEIT_URL="http://snipe.invalid",
        SNIPEIT_OAUTH_CLIENT_ID="cid",
        SNIPEIT_OAUTH_CLIENT_SECRET="secret",
        SNIPEIT_MCP_BASE_URL="https://mcp.invalid",
        MCP_TRANSPORT="http",
        SNIPEIT_READ_ONLY="true",
    )
    env.pop("SNIPEIT_TOKEN", None)
    out = subprocess.run([sys.executable, "-W", "ignore", "-c", _CALL_OAUTH], env=env,
                         capture_output=True, text=True)
    assert "read-only" in out.stdout, (out.stdout, out.stderr[-500:])
