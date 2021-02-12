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

    if message.author == client.user:
        return

    if bot.new_entry == False:

        if "entry" in str(message.content.lower()):
            reply = 'What is the problem called?'
        else:
            return

        bot.new_entry = True
        await message.channel.send(reply)
        return
    
    if bot.new_entry == True:
    
        # prepare an iterable to be inserted in the mongo collection

        problem_data = {"_id": message.author.id, "problem": str(message.content.lower())}
        

        # reset new_entry to prepare for next commands, sends a confimation message to user 
        bot.new_entry = False
        bot.runtime_entry = True

        await message.channel.send('Creating a save for ' + str(message.content.lower()))
        await message.channel.send('Please enter your runtime')
        return
    
    if bot.runtime_entry == True:
        
        runtime = 0

        # loop through the message to pull out only the numerical value
        for i in str(message.content):
            
            if i.isnumeric == False:
                continue
            else:
                runtime = (runtime * 10) + int(i) # multiply by 10 in order to move the decimal place as the number grows, then add the new lowest digit
        
        problem_data["runtime"] = runtime
        collection = db[str(message.content.lower())]
        collection.insert_one(problem_data)




client.run(TOKEN)