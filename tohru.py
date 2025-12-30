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
import string
from dotenv import load_dotenv

# for connection to discord
import discord  # pip install pycord
from discord.ext import commands
from discord import Option
from discord.ui import View, Button

# for connection to sauceypc
import subprocess
import socket
import time

# for archives/stuffpile upload stuff
import mysql.connector
from datetime import datetime
from colorthief import ColorThief
from PIL import ImageColor
from wand.image import Image as MagickImage
import filetype # pip install filetype

# for audio/midi conversion
from pydub import AudioSegment # pip install pydub
import pretty_midi
import soundfile as sf

# for crypto, the secret message tool. it should be in this folder, it's NOT a pip package.
import crypto


# Intents because we need them apparently
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)

# Define stuff.
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
KANNA_IP = os.getenv('KANNA_IP')
PORT = int(os.getenv('PORT'))
SOUNDFONT = os.getenv('SOUNDFONT')
UPLOADS_FOLDER = os.getenv('UPLOADS_FOLDER')
TIMEOUT = 5

# Define all the commands:

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


# Commands that ping stuff.
ping = bot.create_group(
    name="ping",
    description="Commands relating to the pinging of services.",
    integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install]
)

# Check if we're live.
@ping.command(
    name="bot",
    description="Checks if this bot is awake."
)
async def ping_tohru(ctx):
    print("Executing ping command.")
    await ctx.respond("Ping pong! I'm still alive!")

# Connection test to SAUCEY-PC.
@ping.command(
    name="friend",
    description="Checks if the helper service is awake."
)
async def ping_kanna(ctx):
    if KANNA_IP == "KANNA_IP_HERE":
        await ctx.respond("Kanna has been disabled for now.\n She's uh, probably sleeping.")
        return
    print("Executing connection command.")
    await ctx.defer()
    response = sendit(b"connect")
    print(response)
    await ctx.followup.send(response)


# Commands that implement Crypto, The Secret Message Encoding Tool
crypto = bot.create_group(
    name="crypto",
    description="The Secret Message Encoding Tool, now in Discord!",
    integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install]
)

# Encode to Crypto
@crypto.command(
    name="encode",
    description="Encode something to Crypto code."
)
async def crypto_encode(
    ctx: discord.ApplicationContext,
    content: Option(str, "Your message here!", required=True, max_length=333)  # type: ignore
):
    print("Encoding to Crypto.")
    message = crypto.encode_crypto(content)
    await ctx.respond(content=message, ephemeral=True)

# Decode from Crypto
@crypto.command(
    name="decode",
    description="Decode something from Crypto code."
)
async def crypto_decode(
    ctx: discord.ApplicationContext,
    content: Option(str, "Crypto code here!", required=True)  # type: ignore
):
    print("Decoding from Crypto.")
    message = crypto.decode_crypto(content)
    await ctx.respond(content=message, ephemeral=True)


# Commands involving the archives system.
archives = bot.create_group(
    name="archives",
    description="Commands related to the Lossy Files Archive.",
    integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install]
)

# Archives upload fun
@archives.command(
    name="upload",
    description="Upload an image or audio file to be horribly compressed."
)
async def archives_upload(
    ctx: discord.ApplicationContext, 
    file: Option(discord.Attachment, "Choose a file to upload", required=True),  # type: ignore
    caption: Option(str, "Add a caption/title to help identify the upload!", required=False) = ""  # type: ignore
):
    print("Upload command called!")
    await ctx.defer(ephemeral=False)

    response, error, comp_path, caption, upload_id = await submit_to_archives(file, caption, ctx.author.id)
    
    # If it's gone oh so horribly wrong, break the bad news.
    if error:
        await ctx.respond(content=response)
        return

    # Otherwise? We're swimmin'.
    if caption:
        await ctx.respond(content=f"File is now safe in the archives! ID: {upload_id}\n> {caption}",file=discord.File(comp_path))
    else:
        await ctx.respond(content=f"File is now safe in the archives! ID: {upload_id}",file=discord.File(comp_path))
    print(f"Archives ID {upload_id} sent successfully!")

# Archives retrieval fun
@archives.command(
    name="fetch",
    description="Retrieve a file from the archives."
)
async def archives_fetch(
    ctx: discord.ApplicationContext,
    type: Option(str, "The type of upload to be fetched.", choices=['Image', 'Audio'], required=True),  # type: ignore
    upload_id: Option(int, "Specific upload ID", required=False, default=0),  # type: ignore
    uncompressed: Option(bool, "Send the uncompressed version of the upload?", default=False)  # type: ignore
):
    # Let 'em know we're comin'.
    await ctx.defer()

    try:
        if type == "Image": # We should use a switch case but I can't be bothered.
            db = "archives_image"
        else:
            db = "archives_audio"

        try:
            cursor = mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            reconnect_to_db()
            cursor = mydb.cursor()

        if upload_id == 0: # If they asked for a random upload.
            # Count total images
            sql = f"SELECT COUNT(*) FROM {db}"
            cursor.execute(sql)
            total_images = cursor.fetchone()[0]

            if not total_images:
                return await ctx.respond("Nothing was found in the archives!")

            # Generate random number within upload count
            upload_id = random.randint(1, total_images)

        # Get upload details
        if uncompressed:
            sql = f"SELECT original_path, caption FROM {db} WHERE id = %s"
        else:
            sql = f"SELECT path, caption FROM {db} WHERE id = %s"
        val = (upload_id,)
        cursor.execute(sql, val)

        # Check if upload exists
        result = cursor.fetchone()
        if not result:
            return await ctx.respond(f"Upload with ID {upload_id} not found!")

        path, caption = result
        print(f"Retrieved upload path from DB: {path}")

        # Send upload
        if caption:
            await ctx.respond(content=f"Here you go, boss! (ID: {upload_id})\n> {caption}",file=discord.File(path))
        else:
            await ctx.respond(content=f"Here you go, boss! (ID: {upload_id})",file=discord.File(path))
        print(f"Archives ID {upload_id} sent successfully!")
        cursor.close()
        mydb.close()

    except Exception as e:
        print(f"Error retrieving upload: {e}")
        await ctx.respond(f"Uh oh, something went wrong: {e}")
        cursor.close()
        mydb.close()


