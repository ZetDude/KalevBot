import pickle
import pprint
import discord
from discord.ext import commands
from lib import obot
pp = pprint.PrettyPrinter(indent=2)

bot = commands.Bot(command_prefix='k!relay ')

RELAYFILE = 'important/relay.pickle'
CREATE_MESSAGE = ("**Created relay data for the server `{ctx.guild.name}`**\n"
                  "Set the relay channel to be `#{ctx.channel.name}` for now. If this is "
                  "incorrect, a moderator should modify this with `{ctx.prefix}channel`.\n"
                  "A special role given to players when they join can also be added, by "
                  "using `{ctx.prefix}role`.\nIf everyone is ready to go, a moderator can "
                  "start the game with `{ctx.prefix}begin`. Good luck!")
JOIN_MESSAGE = ("Currently, all your info such as the name of your conlang and "
                "the order you are in are not set. To configure this, use "
                "`{ctx.prefix}edit` to begin the configuration wizard.")

DEFAULT_SERVER = {"state": 0,
                  "part": {},
                  "channel": {},
                  "role": None,
                  "turn": None}

DEFAULT_PLAYER = {'lang': None,
                  'order': None}

try:
    with open(RELAYFILE, "rb") as opened_file:
        server_data = pickle.load(opened_file)
except FileNotFoundError:
    server_data = {}
    with open(RELAYFILE, 'wb') as opened_file:
        pickle.dump(server_data, opened_file, protocol=pickle.HIGHEST_PROTOCOL)

async def write_data(to_write):
    with open(RELAYFILE, 'wb') as f:
        pickle.dump(to_write, f, protocol=pickle.HIGHEST_PROTOCOL)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(name='register', aliases=['join', 'participate'])
async def register(ctx):
    active_game = server_data.get(ctx.guild.id, None)
    if active_game is None:
        await ctx.message.add_reaction("\u2705")
        await ctx.send(CREATE_MESSAGE.format(ctx=ctx))
        await ctx.author.send(JOIN_MESSAGE.format(ctx=ctx))
        new_entry = dict(DEFAULT_SERVER)
        new_entry["channel"] = ctx.channel.id

        new_player = dict(DEFAULT_PLAYER)
        new_entry["part"][ctx.author.id] = new_player

        server_data[ctx.guild.id] = new_entry
        await write_data(server_data)
    elif ctx.author.id in active_game["part"]:
        await ctx.message.add_reaction("\u274C")
        await ctx.send("You are already in this relay!")
    elif active_game["state"] == 0:
        await ctx.message.add_reaction("\u2705")
        await ctx.author.send(JOIN_MESSAGE.format(ctx=ctx))
        new_player = dict(DEFAULT_PLAYER)
        server_data[ctx.guild.id]["part"][ctx.author.id] = new_player
        if active_game["role"] is not None:
            add_role = discord.utils.get(ctx.guild.roles, name=active_game["role"])
            await ctx.author.add_roles(add_role)
        await write_data(server_data)
    else:
        await ctx.message.add_reaction("\u274C")
        await ctx.send("A game is already taking place, so you cannot join!")

@bot.command(name='role', aliases=[])
async def role(ctx, *, role_name):
    if not ctx.author.guild_permissions.manage_roles:
        await ctx.send(f"{ctx.author.name}, you don't have permission to do that.")
    elif not ctx.guild.me.guild_permissions.manage_roles:
        await ctx.send(f"{ctx.author.name}, please give me permission to assign roles before doing that.")
    elif discord.utils.get(ctx.guild.roles, name=role_name) is None:
        await ctx.send(f"{ctx.author.name}, couldn't find a role named that.")
    elif server_data.get(ctx.guild.id, None) is None:
        await ctx.send(f"{ctx.author.name}, no relay made for this server ({ctx.prefix}register).")
    players = list(server_data[ctx.guild.id]["part"])
    players = [x for x in ctx.guild.members if x.id in players]
    server_data[ctx.guild.id]["role"] = role_name
    add_role = discord.utils.get(ctx.guild.roles, name=role_name)
    for player in players:
        await ctx.send(f"going back to add {add_role} to {player}")
        await player.add_roles(add_role)
    await write_data(server_data)

@bot.command(name='data', aliases=[])
async def data(ctx):
    formatted = pp.pformat(server_data)
    await ctx.send(f"```\n{formatted}\n```")

bot.run(obot.token)

