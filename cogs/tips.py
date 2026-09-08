# standard discord bs
import discord
from discord.ext import commands
from discord import Option

import utils.tohrudb
import mysql
import random

class Tips(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mydb = utils.tohrudb.get_db()

    # Commands involving the tips system.
    tips = discord.SlashCommandGroup(
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
        self,
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
                cursor = self.mydb.cursor()
            except mysql.connector.Error as err:
                print(f"Error connecting to DB: {err}")
                utils.tohrudb.reconnect_to_db(self.mydb)
                cursor = self.mydb.cursor()

            # Store tip in the database
            sql = f"INSERT INTO {db} (content, author, submitter_id) VALUES (%s, %s, %s)"
            val = (content.replace('"', '\"'), author.replace('"', '\"'), ctx.author.id)  # Escape single quotes
            cursor.execute(sql, val)
            self.mydb.commit()

            # Fetch ID of last upload.
            cursor.execute("SELECT LAST_INSERT_ID()")
            id = cursor.fetchone()[0]
            cursor.close()

            if type == "Tip":
                await ctx.respond(content=f"Your submission has been saved! ID: {id}\n> {content}", ephemeral=False)
            else:
                await ctx.respond(content=f"Your submission has been saved! ID: {id}\n> *\"{content}\" - {author}*", ephemeral=False)

            print(f"Tip {id} submitted successfully!")

        except Exception as e:
            print(f"Oh, fiddlesticks! What now... {e}?!")
            await ctx.respond(content=f"Uh oh, something went wrong: {e}. Please try again.", ephemeral=True)
            if cursor:
                cursor.close()

    # Tip retrieval fun
    @tips.command(
        name="roll",
        description="Roll for a random loading screen tip, or request one via ID."
    )
    async def tips_roll(
        self,
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
                cursor = self.mydb.cursor()
            except mysql.connector.Error as err:
                print(f"Error connecting to DB: {err}")
                utils.tohrudb.reconnect_to_db(self.mydb)
                cursor = self.mydb.cursor()

            if id == 0: # If they asked for a random tip.
                # Count total submissions
                sql = f"SELECT COUNT(*) FROM {db}"
                cursor.execute(sql)
                total_submissions = cursor.fetchone()[0]

                # Generate random number within submission count
                id = random.randint(1, total_submissions)

            # Get submission
            sql = f"SELECT content, author FROM {db} WHERE id = %s"
            cursor.execute(sql, (id,))

            # Check if submission exists
            content, author = cursor.fetchone()
            if not content:
                return await ctx.respond(f"Submission with ID {id} not found!")

            # Send image
            if db == "tips":
                await ctx.respond(content=f"> {content}")
            else:
                await ctx.respond(content=f"> *\"{content}\" - {author}*")
            print(f"Submission ID {id} sent successfully!")
            cursor.close()

        except Exception as e:
            print(f"Error retrieving submission: {e}")
            await ctx.respond(f"Uh oh, something went wrong: {e}")
            if cursor:
                cursor.close()

    # CONTEXT MENU: Submit quote
    @commands.message_command(
        name="Submit Quote",
        integration_types=[discord.IntegrationType.user_install]
    )
    async def context_quote(
        self,
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
                cursor = self.mydb.cursor()
            except mysql.connector.Error as err:
                print(f"Error connecting to DB: {err}")
                utils.tohrudb.reconnect_to_db(self.mydb)
                cursor = self.mydb.cursor()

            # Store quote in the database
            sql = f"INSERT INTO quotes (content, author, submitter_id) VALUES (%s, %s, %s)"
            cursor.execute(sql, (clean_content, clean_uname, ctx.author.id))
            self.mydb.commit()

            # Fetch ID of last upload.
            cursor.execute("SELECT LAST_INSERT_ID()")
            id = cursor.fetchone()[0]
            cursor.close()

            await ctx.respond(content=f"Your submission has been saved! ID: {id}\n> *\"{clean_content}\" - {clean_uname}*", ephemeral=True)
            print(f"Tip {id} submitted successfully!")

        except Exception as e:
            print(f"Oh, fiddlesticks! What now... {e}?!")
            await ctx.respond(content=f"Uh oh, something went wrong: {e}. Please try again.", ephemeral=True)
            if cursor:
                cursor.close()

def setup(bot):
    bot.add_cog(Tips(bot))
