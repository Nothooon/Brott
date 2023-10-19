import os
import pandas as pd # xDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
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
            df = pd.read_csv('features/feurlog.csv', sep=',')
            usernames = []
            for row in df['user']:
                usernames.append(row)
            if message.author.name in usernames:
                df.loc[df["user"]==message.author.name, "countfeur"] = df.loc[df["user"]==message.author.name, "countfeur"] + 1
                df.loc[df["user"]==message.author.name, "lastfeur"] = datetime.datetime.now()
            else:
                df = pd.concat([df, pd.DataFrame({'user': [message.author.name], 'countfeur': [1], 'lastfeur': [datetime.datetime.now()]})])
            df.to_csv('features/feurlog.csv', sep=',', index=False)
            # End logging
            if sticker:
                await message.channel.send(file=sticker)
            else:
                await message.channel.send(content=answer)

client.run(os.getenv('DISCORD_TOKEN'))
