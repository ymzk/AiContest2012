import pygame
from . utility import toTuple
from . coordinate import Coordinate
from . _keyData import KeyData
from . image import Image

class Manager:
  @staticmethod
  def getTitle():
    return pygame.display.get_caption()
  @staticmethod
  def getScreen():
    if not hasattr(Manager, '_screen'):
      Manager._screen = Image(pygame.display.get_surface())
    return Manager._screen
  @staticmethod
  def getScreenSize():
    return Coordinate(*Manager.getScreen().getSize())
  '''
  @staticmethod
  def getRegistratedList():
    return Manager.registrated
  '''
  @staticmethod
  def getKeyStatus(keyId):
    return KeyData.getKeyStatus(keyId)

for m in dir(pygame):
  if m[:2] == 'K_':
    setattr(Manager, m, getattr(pygame, m))
