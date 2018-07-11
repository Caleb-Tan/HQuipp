import discord
import bs4_search as search
import ast
from string import digits
from threading import Thread
import time
import asyncio
from time import sleep


TOKEN = 'NDYwNTkyOTE0MzM5MjAxMDI0.DhHAGA.sem1-DZGmZ5chdamGdd-TE6xQVM'

client = discord.Client()

choices = ["placeholder", "placeholder", "placeholder"]
data = {}

def generate_embed(choice, command, choiceNo):
    result = search.question(command.replace("/", choice))
    data["embed" + str (choiceNo)] = discord.Embed(title=choice, description=result, color=0x00f900)


@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return
        
    if len (message.embeds) == 0:
        if message.content.startswith(".q "):
            command = message.content.strip(".q ")
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
                    await client.send_message(message.channel, embed=data["embed" + str(i)])
            else:
                result = search.question(command)
                new_embed1 = discord.Embed(title=command, description=result, color=0x00f900)
                # new_embed2 = discord.Embed(title=result["result2"][0], url=result["result2"][1], description=result["result2"][2], color=0x00f900)
                await client.send_message(message.channel, embed=new_embed1)
                # await client.send_message(message.channel, embed=new_embed2)

async def post_embed(data):
    print(data)
    url = "https://www.google.com/search?q=" + data["question_str"].replace(" ", "+")
    choices[0] = data["answers"][0]
    choices[1] = data["answers"][1]
    choices[2] = data["answers"][2]
    description = ""
    for i in range(0,3):
        ans = data["answers"][i]
        description += ans + "\n" 
    new_embed = discord.Embed(title=data["question_str"], url=url, description=description, color=0xff2600)
    new_embed.add_field(name="Question", value=str(data["question_number"]) + " out of " + str(data["question_count"]))
    for server in client.servers:
        if server.id == "456623395858022413":
            for channel in server.channels:
                    if channel.id == "456627296317734922":
                        await client.send_message(channel, embed=new_embed)

async def background_log_loop():
    await client.wait_until_ready()
    file = open("data.log", "r")
    while not client.is_closed:
        await asyncio.sleep(0.05)
        where = file.tell()
        line = file.readline()
        if not line:
            continue
        else:
            if ("question_str" in line and line is not "\n"):
                await post_embed(ast.literal_eval(line.strip("INFO:root"))[0])



# uk channel id = 457304971600199680
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    # await post_embed({"answers": ["Isle of Wight", "Isle of Islay", "Isle of Arran"], "question_str": "Of these three British islands, which is the largest in terms of land area?", "question_number": 8, "question_count": 12})

client.loop.create_task(background_log_loop())
client.run(TOKEN)
