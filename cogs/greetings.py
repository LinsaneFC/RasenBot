import discord
from constantvariables import WELCOME_CHANNEL_ID, WELCOME_REACT_EMOJI, VERIFIED_MEMBER_ID
import os
from discord.ext import commands

# Class dedicated to greeting new members when joining the server.
class Greetings(commands.Cog):

# Constructor that assigns the welcome message to the specific new member with their username.
    def __init__(self, client):
        self.client = client
        self.welcome_message_id = self.load_welcome_message_id()

# Helper function responsible for loading and returning the welcome message
    def load_welcome_message_id(self):
        try:
            with open("txtfiles/welcome_message_id.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return None

# Helper function responsible for storing the welcome message id to be loaded later if the bot goes offline in the future.
    def save_welcome_message_id(self, message_id):
        with open("txtfiles/welcome_message_id.txt", "w") as file:
            file.write(str(message_id))

# Command function responsible for sending the welcome message on user join where they must react to a
# terms and conditions message in order to join the server. This message also contains a guide to RasenBot.
    @commands.command()
    async def welcome(self, ctx):
        channel = self.client.get_channel(WELCOME_CHANNEL_ID)

        if channel is not None:
            logo_file = discord.File(os.path.join("media", "rasenbotlogo.jpg"), filename="rasenbotlogo.jpg")
            gif_file = discord.File(os.path.join("media", "discordlogogif.gif"), filename="discordlogogif.gif")

            embed = discord.Embed(
                title="Hello!",
                description=f"Welcome to the server!\nPlease read the rules and react to the emoji below if you want access to the server\n\n1. No racism\n2. No bullying\n3. Be kind\n4. Don't ask for roles\n5. Use common sense\n6. Send Parker **LOTS** of kisses\n\nIf you do not follow any of these rules, you will be kicked and potentially banned\n\nEnjoy your stay!",
                color=discord.Color.blue()
            )

            embed.set_author(name="RasenBot", icon_url="attachment://rasenbotlogo.jpg")
            embed.set_thumbnail(url="attachment://discordlogogif.gif")
            embed.set_footer(text="If you are curious about RasenBot, please type $help in the bot commands channel for more commands!")

            message = await channel.send(embed=embed, files=[logo_file, gif_file])
            await message.add_reaction(WELCOME_REACT_EMOJI)
            self.welcome_message_id = message.id
            self.save_welcome_message_id(message.id)

# Listener function responsible for giving a newcomer a role once they react to the terms and conditions.
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == self.welcome_message_id:
            if payload.channel_id == WELCOME_CHANNEL_ID:
                if WELCOME_REACT_EMOJI in str(payload.emoji):
                    guild = self.client.get_guild(payload.guild_id)
                    member = guild.get_member(payload.user_id)
                    if member is not None and not member.bot:
                        role = guild.get_role(VERIFIED_MEMBER_ID)
                        await member.add_roles(role)

# Listener function that is responsible for removing the role of the user if they are to remove their reaction to
# the terms and conditions thus violating the rules.
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == self.welcome_message_id:
            if payload.channel_id == WELCOME_CHANNEL_ID:
                if WELCOME_REACT_EMOJI in str(payload.emoji):
                    guild = self.client.get_guild(payload.guild_id)
                    member = guild.get_member(payload.user_id)
                    if member is not None and not member.bot:
                        role = guild.get_role(VERIFIED_MEMBER_ID)
                        await member.remove_roles(role)


def setup(client):
    client.add_cog(Greetings(client))
