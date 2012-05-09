from ymzkgame.gameObject import GameObject
from ymzkgame.coordinate import Coordinate
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
    
  def draw(self,screan):
    if self.checkAvailable():
      super().draw(screan)
  def step(self):
    super().step()
    self._remainingTime -= 1
class HpItem(Item):
  def __init__(self, position = Coordinate(0,0)):
    super().__init__(position,image = "hpItem.bmp");
    self._power = 100
  def effect(self, unit):
    if self.checkAvailable():
      super().effect(unit)
      unit.setHp(unit.getHp() + self._power)
      print("inclease hp",unit.getHp())
      '''
  def clone(self):
    return HpItem(self.getPosition())
      '''
class AttackItem(Item):
  def __init__(self, position = Coordinate(0,0)):
    super().__init__(position,image = "attackItem.bmp")
    self._power = 10
  def effect(self, unit):
    if self.checkAvailable():
      super().effect(unit)
      unit.setAttackPower((unit.getAttackPower() + self._power))
      print("inclease attack",unit.getAttackPower())
  def clone(self):
    return AttackItem(self.getPosition)
  