# Commands involving the tips system.
tips = bot.create_group(
    name="tip",
    description="Loading screen tips! Or quotes! Both!!",
    integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install]
)

# Tip submission fun
@tips.command(
    name="submit",
    description="Submit a helpful tip or an important quote."
)
async def tips_submit(
    ctx: discord.ApplicationContext,
    type: Option(str, "Whether you are submitting a tip or a quote.", choices=['Tip', 'Quote'], required=True),  # type: ignore
    content: Option(str, "Type your submission here.", required=True, max_length=4096),  # type: ignore
    author: Option(str, "The person that the tip/quote originated from.", required=False, default="Anonymous", max_length=256)  # type: ignore
):
    print("Tip submission command called!")

    # Figure out which table we're gonna use.
    if type == "Tip":
        db = "tips"
    else:
        db = "quotes"

    try:
        # Connect to database.
        try:
            cursor = mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            reconnect_to_db()
            cursor = mydb.cursor()

        # Store tip in the database
        sql = f"INSERT INTO {db} (content, author, submitter_id) VALUES (%s, %s, %s)"
        val = (content.replace('"', '\"'), author.replace('"', '\"'), ctx.author.id)  # Escape single quotes
        cursor.execute(sql, val)
        mydb.commit()

        # Fetch ID of last upload.
        cursor.execute("SELECT LAST_INSERT_ID()")
        id = cursor.fetchone()[0]
        cursor.close()
        mydb.close()

        if type == "Tip":
            await ctx.respond(content=f"Your submission has been saved! ID: {id}\n> {content}", ephemeral=False)
        else:
            await ctx.respond(content=f"Your submission has been saved! ID: {id}\n> *\"{content}\" - {author}*", ephemeral=False)

        print(f"Tip {id} submitted successfully!")

    except Exception as e:
        print(f"Oh, fiddlesticks! What now... {e}?!")
        await ctx.respond(content=f"Uh oh, something went wrong: {e}. Please try again.", ephemeral=True)
        cursor.close()
        mydb.close()

# Tip retrieval fun
@tips.command(
    name="roll",
    description="Roll for a random loading screen tip, or request one via ID."
)
async def tips_roll(
    ctx: discord.ApplicationContext,
    type: Option(str, "What type of submission you're looking for.", choices=['Tip', 'Quote'], required=True),  # type: ignore
    id: Option(int, "Specific submission ID (leave blank for random)", required=False, default=0)  # type: ignore
):
    print("Tip retrieval command called!")

    # Figure out which table we're gonna use.
    if type == "Tip":
        db = "tips"
    else:
        db = "quotes"

    try:
        # Connect to database
        try:
            cursor = mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            reconnect_to_db()
            cursor = mydb.cursor()

        if id == 0: # If they asked for a random tip.
            # Count total submissions
            sql = f"SELECT COUNT(*) FROM {db}"
            cursor.execute(sql)
            total_submissions = cursor.fetchone()[0]

            # Generate random number within submission count
            id = random.randint(1, total_submissions)

        # Get submission
        sql = f"SELECT content, author FROM {db} WHERE id = {id}"
        cursor.execute(sql)

        # Check if submission exists
        content, author = cursor.fetchone()
        if not content:
            return await ctx.respond(f"Submission with ID {id} not found!")

        # Send image
        if db == tips:
            await ctx.respond(content=f"> {content}")
        else:
            await ctx.respond(content=f"> *\"{content}\" - {author}*")
        print(f"Submission ID {id} sent successfully!")
        cursor.close()
        mydb.close()

    except Exception as e:
        print(f"Error retrieving submission: {e}")
        await ctx.respond(f"Uh oh, something went wrong: {e}")
        cursor.close()
        mydb.close()


# Commands involving the pool system.
pool = bot.create_group(
    name="pool",
    description="Your own personal notepad!",
    integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install]
)

# Pool creation fun
@pool.command(
    name="create",
    description="Create a new pool to hold your stuff."
)
async def pool_create(
    ctx: discord.ApplicationContext,
    pool: Option(str, "Names must be uniques, we recommend adding your own prefix to avoid conflicts.", required=True, max_length=16),  # type: ignore
    visible: Option(bool, "Should this pool be visible to others? They will also be able to modify it.", default=True)  # type: ignore
):
    print(f"User {ctx.author.id} is creating a new pool: {pool}")
    await ctx.defer(ephemeral=True)

    try:
        # Connect to database.
        try:
            cursor = mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            reconnect_to_db()
            cursor = mydb.cursor()

        # Check if the pool already exists
        sql = "SELECT COUNT(*) FROM pools WHERE name = %s"
        val = (pool,)
        cursor.execute(sql, val)
        pool_exists = cursor.fetchone()[0] > 0
        if pool_exists:
            await ctx.respond(content=f"Pool '{pool}' already exists! Please choose a different name.", ephemeral=True)
            cursor.close()
            mydb.close()
            print(f"Nevermind! {pool} already exists!")
            return  

        # Create the pool in the database
        sql = "INSERT INTO pools (name, owner_id, visible) VALUES (%s, %s, %s)"
        val = (pool, ctx.author.id, visible)
        cursor.execute(sql, val)
        mydb.commit()

        print(f"User {ctx.author.id} created pool {pool} successfully!")
        await ctx.respond(content=f"Your pool '{pool}' has been created!", ephemeral=True)
        cursor.close()
        mydb.close()
    except Exception as e:
        print(f"Oh, fiddlesticks! What now... {e}?!")
        await ctx.respond(content=f"Uh oh, something went wrong: {e}. Please try again.", ephemeral=True)
        cursor.close()
        mydb.close()

