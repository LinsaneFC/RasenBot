import os
import asyncio
from discord import Intents
from discord.ext import commands
from secrettoken import token

intents = Intents.default()
intents.presences = True
intents.members = True
intents.reactions = True
intents.message_content = True
 
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print("Rasenbot is running...")

async def load_extensions():
    for file in os.listdir('./cogs'):
        if file.endswith(".py"):
            await bot.load_extension(f'cogs.{file[:-3]}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)

asyncio.run(main())

'''
code that can be used in other parts of project
'''
# @bot.event
# async def on_ready():
#     print("hello world")

# @bot.event
# async def on_member_join(member: discord.Member):
#     id = member.guild.id
#     server = bot.get_guild(id)
#     role = server.get_role(992232900982476800)
#     await member.add_roles(role)

 
# @bot.command(pass_context=True)
# @commands.has_permissions(manage_roles = True)
# async def addRole(ctx, user : discord.Member, * , role:discord.Role):
     
#     if role in user.roles:
#         await ctx.send(f"{user.mention} already has the role, {role}")
#     else:
#         await user.add_roles(role)
#         await ctx.send(f"{user.mention} is a {role}")
# @bot.command()
# async def move(ctx, member : discord.Member, channel : discord.VoiceChannel):
#     await member.move_to(channel)

# Checks if the user activity is one of the name of the voice channels
# @bot.command()
# @commands.has_guild_permissions(move_members=True)
# async def activity_checker(member, id, activity, voicechannels, general_channel):
#     for vc in voicechannels:
#         if str(activity) == str(vc):
#             print("here")
#             await member.move_to(vc)
