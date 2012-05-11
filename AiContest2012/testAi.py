import sys
import time

class Coordinate:
  def __init__(self,CoordinateData):
    stringX = CoordinateData.pop(0)
    stringY = CoordinateData.pop(0)
    stringX[0]=""
class unit:
  def __init__(self, unitdata):
    self.hp = float(unitdata.pop(0))
    self.team = float(unitdata.pop(0))
    self.position = Coordinate(unitdata)
    self.direction = float(unitdata.pop(0))
    self.reload = float(unitdata.pop(0))
class bullet:
  def __init__(self, bulletdata):
    self.team = float(unitdata.pop(0))
    self.position = Coordinate(unitdata)
    self.direction = float(unitdata.pop(0))
    self.move = Coordinate(unitdata)
    

class main:
  def __init__(self):
    self.clear()
  def clear(self):
    self.units = []
    self.bullets = []
    self.items = []
    self.bases = []
  def run(self):
    while True:
      if sys.stdin.readline() == "start\n":
        data = sys.stdin.readline().split()
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

          
