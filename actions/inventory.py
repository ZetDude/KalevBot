import importlib.machinery
import math

loader = importlib.machinery.SourceFileLoader('basic', 'C:/Users/Administrator/Desktop/KALEVBOT/basic.py')
handle = loader.load_module('basic')
loader2 = importlib.machinery.SourceFileLoader('maincore', 'C:/Users/Administrator/Desktop/KALEVBOT/maincore.py')
handle2 = loader2.load_module('maincore')

def run(message, rpgPrefix, alias):
    targetID = ""
    target = ""
    combine = None
    print(len(message.mentions))
    if len(message.mentions) == 1:
        mentiont = message.mentions[0]
        target = mentiont
        targetID = mentiont.id
    else:
        cmdlen = len(rpgPrefix + alias)
        opstring = message.content[cmdlen:].strip()
        gotuser = handle2.userget(opstring)
        if gotuser == None:
            combine = "Something failed, defaulting to message sender"
            target = message.author
            targetID = message.author.id
        else:
            target = gotuser
            targetID = gotuser.id
    playerlist = handle.get_playerlist()
    if targetID not in playerlist:
        return "m", [message.channel, message.author.mention + ", that person hasn't joined the game. %join to join the game!"]
    targetEntity = playerlist[targetID]
    returnMSG = targetEntity.inv
    name = "Inventory of " + targetEntity.name + ":\n"
    compileMSG = ""
    for i in range(len(returnMSG)):
        if returnMSG[i] == None or returnMSG[i] == 0:
            y = "Empty"
        else:
            y = returnMSG[i].name
        compileMSG += "Slot " + str(i+1) + ": " + y + "\n"
    return "m", [message.channel, message.author.mention + ", \n```diff\n" + str(compileMSG) + "\n```"]

def help_use():
    return "Get your inventory"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "inventory"

def help_perms():
    return 0

def help_list():
    return "Get your inventory"

def alias():
    return ['inventory', 'inv']