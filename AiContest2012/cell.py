
from ymzkgame.gameObject import *

class CellCode:
  (NOTHING, WALL) = range(2)

class Cell(GameObject):
  def __init__(self, image = Image(), position = Coordinate(0,0)):
    super().__init__(image = Image(image = image, permeate = False),
                     position = position)
  def getCellCode(self, unit):
#    assert True,"CellCode is not defined"
    raise NotImplementedError('CellCode is not defined')
  def effect(self, *args):
    pass

class WallCell(Cell):  
  def __init__(self):
    super().__init__(image = "graphics/wallCell.bmp")
  def effect(self, runnableObject):
    runnableObject.end()
  def getCellCode(self, teamFlag):
    return CellCode.WALL
      

class NoneCell(Cell):
  def __init__(self):
    super().__init__(image = "graphics/noneCell.bmp")
  def getCellCode(self, unit):
    return CellCode.NOTHING
  def draw(self, *args):
#    print('draw:', self.getPosition())
    super().draw(*args)

class OwnAreaCell(Cell):
  def __init__(self, teamFlag):
    super().__init__(image = "graphics/ownAreaCell.bmp")
    self._teamFlag = teamFlag
  def effect(self, runnableObject):
    if runnableObject.getTeamFlag() != self._teamFlag:
      runnableObject.end()
  def getCellCode(self, unit):
    return CellCode.NOTHING if unit.getTeamFlag() == self._teamFlag else CellCode.WALL

class ItemCell(Cell):
  def __init__(self, gameManager, item):
    super().__init__(image = "graphics/noneCell.bmp")
    self.item = item
    gameManager.addItem(item)
  def setPosition(self, position):
    super().setPosition(position)
    self.item.setPosition(position)
  def getCellCode(self, unit):
    return CellCode.NOTHING

class BaseCell(Cell):
  def __init__(self, gameManager, base):
    super().__init__(image = "graphics/noneCell.bmp")
    self.base = base
    gameManager.addBase(base)
  def setPosition(self, position):
    super().setPosition(position)
    self.base.setPosition(position)
  def setDirection(self, direction):
    super().setDirection(direction)
    self.base.setDirection(direction)
  def getCellCode(self, unit):
    return CellCode.NOTHING

  

