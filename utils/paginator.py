import discord
from discord.ui import View, Button

# Paginator for seeing archives entries
class Paginator(View):
    def __init__(self, entries, per_page=25):
        super().__init__()
        self.entries = entries
        self.per_page = per_page
        self.current_page = 0
        self.total_pages = (len(entries) - 1) // per_page + 1
        self.update_buttons()

    async def interaction_check(self, interaction):
        # If the OG user is the one pushing the button, let's roll.
        print(f"Button pressed! {self.ctx.author} == {interaction.user}?")
        if interaction.user == self.ctx.author:
            if interaction.custom_id == "previous":
                print("Going back to the previous page!")
                await self.turn_page(interaction, -1)
            elif interaction.custom_id == "next":
                print("Going forward to the next page!")
                await self.turn_page(interaction, 1)
        return False

    async def on_timeout(self):
        # Don't hold onto the past. You need to let it go.
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def turn_page(self, interaction, direction):
        # Go to the next/previous page and update the buttons.
        self.current_page += direction
        self.update_buttons()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    def update_buttons(self):
        # Clear the current buttons and add new ones based on where we are in spacetime.
        self.clear_items()
        if self.current_page > 0:
            self.add_item(Button(label="Previous", style=discord.ButtonStyle.primary, custom_id="previous"))
        if self.current_page < self.total_pages - 1:
            self.add_item(Button(label="Next", style=discord.ButtonStyle.primary, custom_id="next"))

    def create_embed(self):
        # List all of our stuff, and make it look all fancy, ooh.
        start = self.current_page * self.per_page
        end = start + self.per_page
        entries = self.entries[start:end]
        formatted_entries = [f"**{id}:** {name}" for id, name in entries]
        embed = discord.Embed(title="Table of Contents", description="\n".join(formatted_entries))
        embed.set_footer(text=f"Page {self.current_page + 1} of {self.total_pages}")
        return embed
