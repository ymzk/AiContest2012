import pygame
from utility import toTuple
from coordinate import Coordinate
from gameObject import GameObject

class Manager:
  registrated = []
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
  @staticmethod
  def register(gameObj):
    if not isinstance(gameObj, GameObject):
      raise TypeError('a GameObject required')
    Manager.registrated.append(gameObj)
  @staticmethod
  def getRegistratedList():
    return Manager.registrated
