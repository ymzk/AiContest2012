import pygame
from ymzkgame.runnable import Runnable
from ymzkgame.coordinate import Coordinate
from ymzkgame.gameObject import GameObject

class CellCode:
  (NOTHING, WALL) = range(2)

class Cell(Runnable):
  def __init__(self, cellWidth, cellHeight):
    super().__init__()
  def getCellCode(self, unit):
    assert True,"CellCode is not defined"
  def run():
    super().run()

class WallCell(Cell):  
  def __init__(self, cellWidth, cellHeight):
    super().__init__(cellWidth, cellHeight)
  def getCellCode(self, teamFlag):
    return CellCode.WALL
      

class NoneCell(Cell):
  def __init__(self):
    super().__init__()
  def getCellCode(self, unit):
    return CellCode.NOTHING

class OwnAriaCell(Cell):
  def __init__(self, teamFlag):
    super().__init__()
    self._teamFlag = teamFlag
  def getCellCode(self, unit):
    return CellCode.NOTHING if unit.getTeamFlag() == self.teamFlag else CellCode.WALL

  

class Field(Runnable):
  def __init__(self):
    super().__init__()
    self.setFieldSize(100, 100, 25, 25)
  def setFieldSize(self, fieldWidth, fieldHeight,cellWidth,cellHeight):
    self._fieldWidth = fieldWidth
    self._fieldHeight = fieldHeight
    self._cellWidth = cellWidth
    self._cellHeight = cellHeight
    self._fieldData = [[0 for i in range(fieldWidth)] for j in range(fieldHeight)]
  def setCellSize(self, cellSize):
    self._cellSize = cellSize
  def wallDistance(self, radius, unit):
    index = self.changePositionToIndex(unit.getPosition())
    point = getNerestPoint()
    pass
  def changePositionToIndex(self,unit):
    Coordinate((int)(unit.getX() / self._cellWidth), (int)(unit.getY() / self._cellHeight))
  def changeIndexToPosition(self,unit):
    Coordinate(unit.getX() * self._cellWidth, unit.getY() * self._cellHeight)
  def getNearestPoint(self, vector):
    #近隣点からのベクトルを返す
    x = index.getX()
    y = index.getY()
    if abs(x) <= self.cellWidth / 2:
      if abs(y) <= self.cellHeight / 2:
        #pointがこのcell内部
        return Coordinate(x / abs(x) * self.cellWidth / 2 - x, 0) if x > y else Coordinate(0, y / abs(y) * self.cellHeight / 2 - y)
      #最寄点はy軸方向への推薦の足
      return Coordinate(0, y / abs(y) * self.cellHeight / 2 - y)
    if abs(y) < self.cellHeight / 2:
      return Coordinate(x / abs(x) * self.cellWidth / 2 - x, 0)
    return Coordinate(x / abs(x) * self.cellWidth / 2 - x, y / abs(y) * self.cellHeight / 2 - y)
  def checkWall(self, unit):
    x = unit.getPosition().getX()
    y = unit.getPosition().getY()
    if x < 0 or y < 0 or x >= fieldWidth or y >= fieldHeight:
      return CellCode.WALL
    return self.feildData[x][y].getCellCode(unit)
  def getDataPoint(self, point):
    return ((int)(point.getx()/self._fieldWidth,(int)(point.gety()/self._fieldHeight)))
  def step(self):
    pygame.display.get_surface().fill((128, 128, 128))
    

if __name__ == '__main__':
  pass
