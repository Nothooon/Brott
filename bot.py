import os
import discord
from discord import app_commands

from features import feur, logging
from features.link_fix import service

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

logger = logging.Logger()
link_fixer = service.LinkFixService()


@tree.command(name="leaderboard", description="Display the leaderboard")
async def leaderboard(ctx):
    res = logger.get_leaderboard()
    await ctx.response.send_message(embed=res)


@tree.command(name="feur", description="Display the user's feur count")
async def feur_user(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.user
    if user.bot:
        await ctx.response.send_message("A bot can't be feur'd!", ephemeral=True)
    else:
        res = logger.get_user(user.name)
        await ctx.response.send_message(embed=res)


@client.event
async def on_ready():
    await tree.sync()
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:  # Useless? bot seems to ignore other bots (including itself?)
        return

    if link_fixer.detect_inner_links(message.content):
        await message.delete()
        await message.channel.send(link_fixer.handle_message(message))

    # The one and only necessary feature
    if "quoi" in message.content.lower():
        feur_controller = feur.FeurController(message)
        answer, sticker = feur_controller.create_feur_answer()
        if answer or sticker:  # Depending on our luck, we don't answer "feur" but use a sticker instead
            logger.log_feur(message.author.name)
            if sticker:
                await message.channel.send(file=sticker)
            else:
                await message.channel.send(content=answer)


client.run(os.getenv('DISCORD_TOKEN'))
