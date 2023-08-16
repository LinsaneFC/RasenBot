import discord
from discord.ext import commands

# Command that moves one user in a voice channel into another voice channel specified by the user.
class MoveUsers(commands.Cog):

# Function dedicated to moving a specified user to a specified channel.
    @commands.command()
    async def move(self, ctx, member : discord.Member, channel : discord.VoiceChannel):
        await member.move_to(channel)


def setup(client):
    client.add_cog(MoveUsers(client))