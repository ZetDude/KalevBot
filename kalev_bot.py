"""This is the main instance that does all the hard work.
Please run this file to run the actual bot itself"""
import errno
# pylint: disable=no-member
import os
import sys
import time

import discord  # Discord API
from discord.ext import commands
from lib import logger, obot

import maincore as dc
<<<<<<< HEAD
#import basic as rpg
from lib import obot
from lib import logger
=======
>>>>>>> f36a8c3e6790ce39d4c12307dfc6edaa9a4bc5ae

bot = commands.Bot(command_prefix=commands.when_mentioned_or(obot.bot_prefix),
                   owner_id = obot.owner_id)

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
print(sp)
print(sp + "/kalev_bot.py")
print("Now running main bot instance")

print("Launching bot, this might take a few seconds")
bStart = time.time()

dirMake = ["actions", "important", "commands", "important/lucky"]
for i in dirMake:
    try:
        os.makedirs(i)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

@bot.event
async def on_ready():
    bEnd = time.time()
    print("Launching of bot took {} seconds".format(bEnd - bStart))
<<<<<<< HEAD
    dc.ready(client)
    #rpg.ready()
    await client.user.edit(username=obot.name)
    s = await client.change_presence(game=discord.Game(type=obot.gametype, name=obot.game),
                                     status=discord.Status.online)
=======
    dc.ready(bot)
    s = await bot.change_presence(activity=discord.Game(type=obot.gametype, name=obot.game),
                                  status=discord.Status.online)
    servers = len(bot.guilds)
    users = len(bot.users)
    print(f"Serving {users} users in " + str(servers) +
          " server" + ("s" if servers > 1 else "") + ".")
>>>>>>> f36a8c3e6790ce39d4c12307dfc6edaa9a4bc5ae
    print(s)

@bot.event
async def on_message(message):
    if message.author != bot.user:
        if bot.user in message.mentions:
            allEmoji = bot.emojis
            pingEmoji = discord.utils.get(allEmoji, id=362665760260227073)
            await message.add_reaction(pingEmoji)

    #if message.guild is None:
        #fse = str(message.channel)
    #else:
        #fse = message.channel.name + " in " + message.guild.name
    #if message.author.bot:
        #return
    await bot.process_commands(message)
    #elif message.content.startswith(obot.game_prefix):
        #async with message.channel.typing():
            #rpg.run(message)
        #print("rpg message detected\n-----------------")

    #await client.send_typing(message.channel)

if __name__ == '__main__':
    coglist = []
    for root, directories, files in os.walk("cogs"):
        for filename in files:
            filepath = os.path.join(root, filename)
            if filepath.endswith(".py"):
                coglist.append(filepath.split(".py")[0].replace("/", "."))

    for cog in coglist:
        try:
            bot.load_extension(cog)
            print(f'Loaded {cog} successfully')
        except Exception as e:
            print(f"Failed to load cog: {cog}, ran into {e}")
    print("Loaded all cogs")
    bot.run(obot.token, bot=True, reconnect=True)
