# standard discord bs
import discord
from discord.ext import commands
from discord import Option

import utils.tohrudb
import mysql

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mydb = utils.tohrudb.get_db()

    # Epic context menu integration stuff (cool).

    # CONTEXT MENU: Reaction
    @commands.message_command(
        name="Reaction",
        integration_types=[discord.IntegrationType.user_install]
    )
    async def context_archive(
        self,
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
                cursor = self.mydb.cursor()
            except mysql.connector.Error as err:
                print(f"Error connecting to DB: {err}")
                utils.tohrudb.reconnect_to_db(self.mydb)
                cursor = self.mydb.cursor()

            # Check if user exists in the DB
            sql = f"SELECT COUNT(*) FROM users WHERE id = %s"
            cursor.execute(sql, (ctx.author.id,))
            user_exists = cursor.fetchone()
            if not user_exists:
                return await ctx.respond("We don't know anything about you!\nPlease use `/reaction` to get started!", ephemeral=True)

            # Get user reaction details
            sql = f"SELECT image, quote, audio FROM users WHERE id = %s"
            cursor.execute(sql, (ctx.author.id,))

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

        except Exception as e:
            print(f"Error retrieving reaction: {e}")
            await ctx.respond(f"Uh oh, something went wrong: {e}", ephemeral=True)
            if cursor:
                cursor.close()


    # And accompanying SET REACTION command
    @commands.slash_command(
        name="set_reaction",
        description="Set any combination of quote.",
        integration_types=[discord.IntegrationType.user_install]
    )
    async def set_reaction(
        self,
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
                cursor = self.mydb.cursor()
            except mysql.connector.Error as err:
                print(f"Error connecting to DB: {err}")
                utils.tohrudb.reconnect_to_db(self.mydb)
                cursor = self.mydb.cursor()

            # Check if user exists in the DB
            sql = f"SELECT COUNT(*) FROM users WHERE id = %s"
            cursor.execute(sql, (ctx.author.id,))
            user_exists = cursor.fetchone()[0] > 0

            if user_exists:
                # Update existing user
                sql = f"UPDATE users SET image = %s, quote = %s, audio = %s WHERE id = %s"
            else:
                # Create new user entry
                sql = f"INSERT INTO users (image, quote, audio, id) VALUES (%s, %s, %s, %s)"

            val = (image_id or None, quote or None, audio_id or None, ctx.author.id)
            cursor.execute(sql, val)
            self.mydb.commit()
            cursor.close()

            await ctx.respond(content="Your reaction has been set successfully!", ephemeral=True)
            print(f"(C) Reaction for {ctx.author.id} set successfully!")

        except Exception as e:
            print(f"Error setting reaction: {e}")
            await ctx.respond(f"Uh oh, something went wrong: {e}", ephemeral=True)
            if cursor:
                cursor.close()

def setup(bot):
    bot.add_cog(Reactions(bot))
