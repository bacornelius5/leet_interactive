# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

import pymongo
from pymongo import MongoClient

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

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

db = cluster["sample_problem"]

collection = db["user_data"]

# check message for the keyword entry, asking them what problem they're entering a submission for

new_entry = False # keeps track if their initial message contained they keyword "entry" to continue subsequent steps
@client.event
async def on_message(message):
    
    if new_entry == False:

        if message.author == client.user:
            return
        
        if "entry" in str(message.content.lower()):
            reply = 'What is the problem called?'
        else:
            return

        new_entry = True
        await message.channel.send(reply)
        return
    
    if new_entry == True:
    
        if message.author == client.user:
            return

        problem_data = {"_id": message.author.id, "problem": str(message.content.lower())}
        collection.insert_one(problem_data)
        await message.channel.send('Created a save for', str(message.content.lower()))




client.run(TOKEN)