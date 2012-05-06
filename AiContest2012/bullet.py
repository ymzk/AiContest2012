from math import *
from ymzkgame.gameObject import GameObject
from ymzkgame.coordinate import Coordinate
class Bullet(GameObject):
  def __init__(self,unit):
    super().__init__(image = "bullet.bmp",position = unit.getPosition(), direction = unit.getDirection())
    self._master = unit
    self._vector = 20 * Coordinate(cos(unit.getDirection()),sin(unit.getDirection()))
    self._attackPower = unit.getAttackPower()
  def getAttackPower(self):
    return self._attackPower
  def getTeamFlag(self):
    return self._master.getTeamFlag()
  def end(self):
    self._attackPower = 0
    super().end()
  def attack(self, unit):
    if self._master == unit:
      return
    if self.getTeamFlag() != unit.getTeamFlag():
      unit.damage(self._attackPower)
    self.end()

  def step(self):
    self.setPosition(self.getPosition() + self._vector)
    super().step()
  
