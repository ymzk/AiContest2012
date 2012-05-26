import pygame
import os
from math import pi as PI
from . utility import toTuple
from . coordinate import Coordinate
from . import defaults
# from . manager import Manager

class Image:
  __loadeds = {}
  def __init__(self, image = defaults.DEFAULT_IMAGE,
                     permeate = defaults.DEFAULT_PERMEATE):
    if isinstance(image, Image):
      self.__image = image.__image
      self.__size = image.__size
      self.__converted = image.__converted
    elif isinstance(image, pygame.Surface):
      self.__image = image
      self.__size = Coordinate(self.__image.get_size())
      self.__converted = [True]
    elif isinstance(image, Coordinate) or isinstance(image, tuple):
      self.__image = pygame.Surface(toTuple(image))
      self.__size = Coordinate(image)
      self.__converted = [False]
    else:
      if self.__loaded(image):
        image = self.__loadeds[image]
        self.__image = image.__image
        self.__size = image.__size
        self.__converted = image.__converted
      else:
        self.__image = self.__load(image)
        self.__size = Coordinate(self.__image.get_size())
        self.__converted = [False]
        if permeate:
          self.__image.set_colorkey(self.__image.get_at((0, 0)))
#          self.__filename = image
  def __loaded(self, filename):
    return filename in self.__loadeds
  def __load(self, filename):
    self.__loadeds[filename] = self
#    print(filename, self.__loadeds[filename].get_size())
    return pygame.image.load(filename)
#  def _getSurface(self):
#    return self.__image
  def getSize(self):
    return self.__size
  def convert(self):
    if not self.__converted[0]:
      self.__image.convert()
      self.__converted[0] = True
  def rotate(self, angle = 0):
    return Image(pygame.transform.rotate(self.__image, angle * 180 / PI).convert())
  def draw(self, image = defaults.DEFAULT_IMAGE, position = Coordinate(0, 0)):
    image = Image(image.__image)
    position = Coordinate(position)
    self.__image.blit(image.__image, toTuple(position))
  def fill(self, color = (0, 0, 0)):
    self.__image.fill(color)
  def getSubImage(self, leftup, size):
    return Image(self.__image.subsurface(pygame.Rect(toTuple(leftup), toTuple(size))))
  def copy(self):
    result = Image(self.getSize())
    result.draw(self)
    return result
  def getSurface(self):
    return self.__image
