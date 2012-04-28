class Item:
  def __init__(self, _id, _position):
    self._TimeReload = 0
    self._id = _id
    self._position = _position
  def effect(self, opponentUnit):
    pass

class HpItem(Item):
  def __init__(self, _id, _position, _power):
    super().__init__(_id,_position);
    self._power = _power
  def run(self, unit):
    unit.setHp(unit.getHp + _power)
    
