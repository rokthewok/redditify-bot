#! /usr/bin/python3
import rbot_commands.hot
import rbot_commands.top


class Commands(object):
  commands = {
                rbot_commands.hot.HotCommand.NAME: rbot_commands.hot.HotCommand(),
                rbot_commands.top.TopCommand.NAME: rbot_commands.top.TopCommand()
             }
  def __init__(self):
    pass
