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

    # The one and only necessary feature
    if "quoi" in message.content.lower():
        feur_controller = feur.FeurController(message)
        answer = feur_controller.create_feur_answer()
        if answer:  # Depending on our luck, we don't answer "feur" and the controller returns an empty message
            await message.channel.send(answer)

client.run(os.getenv('DISCORD_TOKEN'))
