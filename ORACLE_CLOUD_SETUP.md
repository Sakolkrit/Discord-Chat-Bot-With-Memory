# Oracle Cloud Setup Guide

This guide walks you through setting up the Discord bot on Oracle Cloud's Always Free tier.

## Step 1: Create Oracle Cloud Account & VM

1. Go to https://www.oracle.com/cloud/free/
2. Click "Start for free" and create your account
3. Go to **Compute** → **Instances** (left sidebar)
4. Click **Create Instance**
5. Configure:
   - **Name**: discord-bot
   - **Image**: Ubuntu 22.04 (or latest)
   - **Shape**: Ampere (Always Free eligible)
   - **CPU**: 4 cores
   - **RAM**: 24 GB
   - **Storage**: 200 GB
6. Generate SSH key pair:
   - Download the private key (save as `oracle-bot-key.pem`)
   - Create the instance

## Step 2: Create PostgreSQL Database

### Option A: Using Oracle Database (Recommended for Always Free)

1. Go to **Database** → **MySQL Heatwave** or **Autonomous Database**
2. Click **Create Database**
3. Configure:
   - **Display Name**: bot-memory
   - **Database Name**: bot_memory
   - **Always Free**: Enable ✓
   - **Admin Password**: Create a strong password
4. Wait for database to be available (~5-10 mins)
5. Click your database → **DB Connection** → **Connection Strings**
   - Copy the Private Endpoint URL (note host, port, username)

### Option B: Install PostgreSQL on VM (Simpler)

SSH into your VM (see Step 3), then:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE bot_memory;
CREATE USER botuser WITH PASSWORD 'your_strong_password_here';
GRANT ALL PRIVILEGES ON DATABASE bot_memory TO botuser;
\q
EOF
```

## Step 3: Connect to Your VM via SSH

### On Windows (PowerShell):
```powershell
# Set permissions on private key
icacls "oracle-bot-key.pem" /inheritance:r /grant:r "$env:username`:(F)"

# SSH to your VM
ssh -i "oracle-bot-key.pem" ubuntu@YOUR_INSTANCE_IP
```

### On Mac/Linux:
```bash
chmod 600 oracle-bot-key.pem
ssh -i oracle-bot-key.pem ubuntu@YOUR_INSTANCE_IP
```

> Find **YOUR_INSTANCE_IP** in Oracle Cloud Console → Instances → Your instance details

## Step 4: Clone & Setup Bot Repository

```bash
# Install git
sudo apt install git -y

# Clone your repository
git clone https://github.com/YOUR_USERNAME/Discord-Chat-Bot-With-Memory.git
cd Discord-Chat-Bot-With-Memory

# Install Python dependencies
sudo apt install python3 python3-pip -y
pip3 install -r requirements.txt
```

## Step 5: Configure Environment Variables

```bash
# Create .env file with your configuration
nano .env
```

Paste the following (replace YOUR_VALUES):

```env
DISCORD_TOKEN=your_discord_token_here
TYPHOON_API_KEY=your_typhoon_api_key_here
TYPHOON_MODEL=typhoon-v2.1-12b-instruct
BOT_PREFIX=!
PORT=8080
DATABASE_URL=postgresql://botuser:your_strong_password_here@localhost:5432/bot_memory
```

Press `Ctrl+O`, `Enter`, then `Ctrl+X` to save.

## Step 6: Test the Bot

```bash
# Test if bot starts correctly
python3 main.py
```

Check if you see:
- "Database initialized successfully"
- "[bot-name] is online."
- "Health server running on port 8080"

Press `Ctrl+C` to stop.

## Step 7: Run Bot as a Service (24/7)

Create a systemd service file so the bot runs automatically:

```bash
sudo nano /etc/systemd/system/discord-bot.service
```

Paste this:

```ini
[Unit]
Description=Discord Chat Bot with Memory
After=network.target postgresql.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/Discord-Chat-Bot-With-Memory
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/ubuntu/.local/bin"
ExecStart=/usr/bin/python3 /home/ubuntu/Discord-Chat-Bot-With-Memory/main.py
Restart=always
RestartSec=10
StandardOutput=append:/home/ubuntu/Discord-Chat-Bot-With-Memory/bot.log
StandardError=append:/home/ubuntu/Discord-Chat-Bot-With-Memory/bot.log

[Install]
WantedBy=multi-user.target
```

Press `Ctrl+O`, `Enter`, then `Ctrl+X` to save.

Now start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl start discord-bot
sudo systemctl enable discord-bot

# Check status
sudo systemctl status discord-bot

# View logs
tail -f bot.log
```

## Step 8: Open Firewall Port (if needed)

If using Oracle Cloud health server monitoring:

1. Go to **Networking** → **Virtual Cloud Networks**
2. Select your VCN
3. Go to **Security Lists**
4. Click the default security list
5. Click **Add Ingress Rule**:
   - **Source Type**: CIDR
   - **Source CIDR**: 0.0.0.0/0
   - **Protocol**: TCP
   - **Destination Port Range**: 8080
   - Click **Add Ingress Rule**

## Step 9: Monitor Your Bot

### Check if it's running:
```bash
sudo systemctl status discord-bot
```

### View recent logs:
```bash
tail -50 bot.log
```

### Stream live logs:
```bash
tail -f bot.log
```

### Monitor database:
```bash
# Connect to PostgreSQL
sudo -u postgres psql bot_memory

# Check message count
SELECT COUNT(*) FROM messages;

# View recent messages
SELECT guild_id, channel_id, role, content FROM messages ORDER BY id DESC LIMIT 10;

# Exit
\q
```

## Troubleshooting

### Bot won't start
```bash
sudo systemctl status discord-bot
tail -100 bot.log
```

### Database connection error
```bash
# Test PostgreSQL connection
psql -h localhost -U botuser -d bot_memory -c "SELECT 1"

# If that fails, PostgreSQL may not be running:
sudo systemctl start postgresql
```

### Bot goes offline
```bash
# Restart the service
sudo systemctl restart discord-bot

# Check if it auto-restarts properly
journalctl -u discord-bot -n 50
```

### Memory issues (bot crashes)
Edit `/etc/systemd/system/discord-bot.service` and add under `[Service]`:
```ini
MemoryLimit=256M
```

## Updating the Bot

When you make changes to your code:

```bash
cd Discord-Chat-Bot-With-Memory
git pull origin main
pip3 install -r requirements.txt  # if dependencies changed
sudo systemctl restart discord-bot
```

## Costs

✅ **Oracle Cloud Always Free Tier includes:**
- 4 cores, 24GB RAM VM
- 20GB PostgreSQL database
- Perpetually free (not just 12 months)

**Note**: Excessive data transfer or compute might incur charges. Monitor your usage in the Oracle Cloud Console.

## Additional Tips

1. **Use UptimeRobot** to monitor health endpoint at `http://YOUR_INSTANCE_IP:8080/health`
   - Ping every 5 mins → keeps bot responsive
   - Alerts you if bot goes down

2. **Backup your database** periodically:
   ```bash
   pg_dump -U botuser bot_memory > backup.sql
   ```

3. **Rotate Discord token** regularly in Discord Developer Portal for security

4. **Monitor database size**:
   ```bash
   sudo -u postgres psql -d bot_memory -c "SELECT pg_size_pretty(pg_database_size('bot_memory'));"
   ```
