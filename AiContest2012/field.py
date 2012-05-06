import pygame
from ymzkgame.runnable import Runnable
from ymzkgame.coordinate import Coordinate
from ymzkgame.gameObject import GameObject

class CellCode:
  (NOTHING, WALL) = range(2)

class Cell(Runnable):
  def __init__(self):
    super().__init__()
  def getCellCode(self, unit):
    assert True,"CellCode is not defined"
  def effect(self, *args):
    pass
  def step():
    super().step()

class WallCell(Cell):  
  def __init__(self):
    super().__init__()
  def effect(self, runnableObject):
    runnableObject.end()
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
  def effect(self, runnableObject):
    if runnableObject.getTeamFlag() != self._teamFlag:
      runnableObject.end()
  def getCellCode(self, unit):
    return CellCode.NOTHING if unit.getTeamFlag() == self._teamFlag else CellCode.WALL

  

class Field(Runnable):
  def __init__(self):
    super().__init__()
    self.setFieldSize(100, 100, 40, 40)
    self.testInitialize()
  def setFieldSize(self, fieldWidth, fieldHeight,cellWidth,cellHeight):
    self._fieldWidth = fieldWidth
    self._fieldHeight = fieldHeight
    self._cellWidth = cellWidth
    self._cellHeight = cellHeight
    self._fieldData = [[NoneCell() for i in range(fieldWidth)] for j in range(fieldHeight)]
  def testInitialize(self):
    for i in range(self._fieldWidth):
      self._fieldData[i][8] = OwnAriaCell("team0")
  def fieldEffect(self, runnableObject):
    x = int(runnableObject.getPosition().getX() / self._cellWidth)
    y = int(runnableObject.getPosition().getY() / self._cellHeight)
    if x < 0 or y < 0 or x >= self._fieldWidth or y >= self._fieldHeight:
      #場外に出たので消滅
      runnableObject.end()
      return
    self._fieldData[x][y].effect(runnableObject)

  def wallDistance(self, radius, unit):
    offsetX = unit.getPosition().getX() % self._cellWidth - self._cellWidth / 2
    offsetY = unit.getPosition().getY() % self._cellHeight - self._cellHeight /2
    indexX = int(unit.getPosition().getX() / self._cellWidth)
    indexY = int(unit.getPosition().getY() / self._cellHeight)
    minRange = radius
    minVector = Coordinate(0, 0)
    rangeWidth = int(radius/self._cellWidth) + 1
    for i in range(- rangeWidth, rangeWidth + 1):
      val = (radius / self._cellHeight + 1) * (radius / self._cellHeight + 1) - i * i
      if val < 0:
        continue
      rangeHeight = int(val ** 0.5)
      for j in range(- rangeHeight, rangeHeight + 1):
        if i == j == 0:
          continue
        if self.checkWall(indexX + i, indexY + j, unit) == CellCode.NOTHING:
          continue
        vector = self.getVectorFromNearestPoint(offsetX - i * self._cellWidth, offsetY - j * self._cellHeight)
        if abs(vector) < minRange:
          minVector = vector
          minRange = abs(vector)
    if abs(minVector) == 0:
      return Coordinate(0, 0)
    return minVector/minRange * (radius - minRange)
  def changePositionToIndex(self,point):
    return Coordinate((int)(point.getX() / self._cellWidth), (int)(point.getY() / self._cellHeight))
  def changeIndexToPosition(self,point):
    return Coordinate(point.getX() * self._cellWidth, point.getY() * self._cellHeight)
  def getVectorFromNearestPoint(self, x, y):
    #近隣点からのベクトルを返す
    if abs(x) <= self._cellWidth / 2:
      if abs(y) <= self._cellHeight / 2:
        #pointがこのcell内部
        if x > y:
          flag = 1 if x > 0 else -1
          return Coordinate(x - flag * self._cellWidth / 2, 0)
        flag = 1 if y > 0 else -1
        return Coordinate(0, y - flag * self._cellHeight / 2)
      #最寄点はy軸方向への推薦の足
      flag = 1 if y > 0 else -1
      return Coordinate(0, y - flag * self._cellHeight / 2)
    if abs(y) <= self._cellHeight / 2:
      flag = 1 if x > 0 else -1
      return Coordinate(x - flag * self._cellWidth / 2, 0)
    flagX = 1 if x > 0 else -1
    flagY = 1 if y > 0 else -1
    return Coordinate(x - flagX * self._cellWidth / 2, y - flagY * self._cellHeight / 2)
  def checkWall(self, x, y, unit):
    if x < 0 or y < 0 or x >= self._fieldWidth or y >= self._fieldHeight:
      return CellCode.WALL
    return self._fieldData[x][y].getCellCode(unit)
  def getDataPoint(self, point):
    return ((int)(point.getx()/self._fieldWidth,(int)(point.gety()/self._fieldHeight)))
  def step(self):
    pygame.display.get_surface().fill((128, 128, 128))
    

if __name__ == '__main__':
  pass
