from ymzkgame.gameObject import GameObject
from ymzkgame.coordinate import Coordinate
from ymzkgame.manager import Manager
class Base(GameObject):
  def __init__(self, teamFlag, position = Coordinate(0,0), direction = 0):
    super().__init__(position = position,direction = direction, image = "base.bmp")
    self._teamFlag = teamFlag
    self._damagedFlag = False
    self._hp = 1000
  def getHp(self):
    return self._hp
  def getTeamFlag(self):
    return self._teamFlag
  def damage(self, damage):
    self._damagedFlag = True
    #ダメージを受けたかどうかのフラグ
    self._hp -= damage
  def checkDamaged(self):
    return self._damagedFlag
  def step(self):
    self._damagedFlag = False
  def checkAlive(self):
    return self._hp > 0
  def encode(self):
    yield self._hp
    #yield str(self._unitId)
    yield str(self._teamFlag)
    yield str(self.getPosition())
    #yield str(self.getDirection())
  def draw(self, screen, viewPoint):
    image = self.getImage().rotate(viewPoint.getDirection() - self.getDirection())
    screen.draw(image = image,
                position = (self.getPosition() -
                            viewPoint.getPosition()
                            ).rotate(-viewPoint.getDirection()) -
                            image.getSize() / 2 +
                            Manager.getScreenSize() / 2)

