# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Discord bot with conversation memory capabilities that integrates with external LLM services. The project contains two implementations:

- **discord_chat_bot.py**: Basic version using local Ollama
- **main.py**: Production version with persistent database, Typhoon API integration, and commands

## Running the Bot

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables (see .env template)
# Requires: DISCORD_TOKEN and TYPHOON_API_KEY

# Run the bot
python main.py
```

## Architecture

**Memory System**: Conversation history is stored in SQLite (`bot_memory.db`). Recent messages (configurable `CONTEXT_LIMIT`) are retrieved for each channel/server to provide context to the LLM.

**Core Components**:
- **Database Layer** (`init_db`, `store_message`, `get_recent_context`): SQLite async operations via `aiosqlite`. Handles guild/channel-scoped message history.
- **LLM Integration** (`call_typhoon`): Async calls to Typhoon API with configurable temperature and token limits
- **Discord Events** (`on_message`): Handles trigger conditions (mentions or `!ask` command) and sends responses in chunks
- **Commands**: `!ping` (health check), `!reset` (clear channel memory), `!summary` (summarize recent discussion)
- **Health Server**: HTTP endpoint on PORT (default 8080) for uptime monitoring (UptimeRobot)

**Message Flow**: User message → Store in SQLite → Fetch recent context → Call LLM → Store bot response → Split into chunks (max 1900 chars) → Send to Discord

## Key Configuration

- `CONTEXT_LIMIT = 12`: Number of recent messages used for LLM context (main.py)
- `conversation_context_limit = 10`: For discord_chat_bot.py in-memory version
- `BOT_PREFIX = "!"`: Command prefix (configurable via env)
- `SYSTEM_PROMPT`: Controls bot behavior/personality

## Environment Variables Required

- `DISCORD_TOKEN`: Discord bot token
- `TYPHOON_API_KEY`: API key for Typhoon LLM service
- `TYPHOON_MODEL`: Model to use (default: "typhoon-v2.1-12b-instruct")
- `BOT_PREFIX`: Command prefix (default: "!")
- `PORT`: Health server port (default: 8080)

## Important Notes

- **Database**: SQLite file (`bot_memory.db`) is auto-created at runtime. Persists across restarts.
- **Security**: The .env file in git history contains exposed credentials. Regenerate Discord token and API keys immediately. Use `.env.example` as template.
- **Discord Intent**: `message_content` intent required to read message content.
- **Async Design**: All database and API calls are non-blocking via `aiosqlite` and `httpx`.
- **Logging**: Errors are logged to console. Useful for debugging.
- **Cloud Deployment**: See `REPLIT_SETUP.md` for complete Replit deployment guide. Use UptimeRobot to keep bot online 24/7.
