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

# for image upload stuff
import pymagick
import mysql.connector
from datetime import datetime
from colorthief import ColorThief
from PIL import ImageColor

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

# Mount the drives that Ubuntu is too scared to.
@bot.slash_command(
    name="mount",
    description="Mounts all drives in case of broken website.",
    guild_ids=[GUILD_ID]
)
async def mount(ctx):
    print("Executing mount command...")
    response = runme("sudo mount -a")
    await ctx.respond(response)

# Restart szurubooru because it sucks.
@bot.slash_command(
    name="debug",
    description="Runs the debug script that you probably don't need to run.",
    guild_ids=[GUILD_ID]
)
async def debug(ctx):
    print("Running debug script.")
    response = runme("./scripts/dragonmaid_debug.sh")
    await ctx.respond(response)

# Instantly opens Death Stranding on the SAUCEY-PC.
@bot.slash_command(
    name="gaming",
    description="Launches Death Stranding on Josh's computer.",
    guild_ids=[GUILD_ID]
)
async def gaming(ctx):
    print("Executing Death Stranding command.")
    response = sendit(b"gaming")
    await ctx.respond(response)

# Downloads new videos from AstralSpiff.
@bot.slash_command(
    name="download_spigg",
    description="Attempts to download any new AstralSpiff videos into the archives.",
    guild_ids=[GUILD_ID]
)
async def download_spigg(ctx):
    print("Executing YT-DLP (spigg) command.")
    response = sendit(b"download_spigg")
    await ctx.respond(response)

# Repeat whatever is said.
@bot.slash_command(
    name="echo",
    description="Make Tohru say something."
)
async def echo(
    ctx: discord.ApplicationContext,
    content: Option(str, "Your message here!", required=True)
):
    print("Executing ping command.")
    await ctx.respond("I gotchu, bro.", ephemeral=True)
    await ctx.send(content=content)


# Commands that ping stuff.
ping = bot.create_group(
    name="ping",
    description="Commands relating to the pinging of services."
#    integration_types=["GUILD_INSTALL", "USER_INSTALL"],
#    contexts=["GUILD","BOT_DM","PRIVATE_CHANNEL"]
)

# Check if we're live.
@ping.command(
    name="tohru",
    description="Checks if this bot is awake."
)
async def ping_tohru(ctx):
    print("Executing ping command.")
    await ctx.respond("Ping pong! I'm still alive!")

# Connection test to SAUCEY-PC.
@ping.command(
    name="kanna",
    description="Checks if the helper service is awake."
)
async def ping_kanna(ctx):
    print("Executing connection command.")
    await ctx.defer()
    response = sendit(b"connect")
    print(response)
    await ctx.respond(response)


# Commands that restart stuff.
restart = bot.create_group(
    name="restart",
    description="Commands relating to the restarting of services.",
    guild_ids=[GUILD_ID]
)

# Restarts the bot. Ends early so it looks nice on the Discord-side of things.
@restart.command(
    name="bot",
    description="Restarts Tohru to reload any changes."
)
async def restart_bot(ctx):
    print("Restarting bot...")
    await ctx.respond("Restarting Tohru...", ephemeral=True)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your every move."))
    await bot.close()
    response = runme("sudo supervisorctl restart tohru")

# Restarts Emby in the unlikely event of a crash.
@restart.command(
    name="emby",
    description="Launches Emby in the event of it crashing."
)
async def restart_emby(ctx):
    print("Executing Emby command.")
    response = sendit(b"emby")
    await ctx.respond(response)

# Restart szurubooru because it sucks.
@restart.command(
    name="szurubooru",
    description="Restarts szurubooru after a power failure."
)
async def restart_szurubooru(ctx):
    print("Restarting szurubooru...")
    response = runme("scripts/mountbooru.sh")
    await ctx.respond(response)


# Commands involving the archives system.
archives = bot.create_group(
    name="archives",
    description="Commands relating to the use of the Archives feature."
)

