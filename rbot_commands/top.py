#! /usr/bin/python3
import discord
import rbot_commands.command
import rbot_utils


class TopCommand(rbot_commands.command.Command):
  """Command that retrieves the current top post of the day from a given
  subreddit.
  """
  NAME = 'top'
  def __init__(self):
    rbot_commands.command.Command.__init__(self,
        help= {
                'name': TopCommand.NAME,
                'text': 'retrieve today\'s top scoring ' + \
                        'post for the given subreddits'
              })

  def do(self, message, subreddit):
    """Perform the action described by this command - in this case, retrieve
    the last 24 hour's top post on a given subreddit.
    """
    if not subreddit:
      return None
    try:
      resp = rbot_utils.get_subreddit_json('/top/.json?count=1?t=day',
                                           subreddit)
      if resp['data']['children']:
        return resp['data']['children'][0]['data']['url']
    except rbot_utils.URLError as e:
      print('Failed to retrieve top url for {}.'.format(subreddit))
      raise e
