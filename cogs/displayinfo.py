import discord
import constantvariables
import mongoDB
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime
from datetime import date
import datetime as dt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import asyncio




# Create a new client and connect to the MongoDB server
mongoClient = MongoClient(mongoDB.MONGODB_URI, server_api=ServerApi('1'))


try:
    # Send a ping to confirm a successful connection to MongoDB
    mongoClient.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Select the database
db = mongoClient.Rasenbot



class DisplayInfo(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.current_collection = db["UserTracking"] # TODO: Move this secrets file
        self.timers = self.current_collection.find_one() 
        self.current_guild_name = ""
        self.current_date = str(date.today())
        self.members_online = set()
        self.timed_task = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.status == discord.Status.online:
                    self.members_online.add(member)

        if len(self.members_online) != 0:
            self.timed_task = asyncio.create_task(self.timed_update()) #start timed_update once bot goes online if a member is online


        
    # The 'mem_before' parameter represents the member's previous state, and 'mem_after' represents the current state.
    @commands.Cog.listener()
    async def on_member_update(self, mem_before:discord.Member, mem_after:discord.Member):
        self.current_guild_name = mem_before.guild.name
        
        if mem_before.activity and mem_before.activity == mem_after.activity:
            return

        if mem_before.status is discord.Status.offline and mem_after.status is discord.Status.online:
            self.members_online.add(mem_after)
            if self.timed_task.done():
                self.timed_task = asyncio.create_task(self.timed_update())
            print("added:", mem_after.name)
        
        elif mem_before.status is discord.Status.online and mem_after.status is discord.Status.offline:
            self.members_online.remove(mem_before)
            print("removed:", mem_before.name)
            if len(self.members_online) <= 0:
                self.timed_task.cancel()
                try:
                    await self.timed_task
                except asyncio.CancelledError:
                    print("task is now cancelled")
        
        # Track activity updates for members
        if not mem_before.activity and mem_after.activity: # activity starts/ongoing
            after_string_id = str(mem_after.id)
            if after_string_id not in self.timers:
                self.timers[after_string_id] = {} # If the member is not already tracked, add them
            if self.current_date not in self.timers[after_string_id]:
                self.timers[after_string_id][self.current_date] = {} # If the current date is not present in the member's dictionary, add it
            if mem_after.activity.name not in self.timers[after_string_id][self.current_date]: # If the member's current activity/game/status is not present, add it with initial values
                self.timers[after_string_id][self.current_date][mem_after.activity.name] = {
                    "totalTime" : 0, 
                    "startTime" : 0,
                }
            self.timers[after_string_id][self.current_date][mem_after.activity.name]["startTime"] = datetime.now() # Record the start time of the member's current activity
            print("start:", self.timers)
        elif (mem_before.activity and not mem_after.activity) or (mem_before.status != mem_after.status and mem_after.status == discord.Status.offline): # activity stopped or member
            before_string_id = str(mem_before.id)
            if before_string_id in self.timers:
                if self.current_date in self.timers[before_string_id]:
                    if mem_before.activity is not None and mem_before.activity.name in self.timers[before_string_id][self.current_date]:
                        currentStartTime = self.timers[before_string_id][self.current_date][mem_before.activity.name]["startTime"]
                        self.timers[before_string_id][self.current_date][mem_before.activity.name]["startTime"] = None
                        if currentStartTime:
                            playTime = datetime.now() - currentStartTime # Calculate the time difference (playTime) between the start and end time of the activity
                            self.timers[before_string_id][self.current_date][mem_before.activity.name]["totalTime"] = self.timers[before_string_id][self.current_date][mem_before.activity.name].get("totalTime", 0) + playTime.total_seconds() # Add the play time to the member's total play time for that activity for that day
                        print("end:", self.timers) # printing the dictionary to see the updates after an activity is ended
                        self.current_collection.replace_one({}, self.timers) # Update the MongoDB collection with the updated activity data(self.timers)

    async def timed_update(self):
        while len(self.members_online) != 0:
            await asyncio.sleep(300)
            for member in self.members_online:
                string_id = str(member.id)
                if string_id in self.timers and self.current_date in self.timers[string_id]:
                    for activity, info in self.timers[string_id][self.current_date].items():
                        if info["startTime"] != None:
                                if member.activity.name in self.timers[string_id][self.current_date]:
                                    currentStartTime = self.timers[string_id][self.current_date][member.activity.name]["startTime"]
                                    playTime = datetime.now() - currentStartTime 
                                    self.timers[string_id][self.current_date][activity]["totalTime"] = self.timers[string_id][self.current_date][activity].get("totalTime", 0) + playTime.total_seconds()
                                    self.timers[string_id][self.current_date][activity]["startTime"] = datetime.now()
            
            print("timed update:", self.timers)
            self.current_collection.replace_one({}, self.timers) 
                        
            

    # This is a Discord bot command that retrieves and displays activity time information for a given member.
    @commands.command()
    async def get_info(self, member):
        # self.current_collection.replace_one({}, self.timers)
        string_id = str(member.author.id)
        if string_id in self.timers:
            channel = member.channel
            user = await self.bot.fetch_user(string_id)
            embed = discord.Embed(
                title = f"{user.name}'s Time Information",
                color = discord.Color.blue()
            )
            for date, activities in self.timers[string_id].items():
                temp_string = " "
                for activity, time in activities.items():
                    temp_time = time["totalTime"]
                    convert = str(dt.timedelta(seconds = round(temp_time)))
                    temp_string += f'> {activity}: {convert}\n'

                embed.add_field(name=f'**{date}**', value= temp_string,inline=False)

            await channel.send(embed=embed)
        

def setup(bot):
    bot.add_cog(DisplayInfo(bot))
            
