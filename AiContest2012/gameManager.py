
# import coordinate
from field import Field
from unit import Unit
from base import Base
from item import *
# import bullet
# import item
from reciever import Reciever
from ymzkgame.runnableList import RunnableList
from ymzkgame.coordinate import Coordinate
from ymzkgame.runnable import Runnable
from ymzkgame.runner import run
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
    self.bases.append(Base(Coordinate(60,120),1,"team0"))
    self.bases.append(Base(Coordinate(100,120),0,"team1"))
    self.units.append(Unit(Coordinate(200,200),1,self,"team0",Reciever(1)))
    self.units.append(Unit(Coordinate(201,201),1,self,"team1",Reciever(2)))
    self.units.append(Unit(Coordinate(302,302),1,self,"team0",Reciever(3)))
    self.units.append(Unit(Coordinate(600,400),0,self,"team1",Reciever(4)))
    self.units.append(Unit(Coordinate(601,401),0,self,"team0",Reciever(5)))
    self.units.append(Unit(Coordinate(602,402),0,self,"team1",Reciever(6)))
  def writeMessage(self,unit,file):
    for i in self.bases:
      self.writeMessageBase(i,file)
    for i in self.units:
      if i.getTeamflag() == unit.getTeamFlag():
        self.writeMessageUnit(i)
        continue
      if abs(i.getPosition() - unit.getPosition()) < self._VISILITY:
        self.writeMessageUnit(i)
        continue
    for i in self.bullets:
      if abs(i.getPosition() - unit.getPosition()) <self._VISILITY:
        self.writeMessageBullet(i)
    
  def writeMessageUnit(self,unit,file):
    file.write(unit.getHp())
    file.write(unit.getPosition())
    file.write(unit.getDirection())
  def writeMessageBullet(self,bullet,file):
    file.write(bullet.getTeamFlag())
    file.write(bullet.getPosition())
    file.write(bullet.getDirection())
  def writeMessageBase(self,base,file):
    file.write(base.getHp())
    
  def addBullet(self, bullet):
    self.bullets.append(bullet)
  def addItem(self, item):
    self.items.append(item)
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
    self.field.draw(screan)
    self.bases.draw(screan)
    self.units.draw(screan)
    self.bullets.draw(screan)
    self.items.draw(screan)

run( GameManager())
