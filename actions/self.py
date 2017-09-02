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
    print(targetID)
    
    print(target)
    print(target.name)
    playerlist = handle.get_playerlist()
    if targetID not in playerlist:
        return "m", [message.channel, message.author.mention + ", that person hasn't joined the game. %join to join the game!"]
    targetEntity = playerlist[targetID]
    targetStats = targetEntity.stats
    targetrStats = targetEntity.rawstats
    targetiStats = targetEntity.invstats
    targetName = targetEntity.name
    targetID = targetEntity.id
    targetInv = targetEntity.inv
    targetInvList = []
    for i in targetInv:
        if i == None:
            targetInvList.append(None)
            continue
        targetInvList.append(i.name)
    compileMSG = str("Entity: " + str(targetEntity) +
                     "\nStats: " + str(targetStats) +
                     "\nRaw stats: " + str(targetrStats) +
                     "\nEquip stats: " + str(targetiStats) +
                     "\nName: " + str(targetName) +
                     "\nID: " + str(targetID) +
                     "\nInventory: " + str(targetInv) +
                     "\nInventory Items: " + str(targetInvList)
    )
    return "m", [message.channel, message.author.mention + ", \n```\n" + str(compileMSG) + "\n```"]

def help_use():
    return "Fetch someone's Entity class and everything related to it"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "self"

def help_perms():
    return 2

def help_list():
    return "Fetch someone's Entity class"

def alias():
    return ['self']