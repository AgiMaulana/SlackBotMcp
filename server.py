"""
Slack Bot MCP Server
Posts messages as the bot itself (Alley) using the xoxb- token directly.
"""
import json
import os
import urllib.parse
import urllib.request
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("slack-bot")

BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")


def _slack_api(method: str, payload: dict[str, Any]) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"https://slack.com/api/{method}",
        data=data,
        headers={
            "Authorization": f"Bearer {BOT_TOKEN}",
            "Content-Type": "application/json; charset=utf-8",
        },
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    if not result.get("ok"):
        raise RuntimeError(f"Slack API error ({method}): {result.get('error')}")
    return result


def _slack_get(method: str, params: dict[str, Any]) -> dict[str, Any]:
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    req = urllib.request.Request(
        f"https://slack.com/api/{method}?{query}",
        headers={"Authorization": f"Bearer {BOT_TOKEN}"},
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    if not result.get("ok"):
        raise RuntimeError(f"Slack API error ({method}): {result.get('error')}")
    return result


@mcp.tool()
def send_message(
    channel_id: str,
    message: str,
    thread_ts: str | None = None,
    reply_broadcast: bool = False,
) -> str:
    """Send a message to a Slack channel or user DM as the bot (Alley).
    Use channel_id for channels (C...) or user_id (U...) for DMs.
    Set thread_ts to reply inside a thread.
    """
    payload: dict[str, Any] = {"channel": channel_id, "text": message}
    if thread_ts:
        payload["thread_ts"] = thread_ts
    if reply_broadcast:
        payload["reply_broadcast"] = True

    result = _slack_api("chat.postMessage", payload)
    ts = result["ts"]
    channel = result["channel"]
    link = f"https://slack.com/archives/{channel}/p{ts.replace('.', '')}"
    return json.dumps({"message_link": link, "ts": ts, "channel": channel})


@mcp.tool()
def read_channel(
    channel_id: str,
    limit: int = 20,
    oldest: str | None = None,
    latest: str | None = None,
) -> str:
    """Read messages from a Slack channel (newest first).
    Use a user_id as channel_id to read DM history.
    """
    params: dict[str, Any] = {"channel": channel_id, "limit": limit}
    if oldest:
        params["oldest"] = oldest
    if latest:
        params["latest"] = latest

    result = _slack_get("conversations.history", params)
    messages = result.get("messages", [])
    lines = []
    for m in messages:
        ts = m.get("ts", "")
        user = m.get("username") or m.get("bot_id") or m.get("user", "unknown")
        text = m.get("text", "")
        lines.append(f"[{ts}] {user}: {text}")
    return "\n".join(lines) if lines else "(no messages)"


@mcp.tool()
def read_thread(channel_id: str, thread_ts: str, limit: int = 20) -> str:
    """Read replies in a Slack thread."""
    result = _slack_get(
        "conversations.replies",
        {"channel": channel_id, "ts": thread_ts, "limit": limit},
    )
    messages = result.get("messages", [])
    lines = []
    for m in messages:
        ts = m.get("ts", "")
        user = m.get("username") or m.get("bot_id") or m.get("user", "unknown")
        text = m.get("text", "")
        lines.append(f"[{ts}] {user}: {text}")
    return "\n".join(lines) if lines else "(no messages)"


@mcp.tool()
def search_channels(query: str, limit: int = 10) -> str:
    """Search for Slack channels by name."""
    result = _slack_get("conversations.list", {"limit": 200, "types": "public_channel,private_channel"})
    channels = result.get("channels", [])
    matches = [c for c in channels if query.lower() in c.get("name", "").lower()][:limit]
    lines = [f"{c['id']} #{c['name']}" for c in matches]
    return "\n".join(lines) if lines else "(no matches)"


if __name__ == "__main__":
    mcp.run(transport="stdio")
