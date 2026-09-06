import discord
from discord.ext import commands
from discord import Option

class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commands that implement Crypto, The Secret Message Encoding Tool
    crypto = discord.SlashCommandGroup(
        name="crypto",
        description="The Secret Message Encoding Tool, now in Discord!",
        integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install]
    )

    # Encode to Crypto
    @crypto.command(
        name="encode",
        description="Encode something to Crypto code."
    )
    async def crypto_encode(
        ctx: discord.ApplicationContext,
        content: Option(str, "Your message here!", required=True, max_length=333)  # type: ignore
    ):
        print("Encoding to Crypto.")
        message = Crypto.encode_crypto(content)
        await ctx.respond(content=message, ephemeral=True)

    # Decode from Crypto
    @crypto.command(
        name="decode",
        description="Decode something from Crypto code."
    )
    async def crypto_decode(
        ctx: discord.ApplicationContext,
        content: Option(str, "Crypto code here!", required=True)  # type: ignore
    ):
        print("Decoding from Crypto.")
        message = Crypto.decode_crypto(content)
        await ctx.respond(content=message, ephemeral=True)

    # CONTEXT MENU: Decode from Crypto
    @commands.message_command(
        name="Crypto: Decode",
        integration_types=[discord.IntegrationType.user_install]
    )
    async def context_decode(
        ctx: discord.ApplicationContext,
        message: discord.Message
    ):
        print("(C) Decoding from Crypto.")
        message = Crypto.decode_crypto(message.content)
        await ctx.respond(content=message, ephemeral=True)

    # And of course the actual good stuff
    def set_dictionary(code, way):
        match code:
            # IF WE CRYPTO GAMERS AS WE SHOULD BE LETS GOOOO
            case "crypto":
                encode_dict = {
                        "A": "UDFM55",
                        "B": "H22DGF",
                        "C": "FDH76D",
                        "D": "FGS576",
                        "E": "JUK5JH",
                        "F": "ERG55S",
                        "G": "T5H5FD",
                        "H": "RG645G",
                        "I": "RG5F4D",
                        "J": "RT57F6",
                        "K": "VCBC4B",
                        "L": "F8G0GF",
                        "M": "FD5CJS",
                        "N": "G443FG",
                        "O": "F65GC2",
                        "P": "TH6DF5",
                        "Q": "CV4F7R",
                        "R": "XF67TS",
                        "S": "X98DGT",
                        "T": "TH84SJ",
                        "U": "BCX7DF",
                        "V": "FG75SD",
                        "W": "4KL55D",
                        "X": "GFH3F4",
                        "Y": "GH76GF",
                        "Z": "45T6FG",
                        "a": "UDFM45",
                        "b": "H21DGF",
                        "c": "FDH56D",
                        "d": "FGS546",
                        "e": "JUK4JH",
                        "f": "ERG54S",
                        "g": "T5H4FD",
                        "h": "RG641G",
                        "i": "RG4F4D",
                        "j": "RT56F6",
                        "k": "VCBC3B",
                        "l": "F8G9GF",
                        "m": "FD4CJS",
                        "n": "G423FG",
                        "o": "F45GC2",
                        "p": "TH5DF5",
                        "q": "CV4F6R",
                        "r": "XF64TS",
                        "s": "X78DGT",
                        "t": "TH74SJ",
                        "u": "BCX6DF",
                        "v": "FG65SD",
                        "w": "4KL45D",
                        "x": "GFH3F2",
                        "y": "GH56GF",
                        "z": "45T1FG",
                        "0": "87H8G7",
                        "1": "D4G23D",
                        "2": "GB56FG",
                        "3": "SF45GF",
                        "4": "P4FF12",
                        "5": "F6DFG1",
                        "6": "56FG4G",
                        "7": "USGFDG",
                        "8": "FKHFDG",
                        "9": "IFGJH6",
                        "@": "G25GHF",
                        "#": "45FGFH",
                        "$": "75FG45",
                        "*": "54GDH5",
                        ".": "HG56FG",
                        ",": "DF56H4",
                        "-": "F5JHFH",
                        " ": "SGF4HF",
                        "\\": "56F15G", # its also 45GH45 because of a bug
                        "/": "56H45G",
                        "'": "69H45G",
                        "(": "42H05G",
                        ")": "99H54G",
                        ";": "HSBN0L",
                        "[": "USGFGD",
                        "]": "FKHYDK",
                        "=": "56F15G",
                        "%": "D4G23E",
                        "?": "FWIP49",
                        "!": "E933DC",
                        "|": "SID427",
                        "`": "92SID8",
                        "~": "9DDOD2"
                    }

        # Are we gonna pop 'er in reverse, or nah?
        if way == "enc":
            dictionary = encode_dict
        else:
            dictionary = {v: k for k, v in encode_dict.items()}

        return dictionary

    def encode_crypto(user_input):
        # Do the swapping of chacters for codes...
        dictionary = Crypto.set_dictionary("crypto", "enc")
        replaced_string = ""
        for char in user_input:
            replaced_string += dictionary.get(char, "")
        
        # And then pop 'er in reverse...
        out_string = replaced_string[::-1]

        # And we're done!
        return out_string

    def decode_crypto(user_input):
        # We run that back...
        reversed_string = user_input[::-1]

        # Swap the characters for codes...
        dictionary = Crypto.set_dictionary("crypto", "dec")
        out_string = ""
        for chars in range(0, len(reversed_string), 6):  # Loop in chunks of 6 characters
            chars = reversed_string[chars:chars+6]  # Extract 6-character code
            out_string += dictionary.get(chars, "")

        return out_string

def setup(bot):
    bot.add_cog(Crypto(bot))
