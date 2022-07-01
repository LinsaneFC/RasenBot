import discord
from discord.ext import commands
from secrettoken import token
 
intents = discord.Intents.default()
intents.presences = True
intents.members = True
 
client = commands.Bot(command_prefix='$', intents=intents)
 
 

# @client.event
# async def on_ready():
#     general_channel = client.get_channel(989667924291772481)
   
#     #await general_channel.send("Hello, world!")
   
#     voicechannels = []
#     for channel in general_channel.guild.channels:
#         if type(channel) == discord.channel.VoiceChannel:
#             voicechannels.append(channel)
 
@client.command()
async def move(ctx, member : discord.Member, channel : discord.VoiceChannel):
    await member.move_to(channel)
 
    # for member in general_channel.members:
    #     await activity_checker(member, member.id, member.activity, voicechannels, general_channel)
 
# @client.commands
# async def on_member_join(member):
#     print(member)
   
 
# @client.command()
# @commands.has_guild_permissions(move_members=True)
# async def activity_checker(member, id, activity, voicechannels, general_channel):
#     for vc in voicechannels:
#         if str(activity) == str(vc):
#             print("here")
#             await member.move_to(vc)
 
 
 
 
 
       
   
 
 
client.run(token)

