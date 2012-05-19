import sys
import time
import gameConfig
from aiLibrary.moveTo import MoveTo

class Action(tuple):
  def __new__(cls, speed, rollAngle, firing):
    return tuple.__new__(cls, (speed, rollAngle, 1 if firing else 0))
  def __init__(self, speed, rollAngle, firing):
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
    self.team = float(data.pop(0))
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
    self.team = float(data.pop(0))
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
  def log(self, *arg):
    print(*arg, file = self.logfile)
    self.logfile.flush()
  def __init__(self, fieldData,myTeam):
    self.logfile = open("Field.log","w")
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
        return 3
      elif cell == 'B1':
        return 4
      elif cell == 'WA':
        return 5
    self.myTeam = myTeam
    self.width = int(fieldData.pop(0))
    self.height = int(fieldData.pop(0))
    self.cellWidth = int(fieldData.pop(0))
    self.cellHeight = int(fieldData.pop(0))
    self.fieldData = [[None for i in range(self.height)] for j in range(self.width)]
    self.fieldstringdata = fieldData[:-1]
    for h in range(self.height):
      for w in range(self.width):
        self.fieldData[w][h] = getdata(fieldData.pop(0))
  def isPassable(self, x, y, team = None):
    if self.fieldData[int(x)][int(y)] <= 0:
      return True
    elif team == None:
      team = self.myTeam.team
    return self.fieldData[int(x)][int(y)] == 1 + team
  def isPassableSub(self, x, y, team = None):
    self.log(x,y,self.fieldData[int(x)][int(y)])
    if self.fieldData[int(x)][int(y)] <= 0:
      return True
    elif team == None:
      team = self.myTeam.team
    return self.fieldData[int(x)][int(y)] == 1 + team
  def isPassableCheck(self, x, y, team = None):
    if 0 <= x < self.width and 0 <= y < self.height:
      return isPassable(x, y, team)
    return False
  def __str__(self):
    def gen():
      yield self.width
      yield self.height
      yield self.cellWidth
      yield self.cellHeight
      yield self.fieldstringdata
    string = "field"
    for i in gen():
      string += " " + str(i) 
    return string
    
class AiInterface:
  MAXSPEED = 3
  def __init__(self):
    self.__clear()
    self._logFile = open(str(self.__class__.__name__) + ".log","w")
  def __clear(self):
    self.units = []
    self.bullets = []
    self.items = []
    self.bases = []

    # for moveTo
    self.__move = None
    self.__lastTarget = None
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
          self.log("miss to read init")
          self.log("message=", top, data)
    else:
      assert False,"init err"
  def __receive(self,file):
    data = file.readline().split()
    self.__clear()
    if len(data) == 0:
      self.log("missed to read:null data")
      return True
    #self.log("rawdata=", data)
    top = data.pop(0)
    if top == "endGame":
      self.log("endGame")
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
          self.log("miss to read identify")
          self.log("message=top:", top," data=", data)
      return True
    self.log("miss to read start")
    self.log("message=", top,"data=", data)
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
    print(0,0,0)
    sys.stdout.flush()
    self.initCalculation()
    while self.__receive(file):
      action = self.main()
      if not isinstance(action, tuple):
        print('AiInterface.main -- a Action is required', file = sys.stderr)
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
    self.log("angle",angle)
    self.__data = (speed,angle,1 if firing else 0)
  def log(self, *arg):
    print(*arg,file = self._logFile)
    self._logFile.flush()
  def canShoot(self, fromPosition, toPosition):
    def nextDelta(first,remain):
      yield first
      while True:
        yield remain
    dx = toPosition[0] - fromPosition[0]
    dy = toPosition[1] - fromPosition[1]
    if dx == dy == 0:
      return True
    if abs(dx) > abs(dy):
      if dx > 0:
        delta = nextDelta(dy / dx * (self.field.cellWidth - fromPosition[0] % self.field.cellWidth), dy / dx * self.field.cellWidth)
        py = fromPosition[1]
        for ix in range(int(fromPosition[0] // self.field.cellWidth), int(toPosition[0] // self.field.cellWidth)):
          if not self.field.isPassable(ix, py //self.field.cellHeight):
            return False
          py += next(delta)
          if not self.field.isPassable(ix, py // self.field.cellHeight):
            return False
        return True
      else:
        delta = nextDelta(- dy / dx * (fromPosition[0] % self.field.cellWidth), dy / dx * self.field.cellWidth)
        py = fromPosition[1]
        for ix in range(int(fromPosition[0] // self.field.cellWidth), int(toPosition[0] // self.field.cellWidth), -1):
          if not self.field.isPassable(ix, py //self.field.cellHeight):
            return False
          py -= next(delta)
          if not self.field.isPassable(ix, py // self.field.cellHeight):
            return False
        return True
    else:
      if dy > 0:
        delta = nextDelta(dx / dy * (self.field.cellHeight - fromPosition[1] % self.field.cellHeight), dx / dy * self.field.Height)
        px = fromPosition[0]
        for iy in range(int(fromPosition[1] // self.field.cellHeight), int(toPosition[1] // self.field.cellHeight)):
          if not self.field.isPassable(px // self.field.cellWidth, iy):
            return False
          px += next(delta)
          if not self.field.isPassable(px // self.field.cellWidth, iy):
            return False
        return True
      else:
        delta = nextDelta( - dx / dy * (fromPosition[1] % self.field.cellHeight), dx / dy * self.field.cellHeight)
        px = fromPosition[0]
        for iy in range(int(fromPosition[1] // self.field.cellHeight), int(toPosition[1] // self.field.cellHeight), -1):
          if not self.field.isPassable(px // self.field.cellWidth, iy):
            return False
          px -= next(delta)
          if not self.field.isPassable(px // self.field.cellWidth, iy):
            return False
        return True
      
          
          
    
  def regularizeMove(self, moveFrom, moveTo):
    val = ((moveFrom[0] - moveTo[0]) ** 2 + (moveFrom[1] - moveTo[1]) ** 2) ** 0.5
    if val > self.MAXSPEED:
      return tuple((moveTo[i] - moveFrom[i])* self.MAXSPEED / val for i in (0,1))
  def regularizeAngle(self, angle):
    return (angle%(6.2831853)+3.14159265)%(6.2831853)-3.14159265
  def initCalculation(self):
    #はじめに何かしたいときはここに書く
    pass
#  def send(self):
#    #次の動きを計算し、sendDataへ送信する
#    pass
  def main(self):
    #次の動きを計算し、Actionとして返す
    return NotImplemented
  def moveTo(self, target):
    if target != self.__lastTarget:
      self.__move = MoveTo(self.field, self.myunit, target)
      self.__lastTarget = target
    return Action(*self.__move.get(self.field, self.myunit))
  def getAllyTeamId(self):
    return self.myunit.team
  def getOpponentTeamId(self):
    return 1 - self.myunit.team
  def simulate(self, action):
    # self.myunitがactionの通りに移動した未来を返すメソッド。
    # 壁は貫通します
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
    result.hp = self.myunit.hp
    result.team = self.getAllyTeamId()
    result.direction = self.myunit.direction + rollAngle
    result.position = (self.myunit.position[0] + speed * cos(angle),
                       self.myunit.position[1] + speed * sin(angle))
    result.attack = self.myunit.attack
    result.reload = self.myunit.reload
    result.unitId = self.myunit.unitId
    if result.reload > 0:
      result.reload -= 1
    if result.isFirable():
      result.reload = gameConfig.UNIT_TIME_NEXT_FIRING
    return result
