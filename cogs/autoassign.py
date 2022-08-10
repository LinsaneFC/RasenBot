import discord
from discord.ext import commands

class AutoAssign(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online.")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        id = member.guild.id
        server = self.client.get_guild(id)
        role = discord.utils.get(server.roles, name=f'{server.roles[1]}')
        await member.add_roles(role)

def setup(client):
    client.add_cog(AutoAssign(client))