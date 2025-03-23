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
import mimetypes
from pydub import AudioSegment # pip install pydub

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
    content: Option(str, "Your message here!", required=True)
):
    print("Executing ping command.")
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
    content: Option(str, "Your message here!", required=True, max_length=333)
):
    print("Encoding to Crypto.")
    import crypto
    message = crypto.encode_crypto(content)
    await ctx.respond(content=message, ephemeral=True)

# Decode from Crypto
@crypto.command(
    name="decode",
    description="Decode something from Crypto code."
)
async def crypto_decode(
    ctx: discord.ApplicationContext,
    content: Option(str, "Crypto code here!", required=True)
):
    print("Decoding from Crypto.")
    import crypto
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
    file: Option(discord.Attachment, "Choose a file to upload", required=True),
    caption: Option(str, "Add a caption/title to help identify the upload!", required=False) = ""
):
    print("Upload command called!")
    await ctx.defer(ephemeral=True)
    print("Responded in time! AS ALWAYS, DISCORD!!")

    try:
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Generate 4 random characters
        random_suffix = ''.join(random.choice(string.ascii_letters) for _ in range(4)) 

        filename = f"{timestamp}_{random_suffix}_{file.filename}" 
        saved_path = f"uploads/{filename}"
        await file.save(saved_path)
        print("File saved!")

        # Determine whether it's an image, audio, or neither.
        mime_type, _ = mimetypes.guess_type(saved_path)
        if mime_type:
            if mime_type.startswith("image/"): # INCOMING IMAGE!!
                print(f"Incoming IMAGE... {saved_path}")
                db = "archives_image"
                comp_path = f"uploads/{filename}.jpg"

                # Compress the image
                try:
                    from wand.image import Image as MagickImage
                    with MagickImage(filename=f"{saved_path}[0]") as magick_img:
                        magick_img.format = 'jpeg'
                        magick_img.compression_quality = 2  # Adjust quality as needed, but make sure it looks REALLY HORRIBLE. That's the whole point of the archives.
                        magick_img.save(filename=comp_path)
                    print("Image compressed using PyMagick!")
                except Exception as e:
                    # USE THIS WHEN DEBUGGING await ctx.respond(content=f"Something went wrong processing the image: {e}")
                    await ctx.respond(content="Something went wrong processing the image. Your submission has NOT been saved.")
                    print(f"Image NOT compressed! {e}")
                    return  # End command execution if compression failed

            elif mime_type.startswith("audio/"): # INCOMING AUDIO!!
                print(f"Incoming AUDIO... {saved_path}")
                # Add audio processing logic here
                db = "archives_audio"
                comp_path = f"uploads/{filename}.mp3"

                # Compress the audio
                try:
                    audio = AudioSegment.from_file(saved_path)

                    # Convert to mono and slightly downsample for some degradation
                    audio = audio.set_channels(1).set_frame_rate(22050)  # 22.05kHz sample rate

                    # Apply slight filtering to mimic early 2000s MP3 compression
                    audio = audio.low_pass_filter(7000).high_pass_filter(100)

                    # Export with 64kbps MP3 compression
                    audio.export(comp_path, format="mp3", bitrate="64k")

                    print("Audio compressed at 64kbps MP3!")
                except Exception as e:
                    await ctx.respond(content="Something went wrong processing the audio. Your submission has NOT been saved.")
                    print(f"Audio NOT compressed! {e}")
                    return  # End command execution if compression failed

            else:
                print("Unsupported filetype, aborting...")
                await ctx.respond(content=f"Uh oh, something went wrong.\nMaybe the filetype is unsupported?")
                return
        else:
            print("Could not determine file type, aborting...")
            await ctx.respond(content=f"Uh oh, something went wrong.\nAre you sure you're uploading an image or audio file?")
            return


        # Connect to database.
        try:
            cursor = mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            reconnect_to_db()
            cursor = mydb.cursor()

        # Store file info in the database
        sql = f"INSERT INTO {db} (path, original_path, caption, submitter_id) VALUES (%s, %s, %s, %s)"
        val = (comp_path, saved_path, caption.replace('"', '\"'), ctx.author.id)  
        cursor.execute(sql, val)
        mydb.commit()

        # Fetch ID of last upload via the total count of entries in the archive (bad idea but it should work if nothing went wrong).
        sql = f"SELECT COUNT(*) FROM {db}"
        cursor.execute(sql)
        upload_id = cursor.fetchone()[0]
        cursor.close()
        mydb.close()
        print("HOLY BALLS WE DID IT")
        
        # Send image
        if caption:
            await ctx.respond(content=f"File is now safe in the archives! ID: {upload_id}\n> {caption}",file=discord.File(comp_path))
        else:
            await ctx.respond(content=f"File is now safe in the archives! ID: {upload_id}",file=discord.File(comp_path))
        print(f"Archives ID {upload_id} sent successfully!")

    except Exception as e:
        print(f"Oh god, what now... {e}?!")
        await ctx.respond(content=f"Uh oh, something went wrong: {e}. Please try again.")
        cursor.close()
        mydb.close()

