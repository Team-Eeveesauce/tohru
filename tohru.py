import discord
from discord.ext import commands
import subprocess
import socket
import time
HOST = '10.10.0.195'
PORT = 10524

# Define stuff.
bot = commands.Bot()
BOT_TOKEN = 'MTIxNjI1MTM1NDI0NzU5ODE3MQ.GAEGbL.-B4QONFDtbMat5VIkNC-cqgS5Y1NuuwjwogqW0'
intents = discord.Intents.default()
client = discord.Client(intents=intents)


# This tree holds all of our application commands.
@bot.slash_command(
    name="ping",
    guild_ids=[1075360335810269216]
)
async def first_slash(ctx):
    print("Executing ping command.")
    await ctx.respond("Ping pong! I'm still alive!")

@bot.slash_command(
    name="mount",
    description="Mounts all drives in case of broken website.",
    guild_ids=[1075360335810269216]
)
async def mount(ctx):
    print("Executing mount command.")
    response = runme("sudo mount -a")
    await ctx.respond(response)

@bot.slash_command(
    name="gaming",
    description="Launches Death Stranding on Josh's computer.",
    guild_ids=[1075360335810269216]
)
async def gaming(ctx):
    print("Executing Death Stranding command.")
    response = runme("\"C:\\Program Files (x86)\\Epic Games\\Launcher\\Portal\\Binaries\\Win32\\EpicGamesLauncher.exe\"")
    await ctx.respond(response)

@bot.slash_command(
    name="plex",
    description="Launches Plex in the event of it crashing.",
    guild_ids=[1075360335810269216]
)
async def plex(ctx):
    print("Executing Plex command.")
    response = runme("\"C:\\Program Files\\Plex\\Plex Media Server\\Plex Media Server.exe\"")
    await ctx.respond(response)

@bot.slash_command(
    name="connect",
    description="Tests a connection between two computers on a network.",
    guild_ids=[1075360335810269216]
)
async def connect(ctx):
    print("Executing connection command.")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Master listening...")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            conn.sendall(b"plex")
            
            response = conn.recv(1024).decode()  # Receive "ok im going now"
            print(response)

            # Wait for additional results later...
            results = conn.recv(1024).decode()
            print("Results:", results)
    await ctx.respond(response)


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


# And now we run it!
print("Bot running!")
bot.run(BOT_TOKEN) 
