import discord
from discord.ext import commands

# Sends a greeting message that requires a new user to react to the message in order to receive a role to access the server
class Greetings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(1011049173442895902)  # Replace with the actual ID of your welcome text channel

        if channel is not None:

            embed = discord.Embed(
                title="Hello!",
                description=f"Welcome to the server {member.mention}!\nPlease read the rules and react to the emoji below if you want access to the server\n\n1. No racism\n2. No bullying\n3. Be kind\n4. Don't ask for roles\n5. Use common sense\n6. Send Parker **LOTS** of kisses\n\nIf you do not follow any of these rules, you will be kicked and potentially banned\n\nEnjoy your stay!",
                color=discord.Color.blue()
            )
            self._last_member = member
            embed.set_author(name="RasenBot", icon_url="https://avatars.githubusercontent.com/u/39735649?s=280&v=4")
            embed.set_thumbnail(url="http://www.willpap-projects.com/Docus/Educational/Slide_Shows/Gifs/Funny/Cat_Paws_79.gif")
            embed.set_footer(text="If you are curious about RasenBot, please type $help in the bot commands channel for more commands!")

            message = await channel.send(embed=embed)
            await message.add_reaction("👍")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == 1011049173442895902:  # Replace with the actual ID of your welcome text channel
            if "👍" in str(payload.emoji):
                guild = self.client.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)
                if member is not None and not member.bot:  # Check if the member exists and is not a bot
                    role = guild.get_role(1120501110407434301) # Replace with the actual ID of the role you want to assign
                    await member.add_roles(role)


def setup(client):
    client.add_cog(Greetings(client))
