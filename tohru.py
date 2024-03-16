# for connection to discord
import discord
from discord.ext import commands
from discord import Option

# for connection to sauceypc
import subprocess
import socket
import time

# for image upload stuff
from dotenv import load_dotenv
import os
import random
import string
import mysql.connector
from PIL import Image
from datetime import datetime

# Define stuff.
load_dotenv()
bot = commands.Bot()
BOT_TOKEN = os.getenv('BOT_TOKEN')
intents = discord.Intents.default()
client = discord.Client(intents=intents)
HOST = os.getenv('HOST')
PORT = 10524
TIMEOUT = 5


# Database Connection Setup
mydb = mysql.connector.connect(
    host = os.getenv('DB_HOST'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    database = os.getenv('DB_NAME')
)

# Check if we're live.
@bot.slash_command(
    name="ping",
    description="Checks if Tohru (the maid) is awake..",
    guild_ids=[1075360335810269216]
)
async def ping(ctx):
    print("Executing ping command.")
    await ctx.respond("Ping pong! I'm still alive!")

# Connection test to SAUCEY-PC.
@bot.slash_command(
    name="connect",
    description="Checks if Kanna (the friend) is awake.",
    guild_ids=[1075360335810269216]
)
async def connect(ctx):
    print("Executing connection command.")
    await ctx.defer()
    response = sendit(b"connect")
    print(response)
    await ctx.respond(response)

# Mount the drives that Ubuntu is too scared to.
@bot.slash_command(
    name="mount",
    description="Mounts all drives in case of broken website.",
    guild_ids=[1075360335810269216]
)
async def mount(ctx):
    print("Executing mount command.")
    response = runme("sudo mount -a")
    await ctx.respond(response)

# Instantly opens Death Stranding on the SAUCEY-PC.
@bot.slash_command(
    name="gaming",
    description="Launches Death Stranding on Josh's computer.",
    guild_ids=[1075360335810269216]
)
async def gaming(ctx):
    print("Executing Death Stranding command.")
    response = sendit(b"gaming")
    await ctx.respond(response)

# Restarts Plex in the likely event of a crash.
@bot.slash_command(
    name="plex",
    description="Launches Plex in the event of it crashing.",
    guild_ids=[1075360335810269216]
)
async def plex(ctx):
    print("Executing Plex command.")
    response = sendit(b"plex")
    await ctx.respond(response)

# Restarts the bot. Ends early so it looks nice on the Discord-side of things.
@bot.slash_command(
    name="restart",
    description="Restarts Tohru to reload any changes.",
    guild_ids=[1075360335810269216]
)
async def restart(ctx):
    print("Restarting bot...")
    await ctx.respond("Restarting Tohru...")
    response = runme("sudo supervisorctl restart tohru")

# image upload fun
@bot.slash_command(
    name="upload",
    description="Upload a horribly compressed image with a caption",
    guild_ids=[1075360335810269216]
    )
async def upload(
    ctx: discord.ApplicationContext, 
    image: Option(discord.Attachment, "Choose an image to upload", required=True),
    caption: Option(str, "Add a caption (optional)", required=False) = "No caption provided"
):
    print("Upload command called!")
    await ctx.respond("Archiving image...")
    print("Responded in time! AS ALWAYS, DISCORD!!")

    try:
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Generate 4 random characters
        random_suffix = ''.join(random.choice(string.ascii_letters) for _ in range(4)) 

        filename = f"{timestamp}_{image.filename}_{random_suffix}" 
        saved_path = f"uploads/{filename}"
        jpeg_path = f"uploads/{filename}.jpg"
        await image.save(saved_path)
        print("Image saved!")

        # Compress the image
        try:
            img = Image.open(saved_path)
            img.save(jpeg_path, format='JPEG', quality=1)
            print("Image compressed...")
        except Exception as e:
            await ctx.respond(f"Something went wrong compressing the image: {e}")
            print(f"Image NOT compressed! {e}")
            return  # End command execution if compression failed

        # Store image info in the database
        cursor = mydb.cursor()
        sql = "INSERT INTO images (image_path, caption, submitter_id) VALUES (%s, %s, %s)"
        val = (saved_path, caption, ctx.author.id)  
        cursor.execute(sql, val)
        mydb.commit()

        await ctx.edit(content="Image is now safe in the archives!")
        print("HOLY BALLS WE DID IT")

    except Exception as e:
        print(f"Oh god, what now... {e}?!")
        await ctx.edit(content=f"Uh oh, something went wrong: {e}. Please try again.")


# Define special commands
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

def sendit(command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            s.connect((HOST, PORT))
            s.sendall(command)
            data = s.recv(1024)
            print(f"Received: {data.decode()}")
            if data.decode() == "ok":
                return("Command ran successfully!")
            elif data.decode() == "bad":
                return("Command not found! Server is out of date!")
            elif data.decode() == "no":
                return("Command refused!")
            else:
                return("Command failed!")

    except socket.timeout:
        return("Connection timed out.")
    except socket.error as e:
        return(f"Connection error: {e}")


# And now we run it!
print("Bot running!")
bot.run(BOT_TOKEN)
