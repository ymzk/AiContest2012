import sys
import time

class Coordinate(list):
  def __init__(self,data):
    super().__init__()
    stringX = data.pop(0)
    stringY = data.pop(0)
    self.append(float(stringX[1:-1]))
    self.append(float(stringY[:-1]))
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
  def __init__(self, fielddata,myteam):
    def getdata(cell):
      if cell == 'NO':
        return 0
      elif cell == 'WA':
        return 1
      elif cell == 'B0':
        # 4 or 3
        return 3 + myteam.team
      elif cell == 'B1':
        # 3 or 4
        return 4 - myteam.team
      elif cell == 'O0':
        # 2 or -2
        return myteam.team*4 - 2
      elif cell == 'O1':
        # -2 or 2
        return 2 - myteam.team*4
      elif cell == 'IA':
        return -3
      elif cell == 'IH':
        return -4
    self.width = int(fielddata.pop(0))
    self.height = int(fielddata.pop(0))
    self.cellwidth = int(fielddata.pop(0))
    self.cellheight = int(fielddata.pop(0))
    self.fielddata = [[None for i in range(self.height)] for j in range(self.width)]
    self.fieldstringdata = fielddata[:-1]
    for h in range(self.height):
      for w in range(self.width):
        self.fielddata[w][h] = getdata(fielddata.pop(0))
  def isPassable(self, x, y):
    return self.fielddata[x][y] <= 0
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

    
    
class TestAi:
  MAXSPEED = 3
  def __init__(self):
    self.clear()
    self._logFile = open(str(self.__class__.__name__) + ".log","w")
  def log(self, *arg):
    print(*arg,file = self._logFile)
    self._logFile.flush()
  def clear(self):
    self.units = []
    self.bullets = []
    self.items = []
    self.bases = []
  def receiveInit(self,file):
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
  def receive(self,file):
    data = file.readline().split()
    self.clear()
    if len(data) == 0:
      self.log("missed to read:null data")
      return True
    self.log("rawdata=", data)
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
    self.receiveInit(initfile)
    #print(0,0,0)
    sys.stdout.flush()
    while self.receive(file):
      self.send()
  def regularizeMove(self, moveFrom, moveTo):
    val = (moveFrom[0] - moveTo[0]) + (moveFrom[1] - moveTo[1]) ** 0.5
    if val > self.MAXSPEED:
      return ((moveTo[i] - moveFrom[i])* self.MAXSPEED / val for i in (0,1))
  def sendData(self, speed = 0, angle = 0, fireing = False):
    if speed > self.MAXSPEED:
      speed = self.MAXSPEED
    elif speed < 0:
      speed = 0
    angle = self.regularizeAngle(angle)
    if angle > 0.3:
      angle = 0.3
    elif angle < -0.3:
      angle = -0.3
    print(speed,angle,1 if fireing else 0)
    sys.stdout.flush()
  def regularizeAngle(self, angle):
    if angle > 0:
      return (angle - (int((angle/3.14159265+1))-1)*3.14159265*2)
    else:
      return (angle - (int((angle/3.14159265-1))+1)*3.14159265*2)
  def send(self):
    self.sendData(speed = 3, angle = 0.2, fireing = True)
hoge = TestAi()
#hoge.run(open("initMessage","r"),open("message","r"))
hoge.run()