# Pool submission fun
@pool.command(
    name="submit",
    description="Submit something into one of your pools."
)
async def pool_submit(
    ctx: discord.ApplicationContext,
    pool: Option(str, "Which of your pools would you like to use?", required=True, max_length=16),  # type: ignore
    content: Option(str, "Type your submission here.", required=True, max_length=4096)  # type: ignore
):
    print(f"User {ctx.author.id} is submitting into {pool}!")
    await ctx.defer(ephemeral=True)

    try:
        # Connect to database.
        try:
            cursor = mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            reconnect_to_db()
            cursor = mydb.cursor()

        # Check if the pool exists
        sql = "SELECT COUNT(*) FROM pools WHERE name = %s"
        val = (pool,)
        cursor.execute(sql, val)
        pool_exists = cursor.fetchone()[0] > 0
        if not pool_exists:
            await ctx.respond(content=f"Pool '{pool}' does not exist! Please create it first.", ephemeral=True)
            cursor.close()
            mydb.close()
            print(f"Nevermind! {pool} does not exist!")
            return
        
        # Check if the user is permitted to submit to this pool, or if it is public.
        cursor.execute(f"SELECT visible FROM pools WHERE name = {pool}")
        visible = cursor.fetchone()[0]

        if not visible:
            # Check if the user is the owner of this pool.
            sql = "SELECT owner_id FROM pools WHERE name = %s"
            cursor.execute(sql, val)
            owner_id = cursor.fetchone()[0]
            if owner_id != ctx.author.id:
                await ctx.respond(content=f"You do not have permission to submit to pool '{pool}'.", ephemeral=True)
                cursor.close()
                mydb.close()
                print(f"Blocked! User {ctx.author.id} lacks permission to modify {pool}!")
                return

        # Store tip in the database
        sql = f"INSERT INTO pools_content (pool_id, content, submitter_id) VALUES (%s, %s, %s)"
        val = (pool, content.replace('"', '\"'), ctx.author.id)  # Escape single quotes
        cursor.execute(sql, val)
        mydb.commit()

        print(f"User {ctx.author.id} submitted to pool {pool} successfully!")
        await ctx.respond(content=f"Your submission has been saved to pool '{pool}'!", ephemeral=True)
        cursor.close()
        mydb.close()

    except Exception as e:
        print(f"Oh, fiddlesticks! What now... {e}?!")
        await ctx.respond(content=f"Uh oh, something went wrong: {e}. Please try again.", ephemeral=True)
        cursor.close()
        mydb.close()

# Print an index of pool things.
@pool.command(
    name="index",
    description="Print a Table of Contents for pools and their items.",
    integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install])
async def pool_index(
    ctx: discord.ApplicationContext,
    pool: Option(str, "The pool to view.", required=False),  # type: ignore
    all_pools: Option(bool, "View items from all users?", required=False, default=True)  # type: ignore
    ):
    try:
        # It'll freak out if we don't do this.
        reconnect_to_db()
        cursor = mydb.cursor()
        command = ""

        print(f"Index command called for pools...")

        # If no pool is specified, list all of them!
        if pool:
            command = "SELECT id, content FROM pools_content WHERE pool_id = '{pool}'"
        else:
            command = f"SELECT id, name FROM pools"

        # And if we're only looking at this one guy's stuff...
        if not all_pools:
            command = command + f" WHERE user_id = {ctx.author.id}"

        # And thus, we search for entries! And knowledge!!
        cursor.execute(command)
        entries = [(row[0], row[1]) for row in cursor.fetchall()]
        cursor.close()
        mydb.close()

        # Didn't find anything? That's too bad.
        if not entries:
            return await ctx.respond("No entries found in the pools database.")

        # Display that stuff!
        paginator = Paginator(entries)
        paginator.ctx = ctx
        paginator.message = await ctx.respond(embed=paginator.create_embed(), view=paginator)

    except Exception as e:
        print(f"Error retrieving entries: {e}")
        await ctx.respond(f"Uh oh, something went wrong: {e}")
        cursor.close()
        mydb.close()



# Commands involving the Stuffpile (TM).
stuff = bot.create_group(
    name="stuff",
    description="Commands relating to the use of the Stuffpile (TM).",
    integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install]
)

