import discord
import constantvariables
import os
from discord.ext import commands

# A constant greetings message that is sent to a text channel of your choice and requires a new user to react to receive a role to access the server. Removes role if unreacted to.
class Greetings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def welcome(self, ctx):
        channel = self.client.get_channel(constantvariables.welcome_channel_id)

        if channel is not None:
            logo_file = discord.File(os.path.join("media", "copyrightfreelogo.jpg"), filename="copyrightfreelogo.jpg")
            gif_file = discord.File(os.path.join("media", "copyrightfreegif.gif"), filename="copyrightfreegif.gif")

            embed = discord.Embed(
                title="Hello!",
                description=f"Welcome to the server!\nPlease read the rules and react to the emoji below if you want access to the server\n\n1. No racism\n2. No bullying\n3. Be kind\n4. Don't ask for roles\n5. Use common sense\n6. Send Parker **LOTS** of kisses\n\nIf you do not follow any of these rules, you will be kicked and potentially banned\n\nEnjoy your stay!",
                color=discord.Color.blue()
            )

            embed.set_author(name="RasenBot", icon_url="attachment://copyrightfreelogo.jpg")
            embed.set_thumbnail(url="attachment://copyrightfreegif.gif")
            embed.set_footer(text="If you are curious about RasenBot, please type $help in the bot commands channel for more commands!")

            message = await channel.send(embed=embed, files=[logo_file, gif_file])
            await message.add_reaction("👍")
            self.welcome_message_id = message.id

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == constantvariables.welcome_channel_id and payload.message_id == self.welcome_message_id:
            if "👍" in str(payload.emoji):
                guild = self.client.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)
                if member is not None and not member.bot:  # Check if the member exists and is not a bot
                    role = guild.get_role(constantvariables.verified_member_id)
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.channel_id == constantvariables.welcome_channel_id and payload.message_id == self.welcome_message_id:
            if "👍" in str(payload.emoji):
                guild = self.client.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)
                if member is not None and not member.bot:
                    role = guild.get_role(constantvariables.verified_member_id)
                    await member.remove_roles(role)


def setup(client):
    client.add_cog(Greetings(client))
