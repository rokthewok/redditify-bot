#! /usr/bin/python3
import discord
import rbot_commands.command
import rbot_utils


class HotCommand(rbot_commands.command.Command):
  """Command that retrieves the current (non-sticky) hot news from a given
  subreddit.
  """
  def __init__(self):
    rbot_commands.command.Command.__init__(self, help={'name': 'hot',
                                                       'text': 'hot help'})

  def do(self, message, subreddit):
    """Perform the action described by this command - in this case, retrieve
    the hottest post on a given subreddit.
    """
    if not subreddit:
      return None
    try:
      resp = rbot_utils.get_subreddit_json('/hot/.json?count=20', subreddit)
      for post in resp['data']['children']:
        # return the first non-stickied post in the thread (stickied are
        # usually announcements)
        if not post['data']['stickied']:
          return post['data']['url']
    except rbot_utils.URLError as e:
      print('Failed to retrieve hot url for {}.'.format(subreddit))
      raise e
