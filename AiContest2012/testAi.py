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
  def __str__(self):
    def gen():
      yield self.hp
      yield self.team
      yield self.position
      yield self.direction
      yield self.attack
      yield self.reload
    string = "unit"
    for i in gen():
      string += " " + str(i)
    return string
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
        return 1
      elif cell == 'B1':
        return 1
      elif cell == 'O0':
        return myteam.team
      elif cell == 'O1':
        return 1 - myteam.team
      elif cell == 'IA':
        return 2
      elif cell == 'IH':
        return 3
    self.width = int(fielddata.pop(0))
    self.height = int(fielddata.pop(0))
    self.cellwidth = int(fielddata.pop(0))
    self.cellheight = int(fielddata.pop(0))
    self.fielddata = [[None for i in range(self.height)] for j in range(self.width)]
    self.fieldstringdata = fielddata[:-1]
    for h in range(self.height):
      for w in range(self.width):
        self.fielddata[w][h] = getdata(fielddata.pop(0))
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
  
class main:
  def __init__(self):
    self.clear()
  def clear(self):
    self.units = []
    self.bullets = []
    self.items = []
    self.bases = []
  def run(self,file):
    data = file.readline().split()

    if data.pop(0) == "startInit":
      while True:
        top = data.pop(0)
        if top == "endInit":
          break
        if top == "unit":
          self.myunit = Unit(data)
          self.units.append(self.myunit)
        if top == "field":
          self.field = Field(data, self.myunit)
    else:
      assert False,"init err"
    while True:
      self.clear()
      if data.pop(0) == "start":
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
      
hoge.run(sys.stdin)


