#! /usr/bin/python3
import requests
import os


user_agent = os.environ.get('REDDIT_USER_AGENT')


class URLError(Exception):
  """Represents a generic URL exception (non-200 code)"""
  pass


def get_subreddit_json(endpoint, subreddit):
  """Retrieves the json data for a given reddit API endpoint

  positional arguments:
  endpoint -- the API endpoint
  subreddit -- the target subreddit, of the form r/<subreddit name>

  Raises URLError on non-200 response code.
  """
  url = 'https://www.reddit.com/{}'.format(subreddit)
  resp = requests.get(url + endpoint, headers={'User-Agent': user_agent})
  if resp.status_code == 200:
    print('got response: {}'.format(resp))
    return resp.json()
  else:
    print('failed to retrieve top link for {}. status code: {}'
                  .format(url, resp.status_code))
    raise URLError()
