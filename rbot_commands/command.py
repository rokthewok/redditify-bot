#! /usr/bin/python3
import discord
import abc


class Command(object):
  """An abstrace base class representing a Discord bot command

  Requires the method `do (self, message, subreddit)` to be implemented
  by all inheriting classes. Also requires `help` data to be passed
  to Command at creation time.
  """
  __metaclass__ = abc.ABCMeta
  def __init__(self, **kwargs):
    self._help = kwargs['help']

  @property
  def help(self):
    """Retrieve the help data property of this command."""
    return self._help

  @abc.abstractmethod
  def do(self, message, subreddit):
    """Abstract method, to be implemented by child classes."""
    pass
