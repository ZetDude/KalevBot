import importlib.machinery
import os
import sys
import pickle

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

def chunks(s, n):
    """Produce `n`-character chunks from `s`."""
    for start in range(0, len(s), n):
        yield s[start:start+n]

def run(message, prefix, aliasName):
    cmdlen = len(prefix + aliasName)
    opstring = message.content[cmdlen:].strip()
    try:
        fileName = sp + opstring
        with open(fileName, "rb") as f:
            lines = pickle.loads(f.read())
    except:
        fileName = sp + opstring
        with open(fileName, "r") as f:
            lines = [line.rstrip('\n') for line in f]
    rSplit = []
    lines = str(lines)
    print(lines)
    for chunk in chunks(lines, 1990):
        rSplit.append(message.channel)
        rSplit.append("```\n" + chunk + "\n```")
    print(rSplit)
    return "a", rSplit

def help_use():
    return "Read a file's contents"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "file"

def help_perms():
    return 10

def help_list():
    return "Read a file's contents"

def aliasName():
    return ['file', 'read', 'readfile']
