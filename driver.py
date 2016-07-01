import discord
import asyncio
import re
import requests
import json
import time
import os

client = discord.Client()

class URLError(Exception):
  pass

@client.event
async def on_ready():
  '''Listen for on ready event from discord client'''
  print('Logged in as')
  print(client.user.name)
  print(client.user.id)
  print('------')

async def show_help(message):
  '''Print help message in chat

  positional arguments:
  message -- the discord.py Message object provided by the on_message event.
  '''
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
  await client.send_message(message.channel, help_message)

def get_subreddit_post_url(endpoint, url):
  resp = requests.get(url + endpoint)
  if resp.status_code == 200:
    print('got response: {}'.format(resp))
    new_url = resp.json()['data']['children'][0]['data']['url']
    return new_url
  else:
    print('failed to retrieve top link for {}. status code: {}'
                  .format(url, resp.status_code))
    raise URLError()


def get_hot_links(urllist):
  '''Retrieve URLs for hot reddit posts for the given subreddit URLs

  positional arguments:
  urllist -- a list of subreddit URLs, of the form
             "http://www.reddit.com/r/<subreddit>"
  '''
  new_urls = []
  for url in urllist:
    try:
      new_urls.append(get_subreddit_post_url('/hot/.json?count=1', url))
    except URLError as e:
      print('Failed to retrieve hot url for {}.'.format(url))
  return new_urls

def get_top_links(urllist):
  '''Retrieve URLs for top reddit posts for the given subreddit URLs

  positional arguments:
  urllist -- a list of subreddit URLs, of the form
             "http://www.reddit.com/r/<subreddit>"
  '''
  new_urls = []
  for url in urllist:
    try:
      new_urls.append(get_subreddit_post_url('/top/.json?count=1?t=day', url))
    except URLError as e:
      print('failed to retrieve top url for {}.'.format(url))
  return new_urls

@client.event
async def on_message(message):
  '''Handle message events from Discord.

  Presently, handles two separate functionalities; one manages !rbot commands
  and the other simply parses appropriate string productions into subreddit
  links. DEV NOTE: Eventually this functionality needs to be refactored into
  a more properly separated set of handlers.

  positional arguments:
  message -- the discord.py Message object provided on event bus activity
  '''
  if message.author.name == client.user.name:
    return
  text = message.content
  pattern = re.compile(r'\br/([A-Z]|[a-z]|[0-9])+([A-Z]|[a-z]|[0-9]|_)*')
  urllist = ['https://www.reddit.com/{}'.format(sub.group(0))
                    for sub in pattern.finditer(text)]
  if text.startswith('!rbot'):
    words = text.split(' ')
    if len(words) == 1 or words[1] == 'help':
      await show_help(message)
    elif words[1] == 'top':
      urllist = get_top_links(urllist)
    elif words[1] == 'hot':
      urllist = get_hot_links(urllist)
    else:
      show_help(message)

  for url in urllist:
    print(url)
    await client.send_message(message.channel, url)

if __name__ == '__main__':
  token = os.environ.get('DISCORD_TOKEN')

  if token is not None:
    client.run(token)
  else:
    print('ERROR: unable to retrieve discord token.')
