from ymzkgame.gameObject import GameObject
from ymzkgame.coordinate import Coordinate
class Item(GameObject):
  def __init__(self, position = Coordinate(0,0), image = "item.bmp"):
    super().__init__(image = image)
    self._TimeReload = 0
    self.setPosition(position)
    self.setDirection(0)
  def effect(self, opponentUnit):
    pass

class HpItem(Item):
  def __init__(self, position = Coordinate(0,0)):
    super().__init__(position,image = "hpItem.bmp");
    self._power = 100
  def effect(self, unit):
    unit.setHp(unit.getHp() + self._power)
    print("inclease hp",unit.getHp())
    self.end()
  def clone(self):
    return HpItem(self.getPosition())

class AttackItem(Item):
  def __init__(self, position = Coordinate(0,0)):
    super().__init__(position,image = "attackItem.bmp")
    self._power = 10
  def effect(self, unit):
    unit.setAttackPower((unit.getAttackPower() + self._power))
    print("inclease attack",unit.getAttackPower())
    self.end()
  def clone(self):
    return AttackItem(self.getPosition)
  
