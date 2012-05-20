# coding: cp932
from ymzkgame.gameObject import GameObject
from ymzkgame.coordinate import Coordinate
from ymzkgame.manager import Manager
from draw import draw
from gameConfig import *

class Base(GameObject):
  def __init__(self, teamFlag, position = Coordinate(0,0), direction = 0):
    super().__init__(position = position,direction = direction, image = "graphics/base.bmp")
    self._teamFlag = teamFlag
    self._damagedFlag = False
    self._counter = 0
    self._hp = BASE_DEFAULT_HP
  def getHp(self):
    return self._hp
  def getTeamFlag(self):
    return self._teamFlag
  def damage(self, damage):
    self._damagedFlag = True
    #�_���[�W���󂯂����ǂ����̃t���O
    self._hp -= damage
  def checkDamaged(self):
    return self._damagedFlag
  def step(self):
    if self._counter > 0:
      self._counter -= 1
    elif self._hp < BASE_DEFAULT_HP:
      self._counter = BASE_DEFAULT_RECOVER_INTERVAL
      self._hp += 1
    self._damagedFlag = False
  def checkAlive(self):
    return self._hp > 0
  def encode(self):
    yield self._hp
    #yield str(self._unitId)
    yield str(self._teamFlag)
    yield str(self.getPosition().getX())
    yield str(self.getPosition().getY())
    #yield str(self.getDirection())
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
