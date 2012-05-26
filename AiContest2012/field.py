# coding: cp932
from item import *

import pygame
from ymzkgame.runnable import Runnable
from ymzkgame.runnableList import RunnableList
from ymzkgame.coordinate import Coordinate
from ymzkgame.gameObject import GameObject
from ymzkgame.image import Image
from cell import *
from base import Base

import gameConfig

class Field(Runnable):
  def __init__(self, gameManager):
    super().__init__()
    self.setFieldSize(100, 100)
    self._gameManager = gameManager
    self._modified = False
  def setFieldSize(self, fieldWidth, fieldHeight):
    self._fieldWidth = fieldWidth
    self._fieldHeight = fieldHeight
  def setCell(self, positionX, positionY, cell):
    cell.setPosition(Coordinate(positionX * FIELD_CELL_WIDTH + FIELD_CELL_WIDTH/2, positionY * FIELD_CELL_HEIGHT + FIELD_CELL_HEIGHT/2))
    self._fieldData[positionX][positionY] = cell
    self._modified = True
  def testInitialize(self):
    #self.setFieldSize(40, 40)
    self._fieldData = [[None for i in range(self._fieldWidth)] for j in range(self._fieldHeight)]
    for i in range(self._fieldWidth):
      for j in range(self._fieldHeight):
        self.setCell(i, j, NoneCell())
    for i in range(self._fieldWidth):
      self.setCell(i,8,OwnAreaCell(1))
    self.setCell(0,0,ItemCell(self._gameManager,HpItem()))
    self.setCell(1,0,ItemCell(self._gameManager,AttackItem()))
  def fieldEffect(self, runnableObject):
    if 0 <= runnableObject.getPosition().getX() < self._fieldWidth * FIELD_CELL_WIDTH and 0 <= runnableObject.getPosition().getY() < self._fieldHeight * FIELD_CELL_HEIGHT:
      x = int(runnableObject.getPosition().getX() / FIELD_CELL_WIDTH)
      y = int(runnableObject.getPosition().getY() / FIELD_CELL_HEIGHT)
      self._fieldData[x][y].effect(runnableObject)
      return
    #場外に出たので消滅
    runnableObject.end()
  def addRunnableCell(self,cell):
    pass
  def wallDistance(self, radius, unit):
    offsetX = unit.getPosition().getX() % FIELD_CELL_WIDTH - FIELD_CELL_WIDTH / 2
    offsetY = unit.getPosition().getY() % FIELD_CELL_HEIGHT - FIELD_CELL_HEIGHT /2
    indexX = int(unit.getPosition().getX() / FIELD_CELL_WIDTH)
    indexY = int(unit.getPosition().getY() / FIELD_CELL_HEIGHT)
    minRange = radius
    minVector = Coordinate(0, 0)
    rangeWidth = int(radius/FIELD_CELL_WIDTH) + 1
    for i in range(- rangeWidth, rangeWidth + 1):
      val = (radius / FIELD_CELL_HEIGHT + 1) * (radius / FIELD_CELL_HEIGHT + 1) - i * i
      if val < 0:
        continue
      rangeHeight = int(val ** 0.5)
      for j in range(- rangeHeight, rangeHeight + 1):
        if i == j == 0:
          continue
        if self.checkWall(indexX + i, indexY + j, unit) == CellCode.NOTHING:
          continue
        vector = self.getVectorFromNearestPoint(offsetX - i * FIELD_CELL_WIDTH, offsetY - j * FIELD_CELL_HEIGHT)
        if abs(vector) < minRange:
          minVector = vector
          minRange = abs(vector)
    if abs(minVector) == 0:
      return Coordinate(0, 0)
    return minVector/minRange * (radius - minRange)
  def changePositionToIndex(self,point):
    return Coordinate((int)(point.getX() / FIELD_CELL_WIDTH), (int)(point.getY() / FIELD_CELL_HEIGHT))
  def changeIndexToPosition(self,point):
    return Coordinate(point.getX() * FIELD_CELL_WIDTH, point.getY() * FIELD_CELL_HEIGHT)
  def getVectorFromNearestPoint(self, x, y):
    #近隣点からのベクトルを返す
    if abs(x) <= FIELD_CELL_WIDTH / 2:
      if abs(y) <= FIELD_CELL_HEIGHT / 2:
        #pointがこのcell内部
        if x > y:
          flag = 1 if x > 0 else -1
          return Coordinate(x - flag * FIELD_CELL_WIDTH / 2, 0)
        flag = 1 if y > 0 else -1
        return Coordinate(0, y - flag * FIELD_CELL_HEIGHT / 2)
      #最寄点はy軸方向への推薦の足
      flag = 1 if y > 0 else -1
      return Coordinate(0, y - flag * FIELD_CELL_HEIGHT / 2)
    if abs(y) <= FIELD_CELL_HEIGHT / 2:
      flag = 1 if x > 0 else -1
      return Coordinate(x - flag * FIELD_CELL_WIDTH / 2, 0)
    flagX = 1 if x > 0 else -1
    flagY = 1 if y > 0 else -1
    return Coordinate(x - flagX * FIELD_CELL_WIDTH / 2, y - flagY * FIELD_CELL_HEIGHT / 2)
  def checkWall(self, x, y, unit):
    if x < 0 or y < 0 or x >= self._fieldWidth or y >= self._fieldHeight:
      return CellCode.WALL
    return self._fieldData[x][y].getCellCode(unit)
  def getDataPoint(self, point):
    return ((int)(point.getx()/self._fieldWidth,(int)(point.gety()/self._fieldHeight)))
  def step(self):
    pass
  def updateImage(self, surface):
    maxLength = abs(surface.getSize())
    self._image = Image((FIELD_CELL_WIDTH * self._fieldWidth + maxLength, FIELD_CELL_HEIGHT * self._fieldHeight + maxLength))
    for i in self._fieldData:
      for cell in i:
        self._image.draw(cell.getImage(), cell.getPosition() + Coordinate(maxLength / 2, maxLength / 2) - Coordinate(FIELD_CELL_WIDTH / 2, FIELD_CELL_HEIGHT / 2))
  def draw(self,serface,viewPoint):
    PI = 3.14159265
    '''
    for i in self._fieldData:
      for cell in i:
        cell.draw(serface)
    '''
    if self._modified:
      self.updateImage(serface)
      self._modified = False
    maxLength = abs(serface.getSize())
    size = Coordinate(maxLength, maxLength)
    mergin = size / 2
    leftUp = viewPoint.getPosition() - size / 2 + mergin
    leftUp = Coordinate(max(0, leftUp.getX()), max(0, leftUp.getY()))
    image = self._image.getSubImage(leftUp, size)
    image = image.rotate(viewPoint.getDirection() + PI / 2)
#    image = self._image
    serface.draw(image = image, position = -(image.getSize() - serface.getSize()) / 2)
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
    for h in range(self._fieldHeight):
      for w in range(self._fieldHeight):
        yield self.lines[h][w]
    



if __name__ == '__main__':
  pass
