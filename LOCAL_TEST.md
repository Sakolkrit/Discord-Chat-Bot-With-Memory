# Local Testing Before Cloud Deployment

Before deploying to Oracle Cloud, test the bot locally to ensure everything works.

## Prerequisites

- Python 3.9+
- PostgreSQL installed locally (or use Docker)
- Discord token and Typhoon API key

## Option A: Using Local PostgreSQL

### 1. Install PostgreSQL

**Windows**: https://www.postgresql.org/download/windows/

**Mac**: `brew install postgresql`

**Linux**: `sudo apt install postgresql postgresql-contrib`

### 2. Create Database and User

```bash
# Connect to PostgreSQL
psql postgres

# Create database and user
CREATE DATABASE bot_memory;
CREATE USER botuser WITH PASSWORD 'testpass123';
GRANT ALL PRIVILEGES ON DATABASE bot_memory TO botuser;
\q
```

### 3. Setup Environment

```bash
# Create .env file
cp .env.example .env

# Edit .env with your values
# Windows: notepad .env
# Mac/Linux: nano .env

# Make sure DATABASE_URL is:
# DATABASE_URL=postgresql://botuser:testpass123@localhost:5432/bot_memory
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Bot

```bash
python main.py
```

You should see:
```
INFO:__main__:Database initialized successfully
INFO:__main__:[YourBotName] is online.
INFO:__main__:Health server running on port 8080
```

## Option B: Using Docker (No Local PostgreSQL Install)

### 1. Install Docker

Download from https://www.docker.com/products/docker-desktop

### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: bot_memory
      POSTGRES_USER: botuser
      POSTGRES_PASSWORD: testpass123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 3. Start PostgreSQL Container

```bash
docker-compose up -d
```

### 4. Setup & Run Bot

```bash
# Create .env
cp .env.example .env

# Edit .env:
# DATABASE_URL=postgresql://botuser:testpass123@localhost:5432/bot_memory

# Install dependencies
pip install -r requirements.txt

# Run bot
python main.py
```

## Testing the Bot

### 1. Basic Health Check

In another terminal:
```bash
curl http://localhost:8080/health
```

Should return:
```json
{"status": "ok", "bot": "YourBotName"}
```

### 2. Test in Discord

1. Go to your Discord server
2. Try:
   - `@YourBot hello` - Bot should respond
   - `!ask what is the weather` - Bot should ask Typhoon
   - `!ping` - Bot should respond "pong"
   - `!reset` - Bot should clear channel history
   - `!summary` - Bot should summarize recent chat

### 3. Monitor Logs

Watch for errors in the console output. Common issues:

**Error: "Missing DISCORD_TOKEN"**
- Check .env file has valid Discord token

**Error: "Missing TYPHOON_API_KEY"**
- Check .env file has valid Typhoon API key

**Error: "Connection refused" or "Database error"**
- Make sure PostgreSQL is running:
  ```bash
  psql -U botuser -d bot_memory
  \q
  ```

**Error: "Database table exists" warnings**
- These are normal on first run, database creates tables automatically

## Cleanup

### Stop Docker PostgreSQL
```bash
docker-compose down
```

### Stop Bot
Press `Ctrl+C`

## Next Steps

Once local testing works:

1. ✅ Bot responds to messages
2. ✅ LLM integration works (responses from Typhoon)
3. ✅ Commands work (!ping, !reset, !summary)
4. ✅ Database persists messages
5. ✅ Health server responds

Then proceed to Oracle Cloud deployment: See `ORACLE_CLOUD_SETUP.md`
