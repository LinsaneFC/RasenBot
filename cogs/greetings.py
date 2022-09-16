import discord
from discord.ext import commands

#Bot sends out a greeting to the server when a new member joins the server
class Greetings(commands.Cog):

    def __init__(self,client):
        self.client = client
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        #Sends the embedded message to the channel that is the welcome page
        channel = member.guild.system_channel
        if channel is not None:
            #Bot sends an embedded message that is blue
            embed=discord.Embed(title="Hello!", description=f'Welcome to the server {member.mention}!\nPlease read the rules before doing anything on the server\n\n1. No racism\n2. No bullying\n3. Be kind\n4. Don\'t ask for roles\n5. Use common sense\n6. Send Parker **LOTS** of kisses\n\nIf you do not follow any of these rules you will be kicked and potentially banned\n\nEnjoy your stay!', color=discord.Color.blue())
            #Author of the message with a profile picture
            embed.set_author(name="RasenBot", icon_url="https://avatars.githubusercontent.com/u/39735649?s=280&v=4")
            #A thumbnail that is displayed in the right side of the embedded message
            embed.set_thumbnail(url="http://www.willpap-projects.com/Docus/Educational/Slide_Shows/Gifs/Funny/Cat_Paws_79.gif")
            #Footer
            embed.set_footer(text="If you are curious about RasenBot, please type $help in the bot commands channel for more commands!")
            await channel.send(embed=embed)

def setup(client):
    client.add_cog(Greetings(client))
