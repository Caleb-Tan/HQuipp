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
    new_embed = discord.Embed(title=choice, description=result["result"], color=0x00f900)
    new_embed.set_footer(text="Search Time: " + str(result["time"]))
    data["embed" + str (choiceNo)] = new_embed


@client.event
async def on_message(message):
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
                print(message.channel.id)
                result = search.question(command)
                new_embed = discord.Embed(title=command, description=result["result"], color=0x00f900)
                new_embed.set_footer(text="Search Time: " + str(result["time"]))
                await client.send_message(message.channel, embed=new_embed)
        if message.content.startswith(".math "):
            command = message.content.strip(".math").lstrip().rstrip().replace("^", "**")
            try:
                math = round(eval(command),4)
                await client.send_message(message.channel, "`" + str(math) + "`")
            except (SyntaxError, NameError, TypeError):
                await client.send_message(message.channel, "`Um something went wrong there, please try again.`")
            except (ZeroDivisionError):
                await client.send_message(message.channel, "`DIVISION BY ZERO IS NOT ALLOWED BRO`")


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
    await client.send_message(client.get_channel("468613455872524288"), embed=new_embed)


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
            if ("question_str" in line and line != "\n"):
                print(line)
                await post_embed(ast.literal_eval(line.strip("INFO:root"))[0])



# uk channel id = 457304971600199680
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(background_log_loop())
client.run(TOKEN)
