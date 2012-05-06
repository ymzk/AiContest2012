from ymzkgame.gameObject import GameObject

class Base(GameObject):
  def __init__(self, position, direction, teamFlag):
    super().__init__()
    self.setPosition(position)
    self.setDirection(direction)
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
  
