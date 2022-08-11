import discord
from discord.ext import commands


class MoveUsers(commands.Cog):

    @commands.command()
    async def move(self, ctx, member : discord.Member, channel : discord.VoiceChannel):
        await member.move_to(channel)
    

def setup(client):
    client.add_cog(MoveUsers(client))