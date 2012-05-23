# coding: cp932
import sys
import time
from config import gameConfig
from . moveTo import MoveTo
from . checkPassable import checkPassable
from . index import index

from gameConfig import *

class Action(tuple):
  def __new__(cls, speed = 0, rollAngle = 0, firing = False):
    return tuple.__new__(cls, (speed, rollAngle, 1 if firing else 0))
  def __init__(self, speed = 0, rollAngle = 0, firing = 0):
    tuple.__init__(self, (speed, rollAngle, 1 if firing else 0))
  def getattr(self, name):
    if name == 'speed':
      return self[0]
    elif name == 'rollAngle':
      return self[1]
    elif name == 'firing':
      return self[2]
    else:
      raise AttributeError('\'Action\' has no attribute %s' % repr(name))
  def setattr(self, name, value):
    raise TypeError('\'Action\' object does not support attribute assignment')

class Coordinate(tuple):
  def __new__(cls, data):
    return tuple.__new__(cls, (float(data[0][:-1]), float(data[1])))
  def __init__(self, data):
    tuple.__init__(self, (float(data[0][-1]), float(data[1])))
    data.pop(0)
    data.pop(0)
#  def __init__(self,data):
#    self.append(float(data.pop(0)[:-1]))
#    self.append(float(data.pop(0)))
class Unit:
  def __init__(self, data):
    self.hp = float(data.pop(0))
    self.team = int(data.pop(0))
    self.position = Coordinate(data)
    self.direction = float(data.pop(0))
    self.attack = float(data.pop(0))
    self.reload = float(data.pop(0))
    self.unitId = int(data.pop(0))
  def __str__(self):
    def gen():
      yield self.hp
      yield self.team
      yield self.position
      yield self.direction
      yield self.attack
      yield self.reload
      yield self.unitId
    string = "unit"
    for i in gen():
      string += " " + str(i)
    return string
  def isSameUnit(self,unit):
    return self.unitId == unit.unitId
  def __eq__(self, other):
    return self.isSameUnit(other)
  def isFirable(self):
    return self.reload <= 0
class Bullet:
  def __init__(self, data):
    self.team = int(data.pop(0))
    self.position = Coordinate(data)
    self.direction = float(data.pop(0))
    self.move = Coordinate(data)
  def __str__(self):
    def gen():
      yield self.team
      yield self.position
      yield self.direction
      yield self.move
    string = "bullet"
    for i in gen():
      string += " " + str(i)
    return string
class Base:
  def __init__(self, data):
    self.hp = float(data.pop(0))
    self.team = int(data.pop(0))
    self.position = Coordinate(data)
  def __str__(self):
    def gen():
      yield self.hp
      yield self.team
      yield self.position
    string = "base"
    for i in gen():
      string += " " + str(i)
    return string
class Item:
  def __init__(self, data):
    self.position = Coordinate(data)
    self.type = data.pop(0)
  def __str__(self):
    def gen():
      yield self.position
      yield self.type
    string = "item"
    for i in gen():
      string += " " + str(i)
    return string
class Field:
  # def log(self, *arg):
  #   print(*arg, file = self.logfile)
  #   self.logfile.flush()
  def __init__(self, fieldData,myTeam):
    # self.logfile = open("Field.log","w")
    def getdata(cell):
      if cell == 'IH':
        return -2
      elif cell == 'IA':
        return -1
      elif cell == 'NO':
        return 0
      elif cell == 'O0':
        return 1
      elif cell == 'O1':
        return 2
      elif cell == 'B0':
        return -3
      elif cell == 'B1':
        return -4
      elif cell == 'WA':
        return 3
    self.myTeam = myTeam
    self.width = int(fieldData.pop(0))
    self.height = int(fieldData.pop(0))
    self.cellWidth = FIELD_CELL_WIDTH
    self.cellHeight = FIELD_CELL_HEIGHT
#    self.fieldData = [[None for i in range(self.height)] for j in range(self.width)]
#    self.fieldstringdata = fieldData[:-1]
#    for h in range(self.height):
#      for w in range(self.width):
#        self.fieldData[w][h] = getdata(fieldData.pop(0))
    self.data = list(zip(*[[fieldData.pop(0) for j in range(self.width)] for i in range(self.height)]))
    self.fieldData = [[getdata(i) for i in j] for j in self.data]

  def isPassable(self, x, y, team = None):
    if x < 0 or x >= self.width or y < 0 or y >= self.height:
      return False
    elif self.fieldData[int(x)][int(y)] <= 0:
      return True
    elif team == None:
      team = self.myTeam.team
    return self.fieldData[int(x)][int(y)] == 1 + team
#  def isPassableCheck(self, x, y, team = None):
#    if 0 <= x < self.width and 0 <= y < self.height:
#      return isPassable(x, y, team)
#    return False
  def __str__(self):
    def gen():
      yield self.width
      yield self.height
      yield self.cellWidth
      yield self.cellHeight
      yield self.data
    string = "field"
    for i in gen():
      string += " " + str(i) 
    return string
    
