import pygame
import os
from math import pi as PI
from . utility import toTuple
from . coordinate import Coordinate
from . import defaults
# from . manager import Manager

class Image:
  __loaded = {}
  def __init__(self, image = defaults.DEFAULT_IMAGE,
                     permeate = defaults.DEFAULT_PERMEATE):
    if isinstance(image, Image):
      self.__image = image.__image
      self.__size = image.__size
      self.__converted = True
    elif isinstance(image, pygame.Surface):
      self.__image = image
      self.__size = Coordinate(self.__image.get_size())
      self.__converted = True
    else:
      self.__image = self.__load(image)
      self.__size = Coordinate(self.__image.get_size())
      self.__converted = False
#      self.__filename = image
    if not self.__converted and permeate:
      self.__image.set_colorkey(self.__image.get_at((0, 0)))
  def __load(self, filename):
    if filename not in self.__loaded:
      self.__loaded[filename] = pygame.image.load(filename)
    return self.__loaded[filename]
#  def _getSurface(self):
#    return self.__image
  def getSize(self):
    return self.__size
  def convert(self):
    if not self.__converted:
      self.__image.convert()
      self.__converted = True
  def rotate(self, angle = 0):
    return Image(pygame.transform.rotate(self.__image, angle * 180 / PI))
  def draw(self, image = defaults.DEFAULT_IMAGE, position = Coordinate(0, 0)):
    image = Image(image.__image)
    position = Coordinate(position)
    self.__image.blit(image.__image, toTuple(position))
  def fill(self, color = (0, 0, 0)):
    self.__image.fill(color)
  def getSubImage(self, leftup, size):
    result = Image(pygame.Surface(toTuple(size)))
    result.draw(self, toTuple(-leftup))
    return result
  def copy(self):
    return Image(self.__image.subsurface(self._getRect()))
