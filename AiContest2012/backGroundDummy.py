import pygame
from ymzkgame.runnable import Runnable
from ymzkgame.runner import run
from ymzkgame.gameObject import GameObject
from ymzkgame.moveClasses import *
from ymzkgame.coordinate import Coordinate

class BackGroundDummy(Runnable):
  def step(self):
    pygame.display.get_surface().fill((128, 128, 128))

class GameManagerDummy(Runnable):
  def __init__(self):
    super().__init__()
    self.__backGround = BackGroundDummy()
    self.__objs = [GameObject(), GameObject(), GameObject()]
    for i in range(len(self.__objs)):
      self.__objs[i].setMove(MoveTo(Coordinate(800, 300 * i), term = 180))
  def step(self):
    self.__backGround.step()
    for obj in self.__objs:
      obj.step()
    
if __name__ == '__main__':
  run(GameManagerDummy())
