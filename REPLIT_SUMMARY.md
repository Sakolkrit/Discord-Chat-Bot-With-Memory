# Replit Deployment Summary

Switched from Oracle Cloud to Replit. Here's what changed and what you need to do.

## Code Changes (Already Done)

✅ **Reverted to SQLite** (from PostgreSQL)
- Simpler, no external database needed
- Works great with Replit's file storage
- Database is stored as `bot_memory.db` file

✅ **Reverted database driver** (aiosqlite)
- Removed PostgreSQL (asyncpg) dependency
- Back to lightweight SQLite

✅ **Updated requirements.txt**
- Removed `asyncpg`
- Added `aiosqlite`

✅ **Updated .env.example**
- Removed DATABASE_URL (only need Discord token + Typhoon API key)

## What You Need to Do on Replit

### Quick Timeline: 10 minutes

**Step 1: Create Replit Account** (2 mins)
- Go to https://replit.com
- Sign up with email or GitHub

**Step 2: Import Repository** (3 mins)
- Click **+ Create Repl**
- **Import from GitHub**
- Paste your repo URL
- Wait for it to clone

**Step 3: Add Secrets** (2 mins)
- Click **Secrets** (lock icon)
- Add `DISCORD_TOKEN` (from Discord Developer Portal)
- Add `TYPHOON_API_KEY` (from Typhoon)

**Step 4: Run** (2 mins)
- Click **Run** button
- Verify bot starts (you'll see "is online." in console)
- Test in Discord: `@YourBot ping`

**Step 5: Setup UptimeRobot** (5 mins)
- Go to https://uptimerobot.com
- Create free account
- Add monitor:
  - URL: `https://YOUR_REPL_URL/health`
  - Interval: 5 minutes
- This keeps your bot 24/7 (prevents Replit sleep)

## Files to Help You

| File | Read This For |
|------|---------------|
| **REPLIT_SETUP.md** | Complete step-by-step guide |
| **REPLIT_SUMMARY.md** | This file (overview) |

## Key Differences from Oracle

| Feature | Oracle Cloud | Replit |
|---------|-------------|--------|
| **Setup Time** | 45 mins | 10 mins |
| **Database** | PostgreSQL | SQLite |
| **Cost** | $0/month | $0/month |
| **Keep Alive** | Systemd service | UptimeRobot |
| **Complexity** | High (VM setup) | Low (just run) |
| **24/7 Uptime** | Yes (auto) | Yes (with UptimeRobot) |

## What is UptimeRobot?

A free service that:
- Pings your bot every 5 minutes
- Keeps it "active" so Replit doesn't put it to sleep
- Runs 24/7 automatically
- Alerts you if bot goes down

**Cost:** $0 (free tier)
**Setup time:** 5 minutes

## Code Structure (No Changes Needed)

Your bot still has all the same features:
- ✅ Memory system (persists in `bot_memory.db`)
- ✅ Discord integration
- ✅ Typhoon API calls
- ✅ Commands: `!ping`, `!reset`, `!summary`, `!ask`
- ✅ Health check endpoint (for UptimeRobot)

## Next Steps

1. **Read REPLIT_SETUP.md** (detailed guide)
2. **Follow the 5 steps** (takes 10 minutes total)
3. **Setup UptimeRobot** (keeps bot online 24/7)
4. **Test your bot** in Discord

## Replit URL Format

Once deployed, your bot will be at:
```
https://[repl-name].[your-username].repl.co
```

Example:
```
https://discord-bot.john123.repl.co
```

Use this for UptimeRobot monitoring:
```
https://discord-bot.john123.repl.co/health
```

## Costs

**Total cost to run 24/7:**
- Replit: $0
- UptimeRobot: $0
- Discord bot: $0
- Typhoon API: Pay per use (you pay this regardless)

**Total: $0** ✅

## FAQ

**Q: Will my bot really run 24/7?**
A: Yes, with UptimeRobot. Without it, Replit will sleep after 1 hour.

**Q: What if Replit goes down?**
A: UptimeRobot will alert you immediately, and bot comes back online when Replit recovers.

**Q: Can I use my existing Discord token?**
A: Yes, just add it to Replit secrets.

**Q: Do I need to keep my laptop on?**
A: No! It runs on Replit's servers.

**Q: How do I update the code?**
A: Push to GitHub, then pull in Replit (`git pull`), then click Run.

---

**Ready? Open REPLIT_SETUP.md and follow the steps!** 🚀
