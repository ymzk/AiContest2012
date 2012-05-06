from math import *
from ymzkgame.coordinate import Coordinate

class Reciever:
  def __init__(self, _id):
    super().__init__()
    self._id = _id
    self._fireingFlag = False
    self.sendStartingMessage()
  def setPosition(self, position):
    self._position = position
  def setObjectivePoint(self,point):
    #目的地設定
    self._objectivePoint = point
  def setFiring(self,flag):
    #trueになると打っている
    #毎フレームチェックされる。
    self._fireingFlag = flag
  def setDirection(self, arg):
    #方向を変える
    self._direction = arg

  #毎フレームGameManagerが呼び出すもの
  def getPosition(self):
    #todo動き方
    return self._position
  def getFiring(self):
    return self._fireingFlag
  def getDirection(self):
    return self._direction
  
  #通信用
    
  def sendStartingMessage(self):
    #todoとりあえず
    self._fireingFlag = True
  def step(self):
    #todoとりあえず
    self._position+=Coordinate(-10,-10)
    '''
    self._direction += 0.1
    self._position += Coordinate( sin(self._direction), -cos(self._direction))*2
    '''
    return self
  def getMessage(self):
    #todoとりあえず
    pass    

