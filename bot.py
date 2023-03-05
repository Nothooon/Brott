import os
import discord
from features import feur

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "quoi" in message.content.lower():
        feur_controller = feur.FeurController(message)
        feur_controller.trigger_feur_answer()

client.run(os.getenv('DISCORD_TOKEN'))
