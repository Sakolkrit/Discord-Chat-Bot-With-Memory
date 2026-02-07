# -------- Library imports --------
import os # Used for environment variables
from dotenv import load_dotenv # Used for environment variables
import ollama # LLM
import discord # Discord API
# ---------------------------------



# -------- Setup --------
# Set up environment
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Set up bot
intents = discord.Intents.default()
intents.message_content = True # Bot should be able to read and interpret messages
bot = discord.Client(intents=intents)

# Ollama configuration
model = "qwen2.5:1.5b"
system_prompt = '''
    You are a helpful assistant
'''

# conversation_context will have the following format:
# {
# server_id1 : {
#       channel_id1: [{role, msg}, {role, msg} ...],
#       channel_id2: [{role, msg}, {role, msg} ...]
#       },
# server_id2 : {
#       channel_id1: [{role, msg}, {role, msg} ...],
#       channel_id2: [{role, msg}, {role, msg} ...]
#       }, ... 
# }
conversation_context = {}
conversation_context_limit = 8 # Maximum amount of messages per chat
# -----------------------



# -------- Helper Functions --------
# Stores user and LLM messages for history purposes. The caller has to specify if message is
# from the user or LLM
def store_chat(server, channel, message, role):
    if (server in conversation_context) and (channel in conversation_context[server]):
        cur_chat = conversation_context[server][channel]

        # Check if chat limit has reached (remove first message)
        if conversation_context_limit <= len(cur_chat):
            cur_chat.pop(0)

        cur_chat.append({"role": role, "content": message})
    else:
        if server not in conversation_context:
            conversation_context[server] = {}
        conversation_context[server][channel] = [{"role": role, "content": message}]

# Return a list of the entire chat
def get_chat(server, channel):
    return conversation_context[server][channel]
# -----------------------



# -------- Bot Events --------
# When bot is ready to start operating
@bot.event
async def on_ready():
    print(f"{bot.user.name} is online!")


# When a message gets sent to the Discord chat
@bot.event
async def on_message(msg: discord.Message):
    if msg.author == bot.user:
        return

    # Store user message
    store_chat(str(msg.guild.id), str(msg.channel.id), msg.content, "user")

    # Process LLM response
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt}
        ] + get_chat(str(msg.guild.id), str(msg.channel.id))
    )

    # Store LLM message
    store_chat(str(msg.guild.id), str(msg.channel.id), response.message.content, "assistant")

    # Send messages in chunks of 2000 characters (Discord doesn't allow more per message)
    chunks = (len(response.message.content) + 1999) // 2000
    for i in range(chunks):
        await msg.channel.send(response.message.content[i*2000:(i+1)*2000])
# ----------------------------



bot.run(DISCORD_TOKEN)