import discord
import asyncio
import re
import requests
import time
import os
import rbot_commands
import rbot_utils


client = discord.Client()

class URLError(Exception):
  pass

@client.event
async def on_ready():
  """Listen for on ready event from discord client"""
  print('Logged in as')
  print(client.user.name)
  print(client.user.id)
  print('------')

def show_help(message, commands):
  """Print help message in chat

  positional arguments:
  message -- the discord.py Message object provided by the on_message event.
  """
  commands_help = [
    {
        'name': 'help',
        'text': 'show this help message.'
    },
  ]

  commands_help.extend((c.help for key, c in commands.items()))
  command_text = '\n'.join(['   {0[name]:<12}{0[text]}'.format(cmd)
                                for cmd in commands_help])
  help_message = '**redditfy-bot** available commands:\n{}'.format(command_text)
  print(help_message)
  return help_message


@client.event
async def on_message(message):
  """Handle message events from Discord.

  Presently, handles two separate functionalities; one manages !rbot commands
  and the other simply parses appropriate string productions into subreddit
  links. DEV NOTE: Eventually this functionality needs to be refactored into
  a more properly separated set of handlers.

  positional arguments:
  message -- the discord.py Message object provided on event bus activity
  """
  if message.author.name == client.user.name:
    return
  text = message.content
  pattern = re.compile(r'(?<!/)\br/([A-Z]|[a-z]|[0-9])+([A-Z]|[a-z]|[0-9]|_)*')
  match = pattern.search(text)
  subreddit = ''
  if match is None:
    print('No subreddit pattern provided in message text: {}.'.format(text))
  else:
    subreddit = match.group(0)

  outgoing_message = None
  if text.startswith('!rbot'):
    words = text.split(' ')
    if len(words) < 2 or not rbot_commands.Commands.commands.get(words[1]):
      outgoing_message = show_help(message, rbot_commands.Commands.commands)
    else:
      outgoing_message = rbot_commands.Commands.commands[words[1]].do(message, subreddit)
  elif subreddit:
    outgoing_message = 'https://www.reddit.com/{}'.format(subreddit)
  else:
    print('nothing to do for message: {}'.format(text))

  if outgoing_message:
    print('outgoing message: {}'.format(outgoing_message))
    await client.send_message(message.channel, outgoing_message)
  else:
    print('Invalid message result.')

if __name__ == '__main__':
  token = os.environ.get('DISCORD_TOKEN')

  if token is not None:
    client.run(token)
  else:
    print('ERROR: unable to retrieve discord token.')
