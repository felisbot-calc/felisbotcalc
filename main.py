import os
import math
import logging
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message
from discord.ext import commands
import webserver

load_dotenv()
token = os.environ('DISCORD_TOKEN')

handler = logging.FileHandler(filename = 'discord.log', encoding = 'utf-8', mode = 'w')
intents = discord.Intents.default()

intents.message_content = True 
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready() -> None:
    print(f'{bot.user.name} is now running!')

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    
    if 'uwuify' in message.content.lower():
        await message.delete()
        await message.channel.send(f'{message.author.mention} - D')

    await bot.process_commands(message)

@bot.command()
async def calculate(ctx, tokens: int, crafting_time: int, boost: int):
    try: 

        increment_A = 0
        increment_BC = 0 
        increment_D = 0
        increment_E = 0

        cycle = round(crafting_time / 15)
        totalCost = -1
        numthreeS = 0
        
        num_A = numthreeS * 7 
        num_B, num_C = numthreeS * 9, numthreeS * 9 
        num_D = numthreeS * 2
        num_E = numthreeS    

        num_List = [num_A, num_B, num_C, num_D, num_E]

        while tokens >= totalCost:
           
            numthreeS += 1

            num_A = numthreeS * 7 
            num_B, num_C = numthreeS * 9, numthreeS * 9 
            num_D = numthreeS * 2
            num_E = numthreeS    

            num_List = [num_A, num_B, num_C, num_D, num_E]

            a_Cost, b_Cost,  c_Cost = (5 * (num_List[0]) ** 2 + (15 * num_List[0])) / (boost * cycle), (5 * (num_List[1]) ** 2 + (15 * num_List[1])) / (boost * cycle), (5 * (num_List[1]) ** 2 + (15 * num_List[1])) / (boost * cycle)
            
            d_Cost, e_Cost = (37.5 * (num_List[3]) ** 2 + (112.5 * num_List[3])) / (boost * cycle), (50 * (num_List[4]) ** 2 + (150 * num_List[4])) / (boost * (cycle/2))

            costList = [a_Cost, b_Cost, c_Cost, d_Cost, e_Cost]

            for i in range (len(costList)):

                if i == 0:
                    if costList[i] % 1 != 0:
                        increment_A += 1
                        costList[i] += increment_A
                
                elif i == 1:
                    if costList[i] % 1 != 0:
                        increment_BC += 1
                        costList[i] += increment_BC
                        costList[i+1] += increment_BC

                elif i == 3:
                    if costList[i] % 1 == 0:
                        increment_D += 1
                        costList[i] += increment_D
            
                elif i == 4:
                    if costList[i] % 1 == 0:
                        increment_E += 1
                        costList[i] += increment_E

            totalCost = sum(costList, numthreeS * 300)

            for i in range (len(num_List)):
                num_List[i] /= cycle

        await ctx.send(f'The total cost is {int(totalCost)} with {numthreeS} 3 stars\n{round(num_List[0])} A x {cycle} times, {round(num_List[1])} B x {cycle} times, {round(num_List[2])} C x {cycle} times, {round(num_List[3])} D x {cycle} times, {round(num_List[4] * 2)} E x {cycle/2} times')

    except Exception as e:
        await ctx.send(f'An error occurred: {e}')


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("shut down")
    await bot.close()

webserver.keep_alive()
bot.run(token, log_handler=handler, log_level = logging.DEBUG)