# Image upload fun
@archives.command(
    name="upload",
    description="Upload a horribly compressed image with a caption"
)
async def archives_upload(
    ctx: discord.ApplicationContext, 
    image: Option(discord.Attachment, "Choose an image to upload", required=True),
    caption: Option(str, "Add a caption (optional)", required=False) = ""
):
    print("Upload command called!")
    await ctx.defer(ephemeral=True)
    print("Responded in time! AS ALWAYS, DISCORD!!")

    try:
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Generate 4 random characters
        random_suffix = ''.join(random.choice(string.ascii_letters) for _ in range(4)) 

        filename = f"{timestamp}_{random_suffix}_{image.filename}" 
        saved_path = f"uploads/{filename}"
        jpeg_path = f"uploads/{filename}.jpg"
        await image.save(saved_path)
        print("Image saved!")

        # Compress the image
        try:
            from wand.image import Image as MagickImage
            with MagickImage(filename=f"{saved_path}[0]") as magick_img:
                magick_img.format = 'jpeg'
                magick_img.compression_quality = 2  # Adjust quality as needed
                magick_img.save(filename=jpeg_path)
            print("Image compressed using PyMagick!")
        except Exception as e:
            # USE THIS WHEN DEBUGGING await ctx.respond(content=f"Something went wrong processing the image: {e}")
            await ctx.respond(content="Something went wrong processing the image. Your submission has NOT been saved.")
            print(f"Image NOT compressed! {e}")
            return  # End command execution if compression failed

        # Steal the dominant colour from the image.
        color_thief = ColorThief(saved_path)
        dominant_color = color_thief.get_color(quality=1)

        # Connect to database.
        try:
            cursor = mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            reconnect_to_db()
            cursor = mydb.cursor()

        # Store image info in the database
        sql = "INSERT INTO images (image_path, original_path, caption, submitter_id) VALUES (%s, %s, %s, %s)"
        val = (jpeg_path, saved_path, caption.replace('"', '\"'), ctx.author.id)  
        cursor.execute(sql, val)
        mydb.commit()

        # Fetch ID of last upload via the total count of entries in the archive (bad idea but it should work if nothing went wrong).
        sql = "SELECT COUNT(*) FROM images"
        cursor.execute(sql)
        upload_id = cursor.fetchone()[0]
        cursor.close()
        print("HOLY BALLS WE DID IT")
        
        # Send image
        if caption:
            await ctx.respond(content=f"Image is now safe in the archives! ID: {upload_id}\n> {caption}",file=discord.File(jpeg_path))
        else:
            await ctx.respond(content=f"Image is now safe in the archives! ID: {upload_id}",file=discord.File(jpeg_path))
        print(f"Image ID {upload_id} sent successfully!")

    except Exception as e:
        print(f"Oh god, what now... {e}?!")
        await ctx.respond(content=f"Uh oh, something went wrong: {e}. Please try again.")
        cursor.close()

# Image retrieval fun
@archives.command(
    name="fetch",
    description="Retrieve a previously uploaded image"
)
async def archives_fetch(
    ctx: discord.ApplicationContext,
    image_id: Option(int, "Specific image ID (set as 0 for random)", required=True),
    uncompressed: Option(bool, "Send the uncompressed version of the image?", default=False)
):
    try:
        # Connect to database
        try:
            cursor = mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            reconnect_to_db()
            cursor = mydb.cursor()

        if image_id == 0: # If they asked for a random image.
            # Count total images
            sql = "SELECT COUNT(*) FROM images"
            cursor.execute(sql)
            total_images = cursor.fetchone()[0]

            if not total_images:
                return await ctx.respond("No images found in the archive!")

            # Generate random number within image count
            image_id = random.randint(1, total_images)

        # Get image details
        if uncompressed:
            sql = "SELECT original_path, caption FROM images WHERE id = %s"
        else:
            sql = "SELECT image_path, caption FROM images WHERE id = %s"
        val = (image_id,)
        cursor.execute(sql, val)

        # Check if image exists
        result = cursor.fetchone()
        if not result:
            return await ctx.respond(f"Image with ID {image_id} not found!")

        image_path, caption = result
        print(f"Retrieved image path from DB: {image_path}")

        # Send image
        if caption:
            await ctx.respond(content=f"Here you go, boss! (ID: {image_id})\n> {caption}",file=discord.File(image_path))
        else:
            await ctx.respond(content=f"Here you go, boss! (ID: {image_id})",file=discord.File(image_path))
        print(f"Image ID {image_id} sent successfully!")
        cursor.close()

    except Exception as e:
        print(f"Error retrieving image: {e}")
        await ctx.respond(f"Uh oh, something went wrong: {e}")
        cursor.close()


# Commands involving the tips system.
tips = bot.create_group(
    name="tip",
    description="Loading screen tips! Or quotes! Both!!"
)

