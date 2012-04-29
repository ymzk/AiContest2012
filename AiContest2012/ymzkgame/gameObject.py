from ymzkgame.runnable import Runnable
import ymzkgame.defaults as defaults
from ymzkgame.moveClasses import *
from ymzkgame.manager import Manager
from ymzkgame.image import Image
from ymzkgame.coordinate import Coordinate

class GameObject(Runnable):
  def __init__(self,
               image = defaults.DEFAULT_IMAGE,
               position = defaults.DEFAULT_POSITION,
               direction = defaults.DEFAULT_DIRECTION):
    Runnable.__init__(self)
    self.__image = Image(image)
    self.__position = Coordinate(position)
    self.__direction = direction
    self.__move = NoMove()
    self.__lastDirection = None
  def step(self):
    self.__move, self.__position, self.__direction = self.__move(self.__position, self.__direction)
    if self.__direction != self.__lastDirection:
      self.__lastDirection = self.__direction
      self.__lastImage = self.__image.rotate(-self.__direction)
    Manager.draw(self.__position - self.__lastImage.getSize() / 2, self.__lastImage)
  def getPosition(self):
    return self.__position
  def getDirection(self):
    return self.__direction
  def setPosition(self, position):
    self.__position = position
  def setDirection(self, direction):
    self.__direction = direction
  def setMove(self, move):
    self.__move = move
