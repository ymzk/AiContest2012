from ymzkgame.gameObject import GameObject
from ymzkgame.coordinate import Coordinate
class Base(GameObject):
  def __init__(self, teamFlag, position = Coordinate(0,0), direction = Coordinate(0,0)):
    super().__init__(position = position,direction = direction, image = "base.bmp")
    self._teamFlag = teamFlag
    self._hp = 1000
  def getHp(self):
    return self._hp
  def getTeamFlag(self):
    return self._teamFlag
  def damage(self, damage):
    self._hp -= damage
  def checkAlive(self):
    return self._hp > 0
  
