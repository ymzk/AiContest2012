from math import *
from ymzkgame.coordinate import Coordinate
from ymzkgame.runnable import Runnable
from processController import ProcessController

class AiManager(Runnable):
  def __init__(self, excutableName):
    super().__init__()
    self._processController = ProcessController(excutableName)
    self._fireingFlag = False
    self.sendStartingMessage()
  def getProcess(self):
    return self._processController
  def setObjectivePoint(self,point):
    #目的地設定
    self._objectivePoint = point
  def setFiring(self,flag):
    #trueになると打っている
    #毎フレームチェックされる。
    self._fireingFlag = flag

  #毎フレームunit.step()が呼び出すもの
  def setPosition(self, position):
    self._position = position
  def setDirection(self, arg):
    #方向を変える
    self._direction = arg
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
  def getMessage(self):
    #todoとりあえず
    pass    