# Stuff submission fun
@stuff.command(
    name="submit",
    description="Submit something to the Stuffpile (TM)."
)
async def stuff_submit(
    ctx: discord.ApplicationContext,
    type: Option(str, "The type of submission you're making.", choices=['Person', 'Place', 'Thing'], required=True),  # type: ignore
    name: Option(str, "The name of your submission here.", required=True, max_length=256),  # type: ignore
    description: Option(str, "A detailed description of your submission.", required=True, max_length=4096),  # type: ignore
    image: Option(discord.Attachment, "An image of your submission.", required=True),  # type: ignore
    fact: Option(str, "A fun fact about your submission.", required=False, default="None provided.", max_length=1024)  # type: ignore
):
    print("Stuff submission command called!")
    await ctx.defer(ephemeral=False)

    try:
        # Connect to database.
        try:
            cursor = mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            reconnect_to_db()
            cursor = mydb.cursor()

        # Save the image.
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        random_suffix = ''.join(random.choice(string.ascii_letters) for _ in range(4)) 
        filename = f"thing_{timestamp}_{random_suffix}_{image.filename}" 
        saved_path = f"{UPLOADS_FOLDER}/{filename}"
        jpeg_path = f"{UPLOADS_FOLDER}/{filename}.jpg"
        await image.save(saved_path)
        print("Image saved!")

        # Compress the image
        try:
            with MagickImage(filename=f"{saved_path}[0]") as magick_img:
                # Convert to JPEG
                magick_img.format = 'jpeg'
                magick_img.compression_quality = 80  # Adjust quality as needed
                magick_img.save(filename=jpeg_path)
            print("Image compressed using PyMagick!")
        except Exception as e:
            await ctx.respond(content="Something went wrong processing the image. Your submission has NOT been saved.")
            print(f"Image NOT compressed! {e}")
            return  # End command execution if compression failed

        # Steal the dominant colour from the image.
        color_thief = ColorThief(f"{UPLOADS_FOLDER}/{filename}.jpg")
        dominant_color = color_thief.get_color(quality=5)
        hexcode = rgb2hex(*dominant_color)

        # Store thing in the database
        sql = f"INSERT INTO stuff (type, name, description, fact, image, submitter_id, colour) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (type, name.replace('"', '\"'), description.replace('"', '\"'), fact.replace('"', '\"'), filename, ctx.author.id, hexcode)
        cursor.execute(sql, val)
        mydb.commit()

        # Fetch ID of last upload.
        cursor.execute("SELECT LAST_INSERT_ID()")
        id = cursor.fetchone()[0]
        cursor.close()
        mydb.close()

        # Prepare it to send off to the user!
        embed = prepare_embed(name, description, hexcode, fact, id, filename)
        await ctx.respond(content=f"Your submission has been saved! ID: {id}",embed=embed,file=discord.File(jpeg_path))
        print(f"Stuff {id} submitted successfully!")

    except Exception as e:
        print(f"Oh, fiddlesticks! What now... {e}?!")
        await ctx.respond(content=f"Uh oh, something went wrong: {e}. Please try again.")
        cursor.close()
        mydb.close()

# Stuff retrieval fun
@stuff.command(
    name="find",
    description="Look around the Stuffpile (TM) in search of things."
)
async def stuff_find(
    ctx: discord.ApplicationContext,
    type: Option(str, "The type of thing you're looking for.", choices=['Person', 'Place', 'Thing'], required=False, default="Any"),  # type: ignore
    id: Option(int, "Specific image ID (overrides other options)", required=False, default=0)  # type: ignore
):
    try:
        # Connect to database
        try:
            cursor = mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            reconnect_to_db()
            cursor = mydb.cursor()

        try:
            if id == 0:
                if type == "Any":
                    # Grab a really random image.
                    sql = f"SELECT id, name, description, fact, image, colour FROM stuff WHERE visible = true ORDER BY RAND() LIMIT 1;"
                else:
                    # Grab a random image.
                    sql = f"SELECT id, name, description, fact, image, colour FROM stuff WHERE type = \"{type}\" AND visible = true ORDER BY RAND() LIMIT 1;"
            else:
                # Grab the specific image.
                sql = f"SELECT id, name, description, fact, image, colour FROM stuff WHERE id = \"{id}\" AND visible = true;"
            cursor.execute(sql)
            id, name, description, fact, image, hexcode = cursor.fetchone()
        except Exception as e:
            await ctx.respond(f"Submission with ID {id} not found!")
            return

        # Construct the image path.
        image_path = f"{UPLOADS_FOLDER}/{image}.jpg"
        print(f"Retrieved image path from DB: {image_path}")

        # Prepare it to send off to the user!
        embed = prepare_embed(name, description, hexcode, fact, id, image)
        await ctx.respond(content=f"Here's what I found!",embed=embed,file=discord.File(image_path))
        print(f"Thing {id} sent successfully!")
        cursor.close()
        mydb.close()

    except Exception as e:
        print(f"Error retrieving image: {e}")
        await ctx.respond(f"Uh oh, something went wrong: {e}")
        cursor.close()
        mydb.close()

