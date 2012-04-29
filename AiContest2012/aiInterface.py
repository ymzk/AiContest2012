import math
import ymzkgame.runnable import Runnable

class Reciever(Runnable):
  def __init__(self, _id, startingPoint, startingDirection):
    super().__init__()
    self._id = _id
    self._point = startingPoint
    self._objectivePoint = startingPoint
    self._fireingFlag = false
    self._direction = startingDirection
    #todoとりあえず
    self.ai = 0

  def setObjectivePoint(self,point):
    #目的地設定
    self._objectivePoint = point
  def setFiring(self,flag):
    #trueになると打っている
    #毎フレームチェックされる。
    self._fireingFlag = flag
  def setPosition(self, point):
    self._point = point
  def setDirection(self, arg):
    #方向を変える
    self._direction = arg

  #毎フレームGameManagerが呼び出すもの
  def getObjectivePoint(self):
    return self._objectivePoint
  def getFiring(self):
    return self._fireingFlag
  def getDirection(self):
    return self._direction
  def getPosition(self):
    return self._point
  #通信用
    
  def sendStartingMessage(self):
    #todoとりあえず
    self._fireingFlag = true
  def step(self):
    #todoとりあえず
    self._point = self._point + Coordinate(100,100)
  def getMessage(self):
    #todoとりあえず
    pass    
