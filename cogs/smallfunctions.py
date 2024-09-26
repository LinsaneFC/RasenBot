import discord
import random
import #new file storing priv variables
from discord.ext import commands

# Class responsible for all the small commands run by server members.
class SmallFunctions(commands.cog):

# Command function for randomized coinflip. Will return a heads or tails.
    @commands.command()
    async def random_coinflip(self, ctx):
        heads = 1#store in diff file as const variables
        tails = 0#store in diff file as const variables
        rand_cf = random.randint(0,1)
        if (rand_cf == heads):
            return #gif for heads
        else:
            return #gif for tails


# Command function decide which side you believe the coin will land on.
    @commands.command()
    async def decided_coinflip(self, ctx):
        decided_cf = random.randint(0,1)


# Command function that will be a help guide for RasenBot
    @commands.command()
    async def help(self, ctx):

# Command Function executes a Die roll between numbers 1-6 and returns a GIF
    @commands.command()
    async def roll_die(self, ctx):
       rand_die = random.randint(1,6)







def setup(client):
    client.add_cog(SmallFunctions(client))