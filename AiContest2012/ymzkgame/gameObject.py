from . runnable import Runnable
from . import defaults
from . moveClasses import *
from . manager import Manager
from . image import Image
from . coordinate import Coordinate

class GameObject(Runnable):
  def __init__(self,
               image = defaults.DEFAULT_IMAGE,
               position = defaults.DEFAULT_POSITION,
               direction = defaults.DEFAULT_DIRECTION,
               move = defaults.DEFAULT_MOVE):
    Runnable.__init__(self)
    self.__image = Image(image)
    self.__position = Coordinate(position)
    self.__direction = direction
    self.__move = move
    self.__lastDirection = None
  def step(self):
    self.__move, self.__position, self.__direction = self.__move(self.__position, self.__direction)
  def draw(self, screen):
    if self.__direction != self.__lastDirection:
      self.__lastDirection = self.__direction
      self.__lastImage = self.__image.rotate(-self.__direction)
    screen.draw(self.__lastImage, self.__position - self.__lastImage.getSize() / 2)
  def getPosition(self):
    return self.__position
  def getDirection(self):
    return self.__direction
  def getImage(self):
    return self.__image
  def setPosition(self, position):
    self.__position = position
  def setDirection(self, direction):
    self.__direction = direction
  def setMove(self, move):
    self.__move = move
