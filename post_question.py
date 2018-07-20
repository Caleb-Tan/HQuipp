import discord
import bs4_search as search
import ast
from string import digits
from threading import Thread
from discord.ext.commands import Bot
import time
import asyncio
import time
import question as qs
import sys
import json 

sys.dont_write_bytecode = True

TOKEN = 'NDYwNTkyOTE0MzM5MjAxMDI0.DhHAGA.sem1-DZGmZ5chdamGdd-TE6xQVM'
BOT_PREFIX = (".")

client = discord.Client()
client = Bot(command_prefix=BOT_PREFIX)

choices = ["placeholder", "placeholder", "placeholder"]
data = {}

def generate_embed(choice, command, choiceNo):
    result = search.question(command.replace("/", choice))
    new_embed = discord.Embed(title=choice, description=result["result"], color=0x00f900)
    new_embed.set_footer(text="Search Time: " + str(result["time"]))
    data["embed" + str (choiceNo)] = new_embed


@client.command(pass_context=True)
async def q(ctx):
    if ctx.message.author == client.user:
        return
    command = ctx.message.content.strip(".q ")
    if "/" in command:
        global choices
        t1 = Thread(target = generate_embed, args=(choices[0],command,1))
        t2 = Thread(target = generate_embed, args=(choices[1],command,2))
        t3 = Thread(target = generate_embed, args=(choices[2],command,3))
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join
        t3.join()
        for i in range(1,4):
            await client.send_message(ctx.message.channel, embed=data["embed" + str(i)])
    else:
        result = search.question(command)
        new_embed = discord.Embed(title=command, description=result["result"], color=0x00f900)
        new_embed.set_footer(text="Search Time: " + str(result["time"]))
        await client.send_message(ctx.message.channel, embed=new_embed)

@client.command(pass_context=True)
async def math(ctx):
    command = ctx.message.content.strip(".math").lstrip().rstrip().replace("^", "**")
    print(command)
    try:
        math = round(eval(command),4)
        await client.send_message(ctx.message.channel, "`" + str(math) + "`")
    except (SyntaxError, NameError, TypeError):
        await client.send_message(ctx.message.channel, "`Um something went wrong there, please try again.`")
    except (ZeroDivisionError):
        await client.send_message(ctx.message.channel, "`DIVISION BY ZERO IS NOT ALLOWED BRO`")

@client.command(pass_context=True)
async def bping(ctx):
    if "bping" in ctx.message.content:
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await client.send_typing(channel)
        t2 = time.perf_counter()
        embed = discord.Embed(title="Ben10 Ping Delay", description=':stopwatch: {}'.format(round((t2-t1)*1000)) + "ms", color=0xEE82EE)
        msg = await client.send_message(channel, embed=embed)


async def post_embed(data):
    print(data)
    query = data["question_str"].replace(" ", "+")
    url = "https://www.google.com/search?q=" + query
    choices[0] = data["answers"][0]
    choices[1] = data["answers"][1]
    choices[2] = data["answers"][2]
    description = ""
    for i in range(1,4):
        ans = data["answers"][i-1]
        ans_url = url + "+AND+" + ans.replace(" ", "+")
        description += str(i) + ". " + "[" + ans + "]" + "(" + ans_url + ")" + "\n" 
    new_embed = discord.Embed(title=data["question_str"], url=url, description=description, color=0xff2600)
    new_embed.add_field(name="Question", value=str(data["question_number"]) + " out of " + str(data["question_count"]))
    await client.send_message(client.get_channel("468874613498314752"), embed=new_embed)
    
    data = await qs.analyze_question(data["question_str"], data["answers"])
    if data != "":
        new_embed = discord.Embed(title="Location Question Detected", color=0x0000ff)
        new_embed.set_image(url=url)
        await client.send_message(client.get_channel("468874613498314752"), embed=new_embed)

async def background_log_loop():
    await client.wait_until_ready()
    prev = {}
    while not client.is_closed:
        with open('data.json') as f:
            data = json.load(f)
            if data != prev:
                prev = data
                await post_embed(data)

        await asyncio.sleep(0.05)



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(background_log_loop())
client.run(TOKEN)
