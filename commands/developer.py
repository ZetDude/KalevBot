import maincore as core

help_info = {"use": "Try it!",
             "param": "{}dev",
             "perms": None,
             "list": "Display the best developer of 2017"}
alias_list = ['dev', 'developer']

def run(message, prefix, alias_name):
    del prefix
    del alias_name
    core.send(message.channel,
              "ZetDude best developer of 2017 and 2018 <:zetdev:357193244679077890>")