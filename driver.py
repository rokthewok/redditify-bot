import discord
import asyncio
import re
import requests
import time
import os
import rbot_commands.hot
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

def show_help(message):
  """Print help message in chat

  positional arguments:
  message -- the discord.py Message object provided by the on_message event.
  """
  commands = [
    {
        'name': 'help',
        'text': 'show this help message.'
    },
    {   'name': 'top',
        'text': 'retrieve today\'s top scoring post for the given subreddits'
    },
    {   'name': 'hot',
        'text': 'retrieve the current trending post for the given subreddits'
    }
  ]

  command_text = '\n'.join(['  -{0[name]:<12}{0[text]}'.format(cmd)
                                for cmd in commands])
  help_message = '**redditfy-bot** available commands:\n{}'.format(command_text)
  print(help_message)
  return help_message


def get_top_link(subreddit):
  """Retrieve URLs for top reddit posts for the given subreddit URLs

  positional arguments:
  subreddit -- a subreddit name of the form "r/<subreddit>"
  """
  if not subreddit:
    return None
  try:
    resp = rbot_utils.get_subreddit_json('/top/.json?count=1?t=day', subreddit)
    if resp['data']['children']:
      return resp['data']['children'][0]['data']['url']
    else:
      return None
  except URLError as e:
    print('failed to retrieve top url for {}.'.format(url))
    return None


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
  pattern = re.compile(r'\br/([A-Z]|[a-z]|[0-9])+([A-Z]|[a-z]|[0-9]|_)*')
  match = pattern.search(text)
  subreddit = ''
  if match is None:
    print('No subreddit pattern provided in message text: {}.'.format(text))
  else:
    subreddit = match.group(0)

  hot_command = rbot_commands.hot.HotCommand()
  outgoing_message = None
  if text.startswith('!rbot'):
    words = text.split(' ')
    if len(words) == 1 or words[1] == 'help':
      outgoing_message = show_help(message)
    elif words[1] == 'top':
      outgoing_message = get_top_link(subreddit)
    elif words[1] == 'hot':
      outgoing_message = hot_command.do(message, subreddit)
    else:
      show_help(message)

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
