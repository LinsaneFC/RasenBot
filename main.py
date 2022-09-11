import discord
import os
from discord.ext import commands
from secrettoken import token
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get

intents = discord.Intents.default()
intents.presences = True
intents.members = True
 
client = commands.Bot(command_prefix='$', intents=intents)

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for file in os.listdir('./cogs'):
    if file.endswith(".py"):
        client.load_extension(f'cogs.{file[:-3]}')


client.run(token)

'''
code that can be used in other parts of project
'''
# @client.event
# async def on_ready():
#     print("hello world")

# @client.event
# async def on_member_join(member: discord.Member):
#     id = member.guild.id
#     server = client.get_guild(id)
#     role = server.get_role(992232900982476800)
#     await member.add_roles(role)

# @client.command()
# async def move(ctx, member : discord.Member, channel : discord.VoiceChannel):
#     await member.move_to(channel)
 
# @client.command(pass_context=True)
# @commands.has_permissions(manage_roles = True)
# async def addRole(ctx, user : discord.Member, * , role:discord.Role):
     
#     if role in user.roles:
#         await ctx.send(f"{user.mention} already has the role, {role}")
#     else:
#         await user.add_roles(role)
#         await ctx.send(f"{user.mention} is a {role}")
# @client.command()
# async def move(ctx, member : discord.Member, channel : discord.VoiceChannel):
#     await member.move_to(channel)

# Checks if the user activity is one of the name of the voice channels
# @client.command()
# @commands.has_guild_permissions(move_members=True)
# async def activity_checker(member, id, activity, voicechannels, general_channel):
#     for vc in voicechannels:
#         if str(activity) == str(vc):
#             print("here")
#             await member.move_to(vc)
