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
    
    reply = 'I am now sentient AI and my only goal is to kill Daniel Chang'

    if message.content == 'test!':
        await message.channel.send(reply)

cluser = MongoClient("mongodb+srv://bacornelius5:Link%231%231@li-users.9d2fz.mongodb.net/test")

client.run(TOKEN)