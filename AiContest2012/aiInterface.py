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
    self._center = Point - Coordinate( sin(self._direction), -cos(self._direction))*50
  def setDirection(self, arg):
    #方向を変える
    self._direction = arg

  #毎フレームGameManagerが呼び出すもの
  def getObjectivePoint(self):
    return self._objectivePoint
  def getFiring(self):
    return self._fireingFlag
  def getDirection(self, arg):
    return self._direction
  
  #通信用
    
  def sendStartingMessage(self):
    #todoとりあえず
    self._fireingFlag = true
    self._center = Point - Coordinate( sin(self._direction), -cos(self._direction))*50
  def step(self):
    #todoとりあえず
    self._direction += 0.1
    self._point = center + Coordinate( sin(self._direction), -cos(self._direction))*50
    return self
  def getMessage(self):
    #todoとりあえず
    pass    
