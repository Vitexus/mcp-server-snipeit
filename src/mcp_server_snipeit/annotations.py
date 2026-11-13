"""Shared tool-annotation constants (MCP-SERVER-STANDARDS §1).

All four hints are always set explicitly.  Snipe-IT tools are mostly
*multiplexed* (``manage_assets(action="list"|"create"|"delete"...)``), so a
tool that can both read and delete is classified by its most dangerous
action: :data:`MANAGE_ANNOTATIONS`.
"""

from mcp.types import ToolAnnotations

READ_ONLY_ANNOTATIONS = ToolAnnotations(
    read_only_hint=True, destructive_hint=False, idempotent_hint=True, open_world_hint=True
)
CREATE_ANNOTATIONS = ToolAnnotations(
    read_only_hint=False, destructive_hint=False, idempotent_hint=False, open_world_hint=True
)
ASSIGN_ANNOTATIONS = ToolAnnotations(
    read_only_hint=False, destructive_hint=False, idempotent_hint=True, open_world_hint=True
)
MUTATE_ANNOTATIONS = ToolAnnotations(
    read_only_hint=False, destructive_hint=True, idempotent_hint=True, open_world_hint=True
)
# Multiplexed CRUD tools: create + update + delete behind one ``action``
# argument; repeating a call is not guaranteed to leave the same state.
MANAGE_ANNOTATIONS = ToolAnnotations(
    read_only_hint=False, destructive_hint=True, idempotent_hint=False, open_world_hint=True
)
