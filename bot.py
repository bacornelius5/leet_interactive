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

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    reply = 'Hello! Test Complete'

    if message.content == 'test!':
        await message.channel.send(reply)

client.run(TOKEN)