---
name: snipeit
description: Use the Snipe-IT MCP server to look up and manage IT assets, licenses, accessories, consumables, users, locations and kits in a Snipe-IT inventory. Use when asked who has an asset, what is overdue for audit/checkin, license seat usage, or to check out/in hardware.
---

# Snipe-IT MCP server

Tools are grouped by domain and take an `action` argument
(`manage_assets`, `manage_licenses`, `manage_users`, `manage_locations`, ...).

- Start read-only: `action="list"` / `"get"`, `status_summary`, `activity_reports`.
- State-changing actions (`create`, `update`, `delete`, `checkout`, `checkin`,
  `audit`, `restore`, `upload`, `sync`) change real inventory: confirm with
  the user first. When the server runs with `SNIPEIT_READ_ONLY=true` they are
  refused.
- Look up an asset by tag/serial before acting on it; use ids from the lookup.
- `find_duplicates` / `match_records` exist only if a judgment backend is configured.
