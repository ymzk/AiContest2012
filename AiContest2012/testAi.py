import sys
import time

class Coordinate(list):
  def __init__(self,data):
    super().__init__()
    stringX = data.pop(0)
    stringY = data.pop(0)
    self.append(float(stringX[1:-1]),float(stringY[:-1]))
class Unit:
  def __init__(self, unitdata):
    self.hp = float(unitdata.pop(0))
    self.team = float(unitdata.pop(0))
    self.position = Coordinate(unitdata)
    self.direction = float(unitdata.pop(0))
    self.attack = float(unitdata.pop(0))
    self.reload = float(unitdata.pop(0))
class Bullet:
  def __init__(self, data):
    self.team = float(data.pop(0))
    self.position = Coordinate(data)
    self.direction = float(data.pop(0))
    self.move = Coordinate(data)
class Base:
  def __init__(self, data):
    self.hp = float(unitdata.pop(0))
    self.team = float(data.pop(0))
    self.position = Coordinate(data)

class Field:
  def __init__(self, fielddata,myteam):
    def getdata(cell):
      if cell == 'NO':
        return 0
      elif cell == 'WA':
        return 1
      elif cell == 'B0':
        return 1
      elif cell == 'B1':
        return 1
      elif cell == 'O0':
        return myteam
      elif cell == 'O1':
        return 1 - myteam
      elif cell == 'IA':
        return 2
      elif cell == 'IH':
        return 3
    self._width = fielddata.pop(0)
    self._height = fielddata.pop(0)
    self._cellwidth = fielddata.pop(0)
    self._cellheight = fielddata.pop(0)
    self._fielddata = [[None for i in range(self._height)] for j in range(self._width)]
    for h in self.height:
      for w in self.width:
        self._fielddata[w][h] = getdata(fielddata.pop(0))
  def moveto(self,currentpoint,objectpoint = None):
    def movegenerator():
      tox = objectpoint[0] // self._cellwidth
      toy = objectpoint[1] // self._cellheight
      q = [(currentpoint[0] // self._cellwidth, currentpoint[1] // self._cellheight, (0,0)))]
      def add(point):
        q.append((point[0], point[1], (0,1)))
        q.append((point[0], point[1], (0,-1)))
        q.append((point[0], point[1], (1,0)))
        q.append((point[0], point[1], (-1,0)))
      
      
      
  
class main:
  def __init__(self):
    self.clear()
  def clear(self):
    self.units = []
    self.bullets = []
    self.items = []
    self.bases = []
  def run(self,file):
    if file.readline() == "startinit":
      data = file.readline().split()
      while True:
        top = data.pop(0)
        if top == "end":
          break
        if top == "yourunit":
          self.myunit = Unit(data)
        if top == "fielddata":
          self.field = Field(data)
    else:
      assert Fasle,"init err"
    while True:
      clear()
      if file.readline() == "start\n":
        data = file.readline().split()
        while True:
          top = data.pop(0)
          if top == "end":
            break
          elif top == "unit":
            self.units.append(Unit(data))
          elif top == "bullet":
            self.bullets.append(Bullet(data))
          elif top == "item":
            self.items.append(Item(data))
          elif top == "base":
            self.bases.append(Base(data))

          
