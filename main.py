import os
import asyncio
import logging
from typing import List, Dict

import discord
from discord.ext import commands
from dotenv import load_dotenv
import httpx
from aiohttp import web
import asyncpg

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TYPHOON_API_KEY = os.getenv("TYPHOON_API_KEY")
TYPHOON_MODEL = os.getenv("TYPHOON_MODEL", "typhoon-v2.5-30b-a3b-instruct")
TYPHOON_BASE_URL = os.getenv("TYPHOON_BASE_URL", "https://api.opentyphoon.ai/v1")
BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
PORT = int(os.getenv("PORT", "8080"))
DATABASE_URL = os.getenv("DATABASE_URL")

CONTEXT_LIMIT = 12

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are Eduvice internal team assistant.
Your job is to help the team understand progress, blockers, decisions, and next actions.
Answer clearly and concisely.
If you are not sure, say what information is missing.
Do not hallucinate company status.
"""

if not DISCORD_TOKEN:
    raise ValueError("Missing DISCORD_TOKEN")
if not TYPHOON_API_KEY:
    raise ValueError("Missing TYPHOON_API_KEY")
if not DATABASE_URL:
    raise ValueError("Missing DATABASE_URL")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

db_pool: asyncpg.Pool = None


# ---------------- Database ----------------

async def init_db():
    global db_pool
    db_pool = await asyncpg.create_pool(DATABASE_URL)
    async with db_pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                guild_id TEXT,
                channel_id TEXT,
                author_id TEXT,
                role TEXT,
                content TEXT,
                created_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
    logger.info("Database initialized successfully")


async def store_message(guild_id: str, channel_id: str, author_id: str, role: str, content: str):
    try:
        async with db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO messages (guild_id, channel_id, author_id, role, content)
                VALUES ($1, $2, $3, $4, $5)
            """, guild_id, channel_id, author_id, role, content)
    except Exception as e:
        logger.error(f"Failed to store message: {e}")


async def get_recent_context(guild_id: str, channel_id: str) -> List[Dict[str, str]]:
    try:
        async with db_pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT role, content FROM (
                    SELECT role, content, id
                    FROM messages
                    WHERE guild_id = $1 AND channel_id = $2
                    ORDER BY id DESC
                    LIMIT $3
                ) sub
                ORDER BY id ASC
            """, guild_id, channel_id, CONTEXT_LIMIT)
        return [{"role": row["role"], "content": row["content"]} for row in rows]
    except Exception as e:
        logger.error(f"Failed to get context: {e}")
        return []


# ---------------- Typhoon API ----------------

async def call_typhoon(messages: List[Dict[str, str]]) -> str:
    url = f"{TYPHOON_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {TYPHOON_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": TYPHOON_MODEL,
        "messages": messages,
        "temperature": 0.4,
        "max_tokens": 900,
        "top_p": 0.95,
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    return data["choices"][0]["message"]["content"]


def chunk_text(text: str, max_len: int = 1900) -> List[str]:
    return [text[i:i + max_len] for i in range(0, len(text), max_len)]


# ---------------- Discord Events ----------------

@bot.event
async def on_ready():
    logger.info(f"{bot.user} is online.")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    await bot.process_commands(message)

    should_reply = bool(bot.user and bot.user.mentioned_in(message))
    if message.content.startswith(BOT_PREFIX + "ask"):
        should_reply = True

    if not should_reply:
        return

    guild_id = str(message.guild.id) if message.guild else "dm"
    channel_id = str(message.channel.id)
    author_id = str(message.author.id)
    clean_content = message.content.replace(f"<@{bot.user.id}>", "").strip()

    await store_message(guild_id, channel_id, author_id, "user", clean_content)
    context = await get_recent_context(guild_id, channel_id)
    llm_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + context

    async with message.channel.typing():
        try:
            answer = await call_typhoon(llm_messages)
        except Exception as e:
            logger.error(f"Typhoon API error: {e}")
            answer = f"Error while calling Typhoon API: `{type(e).__name__}: {e}`"

    await store_message(guild_id, channel_id, "bot", "assistant", answer)

    for chunk in chunk_text(answer):
        await message.channel.send(chunk)


# ---------------- Commands ----------------

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("pong")


@bot.command(name="reset")
async def reset_memory(ctx):
    guild_id = str(ctx.guild.id) if ctx.guild else "dm"
    channel_id = str(ctx.channel.id)
    try:
        async with db_pool.acquire() as conn:
            await conn.execute("""
                DELETE FROM messages WHERE guild_id = $1 AND channel_id = $2
            """, guild_id, channel_id)
        await ctx.send("Memory for this channel has been reset.")
    except Exception as e:
        logger.error(f"Failed to reset memory: {e}")
        await ctx.send(f"Error resetting memory: {e}")


@bot.command(name="summary")
async def summarize_channel(ctx):
    guild_id = str(ctx.guild.id) if ctx.guild else "dm"
    channel_id = str(ctx.channel.id)
    context = await get_recent_context(guild_id, channel_id)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"""Summarize the recent team discussion below.

Return:
1. Current progress
2. Blockers
3. Decisions
4. Next actions
5. Unclear points

Conversation:
{context}"""
        }
    ]
    async with ctx.typing():
        answer = await call_typhoon(messages)
    for chunk in chunk_text(answer):
        await ctx.send(chunk)


# ---------------- Health Server ----------------

async def health(request):
    return web.json_response({"status": "ok", "bot": str(bot.user) if bot.user else "starting"})


async def start_health_server():
    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_get("/health", health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(f"Health server running on port {PORT}")


async def main():
    await start_health_server()
    await init_db()
    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
