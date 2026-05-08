# Quick Start Guide

## For Impatient Developers ⚡

**Goal**: Get Discord bot running 24/7 on Oracle Cloud in ~1 hour

## Read These in Order

1. **This file** (5 mins) - Overview
2. **ORACLE_CLOUD_SETUP.md** (45 mins) - Detailed deployment steps
3. **LOCAL_TEST.md** (optional, 10 mins) - Test locally first

## 30-Second Summary

```
You have:
  ✅ PostgreSQL code (replaces SQLite)
  ✅ Environment templates
  ✅ Full setup guides

To deploy:
  1. Create Oracle Cloud account (free tier)
  2. Create Ubuntu VM + PostgreSQL database
  3. SSH to VM, clone repo, configure .env
  4. Run bot as systemd service
  5. Monitor with logs
```

## What You'll Need

- **Discord Bot Token** - From https://discord.com/developers
- **Typhoon API Key** - From your Typhoon account
- **Oracle Account** - Free tier (no credit card needed)
- **~1 hour** - For complete setup

## Files Overview

| File | Purpose |
|------|---------|
| `main.py` | Bot code (PostgreSQL version) |
| `requirements.txt` | Python dependencies |
| `.env.example` | Configuration template |
| `ORACLE_CLOUD_SETUP.md` | 👈 **Main guide** |
| `LOCAL_TEST.md` | Test locally first |
| `discord-bot.service` | Auto-run service |
| `.gitignore` | Don't commit secrets |

## The 9 Steps (Simplified)

```
Step 1: Create Oracle account + Ubuntu VM
Step 2: Create PostgreSQL database
Step 3: SSH into VM
Step 4: Clone your repository
Step 5: Create .env with your tokens
Step 6: Test: python3 main.py
Step 7: Copy discord-bot.service to /etc/systemd/system/
Step 8: Start service: systemctl start discord-bot
Step 9: Monitor: tail -f bot.log
```

**Total time**: 30-60 minutes

## What's Different from Original?

- ✅ SQLite → PostgreSQL (persistent, cloud-ready)
- ✅ `aiosqlite` → `asyncpg` (better async support)
- ✅ Added logging and error handling
- ✅ Connection pooling for efficiency
- ✅ Systemd service for 24/7 operation

## Costs

**Oracle Cloud Always Free:**
- 4 vCPU, 24GB RAM VM = **FREE**
- 20GB PostgreSQL database = **FREE**
- Forever (not expiring)

Cost: **$0/month** ✅

## Common Commands Once Deployed

```bash
# Check if bot is running
sudo systemctl status discord-bot

# View logs
tail -f bot.log

# Restart bot
sudo systemctl restart discord-bot

# Stop bot
sudo systemctl stop discord-bot

# Check database
psql -U botuser -d bot_memory
SELECT COUNT(*) FROM messages;
```

## Discord Commands Your Bot Now Has

```
@BotName hello         → Bot responds with AI
!ask what time is it   → AI-powered response
!ping                  → Bot responds "pong"
!reset                 → Clear channel history
!summary               → Summarize recent chat
```

## Next: Read ORACLE_CLOUD_SETUP.md

That's your main guide. Follow it step-by-step and you'll have a 24/7 bot! 🚀

## Troubleshooting Quick Links

| Problem | Solution |
|---------|----------|
| Bot won't start | `tail -100 bot.log` (check errors) |
| Database error | `psql -U botuser -d bot_memory` |
| Missing tokens | Edit `.env` file |
| Bot crashes | Check systemd status or logs |

---

**Ready? → Open ORACLE_CLOUD_SETUP.md**
