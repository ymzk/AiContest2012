import pygame
from ymzkgame.utility import toTuple
from ymzkgame.coordinate import Coordinate

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
  @staticmethod
  def getRegistratedList():
    return Manager.registrated
