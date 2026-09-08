# standard discord bs
import discord
from discord.ext import commands
from discord import Option

import mysql
import utils.tohrudb
import utils.paginator

class Pools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mydb = utils.tohrudb.get_db()

    # Commands involving the pool system.
    pool = discord.SlashCommandGroup (
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
        self,
        ctx: discord.ApplicationContext,
        pool: Option(str, "Names must be uniques, we recommend adding your own prefix to avoid conflicts.", required=True, max_length=16),  # type: ignore
        visible: Option(bool, "Should this pool be visible to others? They will also be able to modify it.", default=True)  # type: ignore
    ):
        print(f"User {ctx.author.id} is creating a new pool: {pool}")
        await ctx.defer(ephemeral=True)

        try:
            # Connect to database.
            try:
                cursor = self.mydb.cursor()
            except mysql.connector.Error as err:
                print(f"Error connecting to DB: {err}")
                utils.tohrudb.reconnect_to_db(self.mydb)
                cursor = self.mydb.cursor()

            # Check if the pool already exists
            sql = "SELECT COUNT(*) FROM pools WHERE name = %s"
            cursor.execute(sql, (pool,))
            pool_exists = cursor.fetchone()[0] > 0
            if pool_exists:
                await ctx.respond(content=f"Pool '{pool}' already exists! Please choose a different name.", ephemeral=True)
                cursor.close()
                print(f"Nevermind! {pool} already exists!")
                return

            # Create the pool in the database
            sql = "INSERT INTO pools (name, owner_id, visible) VALUES (%s, %s, %s)"
            cursor.execute(sql, (pool, ctx.author.id, visible))
            self.mydb.commit()

            print(f"User {ctx.author.id} created pool {pool} successfully!")
            await ctx.respond(content=f"Your pool '{pool}' has been created!", ephemeral=True)
            cursor.close()
        except Exception as e:
            print(f"Oh, fiddlesticks! What now... {e}?!")
            await ctx.respond(content=f"Uh oh, something went wrong: {e}. Please try again.", ephemeral=True)
            if cursor:
                cursor.close()

    # Pool submission fun
    @pool.command(
        name="submit",
        description="Submit something into one of your pools."
    )
    async def pool_submit(
        self,
        ctx: discord.ApplicationContext,
        pool: Option(str, "Which of your pools would you like to use?", required=True, max_length=16),  # type: ignore
        content: Option(str, "Type your submission here.", required=True, max_length=4096)  # type: ignore
    ):
        print(f"User {ctx.author.id} is submitting into {pool}!")
        await ctx.defer(ephemeral=True)

        try:
            # Connect to database.
            try:
                cursor = self.mydb.cursor()
            except mysql.connector.Error as err:
                print(f"Error connecting to DB: {err}")
                utils.tohrudb.reconnect_to_db(self.mydb)
                cursor = self.mydb.cursor()

            # Check if the pool exists
            sql = "SELECT COUNT(*) FROM pools WHERE name = %s"
            cursor.execute(sql, (pool,))
            pool_exists = cursor.fetchone()[0] > 0
            if not pool_exists:
                await ctx.respond(content=f"Pool '{pool}' does not exist! Please create it first.", ephemeral=True)
                cursor.close()
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
                    print(f"Blocked! User {ctx.author.id} lacks permission to modify {pool}!")
                    return

            # Store tip in the database
            sql = f"INSERT INTO pools_content (pool_id, content, submitter_id) VALUES (%s, %s, %s)"
            val = (pool, content.replace('"', '\"'), ctx.author.id)  # Escape single quotes
            cursor.execute(sql, val)
            self.mydb.commit()

            print(f"User {ctx.author.id} submitted to pool {pool} successfully!")
            await ctx.respond(content=f"Your submission has been saved to pool '{pool}'!", ephemeral=True)
            cursor.close()

        except Exception as e:
            print(f"Oh, fiddlesticks! What now... {e}?!")
            await ctx.respond(content=f"Uh oh, something went wrong: {e}. Please try again.", ephemeral=True)
            if cursor:
                cursor.close()

    # Print an index of pool things.
    @pool.command(
        name="index",
        description="Print a Table of Contents for pools and their items.",
        integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install])
    async def pool_index(
        self,
        ctx: discord.ApplicationContext,
        pool: Option(str, "The pool to view.", required=False),  # type: ignore
        all_pools: Option(bool, "View items from all users?", required=False, default=True)  # type: ignore
        ):
        try:
            # It'll freak out if we don't do this.
            utils.tohrudb.reconnect_to_db(self.mydb)
            cursor = self.mydb.cursor()
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

            # Didn't find anything? That's too bad.
            if not entries:
                return await ctx.respond("No entries found in the pools database.")

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
    bot.add_cog(Pools(bot))
