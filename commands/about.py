import importlib.machinery

loader = importlib.machinery.SourceFileLoader('maincore', 'C:/Users/Administrator/Desktop/KALEVBOT/maincore.py')
handle = loader.load_module('maincore')
loader2 = importlib.machinery.SourceFileLoader('basic', 'C:/Users/Administrator/Desktop/KALEVBOT/basic.py')
handle2 = loader2.load_module('basic')

def run(message, prefix, alias):
    nPrefix = handle.prefix
    rpgPrefix = handle2.rpgPrefix
    aboutText = """```
Hi! I am KalevBot, a bot designed specifically for this server!
I was designed by ZetDude, and I consist of 100% spaghetti.
I am here to help with the relay managment and some other minor things.
I also have a little text RPG-battle-explore-dungeon-rogue-like thing, whatever that is.
To learn about that, use <{0}about> instead.
But what are my command, you might wonder?
Just type <{1}help> to see!

I am made in python using the discord.py API wrapper.
```""".format(nPrefix, rpgPrefix)
    return "m", [message.channel, aboutText]

def help_use():
    return "Learn more about the bot"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "about"

def help_perms():
    return 0

def help_list():
    return "Learn more about the bot"

def alias():
    return ['about', 'info']