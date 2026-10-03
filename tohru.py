#    *   )        )
#  ` )  /(     ( /(  (      (
#   ( )(_))(   )\()) )(    ))\
#   (_(_()) )\ ((_)\ (()\  /((_)
#   |_   _|((_)| |(_) ((_)(_))(
#     | | / _ \| ' \ | '_|| || |
#     |_| \___/|_||_||_|   \_,_|
#
# - The Ultimate(?) Discord Maid! -
#
# ░░░░▒░░░░░▒▒░▒▒▒▒░░▒░░░░░░░░░░▒▒▒
# ▒▒▒▒▓▓▓▓▒░░▒░░▒▒▒▒░▒░▒▓▓▓▓▓▒▒▓▓▒▒
# ▒░░░░▒▓▓▓▓░░░░░▒▒▒▒░▒▓▒░▒▓▓▓▒░░▒▒
# ░░▒▓▓▓▓▓▓▒░░░░░░▒▒▒░░░▓▓▒▓▓▓▓░░▒▓
# ░░░▓▒▒▒▒▒▒░░░░░░░▒▒░░░▒▒░░░▒▒░░░▒
# ░░░░▒░░▒▒░░░░░░░░░▒░░░░░░░▒▒░░░░▒
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒
# ▒░░░░░░░░░░░░░░░░░░▒░░░░░░░░░░░▒▒
# ▓░░░░░░░░░▒▓▒▓▓▓▓▓▓▓▓▓░░░░░░░░░▒░
# █▓░░░░░░░░▒▓▓▒▒▒▒▒▒▒▓▒░░░░░░░░▓▒░
# ███▒░░░░░░░▒▒▒▒▒▒▒▒▒▒▒░░░░░░▒██▒░
# █████▒░░░░░░░▒▒▒▒▒▒░░░░░░░▒████▒░


# INITIALIZATIONS...

# for everything
import os
import random
from dotenv import load_dotenv
import asyncio

# for connection to discord
import discord  # pip install pycord
from discord.ext import commands
from discord import Option

# useless things
import mysql
from pydub import AudioSegment

# useful things
import utils.tohrudb
import utils.paginator

# Intents because we need them apparently
intents = discord.Intents.default()
intents.message_content = True

# Define stuff.
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
KANNA_IP = os.getenv('KANNA_IP')
PORT = int(os.getenv('PORT'))
SOUNDFONT = os.getenv('SOUNDFONT')
TIMEOUT = 5

global mydb

# Bots build bots...
async def main():
    print("Winding up...")
    bot = commands.Bot(intents=intents)
    mydb = utils.tohrudb.get_db()

    # Load all the other moduldes that were split off.
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")



    # Repeat whatever is said.
    @bot.slash_command(
        name="echo",
        description="Make Tohru say something.",
        integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install]
    )
    async def echo(
        ctx: discord.ApplicationContext,
        content: Option(str, "Your message here!", required=True)  # type: ignore
    ):
        print(f"User {ctx.author.id} is saying something... {content}")
        await ctx.respond(content=content)

    # When the bot sees something has been sent in one of the channels...
    @bot.event
    async def on_message(message):
        # If the bot posted it, we don't need it to respond to itself.
        if message.author == bot.user:
            return

        # lowercase the message so it can detect words easier.
        msg = message.content.lower()

        # Even if not mentioned, call out anyone lacking skibidi rizz.
        if 'skibidi' in msg:
            responses = ["You are NOT skibidi rizz!! :x: :toilet:"]
            await message.channel.send(random.choice(responses))
            return

        # If bot mentioned in any message...
        if bot.user.mentioned_in(message):
            if 'kill' in msg or 'murder' in msg:
                if 'me' in msg:
                    responses = ["Hey, please take your own health seriously. :heart:", "Later. :knife:"]
                    await message.channel.send(random.choice(responses))
                    return
                if 'yourself' in msg:
                    # Don't respond to hate.
                    return
                await message.channel.send('You want me to *kill someone*?!... Okay! :knife:')
                return

            if 'thanks' in msg:
                await message.channel.send('You\'re welcome! :smiling_face_with_3_hearts:')
                return

            if 'sorry' in msg:
                responses = ["I'll never forgive you... :frowning2:", "It's alright, I guess... :frowning:", "It's okay! :smile:"]
                await message.channel.send(random.choice(responses))
                return

    # When the bot is ready to take on the world...
    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your every move."))
        print("Ready!")

    # Just wait a moment for the DB to kick in...
    await asyncio.sleep(5)
    print("Connecting to DB...")
    utils.tohrudb.reconnect_to_db(mydb)

    # And now we run it!
    print("Connecting to Discord...")
    await bot.start(BOT_TOKEN)

# When all is said and done, time to asyncio.run().
asyncio.run(main())
