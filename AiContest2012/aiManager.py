from math import *
from ymzkgame.coordinate import Coordinate
from ymzkgame.runnable import Runnable
from processController import ProcessController


class DefaultAiManager(Runnable):
  def __init__(self):
    super().__init__()
    self._fireingFlag = True
  def setFiring(self,flag):
    self._fireingFlag = flag
  def getMove(self):
    return Coordinate(0, 0)
  def getRotate(self):
    return 0
  def getFiring(self):
    return self._fireingFlag
  def sendStartingMessage(self):
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
  def __init__(self, excutableName):
    super().__init__()
    self._processController = ProcessController(excutableName)
    self._fireingFlag = False
    self._move = 0
    self._rotate = 0
    self._direction = 0
    self.sendStartingMessage()
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
    return Coordinate(cos(self._direction),sin(self._direction)) * self._move
  def getRotate(self):
    return self._rotate
  def getFiring(self):
    return self._fireingFlag
  '''
  def getPosition(self):
    #todo動き方
    return self._position
  '''
  def getDirection(self):
    return self._direction
  #通信用
  def writeMessage(self, unit, gameManager):
    gameManager.writeMessage(unit,self._processController)
    
  def sendStartingMessage(self):
    #todoとりあえず
    #self._fireingFlag = True
    self._processController.write("end\n".encode())
  def step(self):
    #todoとりあえず
    #self._position += Coordinate(sin(self._arg),cos(self._arg)) * self._move


    self._direction += self._rotate
    
    '''
    self._position += Coordinate( sin(self._direction), -cos(self._direction))*2
    '''
  def readMessage(self):
    pc = self._processController
    import sys
    sys.stdout.flush()
    for i in range(10):
      if pc.readline() == b"start\n":
        sys.stdout.flush()
        for i in range(20):
          if self._matchMessage(pc.readline()):
            continue
          break
        break
  def _matchMessage(self,message):
    factorList = message.decode().split()
    if len(factorList) == 0:
      return True
    if factorList[0] == "end":
      return False
    elif factorList[0] == "fire":
      self._fireingFlag = True
    elif factorList[0] == "move":
      self._move = float(factorList[1])
    elif factorList[0] == "rotate":
      self._rotate = float(factorList[1])
    elif factorList[0] == "stop":
      if factorList[1] == "fire":
        self._fireingFlag = False
    return True  
  def end(self):
    self._processController.end()

