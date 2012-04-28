
# import coordinate
# import field
from unit import Unit
# import bullet
# import item
#from field import Field
from ymzkgame.coordinate import Coordinate
from ymzkgame.runnable import Runnable
from ymzkgame.runner import run
from backGroundDummy import BackGroundDummy as Field
# for test
RunnableList = list
class GameManager(Runnable):
  _unitRange = 25
  _pushStrength = 0.13
  def __init__(self):
    super().__init__()
    self.bullets = RunnableList()
    self.units = RunnableList()
    self.items = RunnableList()
    self.field = Field()
    self.testInitialize()
  def testInitialize(self):
    self.units.append(Unit(Coordinate(400,300),0,self,"team0"))
    self.units.append(Unit(Coordinate(401,301),0,self,"team1"))
  def addBullet(self,bullet):
    self.bullets.append(bullet)
  def step(self):
    self.field.step()
    for i in self.bullets:
      i.step();
    for i in self.units:
      i.step();
    for i in self.items:
      i.step();
    for counter in range(20):
      #振動して無限ループになったとき、20回で終了するようにしている。
      #押し合い
      powerList = [Coordinate(0,0) for i in range(len(self.units))]
      for ii in range(len(self.units)):
        for jj in range(ii):
          i = self.units[ii].getPosition()
          j = self.units[jj].getPosition()
          if abs(i - j) < self._unitRange * 2 :
            factor = (self._unitRange * 2 - abs(i - j))/(abs(i-j) + 10 **(-7)) * (i - j)
            powerList[ii] += factor
            powerList[jj] -= factor
            
            #重なっているとき
      '''
      for i in range(len(self.units)):
        #壁との当たり判定壁との当たり判定はFeildで行う。
        #返り値はかかる力ベクトル(Coordinate)
        powerList[i] += self.field.wallDistance(self._unitRange,self.units[i])
      '''
        
      flag = True
      for i in range(len(self.units)):
        self.units[i].setPosition(self.units[i].getPosition() + powerList[i] * self._pushStrength)
        if powerList[i].norm() > 1 :
          flag = False
      if flag:
        break
    #当たり判定
    for ii in self.bullets:
      if ii.getDeadFlag():
        continue
      i = ii.getPosition()
      for jj in self.units:
        j = jj.getPosition()
        if abs(i-j) < self._unitRange:
          #あたったとき
          jj.damage(ii)
          break
run( GameManager())
