import discord
from discord.ext import commands

#Allows for the bot to auto assign the default role in the server to new members
class AutoAssign(commands.Cog):

    def __init__(self,client):
        self.client = client

    """ Need to move this somewhere else not in a cog """
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print("Bot is online.")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        id = member.guild.id
        server = self.client.get_guild(id)
        role = discord.utils.get(server.roles, name=f'{server.roles[1]}')
        await member.add_roles(role)

def setup(client):
    client.add_cog(AutoAssign(client))