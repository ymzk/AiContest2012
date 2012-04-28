import pygame
import os
from ymzkgame.manager import Manager
from ymzkgame.coordinate import Coordinate

class Image:
  __loaded = {}
  def __init__(self, image = 'ymzkgame/default.bmp', permeate = True):
    if isinstance(image, Image):
      self.__image = image.__image
      self.__converted = True
    elif isinstance(image, pygame.Surface):
      self.__image = image
      self.__converted = True
    else:
      self.__image = self.__load(image)
      self.__converted = False
      self.__filename = image
    if permeate:
      self.__image.set_colorkey(self.__image.get_at((0, 0)))
  def __load(self, filename):
    if filename not in self.__loaded:
      self.__loaded[filename] = pygame.image.load(filename)
    return self.__loaded[filename]
  def getSurface(self):
    return self.__image
  def getSize(self):
    return Coordinate(*self.__image.get_size())
  def convert(self):
    if not self.__converted:
      self.__image.convert()
      self.__converted = True
