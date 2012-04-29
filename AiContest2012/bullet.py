from math import *
from ymzkgame.gameObject import GameObject
from ymzkgame.coordinate import Coordinate
class Bullet(GameObject):
  def __init__(self,unit):
    super().__init__(image = "bullet.bmp",position = unit.getPosition(), direction = unit.getDirection())
    self._masterId = unit
    self._vector = 20 * Coordinate(cos(unit.getDirection()),sin(unit.getDirection()))
    self._attackPower = unit.getAttackPower()
    self._deadFlag = False
  def getAttackPower(self):
    return self._attackPower
  def getTeamFlag(self):
    return self._masterId.getTeamFlag()
  def end(self):
    super().end()
  def step(self):
    self.setPosition(self.getPosition() + self._vector)
    super().step()
  
