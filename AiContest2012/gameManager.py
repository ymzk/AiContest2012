

# import coordinate
from field import Field
from unit import Unit
from base import Base
from item import *
# import bullet
# import item
from aiManager import AiManager
from ymzkgame.runnableList import RunnableList
from ymzkgame.coordinate import Coordinate
from ymzkgame.runnable import Runnable
from ymzkgame.runner import run
from ymzkgame.moveClasses import *
from ymzkgame.gameObject import *
#from backGroundDummy import BackGroundDummy as Field
# for test
#RunnableList = list
'''
class DamyRunnable(Runnable):
  def __init__(self):
    super().__init__()
  def step(self):
    pass
    '''
class GameManager(Runnable):
  _UNIT_RANGE = 16
  _BASE_RANGE = 20
  _ITEM_RANGE = 10
  _PUSH_STRENGTH = 0.5
  _VISILITY = 100
  def __init__(self):
    super().__init__()
    self.bullets = RunnableList()
#    self.bullets.append(None)
    self.units = RunnableList()
#    self.units.append(None)
    self.items = RunnableList()
#    self.items.append(None)
    self.bases = RunnableList()
#    self.bases.append(None)    
    self.field = Field(self)
    self.testInitialize()
  def testInitialize(self):

    self.field.setFieldSize(40, 40, 25, 25)
    self.field.testInitialize()

    self.bases.append(Base("team0",Coordinate(60,120),1))
    self.bases.append(Base("team0",Coordinate(100,120),0))

    self.debugUnit = Unit(Coordinate(200,200),1,self,"team0",AiManager("hoge.py"))
    self.debugUnit.setMove(MoveByKey(velocity = 10))
    self.units.append(self.debugUnit)

    self.units.append(Unit(Coordinate(200,200),1,self,"team0",AiManager("hoge.py")))
    '''
    self.units.append(Unit(Coordinate(201,201),0,self,"team1",AiManager("hoge.py")))
    self.units.append(Unit(Coordinate(302,302),1,self,"team0",AiManager("hoge.py")))
    self.units.append(Unit(Coordinate(600,400),0,self,"team1",AiManager("hoge.py")))
    self.units.append(Unit(Coordinate(601,401),1,self,"team0",AiManager("hoge.py")))
    self.units.append(Unit(Coordinate(602,402),0,self,"team1",AiManager("hoge.py")))
    '''
  def writeMessage(self,unit,file):
    file.write("start\n".encode())
    for i in self.bases:
      self.writeMessageBase(i,file)
    for i in self.units:
      if i.getTeamFlag() == unit.getTeamFlag():
        self.writeMessageUnit(i,file)
        continue
      if abs(i.getPosition() - unit.getPosition()) < self._VISILITY:
        self.writeMessageUnit(i,file)
        continue
    for i in self.bullets:
      if abs(i.getPosition() - unit.getPosition()) <self._VISILITY:
        self.writeMessageBullet(i,file)
    file.write("end\n".encode())
    file.flush()
    
  def writeMessageUnit(self,unit,file):
    file.write("unit".encode())
    file.write(str(unit.getHp()).encode())
    file.write(" ".encode())
    file.write(str(unit.getPosition()).encode())
    file.write(" ".encode())
    file.write(str(unit.getDirection()).encode())
    file.write("\n".encode())
  def writeMessageBullet(self,bullet,file):
    file.write("bullet ".encode())
    file.write(str(bullet.getTeamFlag()).encode())
    file.write(" ".encode())
    file.write(str(bullet.getPosition()).encode())
    file.write(" ".encode())
    file.write(str(bullet.getDirection()).encode())
    file.write("\n".encode())
  def writeMessageBase(self,base,file):
    file.write("base ".encode())
    file.write(str(base.getHp()).encode())
    file.write("\n".encode())
  def addBullet(self, bullet):
    self.bullets.append(bullet)
  def addItem(self, item):
    self.items.append(item)
  def addBase(self, base):
    self.bases.append(base)
  def step(self):
    self.field.step()
    self.bases.step()
    self.units.step()
    self.bullets.step()
    self.items.step()

    for counter in range(20):
      #振動して無限ループになったとき、20回で終了するようにしている。
      #押し合い
      powerList = [Coordinate(0,0) for i in range(len(self.units))]
      for ii in range(len(self.units)):
        for jj in range(ii):
          i = self.units[ii].getPosition()
          j = self.units[jj].getPosition()
          if abs(i - j) < self._UNIT_RANGE * 2 :
            factor = (self._UNIT_RANGE * 2 - abs(i - j))/(abs(i - j) + 10 **(-7)) * (i - j)
            powerList[ii] += factor
            powerList[jj] -= factor
            #重なっているとき
      for ii in range(len(self.units)):
        for jj in range(len(self.bases)):
          i = self.units[ii].getPosition()
          j = self.bases[jj].getPosition()
          if abs(i - j) < self._UNIT_RANGE + self._BASE_RANGE:
            factor = (self._UNIT_RANGE + self._BASE_RANGE - abs(i - j))/(abs(i - j) + 10 **(-7)) * (i - j)
            powerList[ii] += factor
            #重なっているとき
            
      for i in range(len(self.units)):
        #壁との当たり判定壁との当たり判定はFeildで行う。
        #返り値はかかる力ベクトル(Coordinate)
        powerList[i] += self.field.wallDistance(self._UNIT_RANGE, self.units[i])

      flag = True
      for i in range(len(self.units)):
        if powerList[i].norm() > 1e-6:
          self.units[i].setPosition(self.units[i].getPosition() + powerList[i] * self._PUSH_STRENGTH)
          flag = False
      if flag:
        break

    #当たり判定
    for i in range(len(self.units)):
      self.field.fieldEffect(self.units[i])
    for i in range(len(self.bullets)):
      self.field.fieldEffect(self.bullets[i])
    for i in range(len(self.items)):
      self.field.fieldEffect(self.items[i])
    #item
    for ii in range(len(self.items)):
      i = self.items[ii].getPosition()
      for jj in range(len(self.units)):
        j = self.units[jj].getPosition()
        if abs(i-j) < self._ITEM_RANGE + self._UNIT_RANGE:
          #あたったとき
          self.items[ii].effect(self.units[jj])
          break
    #bullet
    for ii in range(len(self.bullets)):
      i = self.bullets[ii].getPosition()
      for jj in range(len(self.units)):
        j = self.units[jj].getPosition()
        if abs(i-j) < self._UNIT_RANGE:
          #あたったとき
          self.bullets[ii].attack(self.units[jj])
          break
    flag = False
    endval = 0
    for ii in range(len(self.bullets)):
      i = self.bullets[ii].getPosition()
      for jj in range(len(self.bases)):
        j = self.bases[jj].getPosition()
        if abs(i-j) < self._BASE_RANGE:
          #あたったとき
          self.bullets[ii].attack(self.bases[jj])
          if self.bases[jj].checkAlive():
            continue
          flag = True
          endval |= 1<<jj
          break
    if flag:
      print(endval)
      self.end()
  def draw(self, screan):
    self.field.draw(screan,self.debugUnit.getPosition())
    self.bases.draw(screan)
    self.units.draw(screan)
    self.bullets.draw(screan)
    self.items.draw(screan)
  def end(self):
    self.field.end()
    self.bases.end()
    self.units.end()
    self.bullets.end()
    self.items.end()
    


if __name__ == "__main__":
  run( GameManager())
