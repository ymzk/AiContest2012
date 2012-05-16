import time


from getKeyEvent import GetKeyEvent
from field import Field
from unit import Unit
from base import Base
from item import *
from moveByKeyAsUnit import MoveByKeyAsUnit

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
  _ITEM_RANGE = 20
  _PUSH_STRENGTH = 0.5
  _VISILITY = 100
  def __init__(self,settingFileName = "gameSettings"):
    super().__init__()
    #self.testInitialize()
    self.initialize(settingFileName)
    time.sleep(1)
  def defaultInitialize(self):
    self.specialUnit = GameObject(move = MoveByKeyAsUnit(velocity = 50))
    self.bullets = RunnableList()
    self.units = RunnableList()
    self.items = RunnableList()
    self.bases = RunnableList()
    self.field = Field(self)
  def initialize(self,settingFilename):
    self.defaultInitialize()
    file = open(settingFilename, "r")
    self.field.loadField(file.readline().strip())
    for team in (0,1):
      gen = self.field.getUnitPosition(team)
      for aiName,(point,direction) in zip(file.readline().split(),gen):
        self.units.append(Unit(point,direction,self,team,len(self.units),AiManager(aiName)))
    self.addDebugUnit(0)
    for i in self.units:
      i.sendStartingMessage()

  def addDebugUnit(self,team):
    self.debugUnit = Unit(Coordinate(200,300),1,self,team,len(self.units))
    self.debugUnit.setMove(MoveByKeyAsUnit(velocity = 10))
    self.units.append(self.debugUnit)
    self._viewPoint = self.debugUnit
        
  def writeEndMessage(self,unit,file):
    file.write("endGame")
    if self._defeatTeam == 3:
      file.write("drawGame")
    elif self._defeatTeam == 0:
      file.write("canceled this Game")
    else:
      file.write("team ")
      file.write(self._defeatTeam)
      file.write(" win")
  def writeStartingMessage(self,unit,file):
    file.write("startInit")
    self.writeMessageUnit(unit,file)
    self.writeMessageField(self.field,file)
    file.write("endInit")
    self.writeMessage(unit,file)
  def writeMessage(self,unit,file):
    file.write("start")
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
    for i in self.items:
      if i.checkAvailable:
        if abs(i.getPosition() - unit.getPosition()) <self._VISILITY:
          self.writeMessageItem(i,file)
    file.write("end")
  def writeMessageUnit(self,unit,file):
    file.write("unit")
    for i in unit.encode():
      file.write(str(i))
  def writeMessageBullet(self,bullet,file):
    file.write("bullet")
    for i in bullet.encode():
      file.write(str(i))
  def writeMessageBase(self,base,file):
    file.write("base")
    for i in base.encode():
      file.write(str(i))
  def writeMessageItem(self,item,file):
    file.write("item")
    for i in item.encode():
      file.write(str(i))      
  def writeMessageField(self,field,file):
    file.write("field")
    for i in field.encode():
      file.write(str(i))


    
  def addBullet(self, bullet):
    self.bullets.append(bullet)
  def addItem(self, item):
    self.items.append(item)
  def addBase(self, base):
    self.bases.append(base)
  def getBase(self, teamFlag):
    for i in self.bases:
      if i.getTeamFlag() == teamFlag:
        #baseはひとつだと仮定
        return i
  def step(self):
    self.readKeyEvent()
    self.specialUnit.step()
    self.field.step()
    self.units.step()
    #baseはunitの後
    self.bases.step()
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
        if powerList[i].norm() >= 1:
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
    self._defeatTeam = 0
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
          self._defeatTeam |= 1<<jj
          break
    if flag:
      self.end()
  
  def draw(self, screan):
    self.field.draw(screan,self._viewPoint)
    self.bases.draw(screan, self._viewPoint)
    self.units.draw(screan, self._viewPoint)
    self.bullets.draw(screan, self._viewPoint)
    self.items.draw(screan, self._viewPoint)
  def readKeyEvent(self):
    self._viewPoint = GetKeyEvent(self._viewPoint, self.units, self.specialUnit)
  def end(self):
    for i in self.units:
      i.sendEndMessage()
    self.field.end()
    self.bases.end()
    self.units.end()
    self.bullets.end()
    self.items.end()
    time.sleep(1)
    Runnable.end(self)
    


if __name__ == "__main__":
  run( GameManager())
