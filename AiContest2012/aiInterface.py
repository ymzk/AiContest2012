import sys
import time

class Coordinate(list):
  def __init__(self,data):
    self.append(float(data.pop(0)[:-1]))
    self.append(float(data.pop(0)))
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
  def __init__(self, fielddata,myTeam):
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
    self.width = int(fielddata.pop(0))
    self.height = int(fielddata.pop(0))
    self.cellwidth = int(fielddata.pop(0))
    self.cellheight = int(fielddata.pop(0))
    self.fielddata = [[None for i in range(self.height)] for j in range(self.width)]
    self.fieldstringdata = fielddata[:-1]
    for h in range(self.height):
      for w in range(self.width):
        self.fielddata[w][h] = getdata(fielddata.pop(0))
  def isPassable(self, x, y, team = None):
    if self.fielddata[x][y] <= 0:
      return True
    elif team == None:
      team = self.myTeam.team
    return self.fielddata[x][y] == 1 + team
  def __str__(self):
    def gen():
      yield self.width
      yield self.height
      yield self.cellwidth
      yield self.cellheight
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
    hoge=0
    print(0,0,0)
    sys.stdout.flush()
    self.initCalculation()
    while self.__receive(file):
      self.send()
  def sendData(self, speed = 0, angle = 0, fireing = False):
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
    print(speed,angle,1 if fireing else 0)
    sys.stdout.flush()
  def log(self, *arg):
    print(*arg,file = self._logFile)
    self._logFile.flush()
  def regularizeMove(self, moveFrom, moveTo):
    val = ((moveFrom[0] - moveTo[0]) ** 2 + (moveFrom[1] - moveTo[1]) ** 2) ** 0.5
    if val > self.MAXSPEED:
      return ((moveTo[i] - moveFrom[i])* self.MAXSPEED / val for i in (0,1))
  def regularizeAngle(self, angle):
    return (angle%(6.2831853)+3.14159265)%(6.2831853)-3.14159265
  def initCalculation(self):
    #はじめに何かしたいときはここに書く
    pass
  def send(self):
    #次の動きを計算し、送信する
    pass
