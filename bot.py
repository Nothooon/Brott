import os
import discord
import logging
import logging.handlers
from features import feur

intents = discord.Intents.default()
intents.message_content = True

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(filename='discord.log', encoding='utf-8', mode='w', maxBytes=32*1024*1024, backupCount=5) # 32MB max, 5 backups
dt_fmt = '%d-%m-%Y %H:%M:%S'
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(os.getenv('DISCORD_TOKEN'), log_handler=None, reconnect=True) # No handler, we already made one
