
# for pointless fun stuff
import whisper


# Transcription fun
@bot.command(
    name="transcribe",
    description="Transcribes any audio file you upload using the power of AI!",
    integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install]
)
async def transcribe(
    ctx: discord.ApplicationContext, 
    audio: Option(discord.Attachment, "Select an audio file to transcribe.", required=True)
):
    print("Audio transcription command called!")
    await ctx.defer(ephemeral=True)
    print("Responded in time! AS ALWAYS, DISCORD!!")

    try:
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Generate 4 random characters
        random_suffix = ''.join(random.choice(string.ascii_letters) for _ in range(4)) 

        filename = f"{timestamp}_{random_suffix}_{audio.filename}" 
        saved_path = f"uploads/{filename}"
        transcription_path = f"uploads/{filename}.txt"
        await audio.save(saved_path)
        print("Audio saved!")

        # Send transcription
        await ctx.respond(content=f"Audio transcription for {filename} is ready!",file=discord.File(transcription_path))
        print(f"Audio transcription for {filename} sent successfully!")

    except Exception as e:
        print(f"Oh god, what now... {e}?!")
        await ctx.respond(content=f"Uh oh, something went wrong: {e}. Please try again.")
        cursor.close()
        mydb.close()
