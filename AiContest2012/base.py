from ymzkgame.gameObject import GameObject
from ymzkgame.coordinate import Coordinate
from ymzkgame.manager import Manager
from draw import draw
class Base(GameObject):
  MAX_HP, RECOVER_INTERVAL = 600, 60
  def __init__(self, teamFlag, position = Coordinate(0,0), direction = 0):
    super().__init__(position = position,direction = direction, image = "graphics/base.bmp")
    self._teamFlag = teamFlag
    self._damagedFlag = False
    self._counter = 0
    self._hp = self.MAX_HP
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
    if self._counter > 0:
      self._counter -= 1
    elif self._hp < self.MAX_HP:
      self._counter = self.RECOVER_INTERVAL
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
