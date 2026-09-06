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

import mysql
from pydub import AudioSegment

import utils
from utils.tohrudb import get_db, reconnect_to_db

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
UPLOADS_FOLDER = os.getenv('UPLOADS_FOLDER')
TIMEOUT = 5

global mydb

# Bots build bots...
async def main():
    print("Winding up...")
    bot = commands.Bot(intents=intents)

    # Load all the other moduldes that were split off.
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")


    # Maintenance commands for admins.
    maintenance = discord.SlashCommandGroup(
        name="maintenance",
        description="Maintenance commands for admins.",
        integration_types=[discord.IntegrationType.guild_install]
    )

    # Restarts the bot. Ends early so it looks nice on the Discord-side of things.
    @maintenance.command(
        name="restart",
        description="Restarts the bot to reload any changes.",
        guild_ids=[GUILD_ID]
    )
    async def restart_bot(self, ctx):
        print("Restarting bot...")
        await ctx.respond("Restarting...", ephemeral=True)
        await asyncio.sleep(1)
        self.mydb.disconnect()
        exit(1)

    @maintenance.command(
        name="reprocess",
        description="Will reprocess an MP3 that's been uploaded, provided the original file still exists.",
        guild_ids=[GUILD_ID]
    )
    async def reencode(
        self,
        ctx: discord.ApplicationContext,
        upload_id: Option(int, "The archives_audio ID to be re-encoded.", required=True) #type: ignore
    ):
        print("Re-encoding an audio upload...")
        await ctx.defer(ephemeral=True)

        try:
            # Connect to database
            try:
                cursor = self.mydb.cursor()
            except mysql.connector.Error as err:
                print(f"Error connecting to DB: {err}")
                reconnect_to_db(self.mydb)
                cursor = self.mydb.cursor()

            # Get upload details
            sql = f"SELECT original_path FROM archives_audio WHERE id = %s"
            cursor.execute(sql, (upload_id,))

            # Check if upload exists
            result = cursor.fetchone()
            if not result:
                return await ctx.respond(f"Upload with ID {upload_id} not found!")

            original_path = result[0]
            print(f"Retrieved original path from DB: {original_path}")

            if not os.path.isfile(original_path):
                return await ctx.respond(f"The original file for upload ID {upload_id} could not be found at {original_path}.")

            # Re-encode the audio
            try:
                audio = AudioSegment.from_file(original_path)

                # Crunch the audio for maximum effect!
                audio = audio.set_channels(1).set_frame_rate(22050)  # 22.05kHz sample rate

                out_path = f"{original_path}_R.mp3"
                out_ = audio.export(out_path, format="mp3", bitrate="64k")
                out_.close()

                print("Audio re-encoded at 64kbps MP3!")
            except Exception as e:
                print(f"Audio NOT re-encoded! {e}")
                return await ctx.respond(content="Something went wrong reprocessing the audio. This task has NOT been completed.")

            # Update database with new path
            sql = f"UPDATE archives_audio SET path = %s WHERE id = %s"
            cursor.execute(sql, (out_path, upload_id))
            self.mydb.commit()
            cursor.close()

            await ctx.respond(content=f"Upload ID {upload_id} has been successfully re-encoded!", file=discord.File(out_path))
            print(f"Archives ID {upload_id} re-encoded successfully!")

        except Exception as e:
            print(f"Error during re-encode: {e}")
            if cursor:
                cursor.close()

    # Check if we're live.
    @maintenance.command(
        name="ping",
        description="Checks if this bot is awake."
    )
    async def ping_tohru(ctx):
        print("Executing ping command.")
        await ctx.respond("Ping pong! I'm still alive!")


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

    # Print an index of database things for fun reasons.
    @bot.slash_command(
        name="index",
        description="Print a Table of Contents for items in the archives/stuffpile.",
        integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install])
    async def index(
        self,
        ctx: discord.ApplicationContext,
        db: Option(str, "The database to view.", choices={'archives_image', 'archives_audio', 'stuff'}, required=True),  # type: ignore
        user: Option(discord.User, "The user to view entries for.", required=False)  # type: ignore
        ):
        try:
            # It'll freak out if we don't do this.
            utils.tohrudb.reconnect_to_db(self.mydb)
            cursor = self.mydb.cursor()
            command = ""

            print(f"Index command called for {db}...")

            # Certain DBs have different column names... but the same kind of data!
            if db in ['archives_image', 'archives_audio']:
                command = "SELECT id, caption AS name FROM " + db
            elif db == 'stuff':
                command = "SELECT id, name FROM " + db

            # And if we're only looking at this one guy's stuff...
            if user:
                command = command + f" WHERE submitter_id = {user.id}"

            # And thus, we search for entries! And knowledge!!
            cursor.execute(command)
            entries = [(row[0], row[1]) for row in cursor.fetchall()]
            cursor.close()

            # Didn't find anything? That's too bad.
            if not entries:
                return await ctx.respond("No entries found in the database.")

            # Display that stuff!
            paginator = utils.paginator.Paginator(entries)
            paginator.ctx = ctx
            paginator.message = await ctx.respond(embed=paginator.create_embed(), view=paginator)

        except Exception as e:
            print(f"Error retrieving entries: {e}")
            await ctx.respond(f"Uh oh, something went wrong: {e}")
            if cursor:
                cursor.close()

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
    mydb = get_db()
    reconnect_to_db(mydb)

    # And now we run it!
    print("Connecting to Discord...")
    await bot.start(BOT_TOKEN)

# When all is said and done, time to asyncio.run().
asyncio.run(main())
