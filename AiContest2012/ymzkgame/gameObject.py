from runnable import Runnable
import defaults
from moveClasses import *
from manager import Manager

class GameObject(Runnable):
  def __init__(self,
               image = defaults.DEFAULT_IMAGE,
               position = defaults.DEFAULT_POSITION,
               direction = defaults.DEFAULT_DIRECTION):
    self.__image = image
    self.__position = position
    self.__direction = direction
    self.__move = NoMove()
  def step(self):
    self.__move, self.__position, self.__direction = self.__move(self.__position, self.__direction)
    Manager.draw(self.__position - self.__image.getSize() / 2, self.__image)
  def getPosition(self):
    return self.__position
  def getDirection(self):
    return self.__direction
  def setMove(self, move):
    self.__move = move
