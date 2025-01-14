# import discord
# import bot.constants as constants
# import mongoDB
from discord.ext import commands
# from discord.ext import tasks
# from datetime import datetime
# from datetime import date
# import datetime as dt
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# import asyncio




# # Create a new client and connect to the MongoDB server
# mongoClient = MongoClient(mongoDB.MONGODB_URI, server_api=ServerApi('1'))


# try:
#     # Send a ping to confirm a successful connection to MongoDB
#     mongoClient.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

# # Select the database
# db = mongoClient.Rasenbot



# class DisplayInfo(commands.Cog):

#     def __init__(self,bot):
#         self.bot = bot
#         self.timers = {}
#         self.current_collection = ""
#         self.current_guild_name = ""
#         self.current_date = str(date.today())
        
#     # The 'mem_before' parameter represents the member's previous state, and 'mem_after' represents the current state.
#     @commands.Cog.listener()
#     async def on_member_update(self, mem_before:discord.Member, mem_after:discord.Member):
#         if mem_before.activity and mem_before.activity == mem_after.activity:
#             return
    
#         if self.current_guild_name != mem_before.guild.name:
#             if mem_before.guild.name not in db.list_collection_names():
#                 newCollection = db[mem_before.guild.name]  # If the collection doesn't exist, create a new one for the guild/server
#                 self.current_guild_name = mem_before.guild.name
#                 self.current_collection = newCollection               
#                 newCollection.insert_one({}) # Create a new blank document in the new Collection
#                 self.timers = self.current_collection.find_one() # Load blank document from the MongoDB collection
#             else:
#                 self.current_collection = db[mem_before.guild.name] # If the collection exists, get the existing collection for the guild
#                 self.current_guild_name = mem_before.guild.name
#                 self.timers = self.current_collection.find_one() # Load existing document from the MongoDB collection
        
#         # Track activity updates for members
#         if not mem_before.activity and mem_after.activity: # activity starts/ongoing
#             if mem_after.name not in self.timers:
#                 self.timers[mem_after.name] = {} # If the member is not already tracked, add them
#             if self.current_date not in self.timers[mem_after.name]:
#                 self.timers[mem_after.name][self.current_date] = {} # If the current date is not present in the member's dictionary, add it
#             if mem_after.activity.name not in self.timers[mem_after.name][self.current_date]: # If the member's current activity/game/status is not present, add it with initial values
#                 self.timers[mem_after.name][self.current_date][mem_after.activity.name] = {
#                     "totalTime" : 0, 
#                     "startTime" : 0,
#                     "updateTask" : None,
#                 }
#             self.timers[mem_after.name][self.current_date][mem_after.activity.name]["startTime"] = datetime.now() # Record the start time of the member's current activity
#             print("start:", self.timers)
#             self.timers[mem_after.name][self.current_date][mem_after.activity.name]["updateTask"] = asyncio.create_task(self.timed_update(mem_before, mem_after))
#         elif (mem_before.activity and not mem_after.activity) or (mem_before.status != mem_after.status and mem_after.status == discord.Status.offline): # activity stopped or member
#             if mem_before.name in self.timers:
#                 if self.current_date in self.timers[mem_before.name]:
#                     if mem_before.activity is not None and mem_before.activity.name in self.timers[mem_before.name][self.current_date]:
#                         if self.timers[mem_before.name][self.current_date][mem_before.activity.name]["updateTask"]:
#                             self.timers[mem_before.name][self.current_date][mem_before.activity.name]["updateTask"].cancel()
#                             try:
#                                 await self.timers[mem_before.name][self.current_date][mem_before.activity.name]["updateTask"]
#                             except asyncio.CancelledError:
#                                 print("task is now cancelled")
#                         self.timers[mem_before.name][self.current_date][mem_before.activity.name]["updateTask"] = None

#                         currentStartTime = self.timers[mem_before.name][self.current_date][mem_before.activity.name]["startTime"]
#                         if currentStartTime:
#                             playTime = datetime.now() - currentStartTime # Calculate the time difference (playTime) between the start and end time of the activity
#                             self.timers[mem_before.name][self.current_date][mem_before.activity.name]["totalTime"] = self.timers[mem_before.name][self.current_date][mem_before.activity.name].get("totalTime", 0) + playTime.total_seconds() # Add the play time to the member's total play time for that activity for that day
#                         print("end:", self.timers) # printing the dictionary to see the updates after an activity is ended
#                         self.current_collection.replace_one({}, self.timers) # Update the MongoDB collection with the updated activity data(self.timers)

#     # This function is an asynchronous coroutine that runs indefinitely in the background when mem_after.activity is True.
#     # It is designed to update activity time information for a Discord member ('mem_after') whenever they start a new activity every 5 minutes.
#     async def timed_update(self, mem_before: discord.Member, mem_after: discord.Member):
#         await asyncio.sleep(300)
#         while not mem_before.activity and mem_after.activity:
#             playTime = 300 # add 5 mins to activity time
#             self.timers[mem_after.name][self.current_date][mem_after.activity.name]["totalTime"] = self.timers[mem_after.name][self.current_date][mem_after.activity.name].get("totalTime", 0) + playTime
#             self.timers[mem_after.name][self.current_date][mem_after.activity.name]["startTime"] = datetime.now()
#             print("in timed_update", self.timers) #printing the dictionary to see the timed updates
#             await asyncio.sleep(300)
            

#     # This is a Discord bot command that retrieves and displays activity time information for a given member.
#     @commands.command()
#     async def get_info(self, member):
#         if member.author.name in self.timers:
#             channel = member.channel
#             embed = discord.Embed(
#                 title = f"{member.author.name}'s Time Information",
#                 color = discord.Color.blue()
#             )
#             for date, activities in self.timers[member.author.name].items():
#                 temp_string = " "
#                 for activity, time in activities.items():
#                     temp_time = time["totalTime"]
#                     convert = str(dt.timedelta(seconds = round(temp_time)))
#                     temp_string += f'> {activity}: {convert}\n'

#                 embed.add_field(name=f'**{date}**', value= temp_string,inline=False)

#             await channel.send(embed=embed)
        
class DisplayInfo(commands.Cog):
    def __init__(self,bot):
        pass

async def setup(bot):
    await bot.add_cog(DisplayInfo(bot))
            