# Stuff updating fun
@stuff.command(
    name="update",
    description="Update something in the Stuffpile (TM)."
)
async def stuff_update(
    ctx: discord.ApplicationContext,
    type: Option(str, "The type of edit you're making.", choices=['Image','Visibility'], required=True),  # type: ignore
    id: Option(int, "The ID of the submission to be updated.", required=True),  # type: ignore
    image: Option(discord.Attachment, "An updated image of your submission.", required=False)  # type: ignore
):
    print("Stuff submission command called!")
    await ctx.defer(ephemeral=False)

    try:
        # Connect to database.
        try:
            cursor = mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            reconnect_to_db()
            cursor = mydb.cursor()

		# Verify that the submission exists, because it would be terrible if it didn't.
        try:
            sql = f"SELECT id, name, description, fact, image, colour, visible FROM stuff WHERE id = \"{id}\" AND visible = true;"
            cursor.execute(sql)
            id, name, description, fact, filename, hexcode, visible = cursor.fetchone()
        except Exception as e:
            return await ctx.respond(f"Submission with ID {id} not found!")

        # Now, before we do anything else, fix some stuff so we can show the entries without anything weird happening.
        jpeg_path = f"{UPLOADS_FOLDER}/{filename}.jpg"

        match type:
            case "Image":
                # Save the new image.
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                random_suffix = ''.join(random.choice(string.ascii_letters) for _ in range(4))
                filename = f"thing_{timestamp}_{random_suffix}_{image.filename}"
                saved_path = f"{UPLOADS_FOLDER}/{filename}"
                await image.save(saved_path)
                print("Image saved!")

                # Compress the new image
                try:
                    from wand.image import Image as MagickImage
                    with MagickImage(filename=f"{saved_path}[0]") as magick_img:
                        # Convert to JPEG
                        magick_img.format = 'jpeg'
                        magick_img.compression_quality = 80  # Adjust quality as needed
                        magick_img.save(filename=jpeg_path)
                    print("Image compressed using PyMagick!")
                except Exception as e:
                    # USE THIS WHEN DEBUGGING await ctx.respond(content=f"Something went wrong processing the image: {e}")
                    await ctx.respond(content="Something went wrong processing the image. Your submission has NOT been saved.")
                    print(f"Image NOT compressed! {e}")
                    return  # End command execution if compression failed

                # Steal the dominant colour from the new image.
                color_thief = ColorThief(f"{UPLOADS_FOLDER}/{filename}.jpg")
                dominant_color = color_thief.get_color(quality=3)
                hexcode = rgb2hex(*dominant_color)

            case "Visibility":
                visible = not visible
                # Update database
                sql = f"UPDATE stuff SET visible = {visible} WHERE id = {id}"
                cursor.execute(sql)
                mydb.commit()
                cursor.close()
                mydb.close()
                return await ctx.respond(content=f"Submission {id} has successfully been hidden!")

        # Update database
        sql = f"UPDATE stuff SET image = '{filename}', colour = '{hexcode}', visible = {visible} WHERE id = {id};"
        cursor.execute(sql)
        mydb.commit()
        cursor.close()
        mydb.close()

        # Prepare it to send off to the user!
        embed = prepare_embed(name, description, hexcode, fact, id, filename)
        await ctx.respond(content=f"Submission {id} has successfully been updated!",embed=embed,file=discord.File(jpeg_path))
        print(f"Stuff {id} updated successfully!")

    except Exception as e:
        print(f"Oh, fiddlesticks! What now... {e}?!")
        await ctx.respond(content=f"Uh oh, something went wrong: {e}. Please try again.")
        cursor.close()
        mydb.close()


# Maintenance commands for admins.
maintenance = bot.create_group(
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
async def restart_bot(ctx):
    print("Restarting bot...")
    await ctx.respond("Restarting...", ephemeral=True)
    time.sleep(1)
    mydb.disconnect()

    # Crash the bot so whatever's running it can restart it.
    exit(1)

@maintenance.command(
    name="reprocess",
    description="Will reprocess an MP3 that's been uploaded, provided the original file still exists.",
    guild_ids=[GUILD_ID]
)
async def reencode(
    ctx: discord.ApplicationContext,
    upload_id: Option(int, "The archives_audio ID to be re-encoded.", required=True)
):
    print("Re-encoding an audio upload...")
    await ctx.defer(ephemeral=True)

    try:
        # Connect to database
        try:
            cursor = mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            reconnect_to_db()
            cursor = mydb.cursor()

        # Get upload details
        sql = f"SELECT original_path FROM archives_audio WHERE id = %s"
        val = (upload_id,)
        cursor.execute(sql, val)

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
        val = (out_path, upload_id)
        cursor.execute(sql, val)
        mydb.commit()
        cursor.close()
        mydb.close()

        await ctx.respond(content=f"Upload ID {upload_id} has been successfully re-encoded!", file=discord.File(out_path))
        print(f"Archives ID {upload_id} re-encoded successfully!")

    except Exception as e:
        print(f"Error during re-encode: {e}")


# Print an index of database things for fun reasons.

@bot.slash_command(
    name="index",
    description="Print a Table of Contents for items in the archives/stuffpile.",
    integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install])
async def index(
    ctx: discord.ApplicationContext,
    db: Option(str, "The database to view.", choices={'archives_image', 'archives_audio', 'stuff'}, required=True),  # type: ignore
    user: Option(discord.User, "The user to view entries for.", required=False)  # type: ignore
    ):
    try:
        # It'll freak out if we don't do this.
        reconnect_to_db()
        cursor = mydb.cursor()
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
        mydb.close()

        # Didn't find anything? That's too bad.
        if not entries:
            return await ctx.respond("No entries found in the database.")

        # Display that stuff!
        paginator = Paginator(entries)
        paginator.ctx = ctx
        paginator.message = await ctx.respond(embed=paginator.create_embed(), view=paginator)

    except Exception as e:
        print(f"Error retrieving entries: {e}")
        await ctx.respond(f"Uh oh, something went wrong: {e}")
        cursor.close()
        mydb.close()


# Epic context menu integration stuff (cool).

# CONTEXT MENU: Decode from Crypto
@bot.message_command(
    name="Crypto: Decode",
    integration_types=[discord.IntegrationType.user_install]
)
async def context_decode(
    ctx: discord.ApplicationContext,
    message: discord.Message
):
    print("(C) Decoding from Crypto.")
    import crypto
    message = crypto.decode_crypto(message.content)
    await ctx.respond(content=message, ephemeral=True)

