# Replit Setup Guide

This guide walks you through deploying your Discord bot on Replit for free 24/7 operation.

## What's Different from Oracle Cloud

✅ **Pros:**
- No setup hassle, works immediately
- Free tier available
- Simple web interface
- No server management

⚠️ **Cons:**
- Free tier sleeps after 1 hour of inactivity
- Need UptimeRobot to keep it awake (pings every 5 mins)
- Slower than Oracle Cloud
- SQLite stored in Replit (not production-grade)

**Bottom line:** Works great for small Discord bots with UptimeRobot monitoring.

## Step 1: Create Replit Account

1. Go to https://replit.com
2. Sign up (email or GitHub)
3. You're done!

## Step 2: Create a New Repl (Import from GitHub)

### Option A: Import from GitHub (Easiest)

1. In Replit, click **+ Create Repl**
2. Click **Import from GitHub**
3. Paste your repo URL:
   ```
   https://github.com/YOUR_USERNAME/Discord-Chat-Bot-With-Memory
   ```
4. Language will auto-detect as Python
5. Click **Import**
6. Wait for Replit to clone your repo

### Option B: Create Empty & Upload Files

1. Click **+ Create Repl**
2. Choose **Python**
3. Name it: `discord-bot`
4. Upload your files:
   - Drag & drop `main.py`, `requirements.txt`, `.env`
   - Or copy-paste the content

## Step 3: Install Dependencies

Replit auto-detects `requirements.txt` and installs on first run, but you can manually install:

1. Go to **Shell** tab (or press Ctrl+Shift+S)
2. Type:
   ```bash
   pip install -r requirements.txt
   ```
3. Wait for installation to complete

## Step 4: Set Environment Variables (Secrets)

**IMPORTANT:** Never paste secrets directly in code!

1. Click **Secrets** icon (lock icon on left sidebar)
2. Click **+ Add new secret**
3. Add each secret:

   **Secret 1:**
   - Key: `DISCORD_TOKEN`
   - Value: Your Discord bot token (from Discord Developer Portal)

   **Secret 2:**
   - Key: `TYPHOON_API_KEY`
   - Value: Your Typhoon API key

4. Repeat for any other variables (BOT_PREFIX, PORT, etc.)

**Example:**
```
DISCORD_TOKEN = MTQ5NzU5MQ... (your actual token)
TYPHOON_API_KEY = sk-abc123... (your actual key)
```

## Step 5: Run the Bot

1. Click **Run** button (green play button)
2. Console will show:
   ```
   Database initialized successfully
   [YourBotName] is online.
   Health server running on port 8080
   ```

3. If you see errors, check:
   - Discord token is correct
   - Typhoon API key is correct
   - All secrets are added

4. Test in Discord: `@YourBot hello` or `!ping`

## Step 6: Keep Bot Running 24/7 (Important!)

### Problem
Replit free tier puts Repl to sleep after **1 hour of inactivity**. Your bot will go offline.

### Solution: Use UptimeRobot

**How it works:**
- UptimeRobot pings your bot every 5 minutes
- This keeps it "active" so Replit doesn't put it to sleep
- Your bot runs 24/7

**Setup UptimeRobot:**

1. Go to https://uptimerobot.com
2. Sign up (free)
3. Create new monitor:
   - Click **+ Add New Monitor**
   - Type: **HTTP(s)**
   - URL: `https://YOUR_REPL_URL/health` (see Step 7)
   - Interval: **5 minutes**
   - Click **Create Monitor**

That's it! UptimeRobot now keeps your bot alive.

## Step 7: Get Your Replit URL

1. In Replit, click **Web View** (top right)
2. Copy the URL from the browser address bar
3. It looks like: `https://discord-bot.YOUR_USERNAME.repl.co`
4. Use this for UptimeRobot in Step 6

Your bot listens on this URL at:
- Health check: `https://discord-bot.YOUR_USERNAME.repl.co/health`
- UptimeRobot pings this endpoint

## Step 8: (Optional) Use Replit's Always On

If you don't want to use UptimeRobot:

1. In Replit, go to **Tools** (wrench icon)
2. Look for **Always On** or similar feature
3. Enable it (requires Replit Pro, ~$7/month)

**OR** just use the free UptimeRobot method - it works great!

## Complete Setup Checklist

- [ ] Create Replit account
- [ ] Import or create Repl
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Add secrets:
  - [ ] DISCORD_TOKEN
  - [ ] TYPHOON_API_KEY
- [ ] Click **Run** and verify bot starts
- [ ] Test in Discord (`@BotName hello`)
- [ ] Get your Replit URL from Web View
- [ ] Setup UptimeRobot to ping `/health` endpoint
- [ ] Verify bot stays online in Discord

## Monitoring Your Bot

### Check if running
```
In Discord: @YourBot ping
Expected response: pong
```

### View logs
In Replit console, you'll see real-time logs:
```
Database initialized successfully
[BotName] is online.
Health server running on port 8080
```

### Restart the bot
Click **Run** button again

### Debug issues
1. Check Replit console for errors
2. Verify secrets are correct
3. Check Discord token validity
4. Verify Typhoon API key is valid

## Storage & Database

- **SQLite file** (`bot_memory.db`) is stored in Replit's file system
- Data persists between restarts
- Maximum storage: Free tier has ~5GB (plenty for chat history)

## Costs

**Replit Free Tier:**
- ✅ Run your bot
- ✅ 5GB storage (for bot_memory.db)
- ⚠️ Sleeps after 1 hour (use UptimeRobot to prevent)

**Optional Paid Tier:**
- Always On feature: $7/month (if you don't want UptimeRobot)

**UptimeRobot Free Tier:**
- ✅ Monitor 50 services
- ✅ Check every 5 minutes
- ✅ Email alerts

**Total cost to run 24/7:** $0 + Free (using UptimeRobot)

## Updating Your Bot

When you make code changes:

1. Push to GitHub:
   ```bash
   git add .
   git commit -m "Update bot"
   git push origin main
   ```

2. In Replit, pull latest:
   - Click **Shell** tab
   - Type: `git pull`
   - Click **Run** to restart

3. Or just edit in Replit's editor and click **Run**

## Troubleshooting

### Bot won't start
- Check console for error messages
- Verify DISCORD_TOKEN secret is correct
- Verify TYPHOON_API_KEY secret is correct

### Bot goes offline
- Check if UptimeRobot is pinging correctly
- Go to UptimeRobot dashboard and verify monitor is working
- If not, the monitor may have failed - recreate it

### Memory errors
- SQLite database got too large
- Delete old messages: `!reset` command in Discord

### Bot responds slowly
- Replit free tier is slower
- Normal behavior
- Upgrade to Replit Pro for faster response

## Discord Commands

```
@BotName hello          → Bot responds with AI
!ask what time is it    → AI-powered response
!ping                   → Bot responds "pong"
!reset                  → Clear channel history
!summary                → Summarize recent chat
```

## Next Steps

1. ✅ Setup Replit (Steps 1-5)
2. ✅ Setup UptimeRobot (Step 6)
3. ✅ Test your bot
4. ✅ Enjoy 24/7 Discord bot!

---

**Your bot is now running 24/7 on Replit!** 🎉
