import os
import pickle
import sys

from discord.ext import commands
from lib import entity, item

PLAYERDATA = "important/playerdata.pickle"
class GameCog():
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = "RPG"

    @commands.command(name='join', aliases=['enter', 'play'],
                      help="Join the RPG!",
                      brief="Creates a player for you so you could participate in the RPG")
    async def join(self, ctx):
        try:
            with open(PLAYERDATA, "rb") as opened_file:
                players = pickle.load(opened_file)
        except FileNotFoundError:
            players = {}
            await ctx.send(f"created new datafile {PLAYERDATA}")
            with open(PLAYERDATA, 'w'): pass
        except pickle.UnpicklingError:
            await ctx.send(f"file {PLAYERDATA} is corrupt, cannot fetch data.")
            return
        except Exception as e:
            await ctx.send(str(e))
        if players.get(ctx.author.id, False):
            await ctx.send(f"{ctx.author.name}, you have already joined!")
            return
        author_data = { 
            "name": ctx.author.name,
            "id": ctx.author.id,
            "invsize": 10,
        }
        new_player = entity.Entity(author_data)
        players[ctx.author.id] = new_player
        with open(PLAYERDATA, 'wb') as opened_file:
            pickle.dump(players, opened_file)
        welcome_message = ("```diff\n"
                           f"+ Welcome to the game, {ctx.author.name}!\n"
                           f"For now, your stats are 0. I advise you upgrade them right away.\n"
                           f"Use {ctx.prefix}upgrade <stat> <amount> for that. "
                           f"I have given you 20 stat points\n"
                           f"The stats are: 'Health', 'Attack', 'Defense', 'Speed' and 'Luck'\n"
                           f"! Learn more using {ctx.prefix}about.\n"
                           f"- Good luck!\n"
                           "```")
        await ctx.send(welcome_message)

    @commands.command(name='debugadd', aliases=[],
                      help="Join the RPG!",
                      brief="Creates a player for you so you could participate in the RPG")
    async def debugadd(self, ctx, to_add):
        try:
            with open(PLAYERDATA, "rb") as opened_file:
                players = pickle.load(opened_file)
        except (pickle.UnpicklingError, FileNotFoundError):
            await ctx.send(f"file {PLAYERDATA} is corrupt, cannot fetch data.")
            return
        target_player = players.get(ctx.author.id)
        if target_player is None:
            await ctx.send(f"No such player.")
            return
        try:
            target_player.inv.add(to_add)
        except IndexError as e:
            await ctx.send(f"IndexError {e.args[0]}")
        except entity.ActionSuccesful as e:
            await ctx.send(f"entity.ActionSuccesful {e.args[0]}")
        with open(PLAYERDATA, 'wb') as opened_file:
            pickle.dump(players, opened_file)

def setup(bot):
    bot.add_cog(GameCog(bot))