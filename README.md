# SlackBotMcp

An MCP (Model Context Protocol) server that lets Claude interact with Slack — send messages, read channels, and read threads as a bot.

## Tools

| Tool | Description |
|------|-------------|
| `send_message` | Send a message to a channel or DM (optionally reply in a thread) |
| `read_channel` | Read recent messages from a channel or DM |
| `read_thread` | Read replies in a thread |
| `search_channels` | Search channels by name |

## Prerequisites

- Python 3.11+
- A Slack bot token (`xoxb-...`) with the following OAuth scopes:
  - `chat:write`
  - `channels:history`, `groups:history`, `im:history`, `mpim:history`
  - `channels:read`, `groups:read`
  - `conversations.replies` (`channels:history`)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Add the server to your Claude Code MCP config (usually `~/.claude/mcp.json` or your project's `.mcp.json`):

```json
{
  "mcpServers": {
    "slack-bot-direct": {
      "command": "python3",
      "args": ["/path/to/SlackBotMcp/server.py"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-token-here"
      }
    }
  }
}
```

Replace `/path/to/SlackBotMcp/server.py` with the actual path and `xoxb-your-token-here` with your Slack bot token.

## Running manually

```bash
SLACK_BOT_TOKEN=xoxb-your-token-here python3 server.py
```

## Getting a Slack Bot Token

1. Go to [api.slack.com/apps](https://api.slack.com/apps) and create a new app.
2. Under **OAuth & Permissions**, add the required bot token scopes listed above.
3. Install the app to your workspace.
4. Copy the **Bot User OAuth Token** (`xoxb-...`).
