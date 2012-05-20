from math import *
from ymzkgame.coordinate import Coordinate
from ymzkgame.runnable import Runnable
from processController import ProcessController
from catString import CatString

class DefaultAiManager(Runnable):
  def __init__(self):
    super().__init__()
    self._fireingFlag = True
  def setFiring(self,flag):
    self._fireingFlag = flag
  def getMove(self):
    return 0
  def getRotate(self):
    return 0
  def getFiring(self):
    return self._fireingFlag
  def sendEndMessage(self,unit,gmeManager):
    pass
  def sendStartingMessage(self,unit,gmeManager):
    pass
  def step(self):
    pass
  def writeMessage(self,unit,message):
    pass
  def readMessage(self):
    pass
  def end(self):
    pass


  
class AiManager(Runnable):
  SPEED = 3
  def __init__(self, excutableName):
    super().__init__()
    self._processController = ProcessController(excutableName)
    self._fireingFlag = False
    self._move = 0
    self._rotate = 0
    self._direction = 0
  def setFiring(self,flag):
    #trueになると打っている
    #毎フレームチェックされる。
    self._fireingFlag = flag
  '''
  def setObjectivePoint(self,point):
    #目的地設定
    self._objectivePoint = point
  #毎フレームunit.step()が呼び出すもの
  def setPosition(self, position):
    self._position = position
  def setDirection(self, arg):
    #方向を変える
    self._direction = arg
  '''
  def getMove(self):
    if self._move > UNIT_MAX_SPEED:
      return UNIT_MAX_SPEED
    if self._move <0:
      return 0
    return self._move
  def getRotate(self):
    if self._rotate > UNIT_MAX_ROLL_ANGLE:
      return UNIT_MAX_ROLL_ANGLE
    if self._rotate < - UNIT_MAX_ROLL_ANGLE:
      return - UNIT_MAX_ROLL_ANGLE
    return self._rotate
  def getFiring(self):
    return self._fireingFlag
  '''
  def getPosition(self):
    #todo動き方
    return self._position
  def getDirection(self):
    return self._direction
    '''
  #通信用
  def writeMessage(self, unit, gameManager):
    string = CatString()
    
    gameManager.writeMessage(unit,string)
    self._processController.write(string)
    
  def sendEndMessage(self,unit,gameManager):
    string = CatString()
    
    gameManager.writeEndMessage(unit,string)
    self._processController.write(string)
  def sendStartingMessage(self,unit,gameManager):
    string = CatString()
    
    gameManager.writeStartingMessage(unit,string)
    self._processController.write(string)
  def step(self):
    #todoとりあえず
    #self._direction += self._rotate
    
    '''
    self._position += Coordinate( sin(self._direction), -cos(self._direction))*2
    '''
  def readMessage(self):
    data = self._processController.readline()
    self._move = 0
    self._rotate = 0
    self._fireingFlag = False
    if data == None:
      return
    data = data.split()
    if len(data) == 3:
      self._matchMessage(data)
  def _matchMessage(self,factorList):
    self._move = float(factorList[0])
    self._rotate = float(factorList[1])
    self._fireingFlag = int(factorList[2]) != 0
  def end(self):
    self._processController.end()

