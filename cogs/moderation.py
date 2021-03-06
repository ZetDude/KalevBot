import inspect

from discord.ext import commands


def chunks(main_text, chunk_size):
    """Produce `chunk_size`-character chunks from `main_text`."""
    for start in range(0, len(main_text), chunk_size):
        yield main_text[start:start+chunk_size]

def can_delete_messages(ctx):
    return (ctx.channel.permissions_for(ctx.author).manage_messages or
            ctx.author.id == ctx.bot.owner_id)

class ModerationCog():
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = "Moderation"

    @commands.command(name='delete', aliases=['del', 'd'],
                      brief="Delete messages from the bot")
    @commands.check(can_delete_messages)
    async def delete(self, ctx, delete_amount: int):
        def is_me(message):
            return message.author == self.bot.user
        await ctx.message.channel.purge(limit=delete_amount+1, check=is_me, bulk=False)
        await ctx.send(f"Tried to delete {delete_amount} messages.", delete_after=3.0)

    @commands.command(name='eval', aliases=['evaluate'],
                      help="Run python code. Exclusive to the bot owner.",
                      brief="Run python code")
    @commands.is_owner()
    async def eval(self, ctx, *, code):
        try:
            result = eval(code) # pylint: disable=eval-used
            if inspect.isawaitable(result):
                result = await result
        except Exception as err: # pylint: disable=broad-except
            await ctx.send(type(err).__name__ + ': ' + str(err))
            return
        chunked = chunks(str(result), 1990)
        for i in chunked:
            await ctx.send("```\n{}\n```".format(i))

    @delete.error
    @eval.error
    async def delete_eval_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.name}, {error.args[0]}")
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.name}, you don't have permission to do that.")

def setup(bot):
    bot.add_cog(ModerationCog(bot))
