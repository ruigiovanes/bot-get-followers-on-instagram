import os

from configparser import ConfigParser

config = ConfigParser()
config.read(os.path.dirname(os.path.dirname(__file__)) + '/config.ini', encoding='utf8')

class ConfigExtension:  
  @staticmethod
  def get(tag):
    return config[tag]