# CONTEXT MENU: Submit quote
@bot.message_command(
    name="Submit Quote",
    integration_types=[discord.IntegrationType.user_install]
)
async def context_quote(
    ctx: discord.ApplicationContext,
    message: discord.Message
):
    print("(C) Submitting quote to DB.")

    # Get this guys stuff
    clean_content = message.content.replace('"', '\"')
    clean_uname = message.author.name.replace('"', '\"')

    try:
        # Connect to database.
        try:
            cursor = mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            reconnect_to_db()
            cursor = mydb.cursor()

        # Store quote in the database
        sql = f"INSERT INTO quotes (content, author, submitter_id) VALUES (%s, %s, %s)"
        val = (clean_content, clean_uname, ctx.author.id)
        cursor.execute(sql, val)
        mydb.commit()

        # Fetch ID of last upload.
        cursor.execute("SELECT LAST_INSERT_ID()")
        id = cursor.fetchone()[0]
        cursor.close()
        mydb.close()
        
        await ctx.respond(content=f"Your submission has been saved! ID: {id}\n> *\"{clean_content}\" - {clean_uname}*", ephemeral=True)
        print(f"Tip {id} submitted successfully!")

    except Exception as e:
        print(f"Oh, fiddlesticks! What now... {e}?!")
        await ctx.respond(content=f"Uh oh, something went wrong: {e}. Please try again.", ephemeral=True)
        cursor.close()
        mydb.close()

# CONTEXT MENU: Submit to archives
@bot.message_command(
    name="Submit to Archives",
    integration_types=[discord.IntegrationType.user_install]
)
async def context_archive(
    ctx: discord.ApplicationContext,
    message: discord.Message
):
    print("(C) Submitting to archives...")
    await ctx.defer(ephemeral=True)

    # Get the attachment from the message.
    attachment = message.attachments[0] if message.attachments else None
    if not attachment:
        await ctx.respond(content="No attachments found.", ephemeral=True)
        return

    response, error, comp_path, caption, upload_id = await submit_to_archives(attachment, message.content or "(C) No caption provided.", ctx.author.id)
    
    # If it's gone oh so horribly wrong, break the bad news.
    if error:
        await ctx.respond(content=response)
        return

    # Otherwise? We're swimmin'.
    if caption:
        await ctx.respond(content=f"File is now safe in the archives! ID: {upload_id}\n> {caption}",file=discord.File(comp_path))
    else:
        await ctx.respond(content=f"File is now safe in the archives! ID: {upload_id}",file=discord.File(comp_path))
    print(f"(C) Archives ID {upload_id} saved successfully!")

# CONTEXT MENU: Reaction
@bot.message_command(
    name="Reaction",
    integration_types=[discord.IntegrationType.user_install]
)
async def context_archive(
    ctx: discord.ApplicationContext,
    message: discord.Message
):
    print(f"(C) {ctx.author.id} is reacting to a message...")
    await ctx.defer()

    # This pulls the user's set image, quote, and audio from the DB and returns it as a reply.
    # Do note that users may have any combination of these set or unset.
    
    try:
        # Connect to database
        try:
            cursor = mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            reconnect_to_db()
            cursor = mydb.cursor()

        # Check if user exists in the DB
        sql = f"SELECT COUNT(*) FROM users WHERE id = %s"
        val = (ctx.author.id,)
        cursor.execute(sql, val)
        user_exists = cursor.fetchone()
        if not user_exists:
            return await ctx.respond("We don't know anything about you!\nPlease use `/reaction` to get started!", ephemeral=True)

        # Get user reaction details
        sql = f"SELECT image, quote, audio FROM users WHERE id = %s"
        val = (ctx.author.id,)
        cursor.execute(sql, val)

        # Check if reaction exists
        result = cursor.fetchone()
        if not result:
            return await ctx.respond("You have not set up a reaction yet!\n Please use `/reaction` to set one!", ephemeral=True)

        image, quote, audio = result

        # Prepare the response
        files = []

        if quote:
            embed = discord.Embed(title=quote)
            print(f"(C) Using quote for reaction: {quote}")
        else:
            embed = discord.Embed(title=f"{ctx.author.name}'s honest reaction")

        if image:
            # Fetch image path from archives
            cursor.execute(f"SELECT path FROM archives_image WHERE id = {image}")
            image_path, = cursor.fetchone()
            files.append(discord.File(image_path))
            filename = image_path.split("/")[-1]
            embed.set_image(url=f"attachment://{filename}")
            print(f"(C) Fetched image for reaction: {image_path}")

        if audio:
            # Fetch audio path from archives
            cursor.execute(f"SELECT path FROM archives_audio WHERE id = {audio}")
            audio_path, = cursor.fetchone()
            files.append(discord.File(str(audio_path)))
            print(f"(C) Fetched audio for reaction: {audio_path}")

        await ctx.respond(embed=embed, files=files)
        print(f"(C) Reaction from {ctx.author.id} sent successfully!")
        cursor.close()
        mydb.close()

    except Exception as e:
        print(f"Error retrieving reaction: {e}")
        await ctx.respond(f"Uh oh, something went wrong: {e}", ephemeral=True)
        cursor.close()
        mydb.close()


