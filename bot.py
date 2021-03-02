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
    
    if bot.should_pull == True:
        
        # find the database for the corresponding problem to pull the information from
        collection = db[str(message.content.lower())]
        data = collection.find_one({"_id" : message.author.id})
        runtime = "Runtime: " + str(data["runtime"])
        memory = "\nMemory usage: " + str(data["memory usage"])
        solution = "\nSolution: \n\n" + str(data["solution"])
        await message.channel.send(runtime)
        await message.channel.send(memory)
        await message.channel.send(solution)

        return

    if bot.new_entry == False:

        if "entry" in str(message.content.lower()):
            reply = 'What is the problem called?'
            bot.new_entry = True
        elif "show me" in str(message.content.lower()):
            reply = 'What is  the problem called?'
            bot.should_pull = True
            

        await message.channel.send(reply)
        return

    if bot.new_problem == False:
    
        # prepare an iterable to be inserted in the mongo collection

        bot.problem_data = {"_id": message.author.id, "problem": str(message.content.lower())}

        bot.new_problem = True

        await message.channel.send('Creating a save for ' + str(message.content.lower()))
        await message.channel.send('Please enter your runtime')
        return
    
    if bot.runtime_entry == False:
        
        runtime = 0

        # loop through the message to pull out only the numerical value
        for i in str(message.content):
            
            if i.isnumeric() == False:
                continue
            else:
                runtime = (runtime * 10) + int(i) # multiply by 10 in order to move the decimal place as the number grows, then add the new lowest digit
        
        bot.problem_data["runtime"] = runtime
        
        bot.runtime_entry = True
        await message.channel.send('Runtime saved')
        await message.channel.send('Please enter your memory usage')
        return

    if bot.memory_usage == False:

        memory_usage = 0

        # pull the memory usage with the same method as the runtime
        for i in str(message.content):
            
            if i.isnumeric() == False:
                continue
            else:
                memory_usage = (memory_usage * 10) + int(i) # multiply by 10 in order to move the decimal place as the number grows, then add the new lowest digit
        
        bot.problem_data["memory usage"] = memory_usage
        
        bot.memory_usage = True
        await message.channel.send('Memory usage saved')
        await message.channel.send('Please enter your solution')
        return

    if bot.solution == False:

        bot.problem_data["solution"] = str(message.content)

        bot.solution = True

        collection = db[bot.problem_data["problem"]]
        collection.insert_one(bot.problem_data)

        await message.channel.send("Solution saved, problem: " + str(bot.problem_data["problem"]) + " is stored")

        # reset class variables
        bot.new_entry = False
        bot.new_problem =  False
        bot.runtime_entry = False
        bot.memory_usage = False
        bot. solution = False

        return
    





client.run(TOKEN)