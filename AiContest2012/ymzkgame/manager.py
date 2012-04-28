import pygame
from ymzkgame.utility import toTuple
from ymzkgame.coordinate import Coordinate
from ymzkgame._keyData import KeyData

class Manager:
  @staticmethod
  def getTitle():
    return pygame.display.get_caption()
  @staticmethod
  def getScreen():
    return pygame.display.get_surface()
  @staticmethod
  def getScreenSize():
    return Coordinate(*Manager.getScreen().get_size())
  @staticmethod
  def draw(position, image):
    image.convert()
    Manager.getScreen().blit(image.getSurface(), toTuple(position))
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
