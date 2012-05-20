from math import *
from ymzkgame.gameObject import GameObject
from ymzkgame.coordinate import Coordinate
from ymzkgame.manager import Manager
from draw import draw
class Bullet(GameObject):
  def __init__(self,unit):
    super().__init__(image = r"graphic/bullet.bmp",position = unit.getPosition(), direction = unit.getDirection())
    self._master = unit
    self._vector = 20 * Coordinate(cos(unit.getDirection()),sin(unit.getDirection()))
    self._attackPower = unit.getAttackPower()
    self._counter = 30
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
    if self._counter < 0:
      self.end()
    self._counter -= 1
    super().step()
    
  def encode(self):
    yield str(self.getTeamFlag())
    yield str(self.getPosition().getX())
    yield str(self.getPosition().getY())
    yield str(self.getDirection())
    yield str(self._vector.getX())
    yield str(self._vector.getY())
  
  def draw(self, screen, viewPoint):
    draw(screen, self.getImage(), self.getPosition(), self.getDirection(),
                                  viewPoint.getPosition(), viewPoint.getDirection())
    '''
    image = self.getImage().rotate(viewPoint.getDirection() - self.getDirection())
    screen.draw(image = image,
                position = (self.getPosition() -
                            viewPoint.getPosition()
                            ).rotate(-viewPoint.getDirection()) -
                            image.getSize() / 2 +
                            Manager.getScreenSize() / 2)
    '''
