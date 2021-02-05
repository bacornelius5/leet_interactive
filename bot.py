# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

import pymongo
from pymongo import MongoClient

from state import Leet

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

bot = Leet()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == guild:
            break
    
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

CONNECTION_URL = os.getenv('CONNECTION_URL')
cluster = MongoClient(CONNECTION_URL) 

db = cluster["leet_code_problems"]



# check message for the keyword entry, asking them what problem they're entering a submission for

@client.event
async def on_message(message):
    
    if bot.new_entry == False:

        if message.author == client.user:
            return
        
        if "entry" in str(message.content.lower()):
            reply = 'What is the problem called?'
        else:
            return

        bot.new_entry = True
        await message.channel.send(reply)
        return
    
    if bot.new_entry == True:
    
        if message.author == client.user:
            return

        # prepare an iterable to be inserted in the mongo collection

        problem_data = {"_id": message.author.id, "problem": str(message.content.lower())}
        collection = db[str(message.content.lower())]
        collection.insert_one(problem_data)

        # reset new_entry to prepare for next commands, sends a confimation message to user 
        bot.new_entry = False
        await message.channel.send('Created a save for ' + str(message.content.lower()))




client.run(TOKEN)