# Accompanying SET REACTION command
@bot.slash_command(
    name="set_reaction",
    description="Set any combination of quote.",
    integration_types=[discord.IntegrationType.user_install]
)
async def set_reaction(
    ctx: discord.ApplicationContext,
    quote: Option(str, "The full text of your favourite quote. This is NOT an ID.", required=False, default=0),  # type: ignore
    image_id: Option(int, "The archives image ID to use with your reaction.", required=False, default=0),  # type: ignore
    audio_id: Option(int, "The archives audio ID to use with your reaction.", required=False, default=0)  # type: ignore
):
    print(f"(C) {ctx.author.id} is setting their reaction...")
    await ctx.defer(ephemeral=True)

    try:
        # Connect to database
        try:
            cursor = mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            reconnect_to_db()
            cursor = mydb.cursor()

        # Check if user exists in the DB
        sql = f"SELECT COUNT(*) FROM users WHERE id = %s"
        val = (ctx.author.id,)
        cursor.execute(sql, val)
        user_exists = cursor.fetchone()[0] > 0

        if user_exists:
            # Update existing user
            sql = f"UPDATE users SET image = %s, quote = %s, audio = %s WHERE id = %s"
        else:
            # Create new user entry
            sql = f"INSERT INTO users (image, quote, audio, id) VALUES (%s, %s, %s, %s)"

        val = (image_id or None, quote or None, audio_id or None, ctx.author.id)
        cursor.execute(sql, val)
        mydb.commit()
        cursor.close()
        mydb.close()

        await ctx.respond(content="Your reaction has been set successfully!", ephemeral=True)
        print(f"(C) Reaction for {ctx.author.id} set successfully!")

    except Exception as e:
        print(f"Error setting reaction: {e}")
        await ctx.respond(f"Uh oh, something went wrong: {e}", ephemeral=True)
        cursor.close()
        mydb.close()



# Define special commands

# Submit to archives!
async def submit_to_archives(file, caption, author_id):
    try:
        saved_path, filename = await download_file(file)

        # Determine whether it's an image, audio, or neither.
        kind = filetype.guess(saved_path)
        if kind is not None:
            mime_type = kind.mime
            
            if mime_type.startswith("image/"): # INCOMING IMAGE!!
                print(f"Incoming {mime_type}... {saved_path}")
                db = "archives_image"
                comp_path = f"{UPLOADS_FOLDER}/{filename}.jpg"

                # Compress the image
                try:
                    from wand.image import Image as MagickImage
                    with MagickImage(filename=f"{saved_path}[0]") as magick_img:
                        magick_img.format = 'jpeg'
                        magick_img.compression_quality = 2  # Adjust quality as needed, but make sure it looks REALLY HORRIBLE. That's the whole point of the archives.
                        magick_img.save(filename=comp_path)
                    print("Image compressed using PyMagick!")
                except Exception as e:
                    print(f"Image NOT compressed! {e}")
                    return "Something went wrong processing the image. Your submission has NOT been saved.", True, None, None, None

            elif mime_type.startswith("audio/"): # INCOMING AUDIO!!
                print(f"Incoming {mime_type}... {saved_path}")
                # Add audio processing logic here
                db = "archives_audio"
                comp_path = f"{UPLOADS_FOLDER}/{filename}.mp3"

                # WAIT! Is it a MIDI file?
                if mime_type == "audio/midi" or mime_type == "audio/x-midi":
                    # Aw sweet let's go render us some midis
                    midi = True
                    saved_path = await synthesize_midi(saved_path)
                    if not saved_path:
                        return False
                else:
                    midi = False

                # Compress the audio
                try:
                    if midi:
                        audio = AudioSegment.from_file(f"{saved_path}.wav")
                    else:
                        audio = AudioSegment.from_file(saved_path)

                    # Crunch the audio for maximum effect!
                    audio = audio.set_channels(1).set_frame_rate(22050)  # 22.05kHz sample rate

                    # There used to be a low-pass high-pass filter put in, but I've had a change of heart.
                    # Music shouldn't be horrible to listen to, even if it is funny.
                    # ... But I reserve the right to change my mind about that later. And we DO have a kbps limit anyway.
                    # audio = audio.low_pass_filter(7000).high_pass_filter(100)

                    # Now export the audio!
                    out_ = audio.export(comp_path, format="mp3", bitrate="64k")
                    out_.close()

                    print("Audio compressed at 64kbps MP3!")
                except Exception as e:
                    print(f"Audio NOT compressed! {e}")
                    return "Something went wrong processing the audio. Your submission has NOT been saved.", True, None, None, None
            else:
                print("Unsupported filetype, aborting...")
                return "Uh oh, something went wrong.\nMaybe the filetype is unsupported?", True, None, None, None
        else:
            print("Could not determine file type, aborting...")
            return f"Sorry, we can't figure out what type of file you're uploading!", True, None, None, None

        # Connect to database.
        try:
            cursor = mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            reconnect_to_db()
            cursor = mydb.cursor()

        # Store file info in the database
        sql = f"INSERT INTO {db} (path, original_path, caption, submitter_id) VALUES (%s, %s, %s, %s)"
        val = (comp_path, saved_path, caption.replace('"', '\"'), author_id)  
        cursor.execute(sql, val)
        mydb.commit()

        # Fetch ID of last upload.
        cursor.execute("SELECT LAST_INSERT_ID()")
        upload_id = cursor.fetchone()[0]
        cursor.close()
        mydb.close()

        # Prep response
        return None, False, comp_path, caption or None, upload_id
    
    except Exception as e:
        print(f"Oh god, what now... {e}?!")
        cursor.close()
        mydb.close()
        return "Uh oh, something went wrong: {e}. Please try again.", True, None, None, None

# MIDI Synthesis
async def synthesize_midi(input):
    # Load the MIDI file
    midi = pretty_midi.PrettyMIDI(input)

    # Check for soundfont file
    if not SOUNDFONT:
        # Use default soundfont (boring)
        audio = midi.fluidsynth(fs=44100)
    else:
        # Use custom soundfont (awesome)
        audio = midi.fluidsynth(fs=44100, sf2_path=SOUNDFONT)

    # Save as WAV
    output = input + ".wav"
    sf.write(output, audio, 44100)
    return input # this is not a mistake; when requesting the original version of the file, it should return the midi, not the intermediate wav.