# Archives retrieval fun
@archives.command(
    name="fetch",
    description="Retrieve a file from the archives."
)
async def archives_fetch(
    ctx: discord.ApplicationContext,
    type: Option(str, "The type of upload to be fetched.", choices=['Image', 'Audio'], required=True),
    upload_id: Option(int, "Specific upload ID", required=False, default=0),
    uncompressed: Option(bool, "Send the uncompressed version of the upload?", default=False)
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
    type: Option(str, "Whether you are submitting a tip or a quote.", choices=['Tip', 'Quote'], required=True),
    content: Option(str, "Type your submission here.", required=True, max_length=4096),
    author: Option(str, "The person that the tip/quote originated from.", required=False, default="Anonymous", max_length=256)
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

        # Fetch ID of last upload via the total count of entries in the archive (bad idea but it should work if nothing went wrong).
        sql = f"SELECT COUNT(*) FROM {db}"
        cursor.execute(sql)
        id = cursor.fetchone()[0]
        cursor.close()
        mydb.close()
        print("HOLY BALLS WE DID IT")

        if type == "Tip":
            await ctx.respond(content=f"Your submission has been saved! ID: {id}\n> {content}", ephemeral=True)
        else:
            await ctx.respond(content=f"Your submission has been saved! ID: {id}\n> *\"{content}\" - {author}*", ephemeral=True)

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
    type: Option(str, "What type of submission you're looking for.", choices=['Tip', 'Quote'], required=True),
    id: Option(int, "Specific submission ID (leave blank for random)", required=False, default=0)
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
    type: Option(str, "The type of submission you're making.", choices=['Person', 'Place', 'Thing'], required=True),
    name: Option(str, "The name of your submission here.", required=True, max_length=256),
    description: Option(str, "A detailed description of your submission.", required=True, max_length=4096),
    image: Option(discord.Attachment, "An image of your submission.", required=True),
    fact: Option(str, "A fun fact about your submission.", required=False, default="None provided.", max_length=1024)
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
        saved_path = f"uploads/{filename}"
        jpeg_path = f"uploads/{filename}.jpg"
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
        color_thief = ColorThief(f"uploads/{filename}.jpg")
        dominant_color = color_thief.get_color(quality=5)
        hexcode = rgb2hex(*dominant_color)

        # Store thing in the database
        sql = f"INSERT INTO stuff (type, name, description, fact, image, submitter_id, colour) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (type, name.replace('"', '\"'), description.replace('"', '\"'), fact.replace('"', '\"'), filename, ctx.author.id, hexcode)
        cursor.execute(sql, val)
        mydb.commit()

        # Fetch ID of last upload via the total count of entries in the archive (bad idea but it should work if nothing went wrong).
        sql = f"SELECT COUNT(*) FROM stuff"
        cursor.execute(sql)
        id = cursor.fetchone()[0]
        cursor.close()
        mydb.close()
        print("HOLY BALLS WE DID IT")

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
    type: Option(str, "The type of thing you're looking for.", choices=['Person', 'Place', 'Thing'], required=False, default="Any"),
    id: Option(int, "Specific image ID (overrides other options)", required=False, default=0)
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
        image_path = f"uploads/{image}.jpg"
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
    type: Option(str, "The type of edit you're making.", choices=['Image','Visibility'], required=True),
    id: Option(int, "The ID of the submission to be updated.", required=True),
    image: Option(discord.Attachment, "An updated image of your submission.", required=False)
):
    print("Stuff submission command called!")
    await ctx.defer(ephemeral=True)

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
        jpeg_path = f"uploads/{filename}.jpg"

        match type:
            case "Image":
                # Save the new image.
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                random_suffix = ''.join(random.choice(string.ascii_letters) for _ in range(4))
                filename = f"thing_{timestamp}_{random_suffix}_{image.filename}"
                saved_path = f"uploads/{filename}"
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
                color_thief = ColorThief(f"uploads/{filename}.jpg")
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
        print("HOLY BALLS WE DID IT")

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


# Epic context menu integration stuff (cool).

# CONTEXT MENU: Decode from Crypto
@bot.message_command(
    name="Decode (Crypto)",
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

        # Fetch ID of last upload via the total count of entries in the archive (bad idea but it should work if nothing went wrong).
        sql = f"SELECT COUNT(*) FROM quotes"
        cursor.execute(sql)
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


# Define special commands

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
        print("Connected to database!")

    # But if anything were to go very wrong...
    except mysql.connector.Error as err:
        if err.errno == 1049:  # This is the error code for "Unknown database". Let's try recreating it!
            print(f"Database '{os.getenv('DB_NAME')}' not found! Attempting to recreate it...")
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
        else:
            # If you end up here, you should be very frustrated.
            print(f"Error connecting to database: {err}")
            restart_bot()

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
                await message.channel.send('Well that\'s not very nice...')
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


# Just wait a moment for the DB to kick in...
time.sleep(5)
reconnect_to_db()

# And now we run it!
print("Bot running!")
bot.run(BOT_TOKEN)
