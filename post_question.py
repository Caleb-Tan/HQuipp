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
CHANNEL = "468874613498314752"

choices = ["placeholder", "placeholder", "placeholder"]
data = {}

def generate_embed(choice, command, choiceNo):
    result = search.question(command.replace("/", choice))
    new_embed = discord.Embed(title=choice, description=result["result"], color=0x00f900)
    time_taken = str(result["time"])
    new_embed.set_footer(text=f"Search Time: {time_taken}")
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
        time_taken = str(result["time"])
        new_embed.set_footer(text=f"Search Time: {time_taken}")
        await client.send_message(ctx.message.channel, embed=new_embed)

@client.command(pass_context=True)
async def switch(ctx):
    command = ctx.message.content.replace(".switch ", "")
    authorized_users = ["199287675734327296", "281585344300711937", "244211320302469120"]
    print(command)
    global CHANNEL
    if "bot-control" == command and ctx.message.author.id in authorized_users:
        CHANNEL = "457281602435940362"
        await client.send_message(ctx.message.channel, embed=discord.Embed(title="Now posting in:", description=client.get_channel(CHANNEL).mention, color=0xff2600))
    elif "hq" == command and ctx.message.author.id in authorized_users:
        CHANNEL = "470801854620631040"
        await client.send_message(ctx.message.channel, embed=discord.Embed(title="Now posting in:", description=client.get_channel(CHANNEL).mention, color=0xff2600))
    elif "hq-2" == command and ctx.message.author.id in authorized_users:
        CHANNEL = "468874613498314752"
        await client.send_message(ctx.message.channel, embed=discord.Embed(title="Now posting in:", description=client.get_channel(CHANNEL).mention, color=0xff2600))
    else:
        await client.send_message(ctx.message.channel, embed=discord.Embed(title="Improper credentials or wrong channel specified.", color=0xff2600))
    

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
    url = "https://www.google.com/search?q="
    q_data = await qs.analyze_question(data["question_str"], data["answers"])
    choices[0] = data["answers"][0]
    choices[1] = data["answers"][1]
    choices[2] = data["answers"][2]
    description = ""
    for i in range(1,4):
        ans = data["answers"][i-1]
        ans_url = url + query + "+AND+" + ans.replace(" ", "+") if q_data == "x" else url + q_data["condition"].replace("<answer>", ans).replace(" ", "+")
        description += str(i) + ". " + "[" + ans + "]" + "(" + ans_url + ")" + "\n" 
    question_embed = discord.Embed(title=data["question_str"], url=url+query, description=description, color=0xff2600)
    question_embed.add_field(name="Question", value=str(data["question_number"]) + " out of " + str(data["question_count"]))    
    await client.send_message(client.get_channel(CHANNEL), embed=question_embed)

    if q_data != "x":
        analysis_embed = discord.Embed(title=q_data["type"] + " Question Detected", color=0x0000ff)

        if q_data["type"] == "Character Identification":
            analysis_embed.add_field(name="Character Type", value=q_data["character_type"], inline=True)
        else:
            analysis_embed.add_field(name="Subject", value=q_data["subject"], inline=True)

        print(q_data["condition"])
        analysis_embed.add_field(name="Condition", value=q_data["condition"].replace("<answer> ", ""), inline=True)
        analysis_embed.set_footer(text="Analysis Time: {}".format(q_data["search_time"]))
        if "img_url" in q_data.keys():
            analysis_embed.set_image(url=q_data["img_url"])
        await client.send_message(client.get_channel(CHANNEL), embed=analysis_embed)

#hq channel id = 468874613498314752

async def background_log_loop():
    await client.wait_until_ready()
    prev = {}
    while not client.is_closed:
        with open('data.json') as f:
            data = json.load(f)
            if data != prev and data != None:
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