# Download a file into the uploads directory.
async def download_file(file):
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Generate 4 random characters
    random_suffix = ''.join(random.choice(string.ascii_letters) for _ in range(4)) 

    filename = f"{timestamp}_{random_suffix}_{file.filename}" 
    saved_path = f"{UPLOADS_FOLDER}/{filename}"
    await file.save(saved_path)
    print("File saved!")

    return saved_path, filename

# Database Connection Setup
def reconnect_to_db():
    global mydb  # Use global keyword to modify the global variable
    try:
        # Attempt to connect to our database.
        mydb = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )

        # Check if our tables exist.
        cursor = mydb.cursor()
        cursor.execute(f"USE {os.getenv('DB_NAME')}")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        if not tables:
            init_db()
        cursor.close()
        print("Connected to database!")

    # But if anything were to go very wrong...
    except mysql.connector.Error as err:
        if err.errno == 1049:  # This is the error code for "Unknown database", so let's try recreating it!
            init_db()
        else:
            # If you end up here, you should be very frustrated.
            print(f"Error connecting to database: {err}")
            restart_bot()

# Initialize the database from the schema in init.sql, in the case it doesn't exist.
def init_db():
    print("Attempting to recreate database from schema in init.sql...")
    try:
        cursor = mydb.cursor()
        with open('init.sql', 'r') as file:
            sql_script = file.read()
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        mydb.commit()
        # If you end up here, you should be very happy.
        print("Database initialized successfully!")
        cursor.close()
    except mysql.connector.Error as err:
        # If you end up here, you should be very confused.
        print(f"Error recreating database: {err}")
        print("THIS MIGHT CAUSE WEIRD THINGS TO HAPPEN IF YOU DON'T FIX IT!!")

# Run a command on this machine.
def runme(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        if result.returncode == 1:
            print("Error:", result.stderr)
            return("Error:", result.stderr)
        else:
            print("Error:", result.stderr)
            return("Error:", result.stderr)
    else:
        print(result.stdout)
        return("Command run successfully!")

# Tell Kanna to run a command on the other machine.
def sendit(command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            s.connect((KANNA_IP, PORT))
            s.sendall(command)
            data = s.recv(1024)
            print(f"Received: {data.decode()}")
            if data.decode() == "ok":
                return("Command ran successfully!")
            elif data.decode() == "bad":
                return("Command not found! Server is out of date!")
            elif data.decode() == "no":
                return("Command refused! Maybe it's not implemented yet?")
            else:
                return("Command failed!")

    except socket.timeout:
        return("Connection timed out.")
    except socket.error as e:
        return(f"Connection error: {e}")

# Convert RGB values to HEX because who the hell needs RGB values.
def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

# Convert HEX back to RGB because I hate optimization.
def hex2rgb(hexcode):
    return tuple(map(ord,hexcode[1:].decode('hex')))

# Create neat embeds for items in the Stuffpile (TM).
def prepare_embed(name, description, hexcode, fact, id, image):
    embed = discord.Embed(
        title=name,
        description=description,
        color=discord.Color.from_rgb(*ImageColor.getrgb(hexcode)),
    )
    embed.add_field(name="Fun Fact:", value=fact)
    embed.set_footer(text=f"ID: {id}")
    embed.set_image(url=f"attachment://{image}.jpg")
    return embed

# DEFINE SPECIAL MOMENTS

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

# Paginator for seeing archives entries
class Paginator(View):
    def __init__(self, entries, per_page=25):
        super().__init__()
        self.entries = entries
        self.per_page = per_page
        self.current_page = 0
        self.total_pages = (len(entries) - 1) // per_page + 1
        self.update_buttons()

    async def interaction_check(self, interaction):
        # If the OG user is the one pushing the button, let's roll.
        print(f"Button pressed! {self.ctx.author} == {interaction.user}?")
        if interaction.user == self.ctx.author:
            if interaction.custom_id == "previous":
                print("Going back to the previous page!")
                await self.turn_page(interaction, -1)
            elif interaction.custom_id == "next":
                print("Going forward to the next page!")
                await self.turn_page(interaction, 1)
        return False

    async def on_timeout(self):
        # Don't hold onto the past. You need to let it go.
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def turn_page(self, interaction, direction):
        # Go to the next/previous page and update the buttons.
        self.current_page += direction
        self.update_buttons()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    def update_buttons(self):
        # Clear the current buttons and add new ones based on where we are in spacetime.
        self.clear_items()
        if self.current_page > 0:
            self.add_item(Button(label="Previous", style=discord.ButtonStyle.primary, custom_id="previous"))
        if self.current_page < self.total_pages - 1:
            self.add_item(Button(label="Next", style=discord.ButtonStyle.primary, custom_id="next"))

    def create_embed(self):
        # List all of our stuff, and make it look all fancy, ooh.
        start = self.current_page * self.per_page
        end = start + self.per_page
        entries = self.entries[start:end]
        formatted_entries = [f"**{id}:** {name}" for id, name in entries]
        embed = discord.Embed(title="Table of Contents", description="\n".join(formatted_entries))
        embed.set_footer(text=f"Page {self.current_page + 1} of {self.total_pages}")
        return embed


# When the bot is ready to take on the world...
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your every move."))


# Just wait a moment for the DB to kick in...
time.sleep(5)
reconnect_to_db()

# And now we run it!
print("Bot running!")
bot.run(BOT_TOKEN)
