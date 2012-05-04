
# import coordinate
from field import Field
from unit import Unit
# import bullet
# import item
from ymzkgame.runnableList import RunnableList
from ymzkgame.coordinate import Coordinate
from ymzkgame.runnable import Runnable
from ymzkgame.runner import run
#from backGroundDummy import BackGroundDummy as Field
# for test
#RunnableList = list
class DamyRunnable(Runnable):
  def __init__(self):
    super().__init__()
  def step(self):
    pass
class GameManager(Runnable):
  _unitRange = 24
  _pushStrength = 0.5
  def __init__(self):
    super().__init__()
    self.bullets = RunnableList()
#    self.bullets.append(None)
    self.units = RunnableList()
#    self.units.append(None)
    self.items = RunnableList()
#    self.items.append(None)
    self.field = Field()
    self.testInitialize()
  def testInitialize(self):
    self.field.setFieldSize(40, 40, 25, 25)
    self.field.testInitialize()

    self.units.append(Unit(Coordinate(200,200),1,self,"team0"))
    self.units.append(Unit(Coordinate(600,400),1,self,"team1"))
    self.units.append(Unit(Coordinate(201,201),0,self,"team0"))
    self.units.append(Unit(Coordinate(601,401),0,self,"team1"))
  def addBullet(self,bullet):
    self.bullets.append(bullet)
  def step(self):
    self.field.step()
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
          if abs(i - j) < self._unitRange * 2 :
            factor = (self._unitRange * 2 - abs(i - j))/(abs(i - j) + 10 **(-7)) * (i - j)
            powerList[ii] += factor
            powerList[jj] -= factor
            #重なっているとき

      for i in range(len(self.units)):
        #壁との当たり判定壁との当たり判定はFeildで行う。
        #返り値はかかる力ベクトル(Coordinate)
        powerList[i] += self.field.wallDistance(self._unitRange, self.units[i])

      flag = True
      for i in range(len(self.units)):
        if powerList[i].norm() > 1e-6:
          self.units[i].setPosition(self.units[i].getPosition() + powerList[i] * self._pushStrength)
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
    for ii in range(len(self.bullets)):
      i = self.bullets[ii].getPosition()
      for jj in range(len(self.units)):
        j = self.units[jj].getPosition()
        if abs(i-j) < self._unitRange:
          #あたったとき
          self.units[jj].damage(self.bullets[ii])
          break
run( GameManager())
