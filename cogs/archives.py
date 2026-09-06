import discord
from discord.ext import commands
from discord import Option

from pydub import AudioSegment # pip install pydub
import pretty_midi
import soundfile as sf
import filetype # pip install filetype
from utils.tohrudb import reconnect_to_db
import mysql
import random
import string
from datetime import datetime
from wand.image import Image as MagickImage

class Archives(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mydb = ...

    # Commands involving the archives system.
    archives = discord.SlashCommandGroup(
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

        response, error, comp_path, caption, upload_id = await Archives.submit_to_archives(file, caption, ctx.author.id)
        
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
        self,
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
                cursor = self.mydb.cursor()
            except mysql.connector.Error as err:
                print(f"Error connecting to DB: {err}")
                reconnect_to_db(self.mydb)
                cursor = self.mydb.cursor()

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
            cursor.execute(sql, (upload_id,))

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

        except Exception as e:
            print(f"Error retrieving upload: {e}")
            await ctx.respond(f"Uh oh, something went wrong: {e}")
            if cursor:
                cursor.close()

    # CONTEXT MENU: Submit to archives
    @commands.message_command(
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

        response, error, comp_path, caption, upload_id = await Archives.submit_to_archives(attachment, message.content or "(C) No caption provided.", ctx.author.id)
        
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


    # HELPERS

    # Submit to archives!
    async def submit_to_archives(self, file, caption, author_id):
        try:
            saved_path, filename = await Archives.download_file(file)

            # Determine whether it's an image, audio, or neither.
            kind = filetype.guess(saved_path)
            if kind is not None:
                mime_type = kind.mime
                
                if mime_type.startswith("image/"): # INCOMING IMAGE!!
                    print(f"Incoming {mime_type}... {saved_path}")
                    db = "archives_image"
                    comp_path = f"{self.UPLOADS_FOLDER}/{filename}.jpg"

                    # Compress the image
                    try:
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
                    comp_path = f"{self.UPLOADS_FOLDER}/{filename}.mp3"

                    # WAIT! Is it a MIDI file?
                    if mime_type == "audio/midi" or mime_type == "audio/x-midi":
                        # Aw sweet let's go render us some midis
                        midi = True
                        saved_path = await Archives.synthesize_midi(saved_path)
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
                cursor = self.mydb.cursor()
            except mysql.connector.Error as err:
                print(f"Error connecting to DB: {err}")
                reconnect_to_db(self.mydb)
                cursor = self.mydb.cursor()

            # Store file info in the database
            sql = f"INSERT INTO {db} (path, original_path, caption, submitter_id) VALUES (%s, %s, %s, %s)"
            val = (comp_path, saved_path, caption.replace('"', '\"'), author_id)
            cursor.execute(sql, val)
            self.mydb.commit()

            # Fetch ID of last upload.
            cursor.execute("SELECT LAST_INSERT_ID()")
            upload_id = cursor.fetchone()[0]
            cursor.close()

            # Prep response
            return None, False, comp_path, caption or None, upload_id

        except Exception as e:
            print(f"Oh god, what now... {e}?!")
            if cursor:
                cursor.close()
            return f"Uh oh, something went wrong: {e}. Please try again.", True, None, None, None

    # Download a file into the uploads directory.
    async def download_file(self, file):
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Generate 4 random characters
        random_suffix = ''.join(random.choice(string.ascii_letters) for _ in range(4))

        filename = f"{timestamp}_{random_suffix}_{file.filename}"
        saved_path = f"{self.UPLOADS_FOLDER}/{filename}"
        await file.save(saved_path)
        print("File saved!")

        return saved_path, filename

    # MIDI Synthesis
    async def synthesize_midi(self, input):
        # Load the MIDI file
        midi = pretty_midi.PrettyMIDI(input)

        # Check for soundfont file
        if not self.SOUNDFONT:
            # Use default soundfont (boring)
            audio = midi.fluidsynth(fs=44100)
        else:
            # Use custom soundfont (awesome)
            audio = midi.fluidsynth(fs=44100, sf2_path=self.SOUNDFONT)

        # Save as WAV
        output = input + ".wav"
        sf.write(output, audio, 44100)
        return input # this is not a mistake; when requesting the original version of the file, it should return the midi, not the intermediate wav.

def setup(bot):
    bot.add_cog(Archives(bot))