# Tip submission fun
@tips.command(
    name="submit",
    description="Submit a loading screen tip or quote here."
)
async def tips_submit(
    ctx: discord.ApplicationContext,
    type: Option(str, "Whatever type of submission you're looking to make.", choices=['Tip', 'Quote'], required=True),
    content: Option(str, "Type your submission here.", required=True, max_length=4096),
    author: Option(str, "Whoever said the quote.", required=False, default="Anonymous", max_length=256)
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

    except Exception as e:
        print(f"Error retrieving submission: {e}")
        await ctx.respond(f"Uh oh, something went wrong: {e}")
        cursor.close()


# Commands involving the Stuffpile (TM).
stuff = bot.create_group(
    name="stuff",
    description="Commands relating to the use of the Stuffpile (TM)."
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
    await ctx.defer(ephemeral=True)

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

        # Steal the dominant colour from the image.
        color_thief = ColorThief(f"uploads/{filename}.jpg")
        dominant_color = color_thief.get_color(quality=2)
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
        print("HOLY BALLS WE DID IT")

        # Prepare it to send off to the user!
        embed = prepare_embed(name, description, hexcode, fact, id, hexcode)
        await ctx.respond(content=f"Your submission has been saved! ID: {id}",embed=embed,file=discord.File(jpeg_path))
        print(f"Stuff {id} submitted successfully!")

    except Exception as e:
        print(f"Oh, fiddlesticks! What now... {e}?!")
        await ctx.respond(content=f"Uh oh, something went wrong: {e}. Please try again.")
        cursor.close()

# Stuff retrieval fun
@stuff.command(
    name="find",
    description="Look around the Stuffpile (TM) in search of things."
)
async def stuff_find(
    ctx: discord.ApplicationContext,
    type: Option(str, "The type of thing you're looking for.", choices=['Person', 'Place', 'Thing'], required=True)
):
    try:
        # Connect to database
        try:
            cursor = mydb.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")
            reconnect_to_db()
            cursor = mydb.cursor()

        # Grab a random image
        sql = f"SELECT id, name, description, fact, image, colour FROM stuff WHERE type = \"{type}\" AND visible = true ORDER BY RAND() LIMIT 1;"
        cursor.execute(sql)
        id, name, description, fact, image, hexcode = cursor.fetchone()

        # Construct the image path.
        image_path = f"uploads/{image}.jpg"
        print(f"Retrieved image path from DB: {image_path}")

        # Prepare it to send off to the user!
        embed = prepare_embed(name, description, hexcode, fact, id, image)
        await ctx.respond(content=f"Here's what I found!",embed=embed,file=discord.File(image_path))
        print(f"Thing {id} sent successfully!")
        cursor.close()

    except Exception as e:
        print(f"Error retrieving image: {e}")
        await ctx.respond(f"Uh oh, something went wrong: {e}")
        cursor.close()

# Stuff location fun
@stuff.command(
    name="locate",
    description="Find an item in the Stuffpile (TM) by ID."
)
async def stuff_locate(
    ctx: discord.ApplicationContext,
    id: Option(int, "The ID of the thing you're looking for.", required=True)
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
            # Grab the image
            sql = f"SELECT id, name, description, fact, image, colour FROM stuff WHERE id = \"{id}\" AND visible = true;"
            cursor.execute(sql)
            id, name, description, fact, image, hexcode = cursor.fetchone()
        except Exception as e:
            return await ctx.respond(f"Submission with ID {id} not found!")

        # Construct the image path.
        image_path = f"uploads/{image}.jpg"
        print(f"Retrieved image path from DB: {image_path}")

        # Prepare it to send off to the user!
        embed = prepare_embed(name, description, hexcode, fact, id, image)
        await ctx.respond(content=f"Here's what I found!",embed=embed,file=discord.File(image_path))
        print(f"Thing {id} sent successfully!")
        cursor.close()

    except Exception as e:
        print(f"Error retrieving image: {e}")
        await ctx.respond(f"Uh oh, something went wrong: {e}")
        cursor.close()


# Define special commands

# Database Connection Setup
def reconnect_to_db():
    global mydb  # Use global keyword to modify the global variable
    try:
        mydb = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")

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
def prepare_embed(name,description, hexcode, fact, id, image):
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


# And now we run it!
reconnect_to_db()
print("Bot running!")
bot.run(BOT_TOKEN)
