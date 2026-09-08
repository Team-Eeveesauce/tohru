# standard discord bs
import discord
from discord.ext import commands
from discord import Option

import utils.tohrudb
from colorthief import ColorThief
from PIL import ImageColor
from wand.image import Image as MagickImage
import mysql
from datetime import datetime
import random
import string
import os

class Stuffpile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mydb = utils.tohrudb.get_db()
        self.UPLOADS_FOLDER = os.getenv('UPLOADS_FOLDER')

    # Commands involving the Stuffpile (TM).
    stuff = discord.SlashCommandGroup(
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
        self,
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
                cursor = self.mydb.cursor()
            except mysql.connector.Error as err:
                print(f"Error connecting to DB: {err}")
                utils.tohrudb.reconnect_to_db(self.mydb)
                cursor = self.mydb.cursor()

            # Save the image.
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            random_suffix = ''.join(random.choice(string.ascii_letters) for _ in range(4))
            filename = f"thing_{timestamp}_{random_suffix}_{image.filename}"
            saved_path = f"{self.UPLOADS_FOLDER}/{filename}"
            jpeg_path = f"{self.UPLOADS_FOLDER}/{filename}.jpg"
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
            color_thief = ColorThief(f"{self.UPLOADS_FOLDER}/{filename}.jpg")
            dominant_color = color_thief.get_color(quality=5)
            hexcode = Stuffpile.rgb2hex(*dominant_color)

            # Store thing in the database
            sql = f"INSERT INTO stuff (type, name, description, fact, image, submitter_id, colour) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (type, name.replace('"', '\"'), description.replace('"', '\"'), fact.replace('"', '\"'), filename, ctx.author.id, hexcode)
            cursor.execute(sql, val)
            self.mydb.commit()

            # Fetch ID of last upload.
            cursor.execute("SELECT LAST_INSERT_ID()")
            id = cursor.fetchone()[0]
            cursor.close()

            # Prepare it to send off to the user!
            embed = Stuffpile.prepare_embed(name, description, hexcode, fact, id, filename)
            await ctx.respond(content=f"Your submission has been saved! ID: {id}",embed=embed,file=discord.File(jpeg_path))
            print(f"Stuff {id} submitted successfully!")

        except Exception as e:
            print(f"Oh, fiddlesticks! What now... {e}?!")
            await ctx.respond(content=f"Uh oh, something went wrong: {e}. Please try again.")
            if cursor:
                cursor.close()

    # Stuff retrieval fun
    @stuff.command(
        name="find",
        description="Look around the Stuffpile (TM) in search of things."
    )
    async def stuff_find(
        self,
        ctx: discord.ApplicationContext,
        type: Option(str, "The type of thing you're looking for.", choices=['Person', 'Place', 'Thing'], required=False, default="Any"),  # type: ignore
        id: Option(int, "Specific image ID (overrides other options)", required=False, default=0)  # type: ignore
    ):
        try:
            # Connect to database
            try:
                cursor = self.mydb.cursor()
            except mysql.connector.Error as err:
                print(f"Error connecting to DB: {err}")
                utils.tohrudb.reconnect_to_db(self.mydb)
                cursor = self.mydb.cursor()

            try:
                print("Stuff find command called!")
                if not id:
                    if type == "Any":
                        # Grab a really random image.
                        print("Finding something random...")
                        sql = "SELECT id, name, description, fact, image, colour FROM stuff WHERE visible = true ORDER BY RAND() LIMIT 1;"
                        cursor.execute(sql)
                    else:
                        # Grab a random image.
                        print("Finding a random " + type + "...")
                        sql = "SELECT id, name, description, fact, image, colour FROM stuff WHERE type = %s AND visible = true ORDER BY RAND() LIMIT 1;"
                        cursor.execute(sql, (type,))
                else:
                    # Grab the specific image.
                    print("Finding submission no." + str(id) + "...")
                    sql = "SELECT id, name, description, fact, image, colour FROM stuff WHERE id = %s AND visible = true;"
                    cursor.execute(sql, (id,))

                id, name, description, fact, image, hexcode = cursor.fetchone()
            except Exception as e:
                await ctx.respond(f"Submission with ID {id} not found!")
                return

            # Construct the image path.
            image_path = f"{self.UPLOADS_FOLDER}/{image}.jpg"
            print(f"Retrieved image path from DB: {image_path}")

            # Prepare it to send off to the user!
            embed = Stuffpile.prepare_embed(name, description, hexcode, fact, id, image)
            await ctx.respond(content=f"Here's what I found!",embed=embed,file=discord.File(image_path))
            print(f"Thing {id} sent successfully!")
            cursor.close()

        except Exception as e:
            print(f"Error retrieving image: {e}")
            await ctx.respond(f"Uh oh, something went wrong: {e}")
            if cursor:
                cursor.close()

    # Stuff updating fun
    @stuff.command(
        name="update",
        description="Update something in the Stuffpile (TM)."
    )
    async def stuff_update(
        self,
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
                cursor = self.mydb.cursor()
            except mysql.connector.Error as err:
                print(f"Error connecting to DB: {err}")
                utils.tohrudb.reconnect_to_db(self.mydb)
                cursor = self.mydb.cursor()

            # Verify that the submission exists, because it would be terrible if it didn't.
            try:
                sql = "SELECT id, name, description, fact, image, colour, visible FROM stuff WHERE id = %s AND visible = true;"
                cursor.execute(sql, (id,))
                id, name, description, fact, filename, hexcode, visible = cursor.fetchone()
            except Exception as e:
                return await ctx.respond(f"Submission with ID {id} not found!")

            # Now, before we do anything else, fix some stuff so we can show the entries without anything weird happening.
            jpeg_path = f"{self.UPLOADS_FOLDER}/{filename}.jpg"

            match type:
                case "Image":
                    # Save the new image.
                    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                    random_suffix = ''.join(random.choice(string.ascii_letters) for _ in range(4))
                    newfilename = f"thing_{timestamp}_{random_suffix}_{image.filename}"
                    saved_path = f"{self.UPLOADS_FOLDER}/{newfilename}"
                    await image.save(saved_path)
                    print("Image saved!")

                    # Compress the new image
                    try:
                        from wand.image import Image as MagickImage
                        with MagickImage(filename=f"{saved_path}[0]") as magick_img:
                            # Convert to JPEG
                            magick_img.format = 'jpeg'
                            magick_img.compression_quality = 80  # Adjust quality as needed
                            magick_img.save(filename=saved_path + ".jpg")
                        print("Image compressed using PyMagick!")
                    except Exception as e:
                        # USE THIS WHEN DEBUGGING await ctx.respond(content=f"Something went wrong processing the image: {e}")
                        await ctx.respond(content="Something went wrong processing the image. Your submission has NOT been saved.")
                        print(f"Image NOT compressed! {e}")
                        return  # End command execution if compression failed

                    # Steal the dominant colour from the new image.
                    color_thief = ColorThief(f"{self.UPLOADS_FOLDER}/{filename}.jpg")
                    dominant_color = color_thief.get_color(quality=3)
                    hexcode = Stuffpile.rgb2hex(*dominant_color)

                    # Update database
                    sql = "UPDATE stuff SET image = %s, colour = %s WHERE id = %s;"
                    cursor.execute(sql, (newfilename, hexcode, id))
                    self.mydb.commit()
                    cursor.close()

                    # For embed purposes
                    filename = newfilename
                    jpeg_path = saved_path + ".jpg"

                case "Visibility":
                    visible = not visible
                    # Update database
                    sql = "UPDATE stuff SET visible = %s WHERE id = %s"
                    cursor.execute(sql, (visible, id))
                    self.mydb.commit()
                    cursor.close()
                    return await ctx.respond(content=f"Submission {id} has successfully been hidden!")

            # Prepare it to send off to the user!
            embed = Stuffpile.prepare_embed(name, description, hexcode, fact, id, filename)
            await ctx.respond(content=f"Submission {id} has successfully been updated!",embed=embed,file=discord.File(jpeg_path))
            print(f"Stuff {id} updated successfully!")

        except Exception as e:
            print(f"Oh, fiddlesticks! What now... {e}?!")
            await ctx.respond(content=f"Uh oh, something went wrong: {e}. Please try again.")
            if cursor:
                cursor.close()


    # HELPERS

    # Convert RGB values to HEX because who the hell needs RGB values.
    def rgb2hex(r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

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

def setup(bot):
    bot.add_cog(Stuffpile(bot))
