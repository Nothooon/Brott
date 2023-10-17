import os
import discord
import datetime
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
        answer, sticker = feur_controller.create_feur_answer()
        if answer:  # Depending on our luck, we don't answer "feur" and the controller returns an empty message
            # Begin logging
            f = open("features/feurlog.csv", "a")
            f.write(message.author.name+","+datetime.datetime.now()+"\n")
            f.close()
            # End logging
            if sticker:
                await message.channel.send(file=sticker)
            else:
                await message.channel.send(content=answer)

client.run(os.getenv('DISCORD_TOKEN'))