class AiInterface:
  MAXSPEED = 3
  def __init__(self):
    self.__clear()
    # self.__logFile = open(str(self.__class__.__name__) + ".log","w")
    self.__logFile = sys.stderr

    # for moveTo
    self.__move = None
    self.__lastTarget = None
  def __clear(self):
    self.units = []
    self.bullets = []
    self.items = []
    self.bases = []
  def __sendLastData(self):
    print(self.__data[0],self.__data[1],self.__data[2])
    sys.stdout.flush()    
  def __receiveInit(self,file):
    data = file.readline().split()
    if data.pop(0) == "startInit":
      while True:
        top = data.pop(0)
        if top == "endInit":
          break
        elif top == "unit":
          self.myunit = Unit(data)
          self.units.append(self.myunit)
        elif top == "field":
          self.field = Field(data, self.myunit)
        else:
          # self.log("miss to read init")
          # self.log("message=", top, data)
          pass
    else:
      assert False,"init err"
  def __receive(self,file):
    data = file.readline().split()
    self.__clear()
    if len(data) == 0:
      # self.log("missed to read:null data")
      return True
    #self.log("rawdata=", data)
    top = data.pop(0)
    if top == "endGame":
      # self.log("endGame")
      return False
    if top == "start":
      while True:
        if len(data) == 0:
          break
        top = data.pop(0)
        if top == "end":
          break
        elif top == "unit":
          unit = Unit(data)
          if unit.isSameUnit(self.myunit):
            self.myunit = unit;
          else:
            self.units.append(unit)
        elif top == "bullet":
          self.bullets.append(Bullet(data))
        elif top == "item":
          self.items.append(Item(data))
        elif top == "base":
          self.bases.append(Base(data))
        else:
          # self.log("miss to read identify")
          # self.log("message=top:", top," data=", data)
          pass
      return True
    # self.log("miss to read start")
    # self.log("message=", top,"data=", data)
    return True
    '''
      for i in self.units:
        print(i)
      for i in self.bullets:
        print(i)
      for i in self.items:
        print(i)
      for i in self.bases:
        print(i)
      sys.stdout.flush()
      break
      '''
  def run(self,initfile = sys.stdin,file = sys.stdin):
    self.__receiveInit(initfile)
#    print(0,0,0)
#    sys.stdout.flush()
    self.__receive(file)
    self.initCalculation()
    print(0, 0, 0)
    sys.stdout.flush()
    while self.__receive(file):
      action = self.main()
      if not isinstance(action, tuple):
        print('AiInterface.main -- a Action is required', file = sys.stderr)
      if action == None:
        self.__sendData(0, 0, 0)
      else:
        self.__sendData(*action)
      self.__sendLastData()
  def __sendData(self, speed = 0, angle = 0, firing = False):
    if speed > self.MAXSPEED:
      speed = self.MAXSPEED
    elif speed < 0:
      speed = 0
    angle = self.regularizeAngle(angle)
    if angle > 0.2:
      angle = 0.2
    elif angle < -0.2:
      angle = -0.2
    self.__data = (speed,angle,1 if firing else 0)
  def log(self, *arg, **keys):
    keys["file"] = self.__logFile
    print(*arg, **keys)
    self.__logFile.flush()
  def canShoot(self, fromPosition, toPosition):
    f = index(self.field, fromPosition)
    t = index(self.field, toPosition)
    # self.log(f, self.field.isPassable(*f))
    # self.log(t, self.field.isPassable(*t))
    return checkPassable(self.field,
                         index(self.field, fromPosition),
                         index(self.field, toPosition))
    
  def regularizeSpeed(self, speed):
    if speed < 0:
      return 0
    elif speed > MAXSPEED:
      return MAXSPEED
    else:
      return speed
  def regularizeAngle(self, angle):
    return (angle%(6.2831853)+3.14159265)%(6.2831853)-3.14159265
  def initCalculation(self):
    #はじめに何かしたいときはここに書く
    pass
#  def send(self):
#    #次の動きを計算し、sendDataへ送信する
#    pass
  def main(self):
    # 次の動きを計算し、Actionとして返す
    return NotImplemented
  def moveTo(self, target):
    if target != self.__lastTarget:
#      self.log(target, self.__lastTarget)
      self.__move = MoveTo(self.field, self.myunit, target)
      self.__lastTarget = target
#      self.log(target, self.__lastTarget)
    return Action(*self.__move.get(self.field, self.myunit))
  def getAllyTeamId(self):
    return self.myunit.team
  def getOpponentTeamId(self):
    return 1 - self.myunit.team
  def simulate(self, action, unit = None):
    # self.myunitがactionの通りに移動した未来を返すメソッド。
    # 壁は貫通します
    if unit == None:
      unit = self.myunit
    if action.speed > self.MAXSPEED:
      speed = self.MAXSPEED
    elif action.speed < 0:
      speed = 0
    else:
      speed = action.speed
    rollAngle = self.regularizeAngle(action.rollAngle)
    if rollAngle > 0.2:
      rollAngle = 0.2
    elif rollAngle < -0.2:
      rollAngle = -0.2
    result = object.__new__(Unit)
    result.hp = unit.hp
    result.team = unit.team
    result.direction = unit.direction + rollAngle
    result.position = (unit.position[0] + speed * cos(angle),
                       unit.position[1] + speed * sin(angle))
    result.attack = unit.attack
    result.reload = unit.reload
    result.unitId = unit.unitId
    if result.reload > 0:
      result.reload -= 1
    if result.isFirable():
      result.reload = gameConfig.UNIT_TIME_NEXT_FIRING
    return result
