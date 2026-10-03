# standard discord bs
import discord
from discord.ext import commands
from discord import Option

import utils.tohrudb
import os
import asyncio

GUILD_ID = os.getenv('GUILD_ID')

class Maintenance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mydb = utils.tohrudb.get_db()

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

    # Check if we're live.
    @maintenance.command(
        name="ping",
        description="Checks if this bot is awake."
    )
    async def ping_tohru(self, ctx):
        print("Executing ping command.")
        await ctx.respond("Ping pong! I'm still alive!")

    # Print an index of database things for fun reasons.
    @maintenance.command(
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
            self.mydb = utils.tohrudb.reconnect_to_db(self.mydb)
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

def setup(bot):
    bot.add_cog(Maintenance(bot))
