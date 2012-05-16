from ymzkgame.gameObject import GameObject
from ymzkgame.coordinate import Coordinate
from ymzkgame.manager import Manager
class Item(GameObject):
  def __init__(self, position = Coordinate(0,0), image = "item.bmp",time = 60):
    super().__init__(image = image)
    self._nextTime = time
    self.setPosition(position)
    self.setDirection(0)
    self._remainingTime = 0
  def effect(self, opponentUnit):
    self._remainingTime = self._nextTime
  def checkAvailable(self):
    return self._remainingTime < 0
  def encode(self):
    if self.checkAvailable:
      yield self.getPosition().getX()
      yield self.getPosition().getY()
      yield self.getItemType()
  def draw(self, screen, viewPoint):
    if not self.checkAvailable():
      return
    image = self.getImage().rotate(viewPoint.getDirection() - self.getDirection())
    screen.draw(image = image,
                position = (self.getPosition() -
                            viewPoint.getPosition()
                            ).rotate(-viewPoint.getDirection()) -
                            image.getSize() / 2 +
                            Manager.getScreenSize() / 2)
  def step(self):
    super().step()
    self._remainingTime -= 1
class HpItem(Item):
  def __init__(self, position = Coordinate(0,0)):
    super().__init__(position,image = "hpItem.bmp");
    self._power = 30
  def effect(self, unit):
    if self.checkAvailable():
      super().effect(unit)
      unit.setHp(unit.getHp() + self._power)
      print("inclease hp",unit.getHp())
  def getItemType(self):
    return "IH"
    '''
  def clone(self):
    return HpItem(self.getPosition())
    '''
class AttackItem(Item):
  def __init__(self, position = Coordinate(0,0)):
    super().__init__(position,image = "attackItem.bmp")
    self._power = 1
  def effect(self, unit):
    if self.checkAvailable():
      super().effect(unit)
      unit.setAttackPower((unit.getAttackPower() + self._power))
      print("inclease attack",unit.getAttackPower())
  def getItemType(self):
    return "IA"
  def clone(self):
    return AttackItem(self.getPosition)
  
