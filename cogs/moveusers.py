import discord
from discord.ext import commands
from difflib import SequenceMatcher
from constantvariables import DIFFERENT_NAME_CHANNELS, AUTO_MOVE_FLAG

class MoveUsers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Helper function to find similar channel name
    def _find_similar_channel(channel_name, voice_channels, threshold=0.5):
        max_channel = None
        max_score = 0
        channel_name_lower = channel_name.lower()
        
        for channel in voice_channels:
            channel_lower = channel.lower()
            similarity_score = SequenceMatcher(None, channel_name_lower, channel_lower).ratio()
            if similarity_score > max_score:
                max_score = similarity_score
                max_channel = channel
                
        if max_score >= threshold:
            return max_channel
        return None


    # Helper function to check if all required channels for automove are fulfilled
    def _check_required_channels(self):
        for req_channel in ["Lounge", "Study", "General", "Cinema"]:
            if req_channel not in DIFFERENT_NAME_CHANNELS:
                return False
        for channel_id in DIFFERENT_NAME_CHANNELS.values():
            channel = self.bot.get_channel(channel_id)
            if not channel:
                return False
        return True


    # Helper function to move users to a channel by the channel ID
    async def _move_users_to_channel_by_id(self, users, channel_id):
        """Move a list of users to the specified destination channel using channel ID."""
        destination_channel = self.bot.get_channel(channel_id)
        if destination_channel and isinstance(destination_channel, discord.VoiceChannel):
            for user in users:
                await user.move_to(destination_channel)

    # Command function that moves one user from one voice channel to another specified by a user
    @commands.command()
    async def move(self, ctx, member: discord.Member, channel: str):
        destination_channel = self._find_similar_channel(channel, ctx.guild.voice_channels)
        await member.move_to(destination_channel)

    # Command function that auto moves users to various different channels depending on activities of all users in all voice channels
    @commands.command()
    async def automove(self, ctx):
        if not self._check_required_channels():
            try:
                with open("constantvariables.py", "r+") as file:
                    content = file.read()
                    updated_content = content.replace("AUTO_MOVE_FLAG = True", "AUTO_MOVE_FLAG = False")
                    file.seek(0)
                    file.write(updated_content)
                    file.truncate()
                print("Required channels for using auto move error. Set AUTO_MOVE_FLAG in constantvariables.py to False")
                return
            except Exception as e:
                print("Error updating AUTO_MOVE_FLAG:", e)

        if AUTO_MOVE_FLAG:
            voice_channels = ctx.guild.voice_channels
            # Group users by their activities in voice channels
            voice_channel_groups = {}
            
            for channel in voice_channels:
                activity_members = {"Streaming": {}, "Nothing": []}
                for member in channel.members:
                    if member.activity and member.activity.name != "Spotify":
                        activity_name = member.activity.name
                    else:
                        activity_name = "Nothing"

                    if member.voice and member.voice.self_stream:
                        if member.activity:
                            activity_members["Streaming"][member.name] = member.activity.name
                        else:
                            activity_members["Streaming"][member.name] = "General"

                    if activity_name in activity_members:  # Check if activity exists in the dictionary
                        activity_members[activity_name].append(member)
                    else:
                        activity_members[activity_name] = [member]

                voice_channel_groups[channel.name] = activity_members

            print(voice_channel_groups)

            # voice_channel_groups would look like this: { VC_Name1 : { Activity 1 : [], Activity 2 : [] } , VC_Name2 : { Activity3 : [], Activity 1 : [] } }
            
            # Movement
            for channel in voice_channel_groups:  # Loop through voice channel groups
                current_channel = discord.utils.get(ctx.guild.voice_channels, name=channel)
                members_to_move = current_channel.members

                if len(voice_channel_groups[channel]["Streaming"]) >= 1: # if there is at least one person streaming
                    for member_screen_shares in voice_channel_groups[channel]["Streaming"]:
                        if voice_channel_groups[channel]["Streaming"][member_screen_shares] == "Visual Studio Code":
                            if self.bot.get_channel(DIFFERENT_NAME_CHANNELS["Study"]).voice_states: # If Study channel full then move to Lounge
                                await self._move_users_to_channel_by_id(members_to_move, DIFFERENT_NAME_CHANNELS["Lounge"])
                            else:
                                await self._move_users_to_channel_by_id(members_to_move, DIFFERENT_NAME_CHANNELS["Study"])
                        elif voice_channel_groups[channel]["Streaming"][member_screen_shares] == "General":
                            if self.bot.get_channel(DIFFERENT_NAME_CHANNELS["Cinema"]).voice_states: # If Cinema channel full then move to Lounge
                                await self._move_users_to_channel_by_id(members_to_move, DIFFERENT_NAME_CHANNELS["Lounge"])
                            else:
                                await self._move_users_to_channel_by_id(members_to_move, DIFFERENT_NAME_CHANNELS["Cinema"])   
                        else: # If someone is streaming and playing an activity
                            continue
                
                elif voice_channel_groups[channel]["Nothing"] == len(current_channel.members): # If noone is playing a game
                    await self._move_users_to_channel_by_id(members_to_move, DIFFERENT_NAME_CHANNELS["Lounge"])
                
                elif len(voice_channel_groups[channel]) == 3: # Only one activity being played
                    keys_list = list(voice_channel_groups[channel].keys())
                    destination_channel = discord.utils.get(ctx.guild.voice_channels, name=keys_list[2])
                    if self.bot.get_channel(destination_channel.id).voice_states: # If destination channel is occupied
                        similar_channel_name = self._find_similar_channel(destination_channel.name+" 2", ctx.guild.voice_channels)
                        if similar_channel_name == destination_channel.name: # If the result is the same name
                            await self._move_users_to_channel_by_id(members_to_move, DIFFERENT_NAME_CHANNELS["General"]) # Moved to general channel
                        else: # Moved to second channel (IE: Valorant 2)
                            destination_channel = discord.utils.get(ctx.guild.voice_channels, name=similar_channel_name)
                            await self._move_users_to_channel_by_id(members_to_move, destination_channel.id)
                    else:
                        await self._move_users_to_channel_by_id(members_to_move, destination_channel.id)
                
                # elif len(voice_channel_groups[channel]) >= 4:  # Multiple activities being played




        else:
            print("Auto move flag set to False. Set to True in constantvariables.py if you want to use auto move ability")    

                

def setup(bot):
    bot.add_cog(MoveUsers(bot))
