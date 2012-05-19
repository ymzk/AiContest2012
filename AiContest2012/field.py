
from item import *

import pygame
from ymzkgame.runnable import Runnable
from ymzkgame.runnableList import RunnableList
from ymzkgame.coordinate import Coordinate
from ymzkgame.gameObject import GameObject
from ymzkgame.image import Image
from cell import *
from base import Base

class Field(Runnable):
  def __init__(self, gameManager):
    super().__init__()
    self.setFieldSize(100, 100, 40, 40)
    self._gameManager = gameManager
    self._image = Image(pygame.Surface((self._fieldWidth * self._cellWidth, self._fieldHeight * self._cellHeight)), permeate = False)
    self._modified = False
  def setFieldSize(self, fieldWidth, fieldHeight,cellWidth,cellHeight):
    self._fieldWidth = fieldWidth
    self._fieldHeight = fieldHeight
    self._cellWidth = cellWidth
    self._cellHeight = cellHeight
  def setCell(self, positionX, positionY, cell):
    cell.setPosition(Coordinate(positionX * self._cellWidth + self._cellWidth/2, positionY * self._cellHeight + self._cellHeight/2))
    self._fieldData[positionX][positionY] = cell
    self._modified = True
  def testInitialize(self):
    #self.setFieldSize(40, 40, 25, 25)
    self._fieldData = [[None for i in range(self._fieldWidth)] for j in range(self._fieldHeight)]
    for i in range(self._fieldWidth):
      for j in range(self._fieldHeight):
        self.setCell(i, j, NoneCell())
    for i in range(self._fieldWidth):
      self.setCell(i,8,OwnAreaCell(1))
    self.setCell(0,0,ItemCell(self._gameManager,HpItem()))
    self.setCell(1,0,ItemCell(self._gameManager,AttackItem()))
  def fieldEffect(self, runnableObject):
    if 0 <= runnableObject.getPosition().getX() < self._fieldWidth * self._cellWidth and 0 <= runnableObject.getPosition().getY() < self._fieldHeight * self._cellHeight:
      x = int(runnableObject.getPosition().getX() / self._cellWidth)
      y = int(runnableObject.getPosition().getY() / self._cellHeight)
      self._fieldData[x][y].effect(runnableObject)
      return
    #場外に出たので消滅
    runnableObject.end()
  def addRunnableCell(self,cell):
    pass
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
    pass
  def updateImage(self):
    for i in self._fieldData:
      for cell in i:
        cell.draw(self._image)
  def draw(self,serface,viewPoint):
    '''
    for i in self._fieldData:
      for cell in i:
        cell.draw(serface)
    '''
    if self._modified:
      self.updateImage()
      self._modified = False
    maxLength = abs(Manager.getScreenSize())
    areaSize = Coordinate(maxLength, maxLength)
    image = self._image.getSubImage(viewPoint.getPosition() - areaSize / 2, areaSize).rotate(viewPoint.getDirection())
    serface.draw(image = image, position = -(image.getSize() - Manager.getScreenSize()) / 2)
#    serface.draw(self._image)
  def loadField(self, filename):
    def convert(token):
      if token == 'NO':
        return NoneCell()
      elif token == 'WA':
        return WallCell()
      elif token == 'B0':
        return BaseCell(self._gameManager,Base(0))
      elif token == 'B1':
        return BaseCell(self._gameManager,Base(1))
      elif token == 'O0':
        return OwnAreaCell(0)
      elif token == 'O1':
        return OwnAreaCell(1)
      elif token == 'IA':
        return ItemCell(self._gameManager,AttackItem())
      elif token == 'IH':
        return ItemCell(self._gameManager,HpItem())
      else:
        print(token)
        assert False,"cellCodeError"
    file = open(filename, "r")
    self._fieldWidth, self._fieldHeight = file.readline().split()
    self._fieldWidth, self._fieldHeight = int(self._fieldWidth), int(self._fieldHeight)
    self._unitPosition = [[],[]]
    for i in (0,1):
      positionAndDirectionList = [i.strip()[1:].split(",") for i in file.readline().strip()[:-1].split(")")]
      for positionAndDirection in positionAndDirectionList:
        # print([Coordinate(positionAndDirection[0], positionAndDirection[1]),positionAndDirection[2]])
        self._unitPosition[i].append([Coordinate(float(positionAndDirection[0].strip()) * self._fieldWidth, float(positionAndDirection[1].strip()) * self._fieldHeight), float(positionAndDirection[2].strip())])
    self.lines = [line.split() for line in file.readlines()]
    self._fieldData = [[None for i in range(self._fieldHeight)] for j in range(self._fieldWidth)]
    team = [0,1]
    for i, line in enumerate(self.lines):
      for j, token in enumerate(line):
        self.setCell(j, i, convert(token))
  def getUnitPosition(self, team):
    for i in self._unitPosition[team]:
      yield i
  def encode(self):
    yield self._fieldWidth
    yield self._fieldHeight
    yield self._cellWidth
    yield self._cellHeight
    for h in range(self._fieldHeight):
      for w in range(self._fieldHeight):
        yield self.lines[h][w]
    



if __name__ == '__main__':
  pass
