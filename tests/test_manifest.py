"""MCP-SERVER-STANDARDS section 7: server.json / README consistency."""

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "debian" / "server.json").read_text())
PKG = MANIFEST["packages"][0]
EXT = MANIFEST["_meta"]["io.modelcontextprotocol.registry/publisher-provided"]["cz.vitexsoftware.mcp"]

# uuid is the identity of the server kind: never change it.
FIXED_UUID = "b3083c33-c095-4fb4-87c1-f91cdac11968"


def test_uuid_is_stable():
    assert EXT["uuid"] == FIXED_UUID


def test_every_manifest_env_var_is_in_readme():
    readme = (ROOT / "README.md").read_text()
    for var in PKG["environmentVariables"]:
        assert var["name"] in readme, var["name"]


def test_every_env_var_read_by_code_is_in_manifest():
    declared = {v["name"] for v in PKG["environmentVariables"]}
    code = "\n".join(p.read_text() for p in (ROOT / "src").rglob("*.py"))
    used = set(re.findall(r'"((?:SNIPEIT|JUDGMENT|MCP)_[A-Z_]+)"', code))
    used -= {"SNIPEIT_IDENTITY_", "MCP_TOKEN_"}
    assert used <= declared, used - declared
