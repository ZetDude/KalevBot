"""This is the main instance that does all the command processing.
Please run this file to run the actual bot itself"""
import asyncio
import errno
import os
import sqlite3 as lite
import sys
import time
from datetime import datetime

import arrow
import discord  # Discord API
from discord.ext import commands
from lib import obot

bot = commands.Bot(command_prefix=commands.when_mentioned_or(*obot.BOT_PREFIX),
                   owner_id=obot.OWNER_ID)
bot.launch_time = datetime.utcnow()

DIR_MAKE = ["important", "important/rpg"]
for i in DIR_MAKE:
    try:
        os.makedirs(i)
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise

NODE_MAKE = ["important/serverdata.db", "important/userdata.db"]
for i in NODE_MAKE:
    if not os.path.exists(i):
        with open(i, 'w'):
            pass

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=obot.BOT_GAME_TYPE,
                                                        name=obot.BOT_GAME_NAME),
                              status=discord.Status.online)
    await bot.user.edit(username=obot.BOT_NAME)
    servers = len(bot.guilds)
    users = len(bot.users)
    print(f"Serving {users} users in " + str(servers) +
          " server" + ("s" if servers > 1 else "") + ".")

    # reminder routine
    con = lite.connect("important/data.db")
    while True:
        with con:
            try:
                current_time = time.strftime('%Y%m%d%H%M%S', time.gmtime())
                cur = con.cursor()
                cur.execute("SELECT * FROM Reminders WHERE ? > remind_time;", (current_time, ))
                rows = cur.fetchall()
                for row in rows:
                    target_user = bot.get_user(row[3])
                    time_arrow = arrow.get(str(row[4])).humanize()
                    embed = discord.Embed(
                        title="KalevBot reminder direct message here!",
                        color=0xff8300
                        )
                    embed.set_author(
                        name=target_user.name,
                        icon_url=target_user.avatar_url
                        )
                    embed.add_field(
                        name="Included message:",
                        value=row[0],
                        inline=False
                        )
                    embed.add_field(
                        name="Original message link:",
                        value=row[1],
                        inline=False
                        )
                    embed.set_footer(
                        text=f"You requested this at {row[4]} UTC ({time_arrow})"
                        )
                    await target_user.send(embed=embed)
                cur.execute("DELETE FROM Reminders WHERE ? > remind_time;", (current_time, ))
            except lite.OperationalError as err:
                if str(err) == "no such table: Reminders":
                    cur.execute(
                        ("CREATE TABLE Reminders(message TEXT NOT NULL, "
                         "link TEXT NOT NULL, remind_time INTEGER NOT NULL, "
                         "requester INTEGER NOT NULL, request_time TEXT NOT NULL);")
                        )
                    print("Created new reminders table")
                else:
                    raise
            except AttributeError:
                print("sliently passing invalid id")
        await asyncio.sleep(10)

@bot.event
async def on_guild_join(server):
    con = lite.connect("important/serverdata.db")
    with con:
        try:
            cur = con.cursor()
            cur.execute("INSERT INTO Server VALUES(?, ?, ?)",
                        (server.id, obot.BOT_PREFIX, None))
        except lite.OperationalError as err:
            if str(err) == "no such table: Server":
                cur.execute(
                    "CREATE TABLE Server(id INTEGER NOT NULL UNIQUE, prefixes TEXT, tags BLOB);")
                cur.execute("INSERT INTO Server VALUES(?, ?, ?)",
                            (server.id, obot.BOT_PREFIX, None))
            else:
                raise


@bot.event
async def on_message(message):
    if message.author != bot.user:
        if bot.user in message.mentions:
            ping_emoji = discord.utils.get(bot.emojis, id=362665760260227073)
            await message.add_reaction(ping_emoji)
    if not message.author.bot:
        await bot.process_commands(message)

if __name__ == '__main__':
    sp = os.path.dirname(os.path.realpath(sys.argv[0]))
    print(sp)
    print(sp + "/kalev_bot.py")
    print("Now running main bot instance")

    print("Launching bot, this might take a few seconds")
    coglist = []
    for root, directories, files in os.walk("cogs"):
        for filename in files:
            filepath = os.path.join(root, filename)
            if filepath.endswith(".py"):
                coglist.append(filepath.split(".py")[0].replace(
                    "/", ".").replace("\\", "."))

    for cog in coglist:
        try:
            bot.load_extension(cog)
            print(f'Loaded {cog} successfully')
        except Exception as err:
            print(f"Failed to load cog: {cog}, ran into {err}")
            raise
    print("Loaded all cogs")

    bot.run(obot.BOT_TOKEN, bot=True, reconnect=True)
