import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
import maincore as core

def run(message, prefix, aliasName):
    core.send(message.channel, core.clink(message, aliasName, "<https://www.google.com/search?q=", ">", "+"))


def help_use():
    return "Return the link for the google search page for the specified text"

def help_param():
    return "<TEXT*>: A string of character to search for in google"

def help_cmd(prefix):
    return prefix + "google <TEXT*>"

def help_perms():
    return 0

def help_list():
    return "Google the specified subject"

def aliasName():
    return ['google', 'g']
